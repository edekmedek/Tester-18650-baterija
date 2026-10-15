# R3 — provjera proizvođačkih podataka i ispravci R2
Datum: 2026-10-15. Status: provjerene osnovne funkcije iz službenih izvora; **nije odobreno za proizvodnju**.

## Službeni izvori
- TI INA226: https://www.ti.com/product/INA226 ; datasheet https://www.ti.com/lit/ds/symlink/ina226.pdf
- TI BQ24074: https://www.ti.com/product/BQ24074 ; datasheet https://www.ti.com/lit/ds/symlink/bq24074.pdf
- Microchip MCP73831: https://www.microchip.com/en-us/product/MCP73831 ; datasheet https://ww1.microchip.com/downloads/en/DeviceDoc/MCP73831-Family-Data-Sheet-DS20001984H.pdf

## Rezultati

| Funkcija | Potvrđeno iz službenog izvora | Posljedica za dizajn |
|---|---|---|
| INA226 | **16 programabilnih I²C adresa**, 0–36 V bus, 2,7–5,5 V napajanje, shunt i bus mjerenje | **10 INA226 na jednoj I²C sabirnici je načelno moguće** uz deset različitih hardverskih adresnih kombinacija. R2 je pogrešno upozorio da nužno treba multiplekser. |
| BQ24074 | 1S 4,2 V Li-ion punjač; 1,5 A maks., linearna topologija, TS/NTC nadzor, PowerPath, termička regulacija, upravljanje CE | Primarni kandidat za jedan punjački kanal. Provjeriti BAT/SYS putanje pri uključenom loadu, kako prekinuti punjenje i je li neovisna zaštita zaista fail-off. |
| MCP73831 | 1S linearni punjač, 15–500 mA, nema ugrađen ulaz za nadzor temperature ćelije, nema sigurnosni timer, ima termičku regulaciju vlastitog čipa | Sam po sebi nije poželjan za sigurnosno nadzirani 10-kanalni uređaj bez dodatne vanjske zaštite. |

## Numerička procjena za BQ24074 — NIJE termička simulacija

Ako je ulaz 5,0 V, ćelija 3,0 V i punjenje 0,5 A, približna disipacija linearnog punjača je **(5,0 − 3,0) × 0,5 = 1,0 W po kanalu**. Za 10 kanala do **10 W** dodatne topline pri istovremenom punjenju, prije pomoćnih gubitaka. Ako je ćelija na 4,2 V, približno **0,4 W/kanal**. U fazi predpunjenja stvarna struja je manja i ova aproksimacija nije točan profil rada.

Pri 0,5 A konstantnog pražnjenja linearni load na 4,2 V disipira približno **2,1 W po kanalu**, tj. **21 W** ako svih deset kanala istodobno prazni. Potreban je zaseban toplinski proračun MOSFET-a i kućišta; SOA se mora provjeriti za **kontinuirani DC linearni režim**.

## Napomena za mjerenje INA226
INA226 na jednom shuntu mjeri smjer i iznos struje kroz **taj shunt**. Ako se putovi punjenja i pražnjenja odvoje prije shunta, očitanje neće predstavljati ukupnu struju ćelije. Projektirati topologiju tako da se stvarna struja ćelije mjeri u oba smjera ili koristiti dva odvojena mjerenja i kalibriranu integraciju. Provjeriti polaritet napona shunta i negativna očitanja te definiciju bus napona.

## Odluka R3
1. **INA226**: zadržati kao glavni kandidat, adresiranje deset komada bez TCA9548A je izvedivo.
2. **BQ24074**: zadržati kao primarni kandidat; još nije potvrđena topologija punjenje/pražnjenje ni termika.
3. **MCP73831**: rezervni kandidat samo uz vanjsku termičku i sigurnosnu zaštitu.
4. **NE projektirati 10-kanalni PCB** prije završetka sheme jednog kanala, DC SOA i testova neovisnog fail-off prekida.
5. Sljedeći zadatak: provjeriti BQ24074 pinout i preporučenu aplikacijsku shemu, te nacrtati jednokanalnu shemu s jasno odvojenim mjernim i strujnim putovima.
