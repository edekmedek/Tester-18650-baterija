# R66 — Četiri nezavisno uključiva otpornika za jednokanalni 18650 tester

Status: **projektna topologija odabrana, nije izrađena ni odobrena PCB/shema.**

## Ideja korisnika
Četiri postojeća tranzistora uključuju četiri opterećenja neovisno. Struja se mijenja promjenom broja uključenih paralelnih otpornika, bez analognog linearnog MOSFET tereta. INA219 mjeri **zbroj struja** prije razdvajanja grana.

### Početni izbor: četiri jednaka 10 Ω / najmanje 5 W, pojedinačna vanjska opterećenja
- 1 grana: približno 0,42 A pri 4,2 V; 0,30 A pri 3,0 V.
- 2 grane: 0,84 / 0,60 A.
- 3 grane: 1,26 / 0,90 A.
- 4 grane: 1,68 / 1,20 A.
- Maksimalno po otporniku pri 4,2 V: 1,764 W; ukupno 7,056 W. Osigurati metalni hladnjak i toplinsko razdvajanje od ćelije. Nazivna snaga ovisi o montaži.
- Stvarna struja manja je zbog otpora baterije, INA219 shunta, MOSFET-a i vodiča. Otpori imaju toleranciju.

### Blok dijagram (funkcionalni, nije verifikacijska shema)
```
18650 -> potvrđeni zaštićeni TP4056 izlaz OUT+ -> osigurač
  -> INA219 visoki shunt VIN+ / VIN- -> zajednički LOAD+
     |-> 10 Ω -> Q1 prekidač -> OUT-
     |-> 10 Ω -> Q2 prekidač -> OUT-
     |-> 10 Ω -> Q3 prekidač -> OUT-
     |-> 10 Ω -> Q4 prekidač -> OUT-
ESP32 -> zaseban GPIO za Q1/Q2/Q3/Q4; otpornici za gašenje gatea
ESP32 <- INA219 I2C (mAh integracija); zaseban siguran nadzor napona ćelije
```
Zaštitni OUT- **ne premostiti** izravnim povezivanjem na baterijski B-.

### Kritične točke
1. Provjeriti koji su točno četiri korisnikova tranzistora; IRF3205 možda se **ne može potpuno uključiti** s 3,3 V. Ako su BJT, potrebni su drugačiji bazni otpornici i dimenzioniranje.
2. INA219 je jednosmjerni monitor sa shuntom po modulu; raspon struje određuje njegova vrijednost i kalibracija. Pri 1,68 A standardni 0,1 Ω shunt ima pad 0,168 V, snagu 0,282 W (provjeriti stvarni shunt i dopuštenje). TI navodi mjerenu diferencijalnu vrijednost do ±320 mV i 3–5,5 V napajanje: https://www.ti.com/product/INA219
3. Zaštićeni izlaz TP4056 mora podnijeti 1,68 A bez prerane zaštite; provjeriti stvarne čipove i pragove.
4. Hardverska zaštita od dubokog pražnjenja, previsoke temperature, osigurač, blokada simultanog punjenja i pražnjenja i fail-safe svi MOSFET-i isključeni pri resetu ESP32.
5. Ovo nije konstanta struja, nego **četiri brzine** koje padaju s naponom. Kapacitet se dobiva integracijom INA219 mjerenja.
6. Postojeći R42 PCB i R60 shema odnose se na **jedan linearni kanal** i nisu valjani za novu topologiju. Novi PCB zahtijeva četiri upravljačka kanala, četiri MOSFET footprinta, četiri vanjska otpornička terminala i zajednički INA219.

## Daljnji zadatak
Provjeriti točne oznake četiri tranzistora iz stvarne zalihe; zatim izraditi novu funkcionalnu shemu sa zaštitom, ERC i novi PCB. Ne priključivati 18650 dok to nije provedeno.
