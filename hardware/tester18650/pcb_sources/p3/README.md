# P3 — izvori osmoizvodnog releja i rotacije

[geometry.json](geometry.json) sadrži korisnikov proizvođački izvor, točan status pristupa, dostupne CAD koordinate, transformaciju i SHA-256 kopiranih datoteka.

- Primarni izvor koji je korisnik potvrdio: [TE RT1, rev. 6, str. 5](https://www.mouser.com/catalog/specsheets/ENG_DS_RT1_6-9724925.pdf), 16 A / 5 mm / 1 Form C / BOTTOM VIEW. **8 fizičkih nožica, 5 električnih funkcija.**
- `RT1_16A_GitHub_reference.kicad_mod`: nepromijenjeni [KiCad RT1 16 A footprint](https://raw.githubusercontent.com/KiCad/kicad-footprints/master/Relay_THT.pretty/Relay_SPDT_Schrack-RT1-16A-FormC_RM5mm.kicad_mod). Uspoređen s već priloženom [instaliranom varijantom](../p2/relay-8pin-library.kicad_mod); iste koordinate i mapiranje.
- `RT1_16A_library_8pin_source.step`: nepromijenjeni [KiCad osmoizvodni model](https://raw.githubusercontent.com/KiCad/kicad-packages3D/master/Relay_THT.3dshapes/Relay_DPDT_Schrack-RT2-FormC_RM5mm.step), koji sama standardna RT1 16 A biblioteka navodi kao svoj 3D model. Nije preuzet službeni TE STEP i nije tvrdnja da relej ima DPDT funkciju. Broj, položaji pinova i omotač odgovaraju ovdje korištenoj RT1 16 A knjižničnoj geometriji.

`tools/make_p3_relay_model.py` izdvaja i provjerava osam pinova, centrira i pravilno zakreće cijelu geometriju. Boja kućišta/pinova odvojena je presjekom na z=0; geometrijski zbroj zadržava cijeli izvorni model. Rezultat [p3-relay-model.json](../../reports/pcb/p3-relay-model.json) potvrđuje poravnanje sa svih osam rupa. Izvedeni model ima osam stvarnih pinova, za razliku od povijesne P2 reference bez pinova.

Nominalno 5 mm ne pretvara se u tvrdnju da su knjižnične vrijednosti 15,26 / 20,30 / 25,34 mm izravno očitane iz TE PDF-a. Sve su te vrijednosti javno dostupne i međusobno provjerene u KiCad footprintu i STEP-u; točne TE dimenzije i tolerancije ostaju završna mehanička provjera. Preuzimanje proizvođačkog PDF-a vraćalo je proxy 403; ta datoteka nije lažno priložena.

Ovi modeli/knjižnični podaci i izvedeni model koriste [KiCad CC BY-SA 4.0 s iznimkom](../p2/KICAD_3D_LICENSE.md). Sačuvana su izvorna STEP zaglavlja u izvornoj kopiji. Opis izmjena i atribucija priloženi su uz izvedeni model.
