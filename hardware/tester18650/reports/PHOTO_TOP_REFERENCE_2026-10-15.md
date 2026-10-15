# Fotografska referenca stvarnog testera — gornja strana (15.10.2026.)

Ovaj dokument opisuje fotografiju koju je korisnik dostavio u razgovoru ChatGPT 15.10.2026. Fotografija prikazuje **postojeći funkcionalni sklop na univerzalnoj perforiranoj pločici**. Izvorna fotografija nije automatski spremljena u ovaj GitHub repozitorij; za vizualnu rekonstrukciju Codexu treba zasebno priložiti sliku.

## Vizualni raspored (gledano kao na fotografiji, USB priključak gore)

- **Lijevo, uzdužno:** NodeMCU ESP8266 development board, USB konektor na gornjem rubu, antena dolje. Natpisi uz rub vidljivi, uključujući D5, D4, D1, A0, GND i VIN.
- **Gore sredina:** narančasti Schrack RT314006, natpis 6 VDC, 16 A / 250 VAC, okomita orijentacija na slici.
- **Desno, uzdužno:** držač jedne 18650 baterije, pozitivni kontakt i crvena žica prema gornjem dijelu fotografije; ćelija označena rukom približno 4,252–4,257 V (rukom ispisana oznaka, ne mjerenje u trenutku snimanja).
- **Sredina dolje, jedan ispod drugog:** dva bijela cementna otpornika s natpisom `5W22R0J`, tj. 22 Ω / 5 W svaki.
- **Dolje lijevo:** ljubičasti modul `INA219 BREAKOUT`; lijevi rub s oznakama SCL, SDA, VCC, GND; desno vijčani terminal s oznakama IN− (gore) i IN+ (dolje), prema orijentaciji na fotografiji.
- **Ostali mali dijelovi:** nekoliko komponenti i žica oko releja i ispod njega; na fotografiji se ne mogu pouzdano identificirati fizički C3209, djelitelj 10k/20k, eventualna zaštitna dioda i stvarni podpločni vodovi.

## Obavezno za sljedeću KiCad PCB reviziju

1. **Prvo rekonstruirati raspored na perfboardu** po ovoj fotografiji, uz očuvanje relativnih položaja, orijentacije i vidljivih natpisa. Nemojte zamijeniti stvarni raspored generičkim rasporedom PCB-a.
2. Za fizičke dimenzije, razmak rupa i pinout NodeMCU, INA219 modula, držača ćelije i RT314006 treba provjeriti konkretne izvedbe, a ne samo generičke modele.
3. Fotografija gornje strane **nije dokaz električnih spojeva ispod pločice**. Posebno ne potvrđuje spojeve baze/emitera C3209, 10k/20k djelitelja, izvore napajanja ni točan raspored nožica releja.
4. Pločica za izradu (Gerber) i električki potpuno rutirani PCB nisu odobreni dok se ne utvrde nepoznati spojevi i provede DRC.
5. Ako Codex ima pristup originalnoj fotografiji kao privitku, usporediti vizualni raspored s ovom bilješkom. Izvorna slika je mjerodavnija od teksta.

Status: **vizualna referenca, nije verificirana električna netlista niti mehanički nacrt**.

## Dopuna nakon pregleda priloženog PDF-a u P1

Izvorni PDF ima prednost pred gornjim opisom. Na njegovoj gornjoj fotografiji vidi se **Soldered INA219 bez ugrađenog vijčanog terminala**: desno su vidljive zalemljene strujne rupe IN−/IN+. Raniji izraz „vijčani terminal” nije točan za fotografiranu izvedbu. PCB P1 i njegov proizvođački 3D model prate tu izvedbu. Relativni raspored i granice potvrde opisani su u [PCB.md](../PCB.md).
