# Rekonstrukcija električne sheme — revizija D0

**Datum:** 15.10.2026.  
**Status:** radna rekonstrukcija, nije verificirana shema za izradu ili prelemljivanje.

## Potvrđeni signali iz prethodnog rada

| Oznaka | Uređaj / funkcija | Priključak / vrijednost | Status |
|---|---|---|---|
| U1 | ESP32 | razvojna pločica, točan model nepoznat | potvrđeno |
| U2 | INA219 | I²C adresa 0x40 | potvrđeno |
| DS1 | OLED | I²C adresa 0x3C | potvrđeno |
| SDA | ESP32 → INA219 i OLED | GPIO21 | potvrđeno |
| SCL | ESP32 → INA219 i OLED | GPIO22 | potvrđeno |
| K1 | relej upravljan tranzistorom C3209 | GPIO26 | potvrđeno |
| LED1 | LED na ESP32 pločici | GPIO2 | potvrđeno |
| VBAT_ADC | naponski djelitelj → ESP32 | GPIO34 | potvrđeno |
| R_LOAD1, R_LOAD2 | otpornici opterećenja | 22 Ω / 5 W svaki, paralelno | potvrđeno |
| R_LOAD | ukupni izmjereni otpor | 11,15 Ω | potvrđeno |

Povijesno: GY-712 bio je povezan na GPIO35, ali je zamijenjen INA219. **Ne uključivati GY-712 u aktualnu shemu.**

## Potvrđena mjerenja
- Baterija: 4,222 V.
- GPIO34: 0,58 V.
- Stari GY-712 izlaz GPIO35: 2,32 V (povijesno mjerenje, ne vrijedi za aktualnu izvedbu).

## Logička blok-shema (nije električna shema)
```text
                      +-- OLED (I²C 0x3C)
ESP32 GPIO21 SDA -----+-- INA219 (I²C 0x40)
ESP32 GPIO22 SCL -----+-- oba I²C uređaja

ESP32 GPIO26 -------- upravljački stupanj C3209 ------ relej K1
ESP32 GPIO34 <------- naponski djelitelj <------------ baterija
ESP32 GPIO2 --------- ugrađena LED

Baterija --- mjerni/pražnjeni krug (TOPOLOGIJA NIJE POTVRĐENA)
                       INA219 / relej / 2x22Ω paralelno
```

## Kritične nepoznanice za završnu KiCad shemu
1. Točan model ESP32 pločice i napajanje ESP32, OLED-a i INA219.
2. Vrijednosti otpornika naponskog djelitelja i njihovo ožičenje.
3. Točna veza INA219 VIN+ / VIN− u strujnom krugu.
4. Kontaktni raspored releja (COM/NO/NC), napon zavojnice, zaštitna dioda i otpornik baze C3209.
5. Polaritet priključka baterije, zajedničke mase i zaštite (osigurač, zamjena polariteta, termička zaštita).
6. Razlika između fizički izmjerenih spojeva i posljednje verzije firmwarea.

## Pravila za konačnu dokumentaciju
- Svaku mrežu i komponentu označiti standardnom referencom (U1, U2, K1, Q1, R1...).
- Ne izmišljati vrijednosti ni povezivanja na temelju tipične sheme modula.
- Tek nakon provjere nacrtati KiCad projekt i izvesti PDF s naslovnim blokom, revizijom i popisom komponenti.
- Ne mijenjati radni uređaj radi rekonstrukcije dok se podaci mogu prikupiti iz koda i povijesti.
