# Tester18650 R26 — dovršeno trasiranje i DRC

Izvorni R25 projekt u `Downloads` nije mijenjan. R26 je zasebna radna kopija.

## Napravljene promjene

- D1 i R5 premješteni su s koordinata izvan ploče na pločicu.
- R1, R2, R3 i R4 preraspoređeni su tako da nema fizičkih preklapanja s NodeMCU, INA219 i držačem baterije.
- Sve definirane mreže trasirane su na F.Cu i B.Cu.
- Vodovi snage (`BAT_PLUS`, `BAT_MINUS_GND`, `LOAD_PLUS`, `LOAD_RETURN`) izvedeni su širinom 1,0 mm.
- Upravljački i mjerni vodovi izvedeni su širinama 0,5–0,6 mm.
- Rub silkscreena INA219 footprinta povučen je unutar obrisa ploče.
- Sakriveni su natpisi koji su prelazili preko padova ili ruba ploče.

## Završni DRC

- DRC violations: 7 upozorenja, 0 grešaka
- Unconnected pads: 0
- Footprint errors: 0
- Nema kratkih spojeva, clearance grešaka, presijecanja vodova ni courtyard preklapanja.

Svih 7 preostalih upozorenja su `lib_footprint_mismatch`: lokalno prilagođeni footprintovi u PCB-u razlikuju se od primjeraka u projektnoj biblioteci. Nisu automatski zamijenjeni jer bi osvježavanje iz biblioteke moglo vratiti ranija, nepotvrđena mapiranja pinova.

## Obavezna provjera prije izrade

- Potvrditi fizičku orijentaciju zaštitne diode D1.
- Potvrditi INA219 IN+/IN− orijentaciju na stvarnom modulu.
- Iako je Q1 mapiranje ranije označeno kao korisnički potvrđeno, preporučuje se završna usporedba s točnom izvedbom C3209 prije narudžbe PCB-a.
- Provjeriti termički razmak i očekivanu disipaciju oba otpornika 22 Ω / 5 W u stvarnom kućištu.

Datoteka `DRC_R26.txt` sadrži puni završni izvještaj.

