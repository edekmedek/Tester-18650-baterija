# Tester 18650 V1 – jedan kanal

Status: projektiranje; NIJE SIGURNO ZA SPAJANJE BATERIJE.

## Zahtjevi
- Jedna Li-ion 18650 ćelija, proširivo na osam kanala.
- TP4056 modul sa zaštitom (DW01A + 8205A), početno punjenje 500 mA.
- ESP32/ESPHome vodi lokalni automat stanja, HA šalje naredbe.
- Konstantna struja pražnjenja 250–1000 mA, početni test 500 mA, završetak na 3,0 V.
- Mjerenje napona, struje, temperature, mAh i Wh.
- Neovisna hardverska zaštita od previsoke struje i temperature; sigurno stanje pri resetu.

## Projektne odluke za provjeru
1. Dvije međusobno blokirane sklopke odvajaju punjač i elektroničko opterećenje; zaštitni OUT priključci TP4056 modula nisu automatski prikladni za precizno mjerenje struje ćelije.
2. Linearni MOSFET + op-amp + shunt 0,5 ohma; pri 1 A i 4,2 V očekivana disipacija MOSFET-a do približno 3,7 W. MOSFET se NE odabire bez DC SOA provjere i hlađenja.
3. ESP32 DAC nije sigurnosni element. Analogni regulator mora imati zasebno hardversko ograničenje i enable s pull-downom.
4. Mjerenje struje punjenja i pražnjenja definirati tek nakon potvrde topologije modula i shunt položaja.
5. NTC mora biti na ćeliji; ne oslanjati se samo na softverski prekid.

## Sljedeći kriterij prihvaćanja
Potpuna KiCad shema s provjerenim simbolima/pinovima, ERC bez neriješenih grešaka, pregled DC SOA i zaštita. Bez toga nema PCB-a niti spajanja ćelije.
