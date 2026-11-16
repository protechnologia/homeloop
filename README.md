# homeloop

Domowy asystent głosowy na Raspberry Pi – projekt w trakcie budowy.

![Schemat sprzętu](docs/diagram.png)

<sub>Zdjęcia: sklepy z sekcji [Sprzęt](#sprzęt). Logo z Wikimedia Commons:
[Claude](https://commons.wikimedia.org/wiki/File:Claude_AI_symbol.svg) (CC0),
[ElevenLabs](https://commons.wikimedia.org/wiki/File:ElevenLabs_Logo_01.svg) (CC BY-SA 4.0, zmienione),
[Home Assistant](https://commons.wikimedia.org/wiki/File:New_Home_Assistant_logo.svg) (CC BY-SA 4.0).
Znaki towarowe należą do właścicieli. Kod schematu: `docs/diagram.py`.</sub>

## Pomysł

Raspberry Pi w przedpokoju z głośnikiem i mikrofonem. Mówisz, mowa jest zamieniana na tekst, odpowiada
model w chmurze, a odpowiedź słyszysz głosem. Do tego czujniki (temperatura, wilgotność), kamery w pokojach i urządzenia wykonawcze
(adaptery do żarówek, głowice do grzejników, przyciski naklejane na ścianie).
Kamery w standardzie ONVIF, czujniki i aktuatory oparte o LoRaWAN lub Zigbee.

Co ma umieć:

- **Rozmowa** – „Jaka dziś pogoda?”
- **Polecenia na później** – „O 15:00 włącz światło w salonie.”
- **Reguły** – „Jak w pokoju spadnie poniżej 20°C, odkręć grzejnik.”
- **Kamery** – „Sprawdzaj co 5 minut i daj znać, jak ktoś przyjdzie do domu.”

Jak to działa:

- **Słowo wybudzające (wake word)** – rozpoznaje je lokalnie dotrenowany model.
- **Mowa (STT, TTS)** – rozpoznawanie i synteza mowy to samodzielnie napisana integracja z usługami w chmurze.
- **Model** – pętla ReAct działa bezpośrednio w Pythonie, z użyciem LangGraph. Wszystkie zasoby
  (kamery, Home Assistant itd.) model dostaje jako narzędzia.
- **Sprzęt** – integracja za pośrednictwem Home Assistant.
- **Dwie pętle** – jedna działa w czasie rzeczywistym i obsługuje polecenia głosowe, druga wywołuje
  zaplanowane zadania.

## Stack

| Obszar | Technologie |
|---|---|
| Model | Claude |
| Agent | LangGraph |
| Głos | openWakeWord (wake word), ElevenLabs Scribe (STT), ElevenLabs (TTS), sounddevice |
| Integracja ze sprzętem | Home Assistant |
| Aplikacja | Python 3.10+, NumPy, pydantic-settings |

## Sprzęt

Ceny orientacyjne, stan na listopad 2026.

### Centrala i multimedia

| Element | Model | Cena | Łączność | Zasilanie |
|---|---|---|---|---|
| Komputer | [Raspberry Pi 5, 4 GB RAM](https://botland.com.pl/moduly-i-zestawy-raspberry-pi-5/23904-raspberry-pi-5-4gb-5056561803319.html) | 515 zł | – | sieć (zasilacz USB-C) |
| Obudowa | [oficjalna obudowa Raspberry Pi 5](https://botland.com.pl/obudowy-do-raspberry-pi-5/23923-obudowa-do-raspberry-pi-5-oficjalna-czerwono-biala-5056561803340.html) | 49 zł | – | – |
| Mikrofon | [ReSpeaker USB Mic Array](https://botland.com.pl/asystenci-glosowi/15689-respeaker-usb-mic-array-asystent-glosowy-5904422377939.html) | 279 zł | USB | USB (z Raspberry Pi) |
| Głośnik | [Creative Pebble V2](https://mediamarkt.pl/pl/product/_glosniki-komputerowe-creative-pebble-v2-usb-c-czarny-1434814.html) | 110 zł | jack 3,5 mm (z ReSpeakera) | USB |
| Kamery | [TP-Link Tapo C210](https://www.x-kom.pl/p/659273-inteligentna-kamera-tp-link-tapo-c210-3mpx-led-ir-dzien-noc-obrotowa.html) | 99 zł | Wi-Fi (protokół ONVIF) | sieć (zasilacz) |

### Czujniki

| Element | Model | Cena | Łączność | Zasilanie |
|---|---|---|---|---|
| Bramka LoRaWAN | [SenseCAP M2 Multi-Platform EU868](https://botland.com.pl/sensecap-moduly-lorawan/22110-sensecap-m2-multi-platform-bramka-wewnetrzna-lorawan-sx1302-eu868-seeedstudio-114992981.html) | 489 zł | LoRaWAN, Ethernet / Wi-Fi | sieć (zasilacz) |
| Czujniki temperatury i wilgotności | [Milesight EM320-TH](https://botland.com.pl/milesight-rozwiazania-iot/29221-czujnik-temperatury-i-wilgotnosci-ip67-lorawan-milesight-em320-th-868m-6974225037865.html) | 249 zł | LoRaWAN | bateria |

### Urządzenia wykonawcze

| Element | Model | Cena | Łączność | Zasilanie |
|---|---|---|---|---|
| Koordynator Zigbee | [Sonoff Dongle Plus MG24](https://botland.com.pl/centralki-i-bramki-sieciowe/27518-sonoff-dongle-plus-mg24-bramka-zigbeethread-home-assistant-openhab-zigbee2mqtt-interfejs-usb-6920075743364.html) | 129 zł | Zigbee, USB | USB (z Raspberry Pi) |
| Adapter żarówki | [LoraTap Zigbee E27](https://www.domadoo.fr/pl/peripheriques/5807-loratap-inteligentna-oprawka-lampy-zigbee-30-kompatybilna-z-e27.html) | 37 zł | Zigbee | sieć (230 V z oprawki) |
| Głowica grzejnika | [Tuya Zigbee](https://botland.com.pl/tuya-automatyka-domowa/17148-tuya-inteligentna-glowica-termostatyczna-zigbee-5903794120495.html) | 155 zł | Zigbee | bateria |
| Przycisk na ścianę | [Sonoff SNZB-01P](https://botland.com.pl/sonoff-inteligentne-sterowniki-wifi/26572-sonoff-snzb-01p-bezprzewodowy-przycisk-aktywacji-akcji-i-scen-zigbee-6920075740615.html) | 40 zł | Zigbee | bateria |

## Instalacja

```powershell
py -3.10 -m venv .venv            # tworzymy venv
.\.venv\Scripts\Activate.ps1      # aktywujemy venv
pip install -r requirements.txt   # instalujemy zależności
```

Modele openWakeWord nie są częścią paczki z pip, pobiera się je osobno (trafiają do `.venv`):

```powershell
python -c "from openwakeword.utils import download_models; download_models(['hey_jarvis'])"
```

## Uruchomienie

```powershell
.\.venv\Scripts\Activate.ps1      # aktywujemy venv
python main.py                    # zatrzymanie: Ctrl+C
```

## Konfiguracja

Opcjonalny plik `.env` w głównym folderze projektu:

```
MIC_DEVICE=Realtek MME   # nazwa + sterownik; puste = domyślny
WAKE_WORD=hey_jarvis     # model openWakeWord
WAKE_THRESHOLD=0.5       # próg wykrycia słowa wybudzającego, 0..1
```

Listę dostępnych urządzeń wypisuje `python -m sounddevice`.

## Stan prac

- [ ] 1. Rozmowa głosowa
  - [x] 1.1 mikrofon: odczyt dźwięku blokami z wybranego urządzenia
  - [x] 1.2 słowo wybudzające: wykrywanie przez openWakeWord
  - [ ] 1.3 własne słowo wybudzające: dotrenowanie modelu
  - [ ] 1.4 VAD: wykrycie końca wypowiedzi
  - [ ] 1.5 STT: zamiana nagrania na tekst (ElevenLabs Scribe)
  - [ ] 1.6 model: odpowiedź Claude na pytanie
  - [ ] 1.7 TTS: odpowiedź głosem (ElevenLabs)
  - [ ] 1.8 historia: kontekst rozmowy w ramach sesji
  - [ ] 1.9 strumieniowanie: mówienie zdanie po zdaniu, zanim model skończy
  - [ ] 1.10 LangGraph: pętla ReAct i pierwsze narzędzia (godzina, pogoda)
  - [ ] 1.11 echo: kanał ReSpeakera z usuniętym echem
  - [ ] 1.12 barge-in: słuchanie w trakcie mówienia i przerwanie asystenta głosem
  - [ ] 1.13 strumieniowe STT: tekst już w trakcie mówienia
- [ ] 2. Raspberry Pi: system i przygotowanie pod pracę ciągłą
  - [ ] 2.1 system: Raspberry Pi OS Lite, dostęp przez SSH
  - [ ] 2.2 projekt: Python, zależności, plik `.env`
  - [ ] 2.3 dźwięk: ReSpeaker jako mikrofon, Pebble podłączony do ReSpeakera jako głośnik
  - [ ] 2.4 systemd: start razem z systemem
- [ ] 3. Home Assistant: urządzenia jako narzędzia agenta
  - [ ] 3.1 instalacja: Home Assistant na Raspberry Pi
  - [ ] 3.2 Zigbee: koordynator Sonoff MG24 i parowanie urządzeń
  - [ ] 3.3 narzędzia: odczyt stanu i sterowanie urządzeniami przez API Home Assistant
  - [ ] 3.4 światło: włączanie i wyłączanie głosem
  - [ ] 3.5 przycisk na ścianie: akcja po naciśnięciu
- [ ] 4. Druga pętla: zadania zaplanowane
  - [ ] 4.1 harmonogram: zadania zapisane na dysku, przetrwają restart
  - [ ] 4.2 narzędzia: agent sam dodaje, zmienia i usuwa zadania
  - [ ] 4.3 polecenia na później: „O 15:00 włącz światło w salonie.”
  - [ ] 4.4 pętla autonomiczna: wywołanie agenta co 5 minut, notatki z poprzednich wywołań
  - [ ] 4.5 komunikaty: agent sam odzywa się przez głośnik, nie przerywając rozmowy
- [ ] 5. Czujniki LoRaWAN
  - [ ] 5.1 bramka: SenseCAP M2 i serwer sieci LoRaWAN
  - [ ] 5.2 czujniki: EM320-TH, odczyty w Home Assistant
  - [ ] 5.3 narzędzie: temperatura i wilgotność w pokojach
  - [ ] 5.4 dysk: przeniesienie systemu z karty SD (historia odczytów zużywa kartę)
- [ ] 6. Ogrzewanie: agent ustawia temperatury, regulacja zostaje w głowicach
  - [ ] 6.1 głowice: Tuya w Home Assistant
  - [ ] 6.2 narzędzie: ustawienie temperatury w pokoju
  - [ ] 6.3 reguły: „Jak w pokoju spadnie poniżej 20°C, odkręć grzejnik.”
- [ ] 7. Kamery
  - [ ] 7.1 zdjęcie: klatka z Tapo C210 przez ONVIF
  - [ ] 7.2 PTZ: obrót kamery jako narzędzie
  - [ ] 7.3 analiza: model opisuje, co widać na zdjęciu
  - [ ] 7.4 obserwacja: „Sprawdzaj co 5 minut i daj znać, jak ktoś przyjdzie do domu.”
- [ ] 8. Rozbudowa i utrzymanie
  - [ ] 8.1 kolejne pomieszczenia: czujniki, głowice, kamery
  - [ ] 8.2 kopie zapasowe: konfiguracja i dane
  - [ ] 8.3 monitoring: logi i powiadomienie o awarii

## Licencja

Kod jest na licencji [MIT](LICENSE). Licencja nie obejmuje zdjęć produktów ani logo w `docs/img` i na schemacie,
ich źródła podano pod schematem.
