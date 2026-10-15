# PCB DRC P2 — nije čist, nije za proizvodnju

Nativni **KiCad 10.0.4**, naredba `pcb drc --schematic-parity --all-track-errors --severity-all --exit-code-violations`. [JSON](drc.json), [tekst](drc.rpt), [status](drc-exit-status.txt).

| Kategorija | P1 | P2 |
|---|---:|---:|
| Geometrijska DRC kršenja | 0 | **0** |
| Nepovezane veze, pogreške | 3 | **2** |
| Schematic parity, upozorenja | 16 | **10** |
| Pojedinačna DRC izuzeća | 0 | **0** |
| Nativni izlazni status | 5 | **5** |

Nula geometrijskih kršenja ne znači dovršen PCB. Uključena je usporedba sa shemom; problemi nisu skriveni. Projektna pravila ostaju 0,25 mm minimalni vod/razmak, 0,15 mm tisak i 0,5 mm bakar–rub. Ozbiljnosti se nisu smanjivale; tvornički neaktivne kategorije vidljive su u `ignored_checks` JSON-a.

## Dvije nepovezane veze

- `/VIN_PLUS`: paralelni završetak opterećenja nije povezan s INA219 jer fizički INA polaritet nije potvrđen. Naziv mreže u funkcionalnoj shemi ne pretvara raniju pretpostavku u fizičku potvrdu.
- `/BAT_MINUS`: INA219 strujni priključci nisu spojeni s potvrđenim NodeMCU/BT1 povratom iz istog razloga.

Udvojeni IN+ međusobno su spojeni, kao i udvojeni IN−, prema istoimenim mrežama izvornog proizvođačkog CAD-a modula. To ne određuje vanjski smjer struje. Oba kraja para R1/R2 međusobno su povezana kao potvrđeno paralelno opterećenje.

## Deset upozorenja usporedbe sa shemom

| Dio | Funkcionalni padovi koji nedostaju | Broj |
|---|---|---:|
| K1 | A1, A2, 11/COM, 12/NC, 14/NO | 5 |
| Q1 | 1/B, 2/C, 3/E | 3 |
| R4 | 1 i 2 | 2 |

K1 sada ima osam uređivih **referentnih mjesta nosača** iz korisnikova potvrđenog izreza, a Q1 tri. Ta mjesta nisu električki proglašena proizvođačkim pinovima. Oznake `RL11A/B` ili E/C/B na starom crtežu ne dokazuju stvarni pinout. Zato je upozorenje o nedostajućem funkcionalnom padu točno i zadržano. R4 nema izmišljene rupe jer je par završetaka izvan vidljivog izreza.

**Ove dvije nepovezanosti nisu jedine dvije preostale žice.** Dok funkcionalni K1/Q1 padovi nedostaju, DRC ne može opisati sve prekinute dijelove glavnog strujnog kruga i upravljanja kao ratsnest veze. Napajanja i djelitelj ostaju otvoreni u shemi; ERC prijavljuje **11 pogrešaka i 1 upozorenje**.

## Dodatne provjere i granice

[Provjera PCB-a](board-check.txt) provjerava nativni format 10, sve postojeće P1 trase, 23 segmenta na 5 dopuštenih mreža, povezanost krajeva paralelnih otpornika, udvojene INA padove, odsutnost vanjskog INA spoja i neprovjerenih K1/Q1 mreža, raster izreza, izvorne padove modula i hashove CAD izvora. Nema proizvoljnog bakra kopiranog iz starog predloška.

R1/R2 imaju predloženi zamjenski 3D model i novi prijedlog vertikalne montaže, a K1/BTH1 referentna kućišta. To nisu potvrde stvarnih kućišta, pinoutova, dobavljivosti ni mehaničke provjere. Novi promjeri rupa jesu projektni odabiri, ne izmjerene nožice. Konačno se moraju potvrditi RT314006, C3209, R4, moduli, držač, otpornici/izvodi, napajanja/zaštite i toplina. [PCB.md](../../PCB.md) daje tablicu svakog dijela.
