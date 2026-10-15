# R2 — izbor arhitekture komponenti za 1S analizator, preliminarno
Datum: 2026-10-15. **Kandidati za provjeru datasheetovima prije sheme**; nijedan nije ovdje verificiran kao proizvodni BOM.

## Namjera
Jedan neovisan kanal punjenja/pražnjenja 18650; deset kopija kanala u završnom uređaju. Odvojeno servisno mjerenje Makita 5S.

## Preliminarna usporedba integriranih sklopova

| Funkcija | Kandidat | Zašto je kandidat | Kritična provjera prije odabira |
|---|---|---|---|
| 1S CC/CV punjač | **TI BQ24074** | Poznata serija 1S linearnih punjača s upravljanjem i NTC nadzorom | Je li prikladan režim za izabranu ćeliju, ograničenje ulazne struje, stvarni izlaz BAT i SYS, power-path, završetak punjenja, temperatura, pakiranje, dostupnost |
| 1S CC/CV punjač | **Microchip MCP73831** | Jednostavan linearni 1S punjač s programiranjem struje | Nema zamjene za neovisnu zaštitu; provjeriti dopuštenu struju, termičko ograničenje, dostupne varijante završnog napona i potreban NTC izvan IC-a |
| 1S buck punjač | **TI BQ24650** | Kandidat za učinkovitije punjenje s višeg ulaznog napona | Provjeriti točan raspon ćelija i konfiguraciju, upravljačke petlje, minimalni ulazni napon, vanjske MOSFET-e i kompleksnost; može biti previše složen za 10 kanala |
| Strujno/naponsko mjerenje | **TI INA226** | Digitalni mjerač struje/napona preko shunta, I²C | Raspon common-mode i bus mjerenja, rezolucija, shunt disipacija, I²C adrese: **10 jednakih kanala ne mogu se bez razrade adresiranja samo paralelno spojiti na jednu I²C sabirnicu** |
| Alternativno mjerenje | **TI INA219** | Već poznat iz postojećeg V1 testera | Ograničenja točnosti, offseta i adresiranja; V1 kalibracija nije automatski primjenjiva na novi uređaj |
| I²C multiplekser | **TI TCA9548A** | Razdvaja osam I²C grana, pogodno za osam identičnih senzora | Za 10 kanala treba više multipleksera / više sabirnica ili druga arhitektura, provjeriti naponske razine i reset |
| Upravljački MCU | **ESP32-S3-WROOM-1** | Wi-Fi, dovoljno resursa za stroj stanja i telemetriju | Boot pinovi, GPIO raspoloživost, napajanje, RF keep-out, watchdog, sigurnosni izlazi nakon reseta |
| Pražnjenje | **MOSFET u linearnom režimu + op-amp + shunt** | Omogućuje programiranu konstantnu struju | **SOA pri DC linearnom radu** (mnogi switching MOSFET-i nisu prikladni), op-amp common-mode i stabilnost, temperatura, pasivno OFF, preciznost shunta |
| Temperatura ćelije | **NTC 10 kΩ uz svaki utor** | Termički kontakt s ćelijom, jednostavno mjerenje | B-konstanta, tolerancija, detekcija open/short, stvarno mehaničko pričvršćenje |
| Neovisna zaštita | **namjenski 1S zaštitni IC / analogni komparator + hardversko isključivanje** | Fail-safe bez firmwarea | Stvarna sposobnost prekinuti **i punjenje i pražnjenje** u svakom kvaru; komparator nije dovoljan bez pravilno projektiranog izlaznog stupnja |

Ovo je **shortlist za tehničku provjeru**, a ne tvrdnja da svi sklopovi imaju navedene funkcije u svakoj varijanti. Točne proizvođačke stranice i revizije datasheetova obavezno dodati u zaključani BOM.

## Važna arhitekturna odluka: jedna ćelija = jedan punjač i jedan load
- Svaki utor dobiva vlastitu punjačku regulaciju i elektroničko opterećenje.
- **Punjač i load nisu istodobno aktivni**. Potrebna hardverska međublokada.
- Izlazni napon punjača i eventualni power-path ne smiju omogućiti pražnjenje preko krivog puta.
- MCU smije narediti START samo ako neovisni zaštitni sklop daje OK.
- Prije odabira op-ampa i MOSFET-a računati DC SOA i ukupno do 21 W topline za deset kanala pri kandidatu 0,5 A.
- Kontakt ćelije mora biti zamjenjiv i dovoljno pouzdan za mjerenje; unutarnji otpor mjeri se validiranom metodom, ne izvodi se nekritički iz INA226.

## Minimalni dokumentacijski paket za sljedeći korak
1. Tablica **stvarnih datasheet vrijednosti** i MPN-a za punjač, monitor, MOSFET, op-amp, NTC, držač, napajanje.
2. Odabir jedne topologije, s izračunom gubitaka za 10 kanala i mjerljivim kriterijima prihvaćanja.
3. Jednokanalna električna shema s potvrđenim pinoutima, shuntom, ulaznom zaštitom i neovisnim prekidom.
4. Simulacija i test na laboratorijskom izvoru / simulatoru ćelije prije punjenja stvarne ćelije.

## Preporuka za usmjerenje
Početno razraditi **BQ24074 + INA226 + kontrolirano linearno opterećenje**, ali **ne zaključavati dizajn** dok nisu provjereni BQ24074 power-path i termički budžet, adresiranje 10 mjerača, linearni MOSFET SOA i neovisna zaštita. MCP73831 ostaje jednostavnija alternativa za punjač ako specifikacija i termika dopuštaju.

## Otvorena sigurnosna pitanja
- 4,20 V vrijedi samo za podržane Li-ion ćelije; sumnjive/duboko ispražnjene ćelije zahtijevaju odvojenu servisnu procjenu.
- Ne obećavati rad bez nadzora dok termičke i hardverske zaštite nisu verificirane testom kvarova.
- Ne koristiti BMS servisne kontakte za 1 A punjenje bez dokaza dopuštene struje, pravilnog izoliranog izvora i postupka.
