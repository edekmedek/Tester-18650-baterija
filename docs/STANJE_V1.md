# Stanje prototipa — 15.10.2026.

## Potvrđeno iz Home Assistanta
- Tester radi bez USB veze s računalom.
- Povijest bilježi dva završena testa, oba s razlogom „Završeno - cutoff”.
- U trenutku snimke testira se baterija 3.
- HA prikazuje napon, struju, snagu, kapacitet, energiju, trajanje, grafove i upravljačke tipke.

## Što još nije verificirano
- Točna shema spajanja, pinovi i opterećenje.
- Verzija izvornog koda koja je stvarno instalirana na ESP32.
- Algoritam mjerenja i izračuna kapaciteta/energije.
- Sigurnosne zaštite, temperatura opterećenja i ponašanje pri kvaru senzora.

## Otvorena pitanja
- Zašto dijagnostički INA219 napon prikazuje 0,000 V?
- Zašto je završni napon baterije 2 3,064 V uz cutoff postavljen na 3,00 V?
- Je li pohrana rezultata otporna na restart i gubitak veze?

## Pravilo arhiviranja
Prije bilo kakve izmjene firmwarea sačuvati aktualni izvorni projekt, konfiguraciju Home Assistanta i eventualne build datoteke. U GitHub ne spremati lozinke, API ključeve i tokene.

Dokumentacijska oznaka v1.0 ne znači da je verificirana konkretna binarna verzija firmwarea.
