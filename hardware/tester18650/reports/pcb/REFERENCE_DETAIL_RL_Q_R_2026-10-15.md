# Dodatna korisnikova vizualna referenca — detalj RL/Q/R (15.10.2026.)

**Potvrda korisnika:** slika je iz jednog od ranijih predložaka ovog projekta i **footprint/raster rasporeda na toj slici odgovara stvarnom funkcionalnom sklopu**. Ovo je potvrđena referenca fizičkog rasporeda, a ne samo spekulativan crtež. Prikazani vodovi i njihovo električko značenje ipak se moraju zasebno provjeriti.

## Čitljive oznake na slici

- Relejni izvodi: `RL12B`, `RL12A`, `RL11B`, `RL11A`, `RL14B`, `RL14A`.
- Tranzistor: `Q1`, `E`, `C`, `B` uz tri priključka, redom kako je grafički označeno.
- Otpornici: `R1`, `R2`, `R3`, `R4` u jednom redu na dnu detalja.
- Na gornjem rubu vidljive oznake `A2`, `A1` te tekst koji spominje lemljenje preko `RL...`; natpis je djelomično odrezan pa ga ne treba tumačiti kao pouzdanu električku uputu.
- Na slici su vidljive obojene trase i kružne rupice. Boje i presjeci nisu dokaz kontinuiteta.

## Kako upotrijebiti

1. Koristiti **korisnički potvrđen footprint/raster ovog predloška** kao prioritetnu geometrijsku referencu za područje releja, tranzistora i otpornika. Usporediti s fotografijama obje strane fizičkog testera i PCB P1.
2. Ne pretpostaviti da oznake RL11/RL12/RL14 predstavljaju potvrđen stvarni raspored izvoda Schrack RT314006. Oznake A/B mogu označavati paralelne/udvojene kontaktne točke, ali to je potrebno dokazati.
3. Korisnik potvrđuje da footprint/raster predloška odgovara stvarnosti, ali **simbolički 3D izgled R1–R4 na prikazu nije mjera fizičkog kućišta**. R1/R2 su na stvarnoj fotografiji 22Ω/5W cementni otpornici; treba razlikovati pozicije/raster od grafičkog prikaza tijela.
4. Grafički Q1 E/C/B raspored nije sam po sebi dokaz fizičkog pinouta C3209.
5. Potražiti izvorni uređivi predložak u postojećim projektnim datotekama ako je dostupan, kako bi se **preuzele potvrđene koordinate i rasteri**, a ne ponovno ručno precrtavali.

**Status:** korisnik je izričito potvrdio da **footprint prikazanog ranijeg predloška odgovara stvarnom sklopu**. To opravdava korištenje geometrije za PCB P2. Potvrda geometrije nije automatska potvrda električkog pinouta ili vodova.
