# Aktualni ESPHome firmware — dokumentacijska kopija

Datoteka `battery-tester-8266-wifi-test.yaml` prepisana je iz korisnikove potvrđene aktualne ESPHome konfiguracije od 15.10.2026., osim jedne namjerne sigurnosne izmjene: zaporka rezervnog Wi-Fi AP-a **nije** objavljena u javnom repozitoriju.

Za instalaciju / lokalnu provjeru YAML-a potrebno je lokalno u ESPHome tajne (`secrets.yaml`) dodati:

```yaml
wifi_ssid: "..."
wifi_password: "..."
battery_tester_fallback_password: "..."
```

**Nemojte spremati `secrets.yaml` u javni repozitorij.** Arhivski zapis nije potrebno flashati na uređaj kako bi se izradila električna shema.

## Potvrđeni pinout

- GPIO14 / NodeMCU D5: relej
- GPIO2 / NodeMCU D4: INA219 SDA
- GPIO5 / NodeMCU D1: INA219 SCL
- A0: očitanje napona baterije; faktor `9.5079`
- INA219 adresa `0x40`; u konfiguraciji je `shunt_resistance: 0.11425 ohm`
- OLED nije ugrađen

## Napomene za električnu rekonstrukciju

Kod koristi `fabsf(ina219_current)`, dakle objavljena pozitivna struja **ne dokazuje** fizički polaritet spajanja VIN+/VIN−. `shunt_resistance` je kalibracijski parametar u firmwareu, ne nužno izmjerena vrijednost otpornika na INA219 modulu. Napon INA219 sabirnice odnosi se na VIN− prema GND modula, a nije automatski napon baterije koji se zasebno mjeri na A0.

Sama konfiguracija također ne utvrđuje vanjske otpornike, zaštitnu diodu ni raspored fizičkih nožica; to su pitanja za shemu i provjeru izvedbe.
