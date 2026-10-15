# RT314006 — ispravak: osam fizičkih izvoda, pet električnih funkcija

**Ranija tvrdnja da RT314006 ima pet fizičkih izvoda bila je pogrešna.** Za potvrđenu izvedbu 16 A, 1 Form C postoje A1, A2 te po dva izvoda 12/NC, 11/COM i 14/NO: ukupno **8 izvoda**. Broj pet odnosi se na električne funkcije standardnog SPDT simbola, ne na broj nožica. Ranija uputa da se ne koristi osmoizvodna varijanta povučena je.

Korisnik je potvrdio službeni TE/SCHRACK [ENG_DS_RT1_6-9724925.pdf](https://www.mouser.com/catalog/specsheets/ENG_DS_RT1_6-9724925.pdf), **str. 5, PCB LAYOUT / TERMINAL ASSIGNMENT, 16A pinning 5mm, 1 form C, BOTTOM VIEW**. To se podudara s tri para RL12A/B, RL11A/B i RL14A/B u potvrđenom izrezu.

Izravno preuzimanje tog PDF-a i službenih TE/Schrack endpointova u ovom okruženju vraća proxy **HTTP 403**, i nakon odobrenog mrežnog pristupa. PDF nije izravno pregledan niti priložen kao da je preuzet. Potvrda broja i funkcija pinova potječe od korisnika; koordinate i 3D položaji dodatno su provjereni prema dostupnoj standardnoj KiCad RT1 16 A biblioteci i njezinu osmoizvodnom modelu.

## Provjerena dostupna geometrija i granica točnosti

KiCad referenca `Relay_SPDT_Schrack-RT1-16A-FormC_RM5mm` ima 8 padova, razmak redova 7,5 mm, zavojnicu na x=0 te kontaktne stanice x=15,26 / 20,30 / 25,34 mm. Iz modela koji standardni footprint koristi izdvojeno je osam metalnih pinova: njihova središta točno odgovaraju tim rupama. Kućište je 29 × 12,7 × 15,7 mm. Kopirani izvori, hashovi i ograničenja su u [P3 manifestu](../../pcb_sources/p3/geometry.json).

**To su provjerene knjižnične koordinate, a ne tvrdnja o izravno očitanim točnim TE dimenzijama.** Korisnikov podatak navodi nominalno 5 mm; biblioteka sadrži uzdužne korake 5,04 mm. Proizvođačke točne mjere i tolerancije treba izravno usporediti prije izrade. Prethodna perfboard aproksimacija 7,62 mm / 5,08 mm više nije aktivni K1 footprint.

## Rotacija i pogled

KiCad footprint zadan je pogledom odozgo, s A1=(0,0), A2=(0,−7,5), kontaktima u pozitivnom x smjeru. Centar kućišta je (12,15,−3,75). Za fotografsku orijentaciju sa zavojnicom gore primijenjena je prava rotacija 90° u smjeru kazaljke na satu na ekranu PCB-a:

```text
x_lokalno = −(y_KiCad + 3,75)
y_lokalno = x_KiCad − 12,15
```

U završnom **pogledu odozgo** A1 je lijevo, A2 desno. Pri usporedbi s **pogledom odozdo** vodoravna koordinata mora se zrcaliti jednom: donji prikaz tada ima A2 lijevo i A1 desno, kao u izrezu. Oznake s donjeg pogleda nisu doslovno kopirane na gornju stranu. Udvojeni kontakti simetrični su; njihova funkcija ostaje jednaka na obje strane.

STEP model centriran je na (12,15,3,75) i zakrenut −90° oko kartezijskog Z; nema refleksije modela ni uklanjanja pinova. Suprotan predznak Y STEP/PCB koordinata uzet je u obzir. [Modelna provjera](p3-relay-model.json) bilježi svih osam središta, a [CSV](K1_COORDINATES.csv) stvarne položaje u završnom footprintu.

| Funkcija | Broj fizičkih padova | Mreža sheme |
|---|---:|---|
| A1 | 1 | `+5V_RELEJ` |
| A2 | 1 | `K1_C`, kolektorska mreža |
| 11 / COM | 2 | `BAT_PLUS` |
| 12 / NC | 2 | isti nekorišten NC kontakt, bez vanjske funkcijske veze |
| 14 / NO | 2 | `LOAD_IN`, paralelni ulaz R1/R2 |

Svi kontakti istog broja međusobno su spojeni bakrom. BAT+ je rutiran do COM-a, NO do opterećenja. COM i NO **nisu premošteni bakrom**. A1/A2 imaju mreže, ali izvor napajanja i stvarni fizički kolektorski pad C3209 još nisu potvrđeni, pa te veze nisu proizvoljno rutirane.

Nazivna zavojnica i dalje je 6 V DC, 90 Ω, oko 0,4 W; dokumentirani pogon je 5 V. Mapiranje pinova ne dokazuje marginu uklapanja na 5 V, ispravnost zaštite ili fizičko ožičenje korisnikova primjerka.
