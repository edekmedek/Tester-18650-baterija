# Rekonstrukcija električne sheme — revizija D1

Datum: 15.10.2026. Status: radna rekonstrukcija na temelju fotografija i korisnikovih podataka. **Nije verificirana izvedbena shema.**

## Ispravak identifikacije kontrolera
Na dostavljenim fotografijama je **NodeMCU s ESP8266 / ESP-12F**, a ne ESP32. Ranije zabilježeni GPIO21/22/26/34 pripadaju drugoj platformi i NE SMIJU se prenijeti u shemu ove pločice bez provjere izvornog koda. Vidljivi su pinovi D0–D8, A0, RX, TX, 3V, VIN i GND.

## Komponente i podaci
- U1: NodeMCU ESP8266, ESP-12F; napajanje preko micro-USB vidljivo na fotografiji. Ostali putovi napajanja nisu potvrđeni.
- U2: INA219 breakout, oznake SCL, SDA, VCC, GND i VIN+/VIN− (položaj u krugu provjeriti).
- DS1: OLED I²C (poznat iz prethodnog projekta, nije vidljiv na fotografijama).
- K1: Schrack RT314006, zavojnica označena 6 V DC, u uređaju napajana s 5 V prema korisniku.
- Q1: tranzistor C3209 za upravljanje relejem, prema prethodnom projektu; vrijednost baznog otpornika i zaštitna dioda nisu utvrđene.
- R_LOAD1, R_LOAD2: 22 Ω / 5 W paralelno, vidljivo na fotografiji. Izmjeren ukupni otpor oko 11,15 Ω.
- R_DIV1, R_DIV2: 10 kΩ i 20 kΩ, korisnik potvrdio; redoslijed u djelitelju i spoj na A0 još provjeriti.
- BAT1: držač 18650; minus baterije spojen na zajedničku masu.
- Nema ugrađene zaštite od obrnutog polariteta prema korisniku; evidentirano kao sigurnosni rizik, ne kao preporuka.

## Put struje — korisnikov opis
BAT+ → kontakt releja → shunt / INA219 → BAT−.

**Otvoreno:** točan spoj dvaju opteretnih otpornika u tom putu, položaj INA219 VIN+ i VIN− u odnosu na shunt i kontakt releja. Ne spajati shemu prema pretpostavci.

## Potrebno iz izvornog firmwarea
- Stvarni pinovi ESP8266 za SDA/SCL, relej, LED i analogni ulaz A0.
- Polaritet relejnog upravljanja i logika sigurnog isključivanja.
- Skala ADC-a i logika mjerenja INA219.

## Napomena o fotografijama
Fotografije potvrđuju tip pločice, oznaku releja, INA219 i 2×22 Ω/5 W. Ne potvrđuju nevidljive veze na poleđini pločice. Nije potrebno rastavljati funkcionalan uređaj radi ove dokumentacije.
