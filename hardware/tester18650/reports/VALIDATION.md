# Provedena provjera — 15.10.2026.

## Alati

Cloud računalo: Debian 13, amd64. Predinstalirani KiCad 9.0.2 nije korišten za konačnu isporuku. KiCad CLI **10.0.4** i standardne biblioteke simbola 10.0.4 instalirani su lokalnim raspakiravanjem službenih KiCad PPA paketa u `/workspace/.tools/kicad10/10.0.4`. Nisu mijenjani sistemski paketi.

Preuzimanje je koristilo HTTPS s uključenom TLS provjerom. SHA-256 arhiva provjeren je prema PPA indeksu:

| Paket | Verzija | SHA-256 |
|---|---|---|
| kicad | 10.0.4~ubuntu25.10.1 | `fe312104b363c409186eecc764131db590a9382dd40f5effc5516a769e3379b0` |
| kicad-symbols | 10.0.4~ubuntu25.10.1 | `ed3165109290ae340aa6926fd93f6f4c262d2986b7c3ea9d55ae060af24aed6c` |

Izvor: `https://ppa.launchpadcontent.net/kicad/kicad-10.0-releases/ubuntu/`, distribucija `questing`. Biblioteka wxWebView i potrebne ovisnosti preuzete su APT-om iz Debian `trixie/main` preko HTTPS-a, uz provjeru potpisanih metapodataka Debianovim arhivskim ključem i provjeru paketa. PPA paketi provjereni su TLS-om i SHA-256; ne tvrdi se da je dodatno verificiran PPA potpis. Nisu isključene TLS ili kontrolne provjere, niti korištene zamjenske biblioteke s pogrešnim ABI-jem.

## Rezultati R2

- Checkout je prije izmjena usklađen s `main`, commit `bfc8b56`, koji uključuje puni firmware i uputu za funkcionalni COM–NO / VIN spoj. Firmware je pregledan i ostao nepromijenjen.
- Nastavljena je postojeća `.kicad_sch`: zadržan je UUID lista i identiteti jedanaest preostalih simbola. `.kicad_pro` je nepromijenjen. TP1–TP4 uklonjeni su jer su njihovi prekidi zamijenjeni električnim vodovima. Unutar prikaza INA219 dodan je interni shunt RSH1 s nepoznatom vrijednošću, izuzet iz zasebnog BOM-a i PCB-a.
- Nativni KiCad 10 parser uspješno učitava shemu kroz PDF/netlist/ERC operacije. PDF je jedan vektorski list A3 vodoravno. Rasteriziran je i vizualno pregledan radi položaja kontakata, teksta, vodova i oznaka priključaka.
- Izvezena lista mreža potvrđuje BAT+ na K1 COM/11, K1 NO/14 na oba otpornika 22 Ω / 5 W, njihove druge krajeve na VIN+ / RSH1/1, te RSH1/2 i VIN− na BAT−. +5 V i kolektor su na različitim krajevima zavojnice; GPIO2/GPIO5 i SDA/SCL nisu zamijenjeni.
- Provjera grafa spojeva testira otvoren i zatvoren radni kontakt, obje pojedinačne paralelne grane te odsutnost premosnice opterećenja. Provjerene su vrijednosti komponenti, deset funkcionalnih mreža i deset preostalih izoliranih pinova. Rezultat je u `connectivity-check.txt`.
- Nativni ERC: **11 pogrešaka + 1 upozorenje**, status **5**. `validate.sh` sada također završava statusom **5**, umjesto ranijeg statusa 0 nakon provjere očekivanih nalaza. Rezultati se ne prikazuju kao čist ERC.
- Nema ERC izuzeća ili namjerno utišanih pinova. Nema dodatnih nepovezanih vodova, izvanmrežnih završetaka ili sukobljenih naziva mreža u konačnom izvještaju.
- Firmware nije kompajliran ni flashan; za ovaj zadatak služi kao izvor GPIO-a, kalibracije i logike rada. Nisu provedena fizička mjerenja, potvrda ožičenja ili SPICE simulacija. Bazni sklop, emiter, napajanja i topologija djelitelja nisu izmišljeni radi uklanjanja nalaza.

## Ponoviti

```sh
cd /workspace/Tester-18650-baterija/hardware/tester18650
./tools/validate.sh
# Očekivan završni status: 5; stvarni ERC nije čist.
python3 tools/check_connectivity.py
# Zasebna provjera grafa spojeva: status 0.
sha256sum -c reports/SHA256SUMS
```

Kontrolni zbrojevi uključuju `.kicad_pro`, `.kicad_sch`, PDF, nativne ERC izvještaje, netlist i korišteni firmware. Skripta je izvršena iz direktorija projekta te iz drugog radnog direktorija. Na drugom računalu potrebni su KiCad 10 sa standardnim bibliotekama i Python 3; `sym-lib-table` koristi `KICAD10_SYMBOL_DIR`.

## PCB P1 — nastavak prema fotografijama

Dodan je nativni KiCad 10 PCB, PDF 1:1, GLB i PNG prema korisnikovoj fotografiji. U ovoj fazi promijenjeni su footprint-metapodaci sheme (bez promjene električnih mreža) i KiCadove PCB postavke u `.kicad_pro`. J1/J2 sada su uključeni u PCB kao referentni footprintovi; nepotvrđeni paketi ostaju bez padova. Provjere su u [pcb/DRC.md](pcb/DRC.md) i [pcb/board-check.txt](pcb/board-check.txt). ERC ostaje 11 pogrešaka + 1 upozorenje. DRC je nečist: 3 nepovezane veze + 16 upozorenja usporedbe sa shemom, status 5. Fizičko i termičko stanje nije potvrđeno.

## PCB P2 — provedba potvrđenog izreza

Izmijenjena je stvarna `.kicad_pcb` datoteka nativnim KiCad 10 Python API-jem, bez ponovnog generiranja P1. Sačuvano je svih 15 P1 segmenata; dodano ih je 8. Shemi su ažurirana samo polja footprintova, bez promjene mreža; projektna pravila i firmware nisu promijenjeni. K1/Q1 imaju nedodijeljene fizičke točke izreza, R1/R2/R3 dvoizvodni raster, a R4 zbog odrezanih završetaka nema padove. Kućišta i zamjenski modeli imaju jasno odvojen status u [PCB.md](../PCB.md).

Ponovljeni nativni ERC vraća 5, **11 pogrešaka + 1 upozorenje**. DRC sa schematic parity vraća 5: **0 geometrijskih kršenja, 2 nepovezane veze, 10 upozorenja**. Provjera izvora, mreža i rastera prolazi. PDF i GLB ponovno su izvezeni iz tog PCB-a; PNG je render tog GLB-a, uz grafičke opise statusa. Nema Gerbera, pojedinačnih izuzeća ni tvrdnje da je glavni strujni krug rutiran ili fizički uređaj verificiran.

## PCB P3 — osam fizičkih pinova releja

Ispravljena je pogrešna prethodna pretpostavka o pet fizičkih izvoda RT314006. Funkcijski SPDT simbol i mreže sheme nisu promijenjeni; K1 ima osam padova s pet funkcija. Dostupni standardni KiCad RT1 16 A footprint uspoređen je s njegovim cjelovitim modelom: svih osam pinova poravnato je s rupama nakon pravilne top-view rotacije. Korisnikov primarni PDF vraća proxy 403, pa proizvođačke točne mjere/tolerancije nisu lažno proglašene očitanima. Sačuvana su sva 23 P2 segmenta, dodano deset za kontaktne parove i potvrđene veze COM/BAT+ i NO/opterećenje. Q1 i INA pretpostavke nisu rutirane.

Nativni ERC ostaje status 5, **11 pogrešaka + 1 upozorenje**. DRC sa schematic parity: **0 geometrijskih kršenja, 2 nepovezane veze, 5 upozorenja, status 5**. Nema K1 upozorenja o nedostajućim funkcionalnim padovima. PDF/GLB/PNG ponovno su izvezeni iz stvarnog P3 PCB-a. Napajanja, C3209, R4, stvarna mehanika, termika i tolerancije sprečavaju proizvodno odobrenje.
