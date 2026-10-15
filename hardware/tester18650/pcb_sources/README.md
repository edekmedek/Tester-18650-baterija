# Izvori geometrije i podrijetlo

Primarni vizualni izvor je korisnikov `tester18650_fotoreferenca_obje_strane.pdf` (jedna stranica, gornja strana lijevo, donja strana već zrcaljena desno). Datoteka nema potvrđeno mjerilo za PCB; korišten je raspored, ne izmišljene milimetarske mjere. SHA-256 i naziv zabilježeni su u [manifestu](reference-geometry.json). Korisnikove fotografije nisu kopirane u javni repozitorij.

## NodeMCU CH340 referenca

Proizvođački otvoreni projekt: [nodemcu/nodemcu-devkit](https://github.com/nodemcu/nodemcu-devkit), commit `b0f19d6d1c49b6db4aef56ddba789a7f92f6ecce`, `ESP12_DEVKIT.lbr`. Kopija je [NodeMCU_CH340_reference.lbr](NodeMCU_CH340_reference.lbr), licenca [MIT](NODEMCU_LICENSE.txt). Footprint P1 izveden je iz tih koordinata i okrenut s USB-om prema gore. Ne tvrdi se da je proizvođački povijesni DevKit isti kao fotografirani klon Ver 0.1; konkretna geometrija klona ostaje blokator.

## Soldered INA219

Proizvođački projekt: [Voltage---current-sensor-INA219-breakout-hardware-design](https://github.com/SolderedElectronics/Voltage---current-sensor-INA219-breakout-hardware-design), commit `bcd0be51f51a1b68144ee6343d713c3ba74b0f48`.

- Original `CAD/V1.0.0/INA219_breakout.kicad_pcb` spremljen je nepromijenjen kao [Soldered_INA219_source.kicad_pcb](Soldered_INA219_source.kicad_pcb).
- Originalni proizvođački `OUTPUTS/V1.0.0/Voltage & current sensor INA219 breakout 3D.step` je [Soldered_INA219_source.step](Soldered_INA219_source.step).
- Geometrijski izvadak s koordinatama izvoda i izvornim SHA-256 je u manifestu. Izravno su provjereni obris 38 × 22 mm i funkcije četiriju upravljačkih kontakata.
- Za fotografiranu varijantu uklonjeno je **samo jedno opcijsko tijelo vijčanog terminala**, jer se na slici jasno vide prazni strujni otvori. Preostalih 28 proizvođačkih tijela sačuvano je bez novih dimenzija. Rezultat je `models/Soldered_INA219_photo_variant.step`, reprodukcija u `tools/adapt_ina_model.py`, zapis u `reports/pcb/ina-model-adaptation.json`.
- Priložena je [proizvođačka TAPR OHL licenca](SOLDERED_LICENSE.md). Izvedeni footprint i prilagođeni model zadržavaju ovo podrijetlo i licencu. Ostala geometrija izvora nije predstavljena kao nova autorska geometrija.

## Područja bez potvrđenog paketa

R1/R2, R3/R4, Q1, K1 i BTH1 koriste jasno imenovane `RESERVE_*_PACKAGE_TBD` položaje bez padova. Njihove dimenzije su **dodijeljene površine na novoj pločici**, ne mjere stvarnog dijela. STEP plohe tih oznaka imaju grafičku debljinu 0,02 mm; to nisu modeli kućišta. Fotografije nisu korištene za izmišljanje dubine, visine ili razmaka nevidljivih izvoda.

Pregledane su standardne KiCad Schrack RT1 varijante, no nisu nasumično zamijenjene za RT314006. Povezani proizvođački PDF-ovi na Schrack/TE odredištima nisu bili dostupni iz ovog okruženja (HTTP proxy 403), a biblioteke sadrže različite rasporede/varijante. Zato taj korak nije označen kao verificiran.

## Alati i provjera

Generiranje početnih objekata koristilo je instalirani `pcbnew` Python API 9.0.2. Konačni PCB je zatim nativno spremljen/učitan u KiCadu **10.0.4**, format `20260206`; PDF, GLB i DRC izvozi izvedeni su KiCadom 10. Dimenzije nisu potvrđivane samo sintaktičkom provjerom teksta.

Grafičke CAD plohe i preinaka proizvođačkog modela koriste OpenCascade preko `cadquery-ocp==7.8.1.1.post1`. To nije potrebno za otvaranje predanog PCB-a ili njegovih već priloženih STEP modela. PNG je render iz stvarnog KiCad GLB-a u Blenderu 4.3.2, uz dodatne grafičke oznake referenci na rezerviranim plohama. Izvorni KiCad CLI renderer u ovom je okruženju završavao statusom 139; nije prikazano da je taj poziv prošao.

Za sve primijenjene izvore uključen je izvorni CAD ili točan javni URL/commit. Nisu objavljeni Wi-Fi podaci, tajne niti drugi firmware parametri izvan već javnog repozitorija.
