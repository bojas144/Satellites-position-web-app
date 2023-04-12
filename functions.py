import numpy as np
from datetime import date
import math as m
import urllib.request


def read_yuma(almanac_file):
    '''
    Reading and parsing YUMA asci format
    INPUT:
        Almanac: YUMA format
    OUTPUT:
        almanac_data -  type list of list [strings value], number of lists is equal to number of satellite
                        one list contain satellites according to the order:
                        ['SV ID', 'Health', 'Eccentricity', 'Time of Applicability(s)', 'Inclination(rad)',
                        'Rate of Right Ascen(r/s)', 'SQRT(A)  (m 1/2)', 'Right Ascen at Week(rad)',
                        'Argument of Perigee(rad)', 'Mean Anom(rad)', 'Af0(s)', 'Af1(s/s)', 'Week no']

    '''

    if almanac_file:
        alm = open(almanac_file)

        alm_lines = alm.readlines()
        all_sat = []
        for idx, value in enumerate(alm_lines):

            if value[0:3] == 'ID:':
                one_sat_block = alm_lines[idx:idx + 13]
                one_sat = []
                for line in one_sat_block:
                    data = line.split(':')
                    one_sat.append(float(data[1].strip()))
                all_sat.append(one_sat)
        alm.close()
        all_sat = np.array(all_sat)

        return (all_sat)


def date2tow(data):
    """
    Parameters
    data : data -- list [year,month,day,hour,minute,second]
    Returns
    week : GPS week, for the second rollover, in range 0-1023
    tow : second of week.
    """
    # difference of days
    dd = date.toordinal(date(data[0], data[1], data[2])) - date.toordinal(date(2019, 4, 7))
    # week number
    week = dd // 7
    # day of week
    dow = dd % 7
    # time of week
    tow = dow * 86400 + data[3] * 3600 + data[4] * 60 + data[5]
    return week, tow


def satellite_xyz(date, almanac):
    id = int(almanac[0])
    week, tow = date2tow(date)
    gps_week = almanac[12]
    toa = almanac[3]
    mikro = 3.986005e14
    omegaE = 7.2921151467e-5
    m0 = almanac[9]
    e = almanac[2]
    omega = almanac[8]
    omega_dot = almanac[5]
    omega0 = almanac[7]
    i = almanac[4]

    t = week * 7 * 86400 + tow
    toa_weeks = gps_week * 7 * 86400 + toa
    tk = t - toa_weeks
    a = (almanac[6])**2
    n = m.sqrt(mikro / a**3)
    mk = m0 + n * tk
    ei = mk
    ek = 0

    while True:
        ei_next = mk + e * m.sin(ei)
        if (abs(ei_next - ei)) < 10e-12:
            ek = ei_next
            break
        else:
            ei = ei_next

    vk = m.atan2(m.sqrt(1 - e**2) * m.sin(ek), (m.cos(ek) - e))

    Fk = vk + omega

    rk = a * (1 - e * np.cos(ek))

    xk = rk * np.cos(Fk)
    yk = rk * np.sin(Fk)

    omega_k = omega0 + (omega_dot - omegaE) * tk - (omegaE * toa)

    x = xk * m.cos(omega_k) - yk * m.cos(i) * m.sin(omega_k)
    y = xk * m.sin(omega_k) + yk * m.cos(i) * m.cos(omega_k)
    z = yk * m.sin(i)

    return np.array([x, y, z]), id


def get_rneu(fi, lam):
    Rneu = np.array([[-m.sin(fi) * m.cos(lam), -m.sin(lam), m.cos(fi) * m.cos(lam)],
                     [-m.sin(fi) * m.sin(lam), m.cos(lam), m.cos(fi) * m.sin(lam)],
                     [m.cos(fi), 0, m.sin(fi)]])

    return Rneu


def getLatLon(XYZ):
    r_delta = np.linalg.norm(XYZ[0:1])
    sinA = XYZ[1]/r_delta
    cosA = XYZ[0]/r_delta

    Lon = m.atan2(sinA,cosA)

    if Lon < - m.pi:
        Lon = Lon + 2 * m.pi
    Lat = m.asin(XYZ[2]/np.linalg.norm(XYZ))

    return m.degrees(Lat), m.degrees(Lon)


def elevation(fi, lam, h, dateOfMeasure, almanac, mask):
    a = 6378137
    e2 = 0.00669438002290

    N = a / m.sqrt(1 - e2 * m.sin(fi)**2)

    xr = (N + h) * m.cos(fi) * m.cos(lam)
    yr = (N + h) * m.cos(fi) * m.sin(lam)
    zr = (N * (1 - e2) + h) * m.sin(fi)

    # vector Xr
    Xr = np.array([xr, yr, zr])

    # matrix of neu
    Rneu = np.array([[-m.sin(fi) * m.cos(lam), -m.sin(lam), m.cos(fi) * m.cos(lam)],
                    [-m.sin(fi) * m.sin(lam), m.cos(lam), m.cos(fi) * m.sin(lam)],
                    [m.cos(fi), 0, m.sin(fi)]])

    az_tab = []
    el_vec = []
    lat, lon = [], []
    A = []
    sat_nr = 0
    el_sky, az_sky, sat_name = [], [], []

    for sat in almanac:
        Xs, id = satellite_xyz(dateOfMeasure, sat)
        latlon = getLatLon(Xs)
        lat.append(latlon[0])
        lon.append(latlon[1])
        Xsr = Xs - Xr
        neu = np.dot(Rneu.T, Xsr)
        n, e, u = neu
        az = m.degrees(m.atan2(e, n))
        if az < 0:
            az = az + 360
        el = m.degrees(m.asin(u / m.sqrt(n**2 + e**2 + u**2)))
        r = np.linalg.norm(Xsr)
        az_tab.append(az)
        el_vec.append(el)
        if el > mask:
            sat_nr+=1
            el_sky.append(90 - el)
            az_sky.append(az)
            sat_name.append(id)
            a1 = np.array([-(Xs[0] - Xr[0])/r, -(Xs[1] - Xr[1])/r, -(Xs[2] - Xr[2])/r, 1])
            A.append(a1)

    A = np.array(A)

    return az_tab, el_vec, A, sat_nr, el_sky, az_sky, sat_name, lat, lon


def sat_dop(Rneu, A):
    Q = np.linalg.inv(np.dot(A.T, A))

    GDOP = m.sqrt(Q[0, 0] + Q[1, 1] + Q[2, 2] + Q[3, 3])
    PDOP = m.sqrt(Q[0, 0] + Q[1, 1] + Q[2, 2])
    TDOP = m.sqrt(Q[3, 3])

    Qxyz = np.delete(Q, -1, 1)
    Qxyz = np.delete(Qxyz, -1, 0)
    Qneu = np.dot(np.dot(Rneu.T, Qxyz), Rneu)

    HDOP = m.sqrt(Qneu[0, 0] + Qneu[1, 1])
    VDOP = m.sqrt(Qneu[2, 2])

    return [GDOP, PDOP, TDOP, HDOP, VDOP]


def time(ourdate, minutes):
    if minutes >= 60:
        hour = m.floor(minutes / 60)
        ourdate[3] = hour
        ourdate[4] = minutes - hour * 60
    else:
        ourdate[4] = minutes

    return ourdate


def arr_to_list(arr):
    arr = np.array(arr)
    arr = arr.T
    new_arr = []
    for i in range(len(arr)):
        new_arr.append(list(arr[i]))

    return new_arr


def new_almanac():
    url_current = 'https://www.navcen.uscg.gov/?pageName=currentAlmanac&format=yuma'
    almanac_name = 'current_almanac.alm'
    urllib.request.urlretrieve(url_current, almanac_name)
    almanac = read_yuma(almanac_name)

    return almanac


def all_day_sat(fi, lam, h, dateOfMeasure, almanac, mask):
    fi = m.radians(fi)
    lam = m.radians(lam)
    az_day = []
    el_day = []
    lat_day, lon_day = [], []
    sat_nr_day, sat_name_hour = [], []
    el_sky, el_sky_hour = [], []
    az_sky, az_sky_hour = [], []
    gdops, pdops, tdops, hdops, vdops = [], [], [], [], []
    rneu = get_rneu(fi, lam)

    for t in range(0, 1500, 10):
        actualdate = time(dateOfMeasure, t)
        az, el, a, sat_nr, el_sky, az_sky, sat_name, lat, lon = elevation(fi, lam, h, actualdate, almanac, mask)
        lat_day.append(lat)
        lon_day.append(lon)
        az_day.append(az)
        el_day.append(el)
        gdop, pdop, tdop, hdop, vdop = sat_dop(rneu, a)
        gdops.append(gdop)
        pdops.append(pdop)
        tdops.append(tdop)
        hdops.append(hdop)
        vdops.append(vdop)
        sat_nr_day.append(sat_nr)
        if actualdate[4] == 0:
            el_sky_hour.append(el_sky)
            az_sky_hour.append(az_sky)
            sat_name_hour.append(sat_name)

    el_day = arr_to_list(el_day)
    az_day = arr_to_list(az_day)
    lat_day = arr_to_list(lat_day)
    lon_day = arr_to_list(lon_day)

    dops_day = [gdops, pdops, tdops, hdops, vdops]

    return az_day, el_day, dops_day, sat_nr_day, el_sky_hour, az_sky_hour, sat_name_hour, lat_day, lon_day


