# Dodatna korisnikova vizualna referenca — detalj RL/Q/R (15.10.2026.)

**Precizna potvrda korisnika:** iz ranijeg predloška **odgovara samo detalj iz dostavljenog izreza slike**. **Sve ostalo u tom predlošku ne odgovara stvarnom sklopu i ne smije se preuzimati.** Potvrda se odnosi na footprint/raster upravo prikazanog detalja, ne na cijeli predložak, ostale komponente, vodove ili shemu.

## Čitljive oznake na slici

- Relejni izvodi: `RL12B`, `RL12A`, `RL11B`, `RL11A`, `RL14B`, `RL14A`.
- Tranzistor: `Q1`, `E`, `C`, `B` uz tri priključka, redom kako je grafički označeno.
- Otpornici: `R1`, `R2`, `R3`, `R4` u jednom redu na dnu detalja.
- Na gornjem rubu vidljive oznake `A2`, `A1` te tekst koji spominje lemljenje preko `RL...`; natpis je djelomično odrezan pa ga ne treba tumačiti kao pouzdanu električku uputu.
- Na slici su vidljive obojene trase i kružne rupice. Boje i presjeci nisu dokaz kontinuiteta.

## Kako upotrijebiti

1. Koristiti **isključivo geometriju unutar korisnikova izreza slike** kao potvrđenu referencu. Ne kopirati ostatak ranijeg predloška. Usporediti taj detalj s fotografijama obje strane stvarnog sklopa.
2. Ne pretpostaviti da oznake RL11/RL12/RL14 predstavljaju potvrđen stvarni raspored izvoda Schrack RT314006. Oznake A/B mogu označavati paralelne/udvojene kontaktne točke, ali to je potrebno dokazati.
3. Korisnik potvrđuje da footprint/raster predloška odgovara stvarnosti, ali **simbolički 3D izgled R1–R4 na prikazu nije mjera fizičkog kućišta**. R1/R2 su na stvarnoj fotografiji 22Ω/5W cementni otpornici; treba razlikovati pozicije/raster od grafičkog prikaza tijela.
4. Grafički Q1 E/C/B raspored nije sam po sebi dokaz fizičkog pinouta C3209.
5. Ako je izvorni uređivi predložak dostupan, iz njega preuzeti **samo elemente koji su vidljivi na korisnikovu izrezu**. Ostali elementi predloška nisu vjerodostojni.

**Status:** korisnik potvrđuje **samo prikazani izrez**; **ostatak predloška je pogrešan**. Ova granica vrijedi i za PCB P2. Potvrda prikazane geometrije nije potvrda električkog pinouta ili vodova.

## Naknadna proizvođačka potvrda u P3

Korisnik je potvrdio TE RT1 rev. 6 str. 5: izvedba RT314006 16 A / 5 mm / 1 Form C ima osam fizičkih izvoda (A1/A2 i udvojene 12/11/14). Time je razriješena struktura kontaktnih parova za K1; ograda o nepotvrđenom fizičkom pinoutu C3209 ostaje. Aktualne top-view koordinate, pravilna rotacija, mapiranje i granica dimenzijske provjere opisani su u [RT314006_MANUFACTURER_SOURCE.md](RT314006_MANUFACTURER_SOURCE.md). Nije kopiran bakar sa starog izreza.
