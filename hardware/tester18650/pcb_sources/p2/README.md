# P2 izvori i izvedeni modeli

[geometry.json](geometry.json) odvojeno bilježi potvrđeni raster korisnikova izreza, izvorni CAD, projektne odabire, nepoznanice i SHA-256 svih kopiranih izvora. Sam izrez i izvorne korisnikove fotografije nisu ponovno objavljeni. Iz cijelog starog predloška nije preuzet nijedan drugi dio niti električna veza.

## Kopirani izvori

- `relay-library.step`: KiCad `Relay_THT.3dshapes/Relay_SPDT_Schrack-RT1-FormC_RM5mm.step`, [izvor](https://github.com/KiCad/kicad-packages3D/blob/b8b3cfdfad88ba66f21002b3de51dc6f7d55ba5a/Relay_THT.3dshapes/Relay_SPDT_Schrack-RT1-FormC_RM5mm.step). Referentni model nije dokaz pinouta RT314006. Omotač kućišta uspoređen je s potvrđenim dimenzijama u [RT314006_MANUFACTURER_SOURCE.md](../../reports/pcb/RT314006_MANUFACTURER_SOURCE.md).
- `cement-5w-library.step`: KiCad `Resistor_THT.3dshapes/R_Axial_Power_L25.0mm_W6.4mm_P30.48mm.step`, [izvor](https://github.com/KiCad/kicad-packages3D/blob/b8b3cfdfad88ba66f21002b3de51dc6f7d55ba5a/Resistor_THT.3dshapes/R_Axial_Power_L25.0mm_W6.4mm_P30.48mm.step). **Nije 7W/9mm varijanta.**
- `resistor-generator-source.py`: [izvor](https://github.com/pointhi/kicad-footprint-generator/blob/76fedd51e8680e6cd3b729dcbd6f1a56af53b12c/scripts/Resistor_THT/make_Resistors_THT.py), blok `POWER Resistors`, 5W, 25 × 6,4 × 6,4 mm, poveznica na Yageo/Reichelt `5WAXIAL_9WAXIAL_11WAXIAL_17WAXIAL#YAG.pdf`. Podatak je bibliotečno provjerljiv; proizvođački PDF nije preuzet zbog proxy 403. `5W AXIAL 22` je predložena katalogna zamjena, nije potvrđeno narudžbeno odobrenje niti identifikacija fotografiranog `5W22R0J`.
- `keystone-1042-library.step`: KiCad `Battery.3dshapes/BatteryHolder_Keystone_1042_1x18650.step`, [izvor](https://github.com/KiCad/kicad-packages3D/blob/b8b3cfdfad88ba66f21002b3de51dc6f7d55ba5a/Battery.3dshapes/BatteryHolder_Keystone_1042_1x18650.step). Drugi, jasno označen referentni držač; nije fotografirani model.
- `*-library.kicad_mod`: nepromijenjene kopije instalirane standardne KiCad 9 biblioteke za usporedbu. Relejni kandidati imaju različit broj padova; nisu automatski dodijeljeni kao fizički RT314006 pinout. Horizontalni power-resistor raster 30,48 mm **nije** kopiran umjesto korisnikova potvrđenog vertikalnog rastera 7,62 mm.

## Izvedene datoteke

`tools/make_p2_models.py` izrađuje modele u `models/`:

- relej: zadržava KiCad geometriju kućišta, odstranjuje sve dijelove ispod z=0, centrira i zakreće 90°. Omotač 29 × 12,7 × 15,7 mm podudara se s proizvođačkim podatkom; nikakvi neprovjereni pinovi ne prikazuju se kao potvrđeni;
- držač: zadržava izvorne oblike iznad ploče, odstranjuje donje montažne dijelove i zakreće 90°. Ne nastaju rupe ili električni padovi;
- otpornik: koristi bibliotečne mjere tijela 25 × 6,4 × 6,4 mm u novom vertikalnom referentnom prijedlogu na korisnikovu rasteru 7,62 mm. Odmak 1 mm, grafički izvod 0,8 mm i oblik savijanja novi su projektni parametri, nisu provjerene mjere izvoda ni uputa za montažu stvarnog dijela. Oba modela ostaju označena `SUBSTITUTE`/`ALT`.

[Izvještaj geometrije](../../reports/pcb/p2-models.json) sadrži dobivene omotače i status modela. Nije izrađen izmišljeni model C3209, R3 ili R4. NodeMCU ostaje grafička oznaka zbog neidentificiranog klona.

## Licence i pristup

KiCad 3D izvori i njihovi izvedeni modeli: [CC BY-SA 4.0 s KiCad iznimkom](KICAD_3D_LICENSE.md); izvorni autori i podaci ostaju u STEP zaglavljima. KiCad footprintovi koriste istu knjižničnu licencu s iznimkom za elektroničke projekte. Recept generatora potječe iz GPL-3.0 repozitorija; njegova licenca priložena je zasebno.

Službeni TE/Schrack, Yageo, MPD i distributerski PDF endpointovi vraćali su proxy HTTP 403 i nakon odobrenja mrežnog pristupa. Nisu korišteni načini zaobilaženja proxyja. Nedostaju upravo tvornički crtež osam fizičkih izvoda RT314006 (`ENG_DS_RT1_7.pdf` / crtež za `9-1393239-3`) i njegov službeni STEP `ENG_CVM_CVM_9-1393239-3_E.3d_stp.zip`, kao i proizvođački list konkretnog C3209. Podatci s grafičkog izreza nisu zamijenili te dokumente.

**Ispravak P3:** ranija pretpostavka o pet fizičkih izvoda bila je pogrešna. RT314006 ima osam fizičkih izvoda i pet funkcija; aktualni osmoizvodni footprint i cijeli model su u [P3](../p3/README.md). Ovdje ostaje povijesna P2 referenca bez pinova, koja se više ne koristi na završnoj pločici.
