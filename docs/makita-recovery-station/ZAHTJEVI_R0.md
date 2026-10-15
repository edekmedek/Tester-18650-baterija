# Makita Recovery Station — projektni zahtjevi i arhitektura R0
Datum: 2026-10-15 · Status: **projektni dokument, nije shema za izradu ni odobrenje za punjenje**

## Polazište: već izrađeno
- Berlin, lipanj–srpanj 2026.: servisni prototip u kućištu, fotografija korisnika (dvije osmerokanalne relejne ploče, DC/DC modul, upravljačka pločica, razvod).
- Makita LXT / BL1850B: komunikacija s BMS-om preko servisnog konektora; ArduinoOBI i Python; očitanja stanja i pet serijskih grupa. Prema ranijim pokusima naredba za otključavanje može uspjeti u komunikaciji, ali originalni punjač ipak može odbiti paket.
- Poznata konfiguracija: **5S**, tipično **5S2P** (deset 18650 ćelija); pet grupa nisu deset neovisnih ćelija.
- Zaseban funkcionalni jednokanalni 18650 tester dokumentiran u [V1](../../hardware/tester18650/DOKUMENTACIJA_POSTOJECEG_TESTERA_V1.md). Ne rastavljati ga.
- Ranije dogovorena servisna ideja: mjerenje pet grupa i ukupnog napona, izračun max–min odstupanja; eventualno selektivno punjenje, prvotno predloženo do 1 A; nakon neuspješne obnove zasebno ispitivanje ćelija.
- **Ne pretpostavljati** da su fotografirani moduli, njihove oznake ili izvedeni spojevi električki potvrđeni samo zato što su na fotografiji.

## Cilj
Profesionalno projektirana servisna stanica s dva **električki odvojena podsustava**:

**A. Dijagnostika sastavljenog Makita paketa (5S):**
1. Identifikacija modela i očitanje BMS-a gdje je protokol potvrđen.
2. Mjerenje svih pet naponskih grupa, ukupnog napona i temperature.
3. Evidencija odstupanja, ponašanja pod opterećenjem i povijesti.
4. Servisne funkcije isključivo uz prethodnu procjenu sigurnosti; nikad automatsko poništavanje sigurnosne blokade kao zamjena za otkrivanje uzroka.
5. Individualno dopunjavanje grupa preko BMS priključaka **nije odobreno** samo na temelju ranijeg plana 1 A. Prije projektiranja potrebni su dokumentirani strujni kapaciteti priključaka/vodova, stvarna topologija, izolacija, neovisna ograničenja napona/struje/temperature i procjena opasnosti. Po potrebi se ova funkcija izostavlja.

**B. Analizator izdvojenih 18650 ćelija:**
1. Cilj: **10 neovisnih utora** za tipični 5S2P paket.
2. Svaki utor: provjera polariteta i početnog napona → CC/CV punjenje → odmor → kontrolirano pražnjenje s mjerenjem mAh/Wh → odmor → završno CC/CV punjenje.
3. Mjerenje temperature ćelije, neovisna zaštita od previsokog napona/struje/temperature i vremenski nadzor; kod gubitka senzora ili komunikacije izlazi prelaze u sigurno isključeno stanje.
4. Mjerenje unutarnjeg otpora kao zasebna **kalibrirana** funkcija s definiranim postupkom i uvjetima; ne obećavati točnost bez validacije.
5. Zapis po ćeliji: jedinstveni ID, oznaka izvornog paketa, utor, datum, početni i završni napon, mAh, Wh, strujni profil, temperatura, izmjereni otpor, status, razlozi odbijanja.
6. Sustav ne odlučuje da je ćelija sigurna za ponovno ugrađivanje samo na temelju kapaciteta ili otpora.

## Arhitektura
- ESP32 ili drugi odgovarajući kontroler za orkestraciju; **kontroler nije jedina sigurnosna barijera**.
- Deset ponovljivih, međusobno nezavisnih kanala s posebnim upravljanjem punjenjem/pražnjenjem i mjerenjem.
- Odvojeni mjerni front-end za 5S paket, uz pravilno zajedničko mjerenje potencijala ili odgovarajuću izolaciju. **Ne spajati međučvorove serijskog paketa izravno na zajednički GND.**
- Mrežno napajanje samo preko certificiranog vanjskog AC/DC adaptera; na pločici niskonaponski razvod, osigurači i zaštite.
- Lokalna baza podataka na računalu/HA poslužitelju; uređaj šalje događaje i mjerenja. Nestanak mreže ne smije utjecati na sigurnost punjenja.
- Kućište, hlađenje, razmaci, odvod topline, mehaničko držanje ćelija i zaštita od slučajnog kratkog spoja projektiraju se zajedno s PCB-om.

## Obavezna projektna dokumentacija prije narudžbe
1. **Zahtjevi** s mjerljivim granicama: podržana kemija i format, maksimalne struje, cutoff, vrijeme, temperature, točnost, sigurnosni scenariji.
2. **Shema** s točnim kataloškim oznakama, pinoutima i izvorima datasheetova; svaka komponenta ima nabavljiv dio.
3. **BOM** s proizvođačem, brojem dijela, alternativama i dostupnošću.
4. **KiCad PCB** s provjerenim footprintovima i 3D mehanikom; provjera opterećenja vodova, topline i izolacije.
5. **ERC i DRC** bez nerazjašnjenih grešaka; nula DRC kršenja sama po sebi nije dokaz ispravnosti.
6. **Analiza kvarova**: obrnuti polaritet, odspojena ćelija, loš kontakt, kratki spoj, pregrijavanje, neispravan senzor, zaglavljen MOSFET/relej, reset kontrolera, nestanak mreže/napajanja.
7. **Protokol ispitivanja prototipa**: bez ćelija → simulirana ćelija/elektroničko opterećenje → jedan kanal uz nadzor → svih deset uz mjerenje temperature → kalibracija → revizija PCB-a ako treba.
8. **Proizvodne datoteke** (Gerber/drill, pick-and-place ako treba, montažni crteži) tek nakon uspješnih provjera.

## Izričite zabrane pretpostavki
- Ne pretpostavljati da dva relejna modula daju deset sigurnih punjačkih kanala.
- Ne zaključivati s fotografije da DC/DC modul ima CC/CV ili izolaciju.
- Ne koristiti servisne kontakte BMS-a za punjenje od 1 A bez provjere dopuštene struje i izolacije.
- Ne zaobilaziti BMS zaštite ni tretirati softverski unlock kao dokaz zdravlja paketa.
- Ne naručivati PCB na temelju neprovjerenih footprintova i nerutiranih mreža.
- Ne mijenjati postojeći funkcionalni 18650 tester.

## Sljedeći projektantski paket R1
Pripremiti **tablicu zahtjeva i sigurnosnu blok-shemu**, zatim usporediti stvarne komercijalno dostupne IC-ove za jedan kanal CC/CV punjenja, pražnjenja i mjerenja. Izbor dijelova mora se temeljiti na datasheetovima, a ne na generičkim nazivima modula. Tek potom zaključati električnu shemu i replicirati kanal deset puta.
