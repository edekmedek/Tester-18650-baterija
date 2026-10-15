# PCB DRC P3 — K1 mapiran, nalaz nije čist

Nativni **KiCad 10.0.4**, `pcb drc --schematic-parity --all-track-errors --severity-all --exit-code-violations`. [JSON](drc.json), [tekst](drc.rpt), [status](drc-exit-status.txt).

| Kategorija | P2 | P3 |
|---|---:|---:|
| Geometrijska DRC kršenja | 0 | **0** |
| Nepovezane veze, pogreške | 2 | **2** |
| Schematic parity, upozorenja | 10 | **5** |
| Pojedinačna izuzeća | 0 | **0** |
| Izlazni status | 5 | **5** |

K1 sada ima osam fizičkih padova s brojevima A1/A2/11/11/12/12/14/14. Svih pet funkcija odgovara mrežama sheme; više nema K1 upozorenja o nedostajućim padovima. Udvojeni kontakti međusobno su spojeni. BAT+–COM11 i NO14–paralelni R1/R2 rutirani su bez bakrene premosnice COM–NO.

## Dvije nepovezane veze

- `/VIN_PLUS`: završetak opterećenja još nije spojen s INA219 zbog nepotvrđenog fizičkog polariteta.
- `/BAT_MINUS`: INA strujni priključci nisu spojeni s potvrđenim NodeMCU/BT1 povratom iz istog razloga.

Udvojeni IN+ i IN− međusobno su povezani prema proizvođačkom CAD-u modula. To ne određuje vanjski smjer struje.

## Pet upozorenja usporedbe sa shemom

| Dio | Nedostajući funkcionalni padovi | Broj |
|---|---|---:|
| Q1 C3209 | 1/B, 2/C, 3/E | 3 |
| R4 | 1 i 2 | 2 |

Tri fizičke rupe Q1 iz izreza ostaju nedodijeljene jer grafički E/C/B natpisi još ne dokazuju pinout konkretnog C3209. R4 nema ekstrapolirane rupe izvan izreza.

**Dvije nepovezanosti nisu sve preostale žice.** A1 nosi `+5V_RELEJ`, a A2 `K1_C`, ali izvor napajanja i fizički kolektorski pad još ne postoje kao potvrđeni završeci. DRC ih zato ne može sve prikazati kao ratsnest. Napajanja i djelitelj ostaju otvoreni u shemi; ERC je **11 pogrešaka + 1 upozorenje, status 5**. NC nije maskiran oznakom No Connect.

Projektna pravila ostaju 0,25 mm minimalni vod/razmak, 0,15 mm tisak i 0,5 mm bakar–rub. Nema smanjivanja ozbiljnosti, dodanih izuzeća ili lažnih PWR_FLAG/No Connect oznaka. Tvornički neaktivne kategorije ostaju u `ignored_checks` JSON-a.

[Provjera PCB-a](board-check.txt) provjerava svih 23 prethodna segmenta, ukupno 33 segmenta/7 bakrenih mreža, mapiranje i koordinate svih osam K1 padova, podudaranje s osam pinova modela, kontinuitet COM/BAT+ i NO/opterećenja, udvojene kontakte, odsutnost vanjskog INA i neprovjerenog C3209/napajanja te izvorne hashove. Položaji prema fotografijama i postojeći razmaci tijela otpornika zadržani su.

**Proizvodni blokatori:** izravna provjera točnih TE dimenzija/tolerancija (PDF proxy 403; korištena je provjerljiva KiCad geometrija), C3209 pinout, puni R4 raster, konkretni moduli/držač, otpornici i savijanje izvoda, napajanja/zaštite/djelitelj te mehanička i termička provjera. Nula geometrijskih nalaza ne odobrava izradu. [PCB.md](../../PCB.md) navodi status svih dijelova.
