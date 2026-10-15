# PCB P4 — oznake priključaka, djelomično rutirano, nije za proizvodnju

[Uređivi KiCad PCB](tester18650.kicad_pcb) · [PDF komponenti 1:1](tester18650_pcb_components.pdf) · [PDF prednjeg bakra](tester18650_pcb_layout.pdf) · [PDF donjeg bakra, gornja registracija](tester18650_pcb_bottom_registered.pdf) · [3D PNG](tester18650_pcb_3d.png) · [3D GLB](tester18650_pcb_3d.glb) · [izvorni DRC](reports/pcb/drc.rpt)

**Nastavak P4 od `9a12d8e`:** u stvarni PCB i lokalnu biblioteku dodane su oznake svih 30 NodeMCU mjesta prema već navedenom proizvođačkom CAD-u, GPIO oznake D5/G14, D4/G2 i D1/G5 prema radnom firmwareu, IN−/pad 6 i IN+/pad 5 na INA219 te jasna napomena o nedodijeljenim Q1 mrežama. Oznake `RSV@0..5` ostaju nazivi iz izvornog CAD-a; nisu izmišljene SD funkcije konkretnog klona. Nazivi pinova ne dodjeljuju mreže ostalim rupama niti potvrđuju klon. Promijenjeni su samo tekstovi i revizija; svih **33 bakrena segmenta**, padovi, položaji i 3D modeli iz P3 ostaju isti. Novi PDF donjeg bakra nije ponovno zrcaljen, kako bi se mogao uspoređivati s već zrcaljenom korisnikovom donjom fotografijom. GLB/PNG i provjere ponovno su izrađeni iz P4.

Noviji dokumenti za budući punjač ne donose potvrdu preostalih fizičkih spojeva V1 i nisu korišteni za proizvoljno dopunjavanje bakra. Ponovni pokušaj službenih Mouser/TE/Toshiba i distributerskih izvora vraća proxy HTTP 403. Nisu dobiveni novi proizvođački podaci koji bi opravdali mapiranje Q1, R4 ili vanjskog INA polariteta.

## Električna i mehanička osnova zadržana iz P3

P3 nastavlja postojeći PCB P2 nativnim KiCadom **10.0.4**, u istom projektu. Zadržani su obris **116 × 132 × 1,6 mm**, položaji prema fotografijama, referentni NodeMCU/INA219 i svih 23 prethodna bakrena segmenta. K1 je zamijenjen osmoizvodnim footprintom i mapiran na pet električnih funkcija; dodano je deset bakrenih segmenata i model sa svih osam pinova. **Glavni strujni put i upravljanje još nisu potpuno rutirani.**

## Granice referenci

Glavni izvor položaja je korisnikov `tester18650_fotoreferenca_obje_strane.pdf`: NodeMCU lijevo/USB gore, relej gore u sredini, Q1 ispod njega, R1/R2 jedan ispod drugoga, INA219 dolje lijevo i držač desno. Donja fotografija u tom PDF-u već je zrcaljena; nije ponovno zrcaljena. SHA-256 je u [izvornom manifestu](pcb_sources/reference-geometry.json). Originalni korisnikovi prilozi nisu ponovno objavljeni.

Iz starog predloška upotrijebljen je **isključivo korisnikov naknadni izrez RL/Q/R**, prema [njegovoj potvrdi](reports/pcb/REFERENCE_DETAIL_RL_Q_R_2026-10-15.md). Nisu preuzeti ostatak predloška, njegove boje bakra, navodni kratki spojevi ili električna netlista. Lokalni razmaci izreza preneseni su na raster 2,54 mm; ukupni raspored dijelova vodi fotografija. Ne tvrdi se metrička registracija cijelog predloška s fotografijom.

Geometrija izreza i ispravak K1:

- K1 je u P2 bio samo perfboard raster 7,62 mm. **RT314006 ima osam fizičkih izvoda i pet električnih funkcija; ranija tvrdnja o pet fizičkih izvoda bila je pogrešna.** U P3 koristi se standardna KiCad RT1 16 A geometrija s mapiranim A1/A2 i udvojenim 11/12/14. [Proizvođački izvor, rotacija i granice provjere](reports/pcb/RT314006_MANUFACTURER_SOURCE.md) te [točne korištene koordinate](reports/pcb/K1_COORDINATES.csv) priloženi su uz PCB. Zavojnica gore: **A1 lijevo, A2 desno u pogledu odozgo**; donji pogled zrcali se jednom za usporedbu. Nisu doslovno kopirane donje oznake A1/A2.
- Q1: tri mjesta na 2,54 mm, `TOP_E_REF`, `MID_C_REF`, `BOT_B_REF`. Oznake E?/C?/B? na ploči ostaju pitanja; nema pretpostavljenih mreža B/C/E.
- R1/R2/R3: vidljiv dvoizvodni raster 7,62 mm. Simboličko tijelo s izreza nije korišteno kao mjera kućišta.
- R4: vidljiva oznaka, ali cijeli par završetaka izvan je izreza. Nisu ekstrapolirane rupe iz položaja ostalih otpornika.

Promjeri rupa jesu projektni odabiri: K1 1,3 mm iz KiCad RT1 16 A reference, Q1 0,9 mm, R1/R2 1,2 mm iz power-resistor reference, R3 0,8 mm. **To nisu izmjereni promjeri nožica/rupa stvarnog sklopa niti potvrda pristajanja.** Izvorni raster i ove pretpostavke odvojeni su u [P2 manifestu](pcb_sources/p2/geometry.json).

**Granica proizvođačke provjere K1:** korisnik je potvrdio str. 5 službenog [TE PDF-a](https://www.mouser.com/catalog/specsheets/ENG_DS_RT1_6-9724925.pdf), ali preuzimanje ovdje vraća proxy 403. Broj/funkcije pinova potvrđeni su tom korisnikovom informacijom; koordinate su uspoređene u dostupnom KiCad footprintu i STEP-u. Knjižnica koristi razmak redova 7,5 mm i stanice 15,26/20,30/25,34 mm (koraci 5,04 mm). To se **ne proglašava izravno očitanim točnim TE dimenzijama ili tolerancijama**, iako datasheet varijantu naziva 5 mm. Ta završna mehanička provjera ostaje otvorena.

## Stanje svakog dijela

| Dio | Stvarni uređivi footprint / bakar | 3D i ograničenje |
|---|---|---|
| J1 NodeMCU CH340 / Ver 0.1 | Zadržan izvorni CH340 referentni footprint: 30 rupa, raster 2,54 mm, redovi 27,94 mm. SDA/SCL/GND rute sačuvane. | Plava **grafička referenca**, nije kućište ni gotov 3D model. Točan klon i njegova montaža nisu identificirani. |
| J2 Soldered INA219 | Zadržan proizvođački CAD 38 × 22 mm, 4 upravljačka + 4 strujna pada. Dodane veze između dvaju IN+ i dvaju IN− mjesta prema istoimenim mrežama izvornog CAD-a. | Proizvođački STEP, sačuvano 28 tijela; uklonjen samo vijčani terminal koji nije ugrađen na fotografiji. Točna revizija/način montaže ostaju nepotvrđeni. |
| K1 RT314006 | **8 mapiranih padova / 5 funkcija**. A1→+5V_RELEJ, A2→K1_C, 11×2→BAT_PLUS, 12×2→nekorišten NC, 14×2→LOAD_IN. Rutirani svi kontaktni parovi, BAT+→COM i NO→R1/R2. | Cijeli KiCad osmoizvodni model, pravilno zakrenut, svih 8 pinova poravnato s rupama. Kućište 29 × 12,7 × 15,7 mm. Nije službeni TE STEP niti izravna potvrda točnih TE tolerancija. |
| Q1 C3209 | Tri fizička mjesta izreza na 2,54 mm; svi padovi nedodijeljeni. | **Nema izmišljenog tijela.** Proizvođač, točno kućište i fizički B/C/E nisu potvrđeni. |
| R1/R2 22 Ω / 5 W | Dva stvarna pada po dijelu, raster 7,62 mm iz izreza. Oba kraja paralelnog para sada povezana bakrom. | **Predložena zamjena**, katalogna obitelj Yageo/Reichelt `5W AXIAL 22`, nije identificirani dio `5W22R0J` s fotografije. Podaci biblioteke daju tijelo 25 × 6,4 × 6,4 mm. Prikazana je nova vertikalna montaža; nabava, formiranje izvoda i konačno pristajanje nisu verificirani. |
| R3 10 kΩ | Dva fizička pada na 7,62 mm. Krajevi ostaju električki otvoreni prema shemi. | Nema odabranog kućišta ni 0,25 W modela na temelju crteža. |
| R4 20 kΩ | Označen položaj; bez padova dok cijeli raster nije potvrđen. | Nema kućišta. |
| BT1 | Zadržane dvije lemne točke za baterijske žice, projektni raster 6 mm. Samo potvrđeni NodeMCU GND–BAT− povrat je rutiran. | Nije identificiran tvornički konektor ni potvrđen presjek žice/rasterećenje sile. |
| BTH1 | Referentni položaj držača; **bez proizvodnih padova i rupa**. | KiCad model **Keystone 1042**, nije identificiran kao fotografirani držač. Omotač izvornog modela približno 86,41 × 20,65 × 16,3 mm. Uklonjeni dijelovi ispod ploče; ne tvrdi se odgovarajuća montaža. |

Za R1/R2 tijelo i snaga provjereni su usporedbom izvornog KiCad STEP-a s receptom generatora. Njegov izvor navodi tvornički/katalogni PDF; taj PDF nije bio dostupan (proxy HTTP 403), pa se ne tvrdi neovisna provjera proizvođačkog lista ili narudžbene oznake. Zamjenski oblik ne zamjenjuje identifikaciju stvarnog otpornika.

Nova vertikalna vizualizacija R1/R2 koristi bibliotečne dimenzije tijela, a 1 mm odmaka od ploče, grafički izvod 0,8 mm i prikaz savijanja jesu **nevalidirani projektni odabiri za referentni model**. Nisu uputa za savijanje stvarnog dijela niti izmjereni gabariti fotografiranih otpornika. Ukupna visina tog prijedloga približno je 27,6 mm iznad modelne ravnine. To treba provjeriti s konkretnim dobavljivim dijelom.

## Bakrene veze i razmaci

Ukupno je **33 segmenta na sedam bakrenih mreža**. Svih 23 P2 segmenta ostalo je nepromijenjeno:

1. GPIO2/D4–SDA i GPIO5/D1–SCL: 0,35 mm;
2. NodeMCU GND–BT1 BAT−: 0,8 mm;
3. nov spoj R1/1–R2/1 i R1/2–R2/2: 0,8 mm, samo potvrđeni paralelni krajevi;
4. spoj udvojenih padova IN+ te udvojenih padova IN−: 1 mm, prema proizvođačkom CAD-u Soldered modula;
5. u P3 svi udvojeni kontakti K1, **BAT+→COM/11 i NO/14→paralelni ulaz otpornika**: 1,2 mm, NC par 0,8 mm. COM i NO nisu premošteni bakrom.

**Nisu spojeni** R1/R2 s pretpostavljenim INA polaritetom, vanjski IN− s BAT−, neprovjereni tranzistorski pinovi, fizički izvor +5 V, napajanja INA219/NodeMCU-a ni redoslijed djelitelja. Nema bakrenih poligona. Firmware `fabsf(ina219_current)` i dalje ne dokazuje fizički polaritet INA219.

Između projekcija zamjenskih tijela R1/R2 ima 17,6 mm; bočno prema INA219 najmanje 19 mm, prema referentnom držaču približno 20,5 mm. Dodani su keepouti pod tim tijelima s otvorom za izlaz potvrđenog izvoda. Ti razmaci nisu termička provjera stvarnih dijelova. Na 4,2 V svaki otpornik 22 Ω disipira približno 0,80 W; oznaka 5 W nije stvarna disipacija testa. Nisu verificirani temperatura baterije, ventilacija, formiranje izvoda, visine i konstrukcijska učvršćenja.

## Provjere i izvozi

Nativni KiCad **10.0.4**: **DRC 0 geometrijskih kršenja, 2 nepovezane veze i 5 upozorenja schematic parity, status 5**. ERC: **11 pogrešaka + 1 upozorenje, status 5**. Nisu mijenjane ozbiljnosti pravila niti dodavana izuzeća, `No Connect` ili `PWR_FLAG` radi utišavanja nalaza. [Tumačenje DRC-a](reports/pcb/DRC.md) objašnjava zašto broj nepovezanih mreža ne predstavlja sav nedovršeni sklop.

Tri PDF-a su nativni izvoz 1:1 na A4 vodoravno. `_pcb_components.pdf` sadrži F.SilkS/F.Fab/Edge.Cuts bez bakra radi čitljivosti svih priključaka; `_pcb_layout.pdf` dodaje F.Cu. `_pcb_bottom_registered.pdf` prikazuje B.Cu s istim gornjim F.Fab/F.SilkS oznakama, bez dodatnog zrcaljenja: to je projekcija za usporedbu fotografija, **nije prikaz dijelova montiranih odozdo ni predložak za jetkanje**. PDF-ovi ne prikazuju ratsnest; otvorene veze navedene su u DRC-u. GLB je nativni KiCad izvoz stvarne pločice, PNG je Blender render tog GLB-a. Opisni natpisi u renderu grafičke su oznake statusa, ne tvornički natpisi ni fizička tijela. Nativni `pcb render` ranije se rušio u ovom okruženju; korišten je provjereni GLB→Blender put.

```sh
./tools/validate.sh       # očekivani stvarni ERC status 5
./tools/validate_pcb.sh   # očekivani stvarni DRC status 5; izvozi PDF/GLB/PNG
sha256sum -c reports/SHA256SUMS
sha256sum -c reports/pcb/SHA256SUMS
```

Izvori, licence, hashovi i granice provjere su u [pcb_sources/p3](pcb_sources/p3/README.md) i ranijem [pcb_sources/p2](pcb_sources/p2/README.md). `tools/annotate_p4.py` jednokratno nastavlja P3 i provjerava da nijedan vod nije promijenjen; ne pokretati ga ponovno preko P4. `tools/implement_p3.py` nastavlja postojeći P2, a `tools/make_p3_relay_model.py` provjerava i zakreće cijeli osmoizvodni model. `tools/implement_p2.py` jednokratna je migracija postojećeg P1 u P2, preko nativnog KiCad 10 Python API-ja (`tools/pcb_python.sh`). `tools/build_pcb.py` ostaje povijesni generator P1; **nije generator konačnog P4**. `tools/make_p2_models.py` reproducira referentne modele pomoću paketa iz `tools/cad-requirements.txt`.

**Za dovršenje nedostaju:** izravna usporedba točnih TE dimenzija/tolerancija s korištenom knjižničnom geometrijom, točan C3209 i pinout, puni R4 raster, stvarna kućišta R3/R4, odobren konkretni otpornik i montaža, točan NodeMCU/INA219/držač, napajanja, zaštite, bazni sklop i djelitelj te mehanička/termička provjera. Nisu izdani Gerberi ni odobrenje za proizvodnju. Fizičko ožičenje funkcionalnog primjerka nije proglašeno potvrđenim.
