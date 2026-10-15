# Tester 18650 — dokumentacija postojećeg funkcionalnog prototipa V1

**Status:** dokumentacija zatečenog, funkcionalnog uređaja (AS-BUILT koliko je moguće utvrditi bez rastavljanja). **Ne predstavlja certificiranu shemu ožičenja, proizvodni PCB niti odobrenje za reprodukciju.** Postojeći fizički tester ostaje netaknut. Datum: 15.10.2026.

## 1. Namjena i granica V1

Ovaj uređaj je **jednokanalni tester kapaciteta 18650** koji kontrolirano prazni ćeliju, mjeri napon i struju te integrira kapacitet (mAh) i energiju (Wh). Nema hardver za automatsko punjenje. Budući višekanalni punjač/analizator za odabir ćelija pri popravku Makita baterijskih paketa **zaseban je razvojni projekt** i ne zahtijeva rastavljanje ovog prototipa.

## 2. Stvarno vidljive komponente

Iz fotografije gornje strane korisnikova funkcionalnog sklopa:
- NodeMCU ESP8266 (USB priključak na vrhu fotografije; antena dolje), lijevo.
- Schrack/TE RT314006, narančasti relej s oznakom zavojnice **6 VDC**, gore u sredini. Koristi se COM/NO za uključivanje pražnjenja.
- Držač jedne 18650 ćelije desno, s vodovima prema perforiranoj pločici.
- Dva bijela cementna otpornika **5W22R0J** (22 Ω, 5 W), jedan ispod drugoga u sredini; funkcionalno paralelno, ekvivalentno **11 Ω**.
- Ljubičasti modul **INA219 BREAKOUT**, dolje lijevo, sa SCL/SDA/VCC/GND te IN+/IN−.
- Manje komponente i ožičenje na pločici; nisu sve njihove fizičke oznake i priključci čitljivi.

Fotografija donje strane prikazuje lemljene točke, bakrene mostove i izolirane vodiče. Ona se pri usporedbi s gornjom stranom mora **vodoravno zrcaliti točno jednom**. Samo križanje izoliranih vodiča ne predstavlja spoj.

Korisnik je potvrdio **samo uski izrez ranijeg predloška** s oznakama RL11A/B, RL12A/B, RL14A/B, Q1 E/C/B i R1–R4 kao točan raster/footprint. **Ostatak tog predloška nije točan** i ne koristi se.

Reference: [opis gornje strane](reports/PHOTO_TOP_REFERENCE_2026-10-15.md), [opis donje strane](reports/PHOTO_BOTTOM_REFERENCE_2026-10-15.md), [potvrđeni izrez](reports/pcb/REFERENCE_DETAIL_RL_Q_R_2026-10-15.md).

## 3. Funkcionalna shema — poznato nasuprot pretpostavljenom

```text
18650 (+) → K1 COM/11 → K1 NO/14 → [R1 22Ω || R2 22Ω]
           → INA219 mjerni strujni put → 18650 (−)
```

K1 ima **osam fizičkih izvoda**: A1/A2 zavojnice i po dva fizička izvoda kontakata 11/COM, 12/NC, 14/NO. P3 ih mapira prema provjerljivoj KiCad 16A referenci; proizvođačke tolerancije i stvarni lemovi nisu mjerenjem verificirani. INA219 je u serijskom strujnom putu, ali **točna orijentacija VIN+/VIN− na stvarnom uređaju nije dokazana**. Firmware uzima apsolutnu vrijednost izmjerene struje, pa predznak mjerenja nije dokaz polariteta.

Pri 4,2 V, idealno opterećenje 11 Ω povlači približno **0,382 A** i disipira ukupno **1,60 W**, odnosno približno **0,80 W po otporniku**. To su teorijske vrijednosti bez otpora vodova, releja i mjernog shunta, a ne izmjerena radna struja. Pri 3,0 V idealno oko **0,273 A**.

## 4. Firmware — konkretne funkcije iz pohranjene datoteke

Izvor: [dokumentacijska ESPHome kopija](../../firmware/battery-tester-8266-wifi-test.yaml). To nije potvrda da su bajtovi te datoteke identični trenutačno flashanoj verziji.

| Funkcija | Stvarno dokumentirana vrijednost |
|---|---|
| Kontroler | ESP8266 / `nodemcuv2` |
| Relej | GPIO14 (D5), `ALWAYS_OFF`; isključenje pri pokretanju |
| INA219 I²C | SDA GPIO2 (D4), SCL GPIO5 (D1), adresa 0x40, 100 kHz |
| INA219 konfiguracija | `shunt_resistance: 0.11425 ohm` (firmware parametar, ne potvrda fizičkog shunta) |
| Napon ćelije | A0 ADC × 9.5079 (kalibracijski faktor; fizički djelitelj nepotvrđen) |
| Početni cutoff | 3,00 V, korisnički raspon 2,50–4,20 V |
| Početak testa | provjera napona iznad cutoffa; poništavanje brojila; nakon 500 ms uključivanje releja |
| Kraj testa | 5 uzastopnih jednokratnih očitanja napona ≤ cutoffa; isključenje releja |
| Integracija | svake sekunde `mAh += A × 1000/3600`; `Wh += V × A/3600` |
| Zapis rezultata | ESPHome senzori `Kapacitet`, `Energija`, `Vrijeme testa`; nema dokaza o zasebnoj trajnoj bazi po ćeliji |
| Punjenje | nije ugrađeno u dokumentirani V1 firmware |

### Važni uočeni sigurnosni i mjerni nedostaci firmwarea — **bez promjene V1**

1. **Nema maksimalnog vremena pražnjenja.** Ako je napon tijekom aktivnog testa `NaN`, uvjet `voltage <= cutoff` je neistinit i brojač niskog napona vraća se na nulu. Test može nastaviti s uključenim relejem dok drugi mehanizam ne prekine rad.
2. **Gubitak valjanog očitanja struje/napona nije zaseban fail-safe uvjet.** Integracija se preskače za `NaN`, ali se relej zbog toga ne isključuje.
3. Relej je zasebno izložen kao ESPHome `switch`; logika gumba i stanje `test_running` nisu jedini način upravljanja fizičkim opterećenjem. U budućoj verziji potrebno je uskladiti sigurnosno upravljanje i izravni prekidač.
4. Integracija koristi trenutačni uzorak jednom u sekundi i pretpostavlja interval točno 1 s; ne mjeri stvarni protekli interval između valjanih uzoraka. Za ozbiljno razvrstavanje ćelija treba validirati kalibraciju i točnost.
5. Nije dokumentirana zasebna termička zaštita ćelije/otpornika ni hardverski watchdog koji samostalno prekida pražnjenje.

Ovi nalazi nisu tvrdnja da je postojeći fizički tester neispravan; oni su **razlozi da se V1 ne ostavlja bez nadzora i da se buduća verzija projektira sa zasebnom zaštitom**. Ne mijenjati postojeći firmware na slijepo.

## 5. KiCad datoteke i stvarno stanje

- [KiCad projekt](tester18650.kicad_pro), [shema R2](tester18650.kicad_sch), [PDF sheme](tester18650.pdf).
- [PCB P3](tester18650.kicad_pcb), [PDF komponenti](tester18650_pcb_components.pdf), [PDF vodova](tester18650_pcb_layout.pdf), [3D PNG](tester18650_pcb_3d.png), [3D GLB](tester18650_pcb_3d.glb).
- [Detaljni opis PCB-a](PCB.md), [DRC](reports/pcb/DRC.md), [ERC](reports/ERC.md).

P3 je **djelomična rekonstrukcija**, a ne potvrđena kopija fizičkog uređaja: DRC **0 geometrijskih kršenja, 2 nepovezane veze, 5 upozorenja**; ERC **11 pogrešaka i 1 upozorenje**. Glavni strujni krug na PCB-u nije potpuno rutiran. Nisu izrađeni proizvodni Gerberi.

## 6. Preostale nepoznanice koje fotografije ne dokazuju

- Fizički pinout/kućište tranzistora C3209 i njegova baza/emiter te eventualni bazni otpornik i zaštitna dioda.
- Stvarni raspored i veze otpornika 10 kΩ/20 kΩ prema A0 te mogući interni djelitelj NodeMCU-a.
- Izvor napajanja releja (zavojnica nominalno 6 V), NodeMCU-a i INA219; INA219 GND i I²C pull-upovi.
- Stvarni VIN+/VIN− polaritet INA219 u strujnom krugu.
- Točne fizičke dimenzije/pinout revizije modula, držača i otpornika te mehaničko i termičko pristajanje.

**Pravilo:** te spojeve ne popunjavati nagađanjem samo radi ERC/DRC nule. Postojeći funkcionalni tester **ne rastavljati** radi dokumentacije.

## 7. Status za daljnji razvoj

V1 je **očuvana funkcionalna referenca**. Novi projekt automatskog analizatora za Makita ćelije treba razvijati odvojeno: punjenje → mjerenje kapaciteta i drugih karakteristika → ponovno punjenje → trajni zapis rezultata; najprije jedan validirani kanal, potom osam. Nije opravdano zamijeniti referentni V1 prototip neprovjerenim P3 PCB-om.
