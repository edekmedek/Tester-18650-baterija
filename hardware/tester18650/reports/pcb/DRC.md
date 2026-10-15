# PCB DRC P1 — stvarni rezultat, pločica nije za proizvodnju

Provjeren je `tester18650.kicad_pcb` u **KiCadu 10.0.4** s `--schematic-parity --all-track-errors --severity-all --exit-code-violations`. Svi izvorni nalazi ostaju u [drc.json](drc.json) i [drc.rpt](drc.rpt); [izlazni status je 5](drc-exit-status.txt).

| Kategorija nativnog izvještaja | Rezultat |
|---|---:|
| Geometrijska DRC kršenja | 0 |
| Nepovezane veze, `unconnected_items` | **3 pogreške** |
| Usporedba sheme i PCB-a, `net_conflict` | **16 upozorenja** |
| Dodana pojedinačna DRC izuzeća | 0 |

**Rezultat nije čist DRC.** Nula geometrijskih kršenja ne znači dovršen električki ili mehanički projekt.

## Što ostaje otvoreno

Tri nepovezanosti odnose se na VIN mreže INA219: dva izvoda IN+ nisu povezana bakrom nosača, dva izvoda IN− nisu povezana bakrom nosača i IN− nije proizvoljno spojen na zajednički BAT−. Dio kontakata pripada istim internim mrežama modula, ali DRC nosača ne dokazuje unutarnju vezu/varijantu i prijavljuje sve tri veze. Polaritet VIN+/VIN− u prethodnoj shemi bio je projektna pretpostavka; nije pretočen u bakar.

Šesnaest upozorenja iz usporedbe sheme i PCB-a znači da **nedostaju stvarni padovi**:

| Dio | Nedostajući padovi | Broj |
|---|---|---:|
| K1 RT314006 | A1, A2, COM/11, NO/14, NC/12 | 5 |
| Q1 C3209 | B/1, C/2, E/3 | 3 |
| R1 i R2 | oba kraja svakog otpornika | 4 |
| R3 i R4 | oba kraja svakog otpornika | 4 |

Ti dijelovi imaju uređive položaje i označene rezervirane površine, ali **nemaju izmišljene rupe, rastere ili pinoutove**. Zbog toga nedovršeni krug napajanja/opterećenja ne treba tumačiti kao samo tri preostala segmenta koja treba povući. Prvo nedostaju fizički footprintovi i pouzdani spojevi. Držač baterije također nema potvrđen montažni footprint; BT1 su nove projektne lemne točke za njegove žice.

## Što je provjereno

- Petnaest bakrenih segmenata pripada isključivo trima potvrđenim mrežama: SDA, SCL i NodeMCU GND–BAT−. Provjerena je neprekinuta veza do namjenskih padova.
- Nema vodova po pretpostavljenom VIN polaritetu, skrivenih poligona, proizvoljnog baznog otpornika, emiterske veze ili redoslijeda djelitelja.
- Provjerene su koordinate i rupe referentnih NodeMCU/INA219 footprintova prema pohranjenim proizvođačkim izvorima. To **ne potvrđuje** konkretni NodeMCU klon, reviziju stvarnog modula niti njihovo konačno mehaničko pristajanje.
- Projekt ima eksplicitno najmanje 0,25 mm vodove i razmake, 0,15 mm razmak tiska i 0,5 mm bakar–rub. Vodovi su 0,35 mm za I²C i 0,8 mm za potvrđeni povrat. Ne tvrdi se da su ovo proizvodna pravila odabranog proizvođača PCB-a.
- Održani su položaji prema gornjoj fotografiji: USB gore lijevo, relej gore u sredini, baterija desno, opterećenje ispod releja i INA219 dolje lijevo. Nisu nagađani skriveni spojevi donje/zrcaljene fotografije.
- Između projektnih područja R1/R2 je 10 mm, a bočno prema INA219 i držaču 13 mm. To su razmaci **rezervacija**, ne potvrđena udaljenost od još neidentificiranih vrućih kućišta.

KiCad je pri prvom spremanju PCB-a dopunio `.kicad_pro` svojim zadanim PCB postavkama; dodatno su postavljeni navedeni minimalni razmaci. Ozbiljnost prijavljenih nalaza nije smanjivana. Nema dodatnih izuzeća; tvornički neaktivne kategorije ostaju navedene u `ignored_checks` izvornog JSON-a. Uključena je usporedba sa shemom kako nedostajući padovi ne bi ostali nevidljivi.

**Preostali proizvodni blokatori:** stvarni footprintovi K1/Q1/R1–R4/držača, točan NodeMCU i revizija INA219, napajanja i zaštite, fizički pinoutovi, bazni sklop i djelitelj te mehanička/termička provjera. ERC sheme također ostaje **11 pogrešaka + 1 upozorenje**. Fotografije i ovaj DRC nisu potvrda sigurnosti ni proizvodne spremnosti.
