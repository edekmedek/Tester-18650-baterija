# Provjereni proizvođački podaci za relej RT314006

Datum provjere: 2026-10-15. Ovi podatci služe kao ulaz za zamjenu rezerviranog footprinta K1 u PCB P1. Ne potvrđuju ožičenje korisnikova fizičkog sklopa.

**Točan dio:** TE Connectivity / SCHRACK `RT314006`, TE interni broj `9-1393239-3`.

Primarni izvori:
- [TE Connectivity – RT314006, službena stranica](https://www.te.com/en/product-9-1393239-3.html)
- [Schrack Hrvatska – RT314006, raster 5 mm](https://www.schrack.hr/trgovina/catalog/product/view/id/150975)
- [Schrack RT1 serija, datasheet](https://image.schrackcdn.com/datenblaetter/h_rt114024--_en.pdf)

## Podaci proizvođača

| Parametar | Vrijednost |
|---|---|
| Namjena | PCB power relay, RT1 |
| Kontakt | 1 Form C (SPDT, COM/NC/NO) |
| Nazivni napon zavojnice | 6 V DC |
| Nazivni otpor zavojnice | 90 Ω |
| Nazivna snaga zavojnice | 0,4 W |
| Maksimalna navedena kontaktna struja | 16 A |
| Dimenzije tijela (D × Š × V) | **29 × 12,7 × 15,7 mm** |
| Raster / pinning varijanta | **5,0 mm** (Schrack HR) |
| Montaža | Lemni pinovi na PCB |

Na službenoj TE stranici objavljeni su **proizvođački STEP i DXF** za točan broj dijela: `ENG_CVM_CVM_9-1393239-3_E.3d_stp.zip` i `ENG_CVM_CVM_9-1393239-3_E.2d_dxf.zip`, te katalog `ENG_DS_RT1_7.pdf`. Za točne koordinate i funkcionalno mapiranje svih **pet izvoda** potrebno je preuzeti i provjeriti tvornički crtež/datasheet prije izrade footprinta. Ne koristiti footprint varijante s osam izvoda.

## Neposredna posljedica za P1

Postojeća rezervacija K1 od `18 × 34 mm` **nije kućište**. Poznato stvarno kućište ima `29 × 12,7 × 15,7 mm`; potrebno je provjeriti smjer orijentacije i ostale razmake. Zamijeniti rezervaciju stvarnim footprintom s pet mapiranih izvoda i dodati službeni 3D model tek nakon provjere padova; ne nagađati iz slike.

**Poseban problem napajanja:** fizički relej s 6 V DC zavojnicom u dokumentiranom uređaju možda se pobuđuje s 5 V. Vrijednosti tipično daju nazivnu struju oko `6/90 = 67 mA` odnosno na 5 V oko `56 mA` ako se aproksimira stalan otpor; to nije potvrda da pouzdano uklapa na 5 V. Provjeriti pickup/dropout iz datasheeta ili mjerenjem, posebno za moguću novu pločicu.

Status: **proizvođač/kućište/raster identificirani; precizne koordinate svih nožica i fizički ožičeni izvodi nisu još potvrđeni.**

## Naknadni izrez i rezultat P2

Korisnikov potvrđeni izrez prikazuje osam mjesta nosača na rasteru perfboarda, uključujući parove `RL11A/B`, `RL12A/B`, `RL14A/B`. To ne dokazuje osam fizičkih izvoda RT314006, niti mapiranje tih mjesta na pet funkcionalnih terminala iz ove bilješke. U P2 su te koordinate unesene kao električki nedodijeljeni referentni padovi. Kućište je dimenzionirana KiCad referenca bez pinova; službeni TE STEP i tvornički crtež pinova nisu preuzeti zbog proxy HTTP 403. Nije proglašena potvrda za izravnu montažu ili napajanje 5 V.
