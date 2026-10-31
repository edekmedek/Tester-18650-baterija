# R68 — Konačan izbor MOSFET-a bez dodatnog napajanja

Datum: 2026-10-31. Status: izbor komponente za NOVU shemu; nije naručeno.

## Kupnja
- **4 kom AO3400A**, Alpha & Omega Semiconductor; preporuka uzeti **6–10 kom** kao zalihu za lemljenje SOT-23.
- SOT-23 N-channel 30 V, proizvođač jamči RDS(on) ≤ 48 mΩ pri VGS=2.5 V (za propisani testni uvjet).
- Originalni datasheet: https://www.aosmd.com/sites/default/files/res/datasheets/AO3400A.pdf
- DigiKey: https://www.digikey.com/en/products/detail/alpha-omega-semiconductor-inc/AO3400A/1855942
- **BEZ 10 V izvora i BEZ TC4427 drivera.**
- Pri idealnih 4.2 V i 10 Ω, I≈0.42 A/grana, P_MOS≈I²×0.048≈8.5 mW maksimalno po parametru RDS(on), ne uključuje preklopne gubitke ni greške.
- Provjeriti SOT-23 G/S/D pinout proizvođača i KiCad footprint; ne koristiti TO-220 footprint s R42.

## Nova 4-kanalna arhitektura
- 4 × 10 Ω / 5 W vanjska žičana otpornika, po jedan po kanalu; otpornici troše do 1.76 W pojedinačno i znatno se zagrijavaju.
- 4 × AO3400A, zasebni GPIO 3.3 V, gate serijski R oko 100 Ω te pull-down Gate–Source 100 kΩ.
- Ukupna idealna struja pri 4.2 V: 1/2/3/4 uključena kanala = 0.42/0.84/1.26/1.68 A.
- Zajednički INA219 shunt mjeri ukupnu struju, ESP32 integrira mAh.
- Zasebna regulirana naponska mjera ćelije, mehanički osigurač, neovisna zaštita od podnapona i pregrijavanja, zaštita od obrnutog polariteta, izbjegavanje istovremenog punjenja i pražnjenja.
- Realni TP4056 modul i INA219 breakout moraju biti potvrđeni zbog zaštitnih izlaza, shunta i granice struje; pri 1.68 A mogući su limiti zaštite.
- R42/R60 odnose se na staru linearnu shemu i ne smiju se slati u proizvodnju.
- Četiri IRF3205 na zajedničkom hladnjaku ostaju slobodna za drugi projekt.

## Status
Odabran konkretan MOSFET primjenjiv izravno na ESP32 3.3 V. Slijedi nova funkcionalna shema, ERC i novi PCB. Bateriju NE priključivati prije dovršetka sigurnosnog sklopa.
