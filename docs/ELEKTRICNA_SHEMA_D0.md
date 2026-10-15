# Električna dokumentacija — revizija D2 (rekonstrukcija)

Datum: 15.10.2026. Izvor: fotografije uređaja, korisnikove potvrde i aktualni ESPHome YAML.

## Aktualna izvedba
- U1: NodeMCU v2 ESP8266 (ESP-12F); konfiguracija `board: nodemcuv2`.
- U2: INA219 breakout; I²C adresa 0x40.
- K1: Schrack RT314006; nazivna zavojnica 6 V DC, prema korisniku pogonjena s 5 V.
- Q1: C3209 upravlja relejem (prema ranijoj izvedbi); bazni otpornik i zaštitna dioda još nisu dokumentirani.
- R_LOAD1/R_LOAD2: 2 × 22 Ω / 5 W paralelno; izmjeren ukupni otpor 11,15 Ω.
- R_DIV1/R_DIV2: 10 kΩ i 20 kΩ; točan redoslijed i dodatni djelitelji/ulazni sklop treba potvrditi.
- BAT1: držač 18650; BAT− na zajedničkoj masi.
- **OLED nije ugrađen u aktualnu izvedbu** i ne smije se prikazati na shemi.

## ESP8266 pinovi — potvrđeni aktualnim YAML-om
| Signal | NodeMCU | GPIO | Konfiguracija |
|---|---|---|---|
| Relej | D5 | GPIO14 | `switch.gpio`, `restore_mode: ALWAYS_OFF` |
| INA219 SDA | D4 | GPIO2 | I²C |
| INA219 SCL | D1 | GPIO5 | I²C, 100 kHz |
| Napon baterije | A0 | ADC0 | `adc`, faktor 9.5079 |
| INA219 adresa | — | — | 0x40 |
| INA219 shunt | — | — | 0,11425 Ω u konfiguraciji |

## Logika rada prema firmwareu
- Prilikom boota relej se isključuje.
- Start testa provjerava napon i uključuje relej nakon 500 ms.
- Test se zaustavlja nakon pet uzastopnih očitanja (u intervalu 1 s) na ili ispod cutoffa, početno 3,00 V.
- Kapacitet i energija integriraju se iz struje i napona svakih 1 s.
- Oznaka `ALWAYS_OFF` i naredba pri bootu predstavljaju softversku zaštitu; stanje izlaza tijekom samog napajanja ovisi o hardveru.

## Put pražnjenja — prema korisnikovu opisu
BAT+ → relej → shunt / INA219 → BAT−. Opteretni otpornici su 2×22 Ω paralelno, ali njihov točan položaj u serijskom strujnom putu još nije potvrđen. Nije dopušteno nacrtati direktan kratki spoj kao zamjenu za nepoznatu vezu.

## Otvoreno prije izvedbene KiCad sheme
1. Stvarni položaj R_LOAD u strujnom krugu i priključaka INA219 VIN+/VIN−.
2. Topologija naponskog djelitelja A0: vrijednosti 10k/20k su poznate, ali ne i redoslijed / eventualni dodatni otpornici na NodeMCU pločici. Faktor 9.5079 sam po sebi ne potvrđuje omjer vanjskog djelitelja.
3. Tranzistorski stupanj: točna veza baze, emitera, kolektora i diode releja.
4. Napajanje modula i releja; USB je vidljiv, ali nisu sve naponske mreže potvrđene.
5. Zaštita od obrnutog polariteta nije ugrađena — dokumentirani rizik.

## Izvorni kod
Aktualni YAML dostavljen u razgovoru 15.10.2026. Treba ga arhivirati u repozitorij uz provjeru uklanjanja tajni.
