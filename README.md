# Satpos - Satellites' position web app
# 1. Cel projektu

Celem projektu było stworzenie aplikacji pozwalającej na otrzymanie wykresów parametrów
satelitów. Program miał działać na podstawie danych takich jak maska obserwacji, współrzędne
stanowiska pomiarowego oraz data pomiaru. Dodatkowo program musiał przyjmować dane z
almanachu – pliku tekstowego z informacjami na temat satelitów ściągniętego ze strony celestrak.com.
Obliczenia miały być przeprowadzone dla całej doby. Podstawowe funkcje np.: czytanie almanachu,
zostały przekazane przez prowadzącego w języku python.

# 2. Efekt pracy

Efektem pracy jest aplikacja webowa „Satpos”. Obliczeniowa oraz serwerowa(back-end) część
programu została przygotowana w języku python przy pomocy biblioteki Flask. Część wizualna
strony(front-end) została stworzona w html, css i javascriptcie. Wykresy zostały stworzone przy
pomocy biblioteki Plotly.

# 3. Opis aplikacji

Głównym plikiem programu jest plik app.py – rdzeń serwera aplikacji webowej. Zdefiniowane
w nim są dwa ‘routy’ – podstrony które występują na stronie. Do pliku importowane są funkcje
obliczeniowe napisane w pliku functions.py. Serwer importuje zmienne wpisane przez użytkownika. Po
wykonaniu wszystkich potrzebnych obliczeń serwer aplikacji przekazuje tablice oraz zmienne do części
front-endowej.
Pliki htmlowe znajdują się folderze ‘templates’. W pliku base.html znajduje się podstawowy
wygląd, importowany do innych plików html za pomocą biblioteki Jinja2. Plik index.html jest podstroną
tytułową aplikacji, z której przekazywane są dane do serwera w celu wykonania obliczeń. Serwer
przekazuje obliczone dane do pliku charts.html, w którym skrypt języka javascript rysuje wykresy. W
pliku charts.html pomiędzy linijkami kodu znajdują się wcięcia na skrypt js, gdzie rysuje się wykresy
oraz dodatkowe funkcje(np. suwak). W skryptach korzysta się z funkcji rysujących wykresy
zdefiniowane w pliku script.js w folderze ‘static/js’. W pliku chart.html posegregowano wykresy na
oddzielnych stronach. Funkcjonowanie stron wykresów zdefiniowano w pliku main.js w folderze
‘static/js’.
Wygląd strony określono w pliku base_style.css w folderze ‘static/css’. Dodatkowo skorzystano
z internetowej biblioteki Bootstrap.

# 4. Opis korzystania z aplikacji

Przez problemy z hostingiem, aplikację webową trzeba uruchomić na swoim własnym
komputerze podręcznym. W tym celu należy zainstalować na komputerze pythona oraz środowisko
pozwalające na włączenie programu. Dodatkowo należy pobrać bibliotekę Flask oraz numpy. Po
spełnieniu powyższych wymagań można włączyć stronę poprzez uruchomienie pliku app.py. Wtedy
należy przejść pod adres http://127.0.0.1:5000 w przeglądarce. W razie nie powodzenia można wpisać
w konsoli/terminalu komendy ‘flask run’. W razie problemów z rozmiarem wykresów należy zmniejszyć
i z powrotem powiększyć okno przeglądarki.
