# Tester 18650 — KiCad 10, rekonstrukcija R1

**Status: dokumentacijska električna rekonstrukcija; nije izvedbeno provjerena.**

Projekt je izrađen iz potvrda korisnika od 15.10.2026. i svih šest aktualnih Markdown dokumenata repozitorija. Sheme D6–D12 nisu korištene kao dokaz ispravnosti. Povijesni `docs/SCHEMA_D9_STATUS.md` nije izvor spojeva. Aktualni uređaj je NodeMCU ESP8266 (`nodemcuv2`); stariji navodi ESP32 u dokumentaciji opisuju raniji zapis.

## Funkcionalni strujni krug — radna shema za dovršetak

Korisnik je više puta potvrdio slijed pražnjenja, bez potrebe za ponovnim praćenjem istih žica:

```text
BAT+ → radni kontakt releja → (22 Ω / 5 W || 22 Ω / 5 W)
     → INA219 mjerni put (VIN+ / interni shunt / VIN−) → BAT−
```

**Funkcionalni zaključak:** u električnoj shemi prikazati relejni radni kontakt **COM–NO**, jer se opterećenje uključuje aktivacijom releja; NC nije dio funkcionalnog puta pražnjenja. Brojevi nožica stvarnog RT314006 nisu time utvrđeni, ali **ne trebaju biti prepreka za spajanje standardnog funkcionalnog simbola**. Ne tražiti korisnika da provjerava očigledni serijski redoslijed.

**Orijentacija INA219:** za standardni prikaz pozitivnog smjera struje označiti `VIN+` sa strane opterećenja, `VIN−` sa strane BAT−. To je **projektna pretpostavka**, a ne izmjerena činjenica; firmware računa apsolutnu vrijednost struje pa iz očitanja ne slijedi polaritet. Nije potrebno rastavljati funkcionalni uređaj radi crtanja načelne sheme.

**Važno:** sljedeća revizija KiCad datoteke treba **stvarno spojiti** COM–NO i VIN+/VIN− u uređivoj shemi te ih označiti kao funkcionalno rekonstruirane. Sam tekst u README-u nije zamjena za izmjenu KiCad sheme. Nepoznate fizičke pinove, bazni otpornik, napajanje i djelitelj prikazati bez izmišljanja.

## Isporuka

- [tester18650.kicad_pro](tester18650.kicad_pro) — pravi KiCad projekt; otvoriti u KiCadu 10.
- [tester18650.kicad_sch](tester18650.kicad_sch) — uređiva shema sa standardnim ugrađenim KiCad simbolima, električnim vodovima, oznakama mreža i spojevima.
- [tester18650.pdf](tester18650.pdf) — vektorski PDF, jedan list A3 vodoravno; izvezen iz iste sheme KiCadom 10.0.4.
- [reports/ERC.md](reports/ERC.md) — tumačenje ERC-a i ograničenja provjere.
- [reports/erc.rpt](reports/erc.rpt), [reports/erc.json](reports/erc.json) — izvorni CLI izvještaji, bez uklanjanja nalaza.
- [reports/netlist.xml](reports/netlist.xml) — KiCadova izvezena električna lista mreža.
- [reports/VALIDATION.md](reports/VALIDATION.md) — provedene provjere i izvor alata.

## Kako čitati shemu

List odvaja strujni put, zavojnicu i tranzistor, digitalna sučelja te vrijednosti djelitelja. Zeleni vodovi označavaju potvrđene funkcionalne mreže. Otvoren pin ili razmak predstavlja nedostatak podatka, a ne potvrdu da je pin u uređaju nepovezan. Ne koristi se oznaka `No Connect` za nepoznate veze.

Potvrđen je slijed **BAT+ → relejni kontakt → R1 || R2 → INA219 → BAT−**. Međutim, nije potvrđeno koji se kontakti releja fizički koriste ni na koji VIN priključak INA219 ide koji kraj strujnog puta. Zato su na tim granicama ostavljeni prekidi umjesto izmišljenih spojeva. TP1–TP6 označavaju dokumentacijske krajeve mreža; nisu ugrađene testne točke i izuzeti su iz BOM-a i pločice.

J1 i J2 koriste standardni simbol `Connector_Generic:Conn_01x06` kao **logička sučelja modula**. Nisu tvrdnja da postoji takav fizički konektor; kao logički prikazi izuzeti su iz BOM-a i pločice. Brojevi 1–6 su indeksi u ovoj shemi i nisu fizički brojevi nožica ni redoslijed pinova na pločici. NodeMCU i INA219 namjerno nisu zamijenjeni simbolima drugog modela pločice ili samog IC-a s pretpostavljenim okolnim sklopom.

| Logički indeks | J1 — NodeMCU ESP8266 | J2 — INA219 modul |
|---|---|---|
| 1 | D5 / GPIO14, izlaz prema baznom sklopu | SDA, povezan s GPIO2 |
| 2 | D4 / GPIO2, SDA | SCL, povezan s GPIO5 |
| 3 | D1 / GPIO5, SCL | VCC, fizički izvor nepoznat |
| 4 | A0, ulaz iz nepotvrđenog djelitelja | GND, referenca nepoznata |
| 5 | Napajanje pločice, ulaz i izvor nepoznati | VIN+, dodjela strujnog puta nepoznata |
| 6 | GND, BAT− prema aktualnom dokumentu D2 | VIN−, dodjela strujnog puta nepoznata |

K1 koristi standardni `Relay:Relay_SPDT`, vrijednosti `Schrack RT314006`. Zavojnica je prikazana između mreže +5 V i kolektora Q1. A1/A2 i 11/12/14 pripadaju funkcionalnom simbolu; ne potvrđuju raspored izvoda konkretnog releja. Spoj +5 V na A1 u simbolu nije identifikacija fizičke nožice niti potvrda polariteta eventualne ugrađene diode. Nazivna zavojnica je 6 V DC, a potvrđeno napajanje 5 V; pouzdanost uklapanja pri tom naponu nije izmjerena ovom provjerom.

Q1 koristi standardni generički NPN simbol, oznake C3209. B/C/E su funkcije; brojevi 1/2/3 nisu utvrđeni raspored nožica kućišta. Ne postoji dodijeljen footprint. Shema nije priprema za proizvodnju PCB-a.

## Nepoznate veze i granice rekonstrukcije

| Oznaka | Što nedostaje | Kako je prikazano |
|---|---|---|
| N1 | Fizički raspored RT314006; koji su kontakti korišteni, COM/NO/NC i veza na BAT+ te ulaz opterećenja | TP1/TP2 su odvojeni; kontakti K1 11/12/14 otvoreni. Zavojnica povezana funkcionalno, raspored izvoda nije potvrđen. |
| N2 | INA219 VIN+/VIN− orijentacija, stvarna veza i vrijednost internog shunta, odnos strujnog puta prema masi | TP3 je kraj nakon R1/R2, TP4 je BAT−; nisu pridruženi VIN+/VIN− pinovima J2. `0,11425 Ω` postoji samo kao firmware podatak, nije fizički izmjeren shunt. |
| N3 | Točan tip/raspored C3209, spoj emitera, bazni otpornik i put GPIO14 do baze; zaštitna dioda zavojnice i njezin polaritet | Zavojnica → kolektor je spojena; baza i emiter su otvoreni. TP5 je kraj GPIO14. Bazni otpornik i dioda nisu izmišljeni ni dodani. |
| N4 | Redoslijed 10 kΩ/20 kΩ, spojevi na BAT+/A0/GND, dodatni djelitelj na NodeMCU pločici | R3 i R4 imaju otvorena oba kraja. A0 završava na TP6. Faktor 9.5079 je napomena o kalibraciji, ne dokaz omjera djelitelja. |
| N5 | Fizička masa INA219 i odnos VIN−, BAT− i GND; prisutnost, vrijednosti i naponska domena I²C pull-upova | J2 GND otvoren. SDA/SCL su povezani prema potvrđenim GPIO-ima; pull-upovi nisu pretpostavljeni. BAT−/NodeMCU GND povezani su samo prema izričitom navodu u D2. |
| N6 | Izvor +5 V releja, način napajanja NodeMCU-a i INA219, stvarna VCC razina modula | Mreža +5V_RELEJ nema pretpostavljen izvor; napajanje J1 i VCC J2 otvoreni. |

Dodatno: OLED je uklonjen i nije nacrtan. Zaštita od obrnutog polariteta prema D2 nije ugrađena. Osigurač, zaštita opterećenja od pregrijavanja i ponašanje releja pri uključivanju napajanja nisu fizički potvrđeni i ne prikazuju se kao postojeće komponente. Ovaj projekt ne mijenja firmware ni podešenja cutoffa.

## Ponovljiva provjera

Na pripremljenom Debian 13 amd64 cloud računalu instalacija se može ponoviti naredbom `./tools/install_cloud.sh` (bez administratorskih prava). Ostale platforme trebaju službenu KiCad 10 instalaciju.

U direktoriju projekta, uz KiCad 10 i Python 3:

```sh
./tools/validate.sh
```

Može se pozvati iz bilo kojeg radnog direktorija. `tools/kicad.sh` bira KiCad 10 iz pripremljene lokalne cloud instalacije ili `kicad-cli` na PATH-u; varijablom `KICAD_CLI` moguće je odabrati drugu izvršnu datoteku. Izolira korisničke KiCad postavke u privremenom direktoriju, bez promjene HOME-a. `sym-lib-table` koristi standardni `KICAD10_SYMBOL_DIR`.

Skripta ponovno izvozi PDF i listu mreža, pokreće nativni ERC s `--exit-code-violations` te provjerava stvarne izvozne mreže i točan popis poznatih ERC nalaza. **Uspjeh skripte znači da rekonstrukcija odgovara dokumentiranom stanju; ne znači čist ERC.** Nativni ERC izlazni status 5 ostaje zapisan u `reports/erc-exit-status.txt`. Nakon potvrde novih fizičkih spojeva potrebno je ažurirati shemu, tablicu nepoznanica i očekivanja provjere zajedno.
