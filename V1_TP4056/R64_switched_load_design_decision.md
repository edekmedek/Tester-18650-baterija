# R64 — Odluka o izvedbi pražnjenja 18650

## Odlučeno
Prekinuti projektiranje kontinuiranog linearnog pražnjenja pomoću IRF3205 i MCP6002. Potvrđeni R42 PCB / R60 shema ostaju arhivirana referenca i **nisu** proizvodni nacrt.

Sljedeći kandidat: **4,7 Ω / najmanje 10 W otpornik kao vanjsko opterećenje**, uključen/isključen 3,3 V logic-level N-MOSFET-om. Ne koristiti PWM regulaciju struje bez posebnog projekta; struja se mijenja s naponom ćelije. Za mAh treba integrirati struju izmjerenu INA219 kroz vrijeme, dok se napon ćelije zasebno mjeri.

### Kandidat Q1: AO3400A SOT-23, samo u prekidačkom načinu rada
Prema dokumentaciji proizvođača Alpha & Omega, AO3400A ima zajamčen RDS(on) do 48 mΩ pri VGS=2,5 V (ID=3 A). Zato je kandidat za logičkih 3,3 V. Datasheet: https://datasheet.lcsc.com/lcsc/Alpha-Omega-Semicon-AOS-AO3400A_C20917.pdf

Pri 4,2 V i idealnom 4,7 Ω otporniku struja je približno 0,894 A; pad na MOSFET-u prema granici RDS(on) iznosi najviše približno 43 mV, a disipacija približno 0,038 W, bez parazitskih otpora. Stvarna termika ovisi o PCB bakru i okolini. AO3400A nije zamjena pin-za-pin za IRF3205 TO-220: zahtijeva novu shemu, footprint i rutu.

### Prije spajanja i izrade
- Odabrati točan AO3400A i provjeriti izvorni SOT-23 raspored G/S/D te footprint.
- Projektirati spoj zaštićenog TP4056 OUT+/OUT- s osiguračem i mjernom INA219 putanjom, **ne premostiti B- i OUT-**.
- Osigurati neovisno isključivanje zbog preniskog napona i previsoke temperature, fail-safe na reset ESP32 te međusobno isključenje punjenja/pražnjenja.
- Odvojeno mjeriti napon same ćelije; samo INA219 BUS napon nije nužno napon ćelije.
- Izraditi novu funkcionalnu KiCad shemu i ERC prije promjene postojećeg PCB-a. Ne zavaravati se s 0 DRC-a na staroj topologiji.
- Provjeriti otpornik, izolaciju, disipaciju i siguran smještaj: otpornik može biti jako vruć.

## STATUS
AO3400A je **tehnički kandidat**, a ne verificirana gotova pločica. Ne priključivati bateriju i ne naručivati PCB.
