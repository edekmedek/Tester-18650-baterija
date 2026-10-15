# Neovisni pregled Codexove rekonstrukcije R1 — 15.10.2026.

## Provjereno čitanjem stvarno spremljenih GitHub datoteka

- `hardware/tester18650/tester18650.kicad_pro`, `.kicad_sch`, PDF i ERC izvještaji postoje u grani `main`.
- `reports/netlist.xml` potvrđuje: R1 i R2 su paralelni između mreža `LOAD_IN` i `LOAD_OUT`; GPIO14 je povezan samo do dokumentacijskog kraja TP5; I²C SDA/SCL su zasebne mreže; K1 A2 je na Q1 kolektoru.
- Kontakti K1 (11/12/14) nisu spojeni s BAT+ / LOAD_IN. INA219 VIN+/VIN− nisu spojeni s LOAD_OUT / BAT−. To je **namjerno nepotpuna električna rekonstrukcija**, a ne potpuno izvedbena shema.
- Izvještaj `ERC.md` odgovara `erc.rpt`: 14 otvorenih priključaka, 1 ulaz bez izvora i 1 upozorenje o izoliranoj oznaci (+5V_RELEJ); 15 pogrešaka + 1 upozorenje. `validate.sh` eksplicitno provjerava **očekivanu nepotpunost**, a ne ERC bez greške.

## Sada dostupan novi izvor koji Codex nije imao u R1

U `firmware/battery-tester-8266-wifi-test.yaml` arhiviran je korisnikov kompletni aktualni ESPHome YAML. Jedina namjerna sigurnosna izmjena je da je lozinka fallback AP-a zamijenjena s `!secret battery_tester_fallback_password`; originalna lozinka se ne objavljuje javno.

Činjenice iz firmwarea:
- `GPIO14` — digitalni izlaz za relej;
- `GPIO2` SDA; `GPIO5` SCL; `0x40` INA219;
- `A0` — ADC, skala napona `9.5079`;
- `shunt_resistance: 0.11425 ohm` — **konfiguracijski parametar**, ne potvrđena vrijednost fizičkog shunta;
- `battery_current` koristi `fabsf(ina219_current)`. **Prikazana pozitivna struja ne može potvrditi polaritet spajanja VIN+/VIN−**.
- OLED nije dio postojećeg uređaja.

## Neovisni tehnički zaključci

1. Kod INA219, izvorni TI datasheet definira `V_BUS = V_IN− − GND`, odnosno napon sa strane VIN− prema masi. Ako je modul na niskoj strani struje i VIN− blizu BAT−/GND, očitanje BUS napona približno nula volti je očekivano i nije automatski kvar. To **ne dokazuje** kako je konkretni uređaj spojen. Izvor: https://www.ti.com/lit/ds/symlink/ina219.pdf.
2. Potvrđeni slijed korisnika je BAT+ → relej → R1||R2 → INA219 → BAT−. Stvarna dodjela NO/COM na releju i VIN+/VIN− na modulu i dalje je fizički nepoznata.
3. RT314006 je 6 V DC, 1CO, 16 A model; korisnik potvrđuje da ga napaja s 5 V i da uređaj radi. Napon pogona ni fizički pinout nisu provjereni. Proizvod: https://www.schrack.hr/trgovina/catalog/product/view/id/150975
4. R3 = 10 kΩ i R4 = 20 kΩ nisu dovoljni da se jednoznačno rekonstruira veza A0, osobito uz mogući djelitelj unutar NodeMCU pločice.

## Uvjeti završetka

Preostale točke N1–N6 ne smiju se precrtavati pretpostavkama i nisu riješene dodavanjem firmwarea. Za izvedbenu shemu potrebno je mapirati barem konkretne fizičke vodove (kontakti releja, VIN+/VIN−, baza/emiter, djelitelj i napajanja). Ažurirati KiCad i provjere tek po primitku dokaza. Ne brisati ERC greške tako da se nepoznati pinovi označe `No Connect`, jer su na ispravnom uređaju stvarno spojeni.

**Status:** neovisni pregled izvornog repozitorija, ne zamjena za KiCad CLI validaciju ili fizičko mjerenje.
