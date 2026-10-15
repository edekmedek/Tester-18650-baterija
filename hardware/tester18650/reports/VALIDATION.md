# Provedena provjera — 15.10.2026.

## Alati

Cloud računalo: Debian 13, amd64. Predinstalirani KiCad 9.0.2 nije korišten za konačnu isporuku. KiCad CLI **10.0.4** i standardne biblioteke simbola 10.0.4 instalirani su lokalnim raspakiravanjem službenih KiCad PPA paketa u `/workspace/.tools/kicad10/10.0.4`. Nisu mijenjani sistemski paketi.

Preuzimanje je koristilo HTTPS s uključenom TLS provjerom. SHA-256 arhiva provjeren je prema PPA indeksu:

| Paket | Verzija | SHA-256 |
|---|---|---|
| kicad | 10.0.4~ubuntu25.10.1 | `fe312104b363c409186eecc764131db590a9382dd40f5effc5516a769e3379b0` |
| kicad-symbols | 10.0.4~ubuntu25.10.1 | `ed3165109290ae340aa6926fd93f6f4c262d2986b7c3ea9d55ae060af24aed6c` |

Izvor: `https://ppa.launchpadcontent.net/kicad/kicad-10.0-releases/ubuntu/`, distribucija `questing`. Biblioteka wxWebView i potrebne ovisnosti preuzete su APT-om iz Debian `trixie/main` preko HTTPS-a, uz provjeru potpisanih metapodataka Debianovim arhivskim ključem i provjeru paketa. PPA paketi provjereni su TLS-om i SHA-256; ne tvrdi se da je dodatno verificiran PPA potpis. Nisu isključene TLS ili kontrolne provjere, niti korištene zamjenske biblioteke s pogrešnim ABI-jem.

## Rezultati

- Nativni KiCad 10 parser uspješno učitava `.kicad_sch` i pripadajući JSON `.kicad_pro` kroz PDF/netlist/ERC operacije.
- PDF: jedan vektorski list A3, vodoravno, izvezen iz isporučene sheme. Rasteriziran i vizualno pregledan; sekcije, nazivi i bilješke su unutar okvira lista. Nema izmišljenog OLED-a.
- Neto veze: provjereno deset funkcionalnih mreža, paralelna dva otpornika 22 Ω / 5 W, 14 izoliranih nepoznatih pinova te oznake vrijednosti komponenti.
- Nativni ERC: **15 pogrešaka + 1 upozorenje**, izlazni status **5**. Svi nalazi mapirani su na dokumentirane nepoznanice; nema tvrdnje o prolaznom ERC-u.
- `tools/validate.sh`: uspješno ponovljeno iz direktorija projekta i iz drugog radnog direktorija; izvodi stvarne KiCad operacije, ne samo sintaktički pregled teksta.
- Nisu rađeni firmware build, flash, električno mjerenje uređaja ni fizička provjera ožičenja. Potpuni izvorni firmware i fizički KiCad/PCB projekt nisu postojali u početnom repozitoriju.

## Ponoviti

```sh
cd /workspace/Tester-18650-baterija/hardware/tester18650
./tools/validate.sh
```

Integritet konačne isporuke može se provjeriti naredbom `sha256sum -c reports/SHA256SUMS` iz direktorija projekta.

Na drugom računalu instalirati KiCad 10 sa standardnim bibliotekama i Python 3, pa pozvati istu skriptu. Sama uređiva shema sadrži kopije korištenih standardnih simbola; za ERC usporedbu s izvornom bibliotekom koristi `sym-lib-table` i instalirani `KICAD10_SYMBOL_DIR`.
