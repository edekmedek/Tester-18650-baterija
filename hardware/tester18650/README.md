# Tester 18650 — postojeći KiCad 10 projekt, R2

**Funkcionalni strujni krug je spojen u uređivoj shemi. Fizičko ožičenje i pinout nisu potvrđeni. ERC nije čist: 11 pogrešaka i 1 upozorenje.**

R2 nastavlja postojeći projekt iz commita `bfc8b56`: isti `.kicad_pro`, isti list i isti UUID-i jedanaest zadržanih simbola. Nije izrađen zaseban projekt. Prekidi TP1–TP4 uklonjeni su i zamijenjeni stvarnim električnim vodovima. Raspored lista i oznake priključaka uređeni su radi čitljivosti.

## Funkcionalni krug u shemi

```text
BAT+ → K1 COM (11) → NO (14) → (R1 22 Ω / 5 W || R2 22 Ω / 5 W)
     → VIN+ → RSH1, interni shunt INA219 → VIN− → BAT−
```

COM–NO koristi se prema korisnikovu zadatku i ponašanju firmwarea: aktivacija releja uključuje opterećenje. NC (12) ne sudjeluje u pražnjenju; ostavljen je otvoren i njegov je ERC nalaz vidljiv. Brojevi 11/12/14 i A1/A2 pripadaju standardnom funkcionalnom simbolu, a nisu potvrđeno mapiranje izvoda stvarnog RT314006.

**VIN+ je spojen prema opterećenju, VIN− prema BAT− kao izričito označena projektna pretpostavka.** Firmware koristi `fabsf(ina219_current)`, pa pozitivna prikazana struja nije dokaz fizičkog polariteta. RSH1 prikazuje postojeći interni mjerni element modula, ne dodatni vanjski otpornik. Njegova je vrijednost označena `vrijednost ?`; firmware parametar `0.11425 Ω` naveden je zasebno kao kalibracijski podatak. RSH1 je izuzet iz zasebnog BOM-a i PCB-a jer pripada modulu.

Zavojnica K1 ostaje spojena između +5 V i kolektora Q1, oznake C3209. Nazivna zavojnica je 6 V DC, a dokumentirani pogon 5 V. Nije provjerena margina uklapanja. Q1 koristi generički NPN simbol; B/C/E su funkcije, a 1/2/3 nisu potvrđeni raspored nožica kućišta.

## Izvori za upravljanje i mjerenje

Pregledan je puni [ESPHome firmware](../../firmware/battery-tester-8266-wifi-test.yaml), njegov [opis](../../firmware/README.md), aktualna dokumentacija i korisnikove potvrde. Stare D6–D12 sheme nisu korištene kao dokaz.

Firmware potvrđuje `nodemcuv2`, GPIO14 bez inverzije (`ALWAYS_OFF` i isključenje pri bootu), SDA GPIO2, SCL GPIO5, I²C 100 kHz, INA219 `0x40` i A0 s faktorom `9.5079`. Prikazane su i radne napomene: uključivanje nakon 500 ms i početni cutoff 3,00 V kroz pet uzastopnih sekundi. Firmware nije izmijenjen ni flashan.

Firmware ne određuje bazni otpornik, spoj emitera, zaštitnu diodu, redoslijed otpornika djelitelja ni napajanja modula. Zato nema izmišljenog otpornika između GPIO14 i baze, izravnog kratkog spoja GPIO14–B, pretpostavljenog emitera na masi ni odabranog redoslijeda R3/R4. Pouzdani spojevi +5 V → zavojnica → kolektor i GPIO-i su nacrtani; preostale granice jasno su označene N3/N4. R3 = 10 kΩ i R4 = 20 kΩ zadržani su s otvorenim krajevima jer faktor A0 ne određuje njihovu fizičku topologiju.

## Logička sučelja i oznake

J1/J2 koriste standardni `Connector_Generic:Conn_01x06` kao logičke prikaze modula, izuzete iz BOM-a i pločice. **Brojevi 1–6 su indeksi sheme, ne fizički raspored nožica.** Svaki priključak dodatno je označen funkcijom na listu. TP5 i TP6 su samo dokumentacijski završeci prema nepoznatom baznom sklopu i djelitelju; nisu ugrađene testne točke.

| Indeks | J1 — NodeMCU ESP8266 | J2 — INA219 modul |
|---|---|---|
| 1 | D5 / GPIO14 → TP5, bazni sklop nepoznat | SDA ↔ GPIO2 |
| 2 | D4 / GPIO2 ↔ SDA | SCL ↔ GPIO5 |
| 3 | D1 / GPIO5 ↔ SCL | VCC, otvoreno |
| 4 | A0 / ADC0 → TP6, djelitelj nepoznat | GND, otvoreno |
| 5 | Napajanje pločice, otvoreno | VIN+ ↔ opterećenje i RSH1/1 |
| 6 | GND ↔ BAT− prema dokumentu D2 | VIN− ↔ RSH1/2 i BAT−, projektna pretpostavka |

`BAT_MINUS` je jedini naziv povratne mreže, uključujući funkcionalni VIN−. `VIN_PLUS` je mreža između opterećenja i ulaza internog shunta. GND modula INA219 nije automatski spojen na VIN−/BAT−.

## Preostale nepoznanice

| Oznaka | Stanje u R2 |
|---|---|
| N1 | COM–NO funkcionalno spojen; fizički izvodi i raspored RT314006 nisu potvrđeni. NC je nekorišten. |
| N2 | VIN+/VIN− i interni shunt spojeni u serijski put. Orijentacija je pretpostavka; fizički polaritet, vrijednost i izvedba shunta nisu izmjereni. |
| N3 | Baza i emiter C3209, fizički pinout, bazni otpornik i zaštitna dioda nisu potvrđeni. Otvoreni B/E i prekid nakon TP5 ostaju vidljivi. |
| N4 | Vrijednosti 10 kΩ/20 kΩ su poznate; njihovi krajevi, redoslijed i eventualni djelitelj na NodeMCU-u nisu. TP6 i R3/R4 ostaju bez pretpostavljenih veza. |
| N5 | GND INA219 te vrijednosti i naponska domena I²C pull-upova nisu potvrđeni. J2 GND je otvoren. |
| N6 | Izvor +5 V za relej, ulaz napajanja NodeMCU-a i VCC INA219 nisu utvrđeni. J1/5 i J2/3 su otvoreni. |

OLED nije ugrađen i nije nacrtan. Nisu dodani nepotvrđeni zaštitni elementi. Footprintovi nisu dodijeljeni; shema nije odobrenje za izradu PCB-a ni potvrda sigurnosti fizičkog uređaja.

## Datoteke i provjera

- [KiCad projekt](tester18650.kicad_pro) i [uređiva shema](tester18650.kicad_sch).
- [Završni PDF](tester18650.pdf), A3 vodoravno, izvezen KiCadom 10.0.4 i vizualno pregledan.
- [ERC tumačenje](reports/ERC.md), [izvorni tekst](reports/erc.rpt) i [JSON](reports/erc.json).
- [Izvezene mreže](reports/netlist.xml), [rezultat provjere spojeva](reports/connectivity-check.txt), [provedena validacija](reports/VALIDATION.md).

```sh
cd /workspace/Tester-18650-baterija/hardware/tester18650
./tools/validate.sh
```

Skripta ponovno izvozi PDF i netlist, pokreće nativni ERC s `--exit-code-violations`, provjerava točne mreže i oba stanja radnog kontakta te zapisuje kontrolne zbrojeve. **Vraća status 5 jer ERC nije čist**, čak i kada provjera funkcionalnog puta prolazi. Ne mijenja se ozbiljnost ERC nalaza i ne dodaju se izuzeća, `No Connect` ili `PWR_FLAG` oznake. NC nalaz također je zadržan.

`tools/check_connectivity.py` može se pokrenuti zasebno: provjerava upravo izvezene mreže, zatvoren/otvoren COM–NO, obje paralelne grane i odsutnost premosnice opterećenja. To je provjera grafa spojeva, ne SPICE simulacija ili mjerenje struje. Kontrolni zbrojevi provjeravaju se naredbom `sha256sum -c reports/SHA256SUMS`.

KiCad 10 već je pripremljen u cloudu. `tools/kicad.sh` bira tu instalaciju ili `kicad-cli` na PATH-u; može se zadati `KICAD_CLI`. Standardne biblioteke koristi preko `KICAD10_SYMBOL_DIR`. Na istom Debian 13 amd64 računalu instalacija se po potrebi ponavlja s `./tools/install_cloud.sh`; ostale platforme trebaju službenu KiCad 10 instalaciju i Python 3.
