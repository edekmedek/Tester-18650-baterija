# ESPHome konfiguracija — referentni zapis

Datum: 15.10.2026.

Aktualni firmware korisnik je dostavio u razgovoru. Zbog javne vidljivosti repozitorija, fallback Wi-Fi lozinka nije spremljena. Ispod je **izvadak za rekonstrukciju električne sheme**, ne potpuna konfiguracija spremna za flash.

```yaml
esphome:
  name: battery-tester-8266-wifi-test
esp8266:
  board: nodemcuv2
i2c:
  sda: GPIO2
  scl: GPIO5
  scan: true
  frequency: 100kHz
switch:
  - platform: gpio
    pin: GPIO14
    id: relay
    restore_mode: ALWAYS_OFF
sensor:
  - platform: adc
    pin: A0
    id: battery_adc
  - platform: ina219
    address: 0x40
    shunt_resistance: 0.11425 ohm
    max_voltage: 16.0V
    max_current: 3.2A
```

Kalibracija napona baterije: `battery_adc * 9.5079`. Cutoff početno 3,00 V, pet uzastopnih sekundi ispod praga. OLED je uklonjen iz aktualne izvedbe.

Prije ponovnog flashanja preuzeti i provjeriti cijeli originalni YAML, uključujući sve automatizacije, umjesto ovog izvatka.
