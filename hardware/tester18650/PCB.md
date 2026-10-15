# PCB P1 — raspored prema fotografijama, nije za proizvodnju

Postojećem KiCad projektu dodan je pravi uređivi [tester18650.kicad_pcb](tester18650.kicad_pcb), spremljen KiCadom 10. **To je PCB raspored s djelomično izvedenim bakrom i otvorenim mehaničkim pitanjima, a ne završena pločica za naručivanje.**

- [PDF rasporeda komponenti, 1:1](tester18650_pcb_layout.pdf)
- [3D prikaz PNG](tester18650_pcb_3d.png) i [uređivi/pregledni GLB model](tester18650_pcb_3d.glb)
- [DRC izvještaj](reports/pcb/DRC.md), [izvorni JSON](reports/pcb/drc.json) i [izvorni tekst](reports/pcb/drc.rpt)
- [Izvori geometrije](pcb_sources/reference-geometry.json), [raspored i razmaci](reports/pcb/placement-map.json), [provjera PCB-a](reports/pcb/board-check.txt)

## Primarni vizualni izvor

Korisnikov PDF `tester18650_fotoreferenca_obje_strane.pdf`, jedna stranica: gornja strana lijevo i već vodoravno zrcaljena donja strana desno. Druga strana nije ponovno zrcaljena. SHA-256 izvornika zabilježen je u manifestu izvora; originalne korisnikove fotografije nisu ponovno objavljene u javnom repozitoriju.

Zadržan je prepoznatljiv raspored: **NodeMCU gore lijevo s USB-om prema gore, relej u sredini gore, držač baterije uz desni rub, C3209 ispod releja, dva otpornika ispod njega, INA219 dolje lijevo.** R3/R4 su rezervirani u zoni sitnih komponenti između NodeMCU-a i upravljanja. Fotografija ne omogućuje pouzdanu identifikaciju svakog malog otpornika niti fizičko mjerenje njegovih izvoda.

Odbačen je početni Adafruit predložak: fotografija pokazuje ljubičasti Soldered INA219 breakout s četiri priključka i easyC konektorima. Fotografija NodeMCU-a pokazuje CH340 i oznaku Ver 0.1; firmware `nodemcuv2` ne određuje njegovu mehaničku varijantu. Zato referentni CH340 footprint nije proglašen potvrđenim footprintom konkretnog klona.

**Donja fotografija služi za usporedbu položaja i provjeru vidljivosti. Nisu dodane električne veze pretpostavljanjem krajeva preklopljenih zelenih žica, skrivenih lemova, baze/emitera, djelitelja ili relejnih izvoda.** Bakrene trase u ovom prijedlogu nove su trase potvrđenih mreža, nisu tvrdnja da su reproducirane sve žice na fotografiji.

## Dimenzije i footprintovi

| Dio | Izvor / provjera | Stanje u PCB-u |
|---|---|---|
| J1 NodeMCU | Izvorni NodeMCU CH340 DevKit `ESP12_DEVKIT.lbr`: raster 2,54 mm, redovi 27,94 mm, referentni obris širine 30,48 mm. Izvor i puni hash su u manifestu. | Referentni footprint s USB-om gore. Konkretni Ver 0.1 klon i konačno pristajanje/otvori **nisu potvrđeni**; nije upotrijebljen uži CP2102/Amica predložak. |
| J2 INA219 | Izvorni Soldered SKU 333066 KiCad CAD V1.0: obris 38 × 22 mm, četiri upravljačka priključka na 2,54 mm, strujni izvodi na 5 mm. Provjerene koordinate i promjeri svih osam izvoda. Izvorni STEP također je od proizvođača. | Oblik i funkcije odgovaraju fotografiranoj obitelji. Točnu reviziju, način montaže i tolerancije treba potvrditi prije izrade. Logički indeksi sheme mapirani su po funkciji, ne po redoslijedu pinova generičkog konektora. |
| K1 RT314006 | Oznaka se čita s fotografije. Pregledani KiCad Schrack RT1 kandidati imaju različite 5-/8-izvodne varijante; dostupni podatci ne dopuštaju proizvoljan izbor. Proizvođački web PDF nije bio dostupan iz okruženja (HTTP proxy 403). | **Rezervirano područje 18 × 34 mm, bez padova ili bušenja. To nije izmjereno kućište.** |
| Q1 C3209 | Fotografija pokazuje položaj i tranzistorsko kućište, ali ne potvrđuje proizvođača, mjeru ni B/C/E raspored. | Područje 12 × 10 mm, bez izmišljenog TO-92 pinouta. |
| R1/R2 22 Ω / 5 W | Oznake 5W22RJ i položaj vidljivi su na fotografiji. Proizvođač, puni broj dijela, razmak izvoda i montažna visina nisu potvrđeni. | Dvije rezervacije po 20 × 14 mm. Nema izmišljenih rupa ni tijela cementnog otpornika. |
| R3/R4 10 kΩ / 20 kΩ | Vrijednosti su iz dokumentacije; kućište, raster i topologija nisu određeni. | Rezervacije 8 × 8 mm bez padova i bakra. |
| BT1 / BTH1 | BT1 su dvije lemne točke za žice: raster 6 mm, rupa 1,2 mm, odabir za novi PCB. Nije identificiran tvornički konektor ili footprint držača sa slike. BTH1 je samo rezervacija uz desni rub. | Odabir presjeka žice, raster stvarnog držača i rasterećenje sile ostaju otvoreni. BTH1 površina 22 × 98 mm **nije mjera stvarnog držača**. |

Svi izrazi **AREA / ALLOCATION / TBD** označavaju prostor koji je projektant ostavio za buduće dovršenje, a ne neprovjerenu fizičku dimenziju komponente. Nepoznate komponente nemaju skrivena bušenja. Standardni TO-92 ili nasumičan power-resistor footprint nisu dodijeljeni samo na temelju izgleda ili snage.

Izvorni proizvođački podaci, licence i pin-mapping pohranjeni su u `pcb_sources/`; lokalna biblioteka `footprints/Tester18650.pretty` čini projekt prenosivim. Originalni Soldered CAD ostavljen je nepromijenjen. Referentna NodeMCU geometrija ne zamjenjuje identifikaciju klona.

## Električne i termičke granice

Bakrom su povezane samo:

- GPIO2/D4 ↔ SDA INA219, F.Cu, 0,35 mm;
- GPIO5/D1 ↔ SCL INA219, B.Cu, 0,35 mm;
- NodeMCU GND ↔ BAT− lemna točka, F.Cu, 0,8 mm, prema izričitoj postojećoj dokumentaciji.

VIN+/VIN−, INA219 VCC/GND, relej, bazni sklop, emiter i djelitelj nemaju proizvoljne bakrene trase. R2 funkcionalna shema i dalje prikazuje pretpostavljeni smjer struje INA219, ali taj smjer nije automatski pretvoren u spoj na PCB-u. Nema bakrenih zona koje bi skriveno povezale nepoznate mreže.

Ploča **116 × 132 × 1,6 mm** i četiri M3 prolaza od 3,2 mm predstavljaju novi projektni odabir, ne izmjeru perfboarda s fotografije. Raspored je proširen radi prostora: između rezervacija R1/R2 je 10 mm, a između njihovih bočnih rubova i INA219/držača ostavljeno je 13 mm. Ispod područja opterećenja nema vodova, via ni bakrenih poligona; dodan je i konzervativni RF keepout.

To nisu dokazani razmaci od stvarnih vrućih tijela dok se ne potvrde njihova kućišta. Pri 4,2 V i 22 Ω na svakom otporniku očekuje se oko 0,80 W; oznaka 5 W nije tvrdnja da disipacija u ovom testu iznosi 5 W. Termička simulacija, temperatura baterije, visina otpornika i ventilacija nisu provjereni. Ne tvrdi se da je dizajn termički siguran ili spreman za proizvodnju.

## Što prikazuje 3D

GLB je izvoz stvarnog PCB-a iz KiCada 10; PNG je render tog GLB-a u Blenderu. Izvorni CLI `pcb render` rušio se statusom 139 u ovom cloud okruženju, pa nije korišten izmišljeni zamjenski prikaz ili slika nepovezanog PCB-a.

Soldered INA219 koristi proizvođački STEP model, iz kojega je uklonjen samo opcijski vijčani terminal koji na fotografiji nije ugrađen. Ostalih 28 izvornih tijela sačuvano je bez zamjene dimenzija; izvor i zapis preinake priloženi su uz projekt. **Plavo je referentni plan NodeMCU-a, a jantarne tanke plohe su rezervirani prostori; nisu 3D kućišta releja, tranzistora, otpornika ili baterije.** Njihova debljina 0,02 mm služi samo grafičkom prikazu i nije fizička mjera dijela. Ne provjeravaju se montažne visine, dodiri ili pristajanje stvarnih kućišta na temelju ovih ploha. Za ta tijela nije izmišljena visina.

## Ponoviti provjere

```sh
./tools/validate_pcb.sh
# Vraća 5 jer DRC ima neriješene nalaze.
```

Skripta izvozi PDF, GLB, oba DRC izvještaja, pokreće provjeru padova/mreža/rasporeda te stvara PNG iz GLB-a. Potrebni su KiCad 10 i Blender za izvoz/render. Generator plana `tools/build_pcb.py` zahtijeva KiCad pcbnew Python API; grafičke STEP oznake nastaju pomoću `tools/make_marker_models.py` i `cadquery-ocp`. Generatori nisu potrebni za otvaranje i uređivanje predanog `.kicad_pcb`.

Prije proizvodnje moraju se dovršiti stvarni footprintovi i pinoutovi K1/Q1/R1–R4/držača, potvrditi referentni klon i revizija modula, napajanja, zaštite i preostale električne veze te provesti ponovni ERC, puni DRC i termička/mehanička provjera. Gerberi i proizvodne bušilice namjerno nisu isporučeni kao odobrenje za izradu.
