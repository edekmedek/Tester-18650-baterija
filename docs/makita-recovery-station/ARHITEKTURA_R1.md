# R1 — Specifikacija sustava i arhitektura električnih kanala
Datum: 2026-10-15. Status: **projektantski nacrt s otvorenim stavkama**. Nadovezuje se na [R0](ZAHTJEVI_R0.md). Ovaj dokument nije uputa za izravno spajanje litijskih ćelija.

## 1. Razgraničenje sustava

**Uređaj A — 10-kanalni analizator izdvojenih 18650** je prioritet za vlastiti profesionalni PCB. **Uređaj B — Makita 5S servisni priključak i BMS dijagnostika** ostaje zaseban električki podsustav, s vlastitim zaštitama i revizijom. Ne dijele mjerne ulaze niti se smiju slučajno povezati međučvorovi serijskog paketa na masu uređaja A.

### Blok dijagram uređaja A
```
Certificirani VANJSKI DC adapter
  |
  +-- ulazna zaštita / osigurač / mjerenje ulazne snage
  |
  +-- DC sabirnica / zasebni nadzor temperature i napajanja
  |      |
  |      +-- KANAL 1 [zaštita polariteta i kontakta] -- [CC/CV punjač] --+
  |      |                                                              |
  |      +-- KANAL 2 ... 10 (isti verificirani sklop)                    +-- [držač 18650]
  |                                                                     |
  |                       [upravljivo pražnjenje + mjerenje I/V] --------+
  |                                         |
  |                          [hardverska zaštita i senzor T]
  |
  +-- 3,3 V upravljačko napajanje -- ESP32 -- lokalni zaslon / mreža
                                     |
                                     +-- baza rezultata na HA/poslužitelju
```
Svaki kanal ima vlastiti analogni mjerni i energetski sklop. Punjenje i pražnjenje moraju biti **međusobno hardverski blokirani**, ne samo programski.

## 2. Predloženi početni projektni parametri (još NE zaključani)

| ID | Zahtjev / kandidat | Razlog i kriterij prihvaćanja |
|---|---|---|
| SYS-01 | 10 utora, pojedinačne 18650 Li-ion ćelije, 1S | Tipični Makita 5S2P paket; svaka ćelija neovisna |
| SYS-02 | U početnoj reviziji samo ćelije za koje je poznat proizvođački dopušten režim punjenja | Nema univerzalnog režima za sve nepoznate/istrošene ćelije |
| CHG-01 | CC/CV, završni napon najviše 4,20 V **samo za odgovarajuću kemiju** | Točan napon i tolerancija definiraju se prema konkretnoj ćeliji i punjačkom IC-u |
| CHG-02 | Početni kandidat punjenja 0,5 A/utor, prilagodljivo prema ćeliji | 10 utora = do 5 A zbirno na strani ćelija; stvarna ulazna snaga računa se nakon izbora topologije |
| DIS-01 | Početni kandidat pražnjenja 0,5 A/utor, podesivo | Maksimalno 10 × (4,2 V × 0,5 A) = 21 W ukupne topline; po kanalu do 2,1 W |
| DIS-02 | Početni cutoff kandidat 3,0 V, ovisno o ćeliji i testnom protokolu | Ne dopustiti da gubitak ADC signala nastavi pražnjenje |
| MET-01 | Napon, struja, mAh, Wh, vrijeme i temperatura po utoru | Integrirati stvarni protekli interval i validirati mjernu točnost |
| MET-02 | Unutarnji otpor mjeriti zasebnim kontroliranim impulsom / kalibriranim postupkom | Mjerenje uključuje otpor kontakta; poželjno 4-žično mjerenje ili korekcija |
| SAF-01 | Neovisni hardverski prekid pri prenaponu, prestruji, previsokoj temperaturi | ESP32 reset/bug ne smije ostaviti punjenje uključeno |
| SAF-02 | Odspojena ćelija, obrnuti polaritet, kratki spoj, nevaljano očitanje, predugo trajanje → isključenje kanala | Testira se simuliranim kvarovima, prije stvarnih ćelija |
| SAF-03 | Temperaturni senzor mora biti termički vezan uz ćeliju, ne samo PCB | Osigurati kontakt i detekciju odspojenog senzora |
| SAF-04 | Bez autonomnog ciklusa na napuhnutim, oštećenim, pregrijanim ili sumnjivim ćelijama | Obvezna početna vizualna i naponska provjera |
| DATA-01 | Lokalna baza: ćelija, izvorni paket, serija testa, kanal, mAh, Wh, T, otpor, status i greška | Ponovljivo uspoređivanje i trag odluka |
| DATA-02 | Nestanak Wi-Fi/HA ne prekida sigurnosnu logiku; zapis se sprema/ponavlja bez dupliciranja | Sigurnost ne smije ovisiti o mreži |
| PCB-01 | 10 kanala kao ponovljeni funkcionalni blokovi, termički razmaknuti | Proračun topline i struje prije layouta |
| PCB-02 | Nema mrežnog napona na PCB-u | Certificirani vanjski adapter |

**VAŽNO:** 0,5 A, 3,0 V i 4,20 V su *početni projektni kandidati*, ne potvrđene univerzalne vrijednosti. Kemija, datasheet ćelije, način mjerenja i sigurnosna analiza imaju prednost.

## 3. Stroj stanja jednog kanala

```
EMPTY
  -> INSERTED / CHECK (polaritet, V, T, kontakt)
  -> CHARGE_CC -> CHARGE_CV -> REST_1
  -> DISCHARGE_CC (integracija mAh/Wh, V, I, T)
  -> REST_2 -> FINAL_CHARGE_CC -> FINAL_CHARGE_CV
  -> COMPLETE / SAVE

BILO KOJE STANJE -> FAULT_LATCHED
   ako: overvoltage, overcurrent, overtemp, missing cell,
        reversed polarity, sensor invalid, timeout, supply fault,
        watchdog fail, charging and discharging simultaneously.
FAULT_LATCHED: hardverski izlazi OFF; događaj i razlog spremljeni;
               ponovno uključivanje samo nakon otklanjanja uzroka.
```

U stvarnoj shemi treba dokazati kako hardver prelazi u OFF i kada je MCU potpuno nefunkcionalan.

## 4. Proračun snage — početni omotač

Pri 10 × 0,5 A punjenja i 4,2 V, snaga isporučena ćelijama je do **21 W**. Uz učinkovitost punjača, napajanje kontrolera, ventilatore i rezervu, vanjski adapter treba dimenzionirati **nakon odabira IC-ova**, ne prema samih 21 W. Pri pražnjenju do **21 W** pretvara se u toplinu ako koristimo linearna elektronička opterećenja; to zahtijeva namjensko termičko rješenje i provjeru najgoreg slučaja.

Ako se punjenje i pražnjenje različitih kanala događaju istodobno, proračun obuhvaća **zbroj punjačkih ulaza i disipacije opterećenja**. Nije dopušteno pretpostaviti da se međusobno poništavaju.

## 5. Kriteriji izbora stvarnih IC-ova (sljedeći zaključak)

| Podsustav | Mora se potvrditi iz datasheeta |
|---|---|
| 1S punjač | CC/CV, regulacija struje, terminacija, termistor, input UVLO, fault status, dopuštena temperatura, mogućnost isključivanja |
| Opterećenje | stabilnost konstantne struje, SOA MOSFET-a pri 4,2 V, strujni shunt, toplina, fail-off |
| Mjerenje | raspon napona 0–4,3 V, mA rezolucija, kalibracija, offset, šum, mogućnost 4-wire |
| Sigurnosni nadzor | neovisni prenaponski/temperaturni pragovi, latched fault, hardverska međublokada |
| Kontroler | raspoloživost I²C/SPI/GPIO, multiplekseri ili više ADC-ova, watchdog, boot-safe pinovi |
| Napajanje | certificirani adapter, osigurači, naponski padovi, startna struja, EMI i termički budžet |
| Držač ćelije | kontaktni otpor, maksimalna struja, termički senzor, mehanička zaštita, mogućnost zamjene |

Bez kataloških oznaka, provjerenih footprintova i proračuna **ne generirati proizvodni PCB**.

## 6. Posebno za Makita 5S servisni podsustav

Potrebna je **odvojena revizija** s mjerilima za svih pet serijskih grupa. Svaki međučvor ima drukčiji potencijal prema minusu paketa; ne spajati izravno na zajedničku masu ESP32. Za punjenje jedne grupe kroz BMS kontakte potrebno je dokazati da su ti kontakti projektirani za zadanu struju i da ne postoji put koji može premostiti zaštitu BMS-a. Dok to nije potvrđeno, ostaje samo **pasivna dijagnostika**; nikakvo automatsko balansiranje ili otključavanje ne smije biti dio sigurnosno odobrenog ciklusa.

## 7. Revizijske točke

**G1 — arhitektura:** potvrđena R1 specifikacija i blok dijagram, identificirani otvoreni rizici.

**G2 — izbor komponenti:** potpuni BOM s MPN-ovima, datasheetovima, cijenom/dostupnošću i footprintima.

**G3 — shema:** svi kanali i zaštite, ERC, proračuni, sigurnosna revizija.

**G4 — PCB:** DRC, provjera struje i topline, mehanika, 3D, montažni crteži.

**G5 — prototip:** test na simulatoru ćelije, test kvarova, jedan stvarni kanal pod nadzorom, svih deset kanala, kalibracija; tek zatim revizija za ponovljivu proizvodnju.
