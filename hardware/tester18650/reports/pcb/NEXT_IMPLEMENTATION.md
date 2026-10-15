# Sljedeća provedba PCB-a P2 — radni zadatak, ne završni izvještaj

Polazište: `de8bc63`, pregledani `PCB.md` i `reports/pcb/DRC.md`; podaci RT314006 u `reports/pcb/RT314006_MANUFACTURER_SOURCE.md`.

**Cilj:** zamijeniti nacrtane pravokutnike fizičkim, uređivim footprintovima i vidljivim 3D kućištima, koliko to proizvođački podaci dopuštaju, bez lažnih pinoutova ili prikrivanja ERC/DRC problema.

## Redoslijed izvršenja u KiCad 10 okruženju

1. K1 RT314006: preuzeti proizvođački STEP/DXF i podatke pet izvoda, nacrtati točan footprint (uključujući padove A1/A2/COM/NO/NC) i 3D kućište. Provjeriti raster i orijentaciju prema fotografiji; ako proizvođački crtež ne potvrđuje pinout, ostaviti rezervaciju i precizno navesti koji dokument nedostaje.
2. R1/R2 5W22R0J: pronaći dokumentirani model cementnog otpornika odgovarajuće veličine; ako proizvođač nije utvrđen, ponuditi konkretan zamjenski model s izvorom i jasno označiti da nije verificiran kao dio sa fotografije. Ne stvarati padove na temelju same vrijednosti 22 Ω/5 W.
3. Q1 C3209: provjeriti točnu oznaku/kućište i proizvođački B/C/E pinout prije dodjele footprinta. U protivnom ostaviti otvoreno, ali dovršiti 3D vizualizaciju potvrđenih dijelova.
4. R3/R4: ne nagađati kućište i topologiju; izdvojiti od fizički potvrđenih dijelova.
5. BTH1: provjeriti model držača i dimenzije; po potrebi ostaviti fizički prikaz kao referencu bez proizvodnih padova.
6. Ponovno pokrenuti KiCad ERC/DRC sa schematic parity, izvesti PCB PDF i GLB/PNG. Objaviti jasnu tablicu: stvarni footprint / privremeni prikaz / bez padova, za svaki dio.
7. Commit na `main` s uređivim `.kicad_pcb` i svim izlazima. Bez Gerbera dok DRC/ERC i fizički pinoutovi nisu verificirani.

**Upozorenje:** prethodni P1 sadrži samo SDA, SCL i jedan GND vod; nema električki rutiran glavni strujni krug. Oznaka '0 geometrijskih kršenja' ne znači dovršenu pločicu. Izvorne fotografije gornje i donje strane su u razgovoru korisnika, a njihov opis u `PHOTO_TOP_REFERENCE_2026-10-15.md` i `PHOTO_BOTTOM_REFERENCE_2026-10-15.md`.

## Provedba P2

[PCB.md](../../PCB.md) i [DRC.md](DRC.md) opisuju stvarno spremljene izmjene i preostale blokatore. Naknadni korisnikov [potvrđeni izrez](REFERENCE_DETAIL_RL_Q_R_2026-10-15.md) dao je raster nosača za K1/Q1/R1/R2/R3, ali ne i proizvođačko mapiranje releja/tranzistora. P2 ima fizičke referentne padove umjesto tih rezervacija, povezane paralelne otpornike i udvojene INA kontakte te volumne referentne/zamjenske modele gdje postoje podaci. Nije dovršen ni odobren direktni RT314006 footprint, pinout C3209 ili proizvodni PCB. R4 raster ostaje nepotpun u izrezu.
