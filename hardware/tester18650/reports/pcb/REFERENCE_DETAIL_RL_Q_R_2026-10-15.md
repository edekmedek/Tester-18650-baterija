# Dodatna korisnikova vizualna referenca — detalj RL/Q/R (15.10.2026.)

Korisnik je u razgovoru poslao uski prikaz rasporeda s mrežom perforirane pločice, obojenim tragovima i oznakama. Slika je referenca za usporedbu s postojećim PCB-om, ali nije dokaz da je svaka mreža električki ispravno mapirana.

## Čitljive oznake na slici

- Relejni izvodi: `RL12B`, `RL12A`, `RL11B`, `RL11A`, `RL14B`, `RL14A`.
- Tranzistor: `Q1`, `E`, `C`, `B` uz tri priključka, redom kako je grafički označeno.
- Otpornici: `R1`, `R2`, `R3`, `R4` u jednom redu na dnu detalja.
- Na gornjem rubu vidljive oznake `A2`, `A1` te tekst koji spominje lemljenje preko `RL...`; natpis je djelomično odrezan pa ga ne treba tumačiti kao pouzdanu električku uputu.
- Na slici su vidljive obojene trase i kružne rupice. Boje i presjeci nisu dokaz kontinuiteta.

## Kako upotrijebiti

1. Usporediti detalj s fotografijama gornje i donje strane fizičkog testera te s PCB P1.
2. Ne pretpostaviti da oznake RL11/RL12/RL14 predstavljaju potvrđen stvarni raspored izvoda Schrack RT314006. Oznake A/B mogu označavati paralelne/udvojene kontaktne točke, ali to je potrebno dokazati.
3. Provjeriti jesu li R1/R2 na detalju isti 22Ω/5W cementni otpornici sa stvarne fotografije. Vizualno na detalju izgledaju kao mali aksijalni otpornici; zato se slika ne smije bez provjere tretirati kao vjerna fotografija izvedenog sklopa.
4. Grafički Q1 E/C/B raspored nije sam po sebi dokaz fizičkog pinouta C3209.
5. Sačuvati ovaj detalj kao referencu za mogući raniji nacrt/raspored; ako je generiran iz nekog alata, tražiti njegov izvorni uređivi dokument umjesto ponovnog precrtavanja.

**Status:** korisna dodatna referenca, ali nije dovoljno pouzdana za automatsku promjenu bakrenih mreža ili proizvodnih padova.
