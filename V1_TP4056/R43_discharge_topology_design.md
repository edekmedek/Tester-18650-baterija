# R43 — Električna topologija testera 18650 (projektna odluka, bez promjene PCB-a)

Status: **NE SMIJE SE PRIKLJUČITI BATERIJA NITI IZRADITI PCB**. R42 ima korisnički potvrđen DRC=0, no nema verificiranu električnu shemu/ERC.

## Potvrđeno iz datasheeta INA219
TI INA219 koristi vlastiti mjerni shunt između VIN+ i VIN−; mjeri također BUS napon na VIN− prema vlastitom GND. Napajanje VS od 3 do 5.5 V podržava 3.3 V. Izvor: https://www.ti.com/product/INA219 ; https://www.ti.com/lit/ds/symlink/ina219.pdf

## Zašto postojeća pločica ne može mjeriti kapacitet
1. J5 ima označene INA_VIN_PLUS / INA_VIN_MINUS, ali nije uklopljen u strujnu putanju; dakle nema dokaza o mjerenju struje.
2. Dvije odvojene mase CELL_MINUS i TP_OUT_MINUS nisu nužno kratko spojene na stvarnom zaštićenom TP4056 modulu; ne premostiti zaštitni MOSFET spajanjem GND ravno na CELL_MINUS.
3. Q1 drain je nepovezan; RSH1 je low-side analogni shunt, nije isto što i shunt na INA219.
4. INA219 mjeri naponsku sabirnicu iza shunta, a ne nužno *napon same ćelije* na J1.1/J1.2. Za kontrolu završetka pražnjenja treba mjerenje stvarnog napona ćelije s definiranim referentnim čvorom, ADC naponskim djeliteljem ili neovisnim senzorom.
5. Gubitak napajanja ili reset ESP32 ne smije ostaviti opterećenje aktivnim; R4 pull-down smanjuje rizik plutajućeg gatea, ali nije neovisni prekid.
6. IRF3205 nije potvrđen za kontinuirani DC linearni režim ni za gate pogon iz MCP6002 na 3.3 V. Nije dovoljno provjeriti Vgs(th) ili RDS(on).

## Kandidat funkcionalne putanje pražnjenja (NIJE ODOBREN ZA PCB)
Zaštićeni OUT+ TP4056 -> osigurač / odvojeni zaštitni prekidač -> visokostrani INA219 shunt (VIN+ ulaz, VIN- izlaz) -> MOSFET drain -> MOSFET source -> RSH1 -> **zaštićeni OUT−**. Ova putanja zahtijeva da analogni GND i opamp/current-sense referenca budu ispravno izvedeni prema OUT− uz provjeru potencijala, a ne prema B−. I dalje nedostaju kompatibilan MOSFET i siguran hardverski prekid.

**Važno**: INA219 breakout obično ima shunt već na pločici; ne koristiti J5 kao dvožični signalni ulaz za veliku struju bez provjere da je to predviđeno za taj modul i priključke. Za strujni put trebaju odgovarajuće žice, osigurač i provjerena strujna nosivost.

## Arhitektura punjenja/pražnjenja
- Fizički spriječiti simultano punjenje i pražnjenje, ili projektirati i validirati poseban power-path sklop.
- Mora biti poznato podržava li konkretni USB-C TP4056 modul zaštitu ćelije i kako su B− / OUT− spojeni.
- Odabrati dopuštene pragove za konkretnu 18650 ćeliju, termalnu zaštitu, overcurrent i sigurnu inicijalizaciju.

## Najbliži inženjerski korak
Prije nove verzije bakra izraditi KiCad shemu s R39/R42 netlistom i korisnikovom stvarnom INA219/TP4056 pločicom; provjeriti SOA i napajanja, zatim ERC i tek onda PCB.

Ovaj dokument *nije* potvrda električne sigurnosti ni spremnosti za proizvodnju.
