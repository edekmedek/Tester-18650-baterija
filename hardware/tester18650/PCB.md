# PCB P2 — stvarne izmjene pločice, djelomično rutirano, nije za proizvodnju

[Uređivi KiCad PCB](tester18650.kicad_pcb) · [PDF rasporeda 1:1](tester18650_pcb_layout.pdf) · [3D PNG](tester18650_pcb_3d.png) · [3D GLB](tester18650_pcb_3d.glb) · [izvorni DRC](reports/pcb/drc.rpt)

P2 mijenja postojeći PCB P1 nativnim KiCadom **10.0.4**, u istom projektu. Zadržani su obris **116 × 132 × 1,6 mm**, položaji prema fotografijama, referentni NodeMCU/INA219 i svih 15 prethodnih bakrenih segmenata. Dodani su fizički padovi potvrđenog rastera, osam bakrenih segmenata i novi 3D prikazi. **Glavni strujni put i upravljanje još nisu potpuno rutirani.**

## Granice referenci

Glavni izvor položaja je korisnikov `tester18650_fotoreferenca_obje_strane.pdf`: NodeMCU lijevo/USB gore, relej gore u sredini, Q1 ispod njega, R1/R2 jedan ispod drugoga, INA219 dolje lijevo i držač desno. Donja fotografija u tom PDF-u već je zrcaljena; nije ponovno zrcaljena. SHA-256 je u [izvornom manifestu](pcb_sources/reference-geometry.json). Originalni korisnikovi prilozi nisu ponovno objavljeni.

Iz starog predloška upotrijebljen je **isključivo korisnikov naknadni izrez RL/Q/R**, prema [njegovoj potvrdi](reports/pcb/REFERENCE_DETAIL_RL_Q_R_2026-10-15.md). Nisu preuzeti ostatak predloška, njegove boje bakra, navodni kratki spojevi ili električna netlista. Lokalni razmaci izreza preneseni su na raster 2,54 mm; ukupni raspored dijelova vodi fotografija. Ne tvrdi se metrička registracija cijelog predloška s fotografijom.

Iz izreza su uneseni:

- K1: dva stupca udaljena 7,62 mm; zavojnici slično označeni red te kontaktni redovi 15,24 / 20,32 / 25,40 mm ispod njega. Padovi su nazvani `REF_A1`, `REF_A2`, `RL12A/B`, `RL11A/B`, `RL14A/B`. **Svi su električki nedodijeljeni.** Osam mjesta na nosaču nije dokaz osam fizičkih izvoda releja niti dokaz njihova funkcionalnog mapiranja.
- Q1: tri mjesta na 2,54 mm, `TOP_E_REF`, `MID_C_REF`, `BOT_B_REF`. Oznake E?/C?/B? na ploči ostaju pitanja; nema pretpostavljenih mreža B/C/E.
- R1/R2/R3: vidljiv dvoizvodni raster 7,62 mm. Simboličko tijelo s izreza nije korišteno kao mjera kućišta.
- R4: vidljiva oznaka, ali cijeli par završetaka izvan je izreza. Nisu ekstrapolirane rupe iz položaja ostalih otpornika.

Promjeri novih rupa jesu projektni odabiri: K1 1,3 mm iz KiCad RT1 reference, Q1 0,9 mm, R1/R2 1,2 mm iz power-resistor reference, R3 0,8 mm. **To nisu izmjereni promjeri nožica/rupa stvarnog sklopa niti potvrda pristajanja.** Izvorni raster i ove pretpostavke odvojeni su u [P2 manifestu](pcb_sources/p2/geometry.json).

## Stanje svakog dijela

| Dio | Stvarni uređivi footprint / bakar | 3D i ograničenje |
|---|---|---|
| J1 NodeMCU CH340 / Ver 0.1 | Zadržan izvorni CH340 referentni footprint: 30 rupa, raster 2,54 mm, redovi 27,94 mm. SDA/SCL/GND rute sačuvane. | Plava **grafička referenca**, nije kućište ni gotov 3D model. Točan klon i njegova montaža nisu identificirani. |
| J2 Soldered INA219 | Zadržan proizvođački CAD 38 × 22 mm, 4 upravljačka + 4 strujna pada. Dodane veze između dvaju IN+ i dvaju IN− mjesta prema istoimenim mrežama izvornog CAD-a. | Proizvođački STEP, sačuvano 28 tijela; uklonjen samo vijčani terminal koji nije ugrađen na fotografiji. Točna revizija/način montaže ostaju nepotvrđeni. |
| K1 RT314006 | **Osam potvrđenih mjesta nosača**, bez dodjele funkcionalnih A1/A2/11/12/14 i bez bakra. Nije odobren footprint za izravnu montažu pet izvoda releja. | Narančasta dimenzionirana referenca kućišta **29 × 12,7 × 15,7 mm**, izvedena iz KiCad RT1 modela jednakog omotača. Sva geometrija pinova uklonjena. Nije preuzet TE STEP. |
| Q1 C3209 | Tri fizička mjesta izreza na 2,54 mm; svi padovi nedodijeljeni. | **Nema izmišljenog tijela.** Proizvođač, točno kućište i fizički B/C/E nisu potvrđeni. |
| R1/R2 22 Ω / 5 W | Dva stvarna pada po dijelu, raster 7,62 mm iz izreza. Oba kraja paralelnog para sada povezana bakrom. | **Predložena zamjena**, katalogna obitelj Yageo/Reichelt `5W AXIAL 22`, nije identificirani dio `5W22R0J` s fotografije. Podaci biblioteke daju tijelo 25 × 6,4 × 6,4 mm. Prikazana je nova vertikalna montaža; nabava, formiranje izvoda i konačno pristajanje nisu verificirani. |
| R3 10 kΩ | Dva fizička pada na 7,62 mm. Krajevi ostaju električki otvoreni prema shemi. | Nema odabranog kućišta ni 0,25 W modela na temelju crteža. |
| R4 20 kΩ | Označen položaj; bez padova dok cijeli raster nije potvrđen. | Nema kućišta. |
| BT1 | Zadržane dvije lemne točke za baterijske žice, projektni raster 6 mm. Samo potvrđeni NodeMCU GND–BAT− povrat je rutiran. | Nije identificiran tvornički konektor ni potvrđen presjek žice/rasterećenje sile. |
| BTH1 | Referentni položaj držača; **bez proizvodnih padova i rupa**. | KiCad model **Keystone 1042**, nije identificiran kao fotografirani držač. Omotač izvornog modela približno 86,41 × 20,65 × 16,3 mm. Uklonjeni dijelovi ispod ploče; ne tvrdi se odgovarajuća montaža. |

Za R1/R2 tijelo i snaga provjereni su usporedbom izvornog KiCad STEP-a s receptom generatora. Njegov izvor navodi tvornički/katalogni PDF; taj PDF nije bio dostupan (proxy HTTP 403), pa se ne tvrdi neovisna provjera proizvođačkog lista ili narudžbene oznake. Zamjenski oblik ne zamjenjuje identifikaciju stvarnog otpornika.

Nova vertikalna vizualizacija R1/R2 koristi bibliotečne dimenzije tijela, a 1 mm odmaka od ploče, grafički izvod 0,8 mm i prikaz savijanja jesu **nevalidirani projektni odabiri za referentni model**. Nisu uputa za savijanje stvarnog dijela niti izmjereni gabariti fotografiranih otpornika. Ukupna visina tog prijedloga približno je 27,6 mm iznad modelne ravnine. To treba provjeriti s konkretnim dobavljivim dijelom.

## Bakrene veze i razmaci

Ukupno je **23 segmenta na pet mreža**. Svih 15 prethodnih segmenata ostalo je nepromijenjeno:

1. GPIO2/D4–SDA i GPIO5/D1–SCL: 0,35 mm;
2. NodeMCU GND–BT1 BAT−: 0,8 mm;
3. nov spoj R1/1–R2/1 i R1/2–R2/2: 0,8 mm, samo potvrđeni paralelni krajevi;
4. nov spoj udvojenih padova IN+ te udvojenih padova IN−: 1 mm, prema proizvođačkom CAD-u Soldered modula.

**Nisu spojeni** R1/R2 s pretpostavljenim INA polaritetom, vanjski IN− s BAT−, nijedan neprovjereni relejni/tranzistorski pin, izvor +5 V, napajanja INA219/NodeMCU-a ni redoslijed djelitelja. Nema bakrenih poligona. Firmware `fabsf(ina219_current)` i dalje ne dokazuje fizički polaritet INA219.

Između projekcija zamjenskih tijela R1/R2 ima 17,6 mm; bočno prema INA219 najmanje 19 mm, prema referentnom držaču približno 20,5 mm. Dodani su keepouti pod tim tijelima s otvorom za izlaz potvrđenog izvoda. Ti razmaci nisu termička provjera stvarnih dijelova. Na 4,2 V svaki otpornik 22 Ω disipira približno 0,80 W; oznaka 5 W nije stvarna disipacija testa. Nisu verificirani temperatura baterije, ventilacija, formiranje izvoda, visine i konstrukcijska učvršćenja.

## Provjere i izvozi

Nativni KiCad **10.0.4**: **DRC 0 geometrijskih kršenja, 2 nepovezane veze i 10 upozorenja schematic parity, status 5**. ERC: **11 pogrešaka + 1 upozorenje, status 5**. Nisu mijenjane ozbiljnosti pravila niti dodavana izuzeća, `No Connect` ili `PWR_FLAG` radi utišavanja nalaza. [Tumačenje DRC-a](reports/pcb/DRC.md) objašnjava zašto broj nepovezanih mreža ne predstavlja sav nedovršeni sklop.

PDF je nativni izvoz slojeva F.Cu/F.SilkS/F.Fab/Edge.Cuts, 1:1 na A4 vodoravno; nije kompletna dokumentacija svih bakrenih slojeva. GLB je nativni KiCad izvoz stvarne pločice, PNG je Blender render tog GLB-a. Opisni natpisi u renderu grafičke su oznake statusa, ne tvornički natpisi ni fizička tijela. Nativni `pcb render` ranije se rušio u ovom okruženju; korišten je provjereni GLB→Blender put.

```sh
./tools/validate.sh       # očekivani stvarni ERC status 5
./tools/validate_pcb.sh   # očekivani stvarni DRC status 5; izvozi PDF/GLB/PNG
sha256sum -c reports/SHA256SUMS
sha256sum -c reports/pcb/SHA256SUMS
```

Izvori, licence, hashovi i granice provjere su u [pcb_sources/p2](pcb_sources/p2/README.md). `tools/implement_p2.py` jednokratna je migracija postojećeg P1 u P2, preko nativnog KiCad 10 Python API-ja (`tools/pcb_python.sh`). `tools/build_pcb.py` ostaje povijesni generator P1; **nije generator konačnog P2**. `tools/make_p2_models.py` reproducira referentne modele pomoću paketa iz `tools/cad-requirements.txt`.

**Za dovršenje nedostaju:** tvorničko mapiranje releja na potvrđeni nosač, točan C3209 i pinout, puni R4 raster, stvarna kućišta R3/R4, odobren konkretni otpornik i montaža, točan NodeMCU/INA219/držač, napajanja, zaštite, bazni sklop i djelitelj te mehanička/termička provjera. Nisu izdani Gerberi ni odobrenje za proizvodnju. Fizičko ožičenje funkcionalnog primjerka nije proglašeno potvrđenim.
