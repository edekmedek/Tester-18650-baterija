# ERC — postojeća shema R2

KiCad CLI **10.0.4**, 15.10.2026. **Stvarni rezultat: 11 pogrešaka i 1 upozorenje. ERC nije čist.** Nativni poziv i završni `tools/validate.sh` vraćaju status **5**.

Izvorni rezultati nisu filtrirani: [erc.rpt](erc.rpt), [erc.json](erc.json), [erc-exit-status.txt](erc-exit-status.txt). Upotrijebljeni su `--severity-all --exit-code-violations`.

| Tip | Broj | Priključci i razlog |
|---|---:|---|
| `pin_not_connected` | 1 | K1/12 — NC nije dio funkcionalnog kruga. Nalaz nekorištenog kontakta namjerno je ostavljen vidljiv. |
| `pin_not_connected` | 2 | Q1 B/1 i E/3 — nema potvrđenog baznog sklopa ni emiterske veze, N3. |
| `pin_not_connected` | 4 | R3 1/2 i R4 1/2 — nema potvrđene topologije djelitelja, N4. |
| `pin_not_connected` | 2 | J2/3 VCC i J2/4 GND — napajanje i referenca modula nisu fizički utvrđeni, N5/N6. |
| `pin_not_connected` | 1 | J1/5 — ulaz i izvor napajanja NodeMCU-a nisu utvrđeni, N6. |
| `pin_not_driven` | 1 | Q1 B/1 — bazni sklop nedostaje, N3. GPIO14 nije izravno kratko spojen na bazu. |
| `isolated_pin_label` | 1 upozorenje | +5V_RELEJ — prikazano odredište na zavojnici, nepoznat izvor napajanja, N6. |

U odnosu na R1, četiri pogreške nestale su zbog stvarnih novih spojeva: K1 COM/11 na BAT+, K1 NO/14 na R1/R2, VIN+ na stranu opterećenja i VIN− na povrat BAT−. Nisu uklonjene izuzećima ili promjenom pravila.

Nema novih isključenih provjera, oznaka `No Connect`, lažnih `PWR_FLAG` simbola ni promjene ozbiljnosti nalaza. Tvornički zadani neaktivni tipovi provjera ostaju navedeni u `ignored_checks` izvornog JSON-a; `.kicad_pro` nije promijenjen. Konačni ERC ne prijavljuje nepovezane krajeve vodova, krajeve izvan mreže, višestruke nazive iste mreže ni nepodudaranje bibliotečnih simbola.

Zasebna [provjera mreža](connectivity-check.txt) prolazi: COM–NO prekida put kada je otvoren i omogućuje put BAT+ → R1/R2 → interni shunt → BAT− kada je zatvoren; obje grane opterećenja su paralelne i nisu premoštene. Provjereno je deset točnih funkcionalnih mreža i deset izoliranih pinova, uključujući poznati nekorišteni NC. Skripta za izvoz zadržava ERC status 5 i nakon uspjeha ovih provjera.

Niti ERC niti provjera mreža ne dokazuju fizički pinout, polaritet stvarnog INA219 spoja, vrijednost shunta, naponsku kompatibilnost modula ili pouzdanost zavojnice 6 V na 5 V. J1/J2 su pasivna logička sučelja pa ERC ne provjerava električne tipove izlaza stvarnih modula. RSH1 ima nepoznatu fizičku vrijednost i nije korišten za izračun ili simulaciju struje. Fizičko ožičenje ostaje nepotvrđeno.
