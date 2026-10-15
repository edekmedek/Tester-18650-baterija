# ERC — rekonstrukcija R1

Provjereno KiCad CLI-jem **10.0.4**, 15.10.2026. Shema se uspješno učitava, izvozi u PDF i u XML listu mreža. **ERC nije čist: 15 pogrešaka i 1 upozorenje.**

Izvorni rezultati: [erc.rpt](erc.rpt), [erc.json](erc.json). CLI je pokrenut s `--severity-all --exit-code-violations`; vraća **5**, što je očuvano u [erc-exit-status.txt](erc-exit-status.txt).

| Nalaz | Broj | Mjesta / razlog |
|---|---:|---|
| `pin_not_connected` | 3 | K1 11/12/14 — nepoznata dodjela fizičkih kontakata (N1). |
| `pin_not_connected` | 2 | Q1 B/1 i E/3 — nepoznat bazni sklop i emiter (N3). |
| `pin_not_connected` | 4 | R3 1/2 i R4 1/2 — nepotvrđena topologija djelitelja (N4). |
| `pin_not_connected` | 4 | J2 3/4/5/6 — VCC, GND, VIN+, VIN− (N2, N5, N6). |
| `pin_not_connected` | 1 | J1 5 — napajanje NodeMCU pločice (N6). |
| `pin_not_driven` | 1 | Q1 B/1 — posljedica nepoznatog puta GPIO14 do baze (N3). |
| `isolated_pin_label` | 1 upozorenje | +5V_RELEJ — poznato odredište na zavojnici, nepoznat izvor (N6). |

Otvoreni pinovi nisu označeni kao namjerno nekorišteni. Nema dodanih ERC izuzeća, lažnih `PWR_FLAG` simbola ni promjene ozbiljnosti nalaza. KiCadovi tvornički zadani neaktivni provjerni tipovi vidljivi su u `ignored_checks` JSON-a; projekt ih nije dodatno isključivao. Nema dodatnih nepovezanih krajeva vodova ni nepodudaranja bibliotečnih simbola u konačnom izvještaju.

Provjera `tools/check_connectivity.py` uspoređuje deset izvezenih funkcionalnih mreža, vrijednosti komponenti i četrnaest izoliranih nepoznatih pinova. Time se provjerava da su R1/R2 doista električki paralelni, da SDA i SCL nisu zamijenjeni, da je kolektor na zavojnici te da nepoznati kontakti, djelitelj i VIN priključci nisu slučajno povezani.

ERC ne potvrđuje fizičku izvedbu, stvarni pinout, pouzdanost releja sa zavojnicom 6 V na 5 V, ispravnost firmwarea ni mjerenja. Budući da su J1/J2 pasivna logička sučelja standardnog konektorskog simbola, ERC također ne provjerava naponsku kompatibilnost i električne tipove stvarnih modula. To ostaje izričito ograničenje N5/N6. Shema se ne smije proglasiti izvedbeno provjerenom na temelju ovih provjera.
