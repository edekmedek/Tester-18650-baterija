# R65 — Odabrano otporno opterećenje i nabava

## Predloženi konkretni dio
- Arcol **HS15 4R7 J**, žičani otpornik u aluminijskom kućištu, 4,7 Ω, 15 W, tolerancija ±5 %; za pričvršćivanje na metalnu podlogu.
- Referenca trgovine: https://hr.rsdelivers.com/brands/arcol ; RS kataloški broj 159-742; javno prikazana cijena 6,41 EUR/kom bez PDV-a na dan 2026-10-31, promjenjiva.
- Nabava **nije obavljena**.
- Potrebno potvrditi podatkovni list proizvoda, način termičkog pričvršćenja i razmak od plastike/ćelije. Snaga 15 W nije automatska slobodnozračna snaga.

## Predviđeno električko opterećenje
R = 4,7 Ω, bez pada na MOSFET-u, osiguraču i mjernom modulu:
- 4,20 V -> 0,894 A / 3,753 W
- 3,70 V -> 0,787 A / 2,913 W
- 3,00 V -> 0,638 A / 1,915 W
Struja nije konstantna. Kapacitet = vremenski integral **izmjerene** struje INA219, a ne samo formula s 4,7 Ω.

## Potrebna nova shema, prije PCB-a
- Žičani otpornik je **vanjsko opterećenje na vijčanoj stezaljci**; ne koristiti footprint starog niskostranskog RSH1 0,5 Ω.
- Pogon: verificirani 3,3 V logic-level MOSFET u potpuno uključenom/isključenom režimu; odabrati stvarni dio i footprint te provjeriti RDS(on) pri VGS <= 3,3 V.
- Zaštićeni put pražnjenja TP4056 OUT+ -> osigurač -> INA219 shunt IN+ / IN- -> vanjski otpornik -> prekidački MOSFET -> zaštićeni OUT-. **B- i OUT- ne kratko spajati** bez provjere stvarnog modula.
- Napon **same ćelije** mjeriti zasebnim validiranim kanalom; INA219 BUS nije uvijek identičan naponu ćelije.
- Osigurati neovisni prekid preniskog napona, pregrijavanja, zaštitu od zamjene polariteta i blokadu punjenja za vrijeme pražnjenja.
- R42 PCB i R60 as-built shema ostaju reference, nisu podloga za proizvodnju nove topologije.

## Status
Odabran otpornik i arhitektura vanjskog opterećenja; **nije naručeno, nema nove provjerene sheme ni gotovog PCB-a**. Ne spajati 18650 dok sklop nije električki projektiran i provjeren.
