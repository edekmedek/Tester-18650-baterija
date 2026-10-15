# Tester 18650 baterija

**Stanje: radni prototip, dokumentacijska verzija 1.0 (15.10.2026.)**

NodeMCU ESP8266 tester Li-ion 18650 baterija s INA219 mjerenjem i prikazom u Home Assistantu.

## Potvrđene funkcije
- Mjerenje napona, struje, snage, kapaciteta (mAh), energije (Wh) i trajanja.
- Pokretanje i prekid testa preko Home Assistanta.
- Povijest testova i grafovi napona i struje.
- Cutoff podešen na 3,00 V; dva testa zabilježena kao završena cutoffom.
- Numeriranje baterija.

## Rezultati
| Baterija | Početni napon | Završni napon | Kapacitet | Energija | Trajanje |
|---|---:|---:|---:|---:|---|
| 1 | 4,200 V | 3,000 V | 1.164,3 mAh | 4,266 Wh | 3 h 33 min 59 s |
| 2 | 4,234 V | 3,064 V | 2.432,9 mAh | 8,805 Wh | 7 h 32 min 43 s |

Na snimci je baterija 3 u testu (3,983 V, 0,351 A). Rezultati još nisu uspoređeni s referentnim mjernim instrumentom.

## Poznata pitanja
- INA219 dijagnostički napon pokazuje 0,000 V: treba utvrditi značenje entiteta.
- Završni napon baterije 2 je 3,064 V, iako je cutoff podešen na 3,00 V: provjeriti trenutak spremanja i logiku prekida.
- Prije arhiviranja firmwarea treba provjeriti točan izvorni kod koji je instaliran.
- Dokumentirati shemu, vrijednost opterećenja i sigurnosne zaštite za Li-ion baterije.

## Daljnji rad
- [Stanje prototipa](docs/STANJE_V1.md)
- [Ideje za budući razvoj](docs/PLAN_RAZVOJA.md)

Ova dokumentacijska oznaka v1.0 **nije** potvrda da je firmware verificiran ili objavljen kao izdanje. Ne mijenjati funkcionalan firmware tijekom dokumentiranja.

## Električna shema u KiCadu 10

[Projekt R2, PDF, ERC i popis nepoznatih spojeva](hardware/tester18650/README.md). Funkcionalni strujni krug u postojećoj shemi je spojen; fizičko ožičenje nije potvrđeno i ERC nije čist.

## PCB raspored prema fotografijama

[PCB P4, PDF i 3D prikaz](hardware/tester18650/PCB.md). Uređivi raspored prema fotografijama i potvrđenom izrezu RL/Q/R, s djelomičnim bakrom i označenim referentnim/zamjenskim 3D modelima. K1 ima osam mapiranih padova i rutirane kontakte. P4 dodaje čitljive oznake priključaka i PDF donjeg bakra u orijentaciji već zrcaljene fotografije; nema novih električnih veza. DRC: 2 nepovezane veze i 5 upozorenja; pločica nije spremna za proizvodnju.
