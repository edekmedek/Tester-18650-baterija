# R67 — Potvrđena zaliha: 4 × IRF3205 na zajedničkom hladnjaku

**Izvor:** korisnikova fotografija i eksplicitna potvrda „4 x irf3205” (2026-10-31).
**Zaključak:** zadržavamo sva četiri IRF3205 kao **prekidače**, ne kao linearno opterećenje.

## Četiri kanala
- Svaki kanal: **10 Ω / barem 5 W** vanjski otpornik u seriji s pripadnim IRF3205; svaki se nezavisno uključuje. Preferirati otpornike u metalnom kućištu pričvršćene na pogodno hlađenje.
- 4,2 V: 0,42 / 0,84 / 1,26 / 1,68 A za 1–4 kanala; 3,0 V: 0,30 / 0,60 / 0,90 / 1,20 A. Stvarna struja ovisi o ćeliji, žicama, INA219 shuntu i MOSFET-u.
- Sva četiri otpornika u paralelnim **granama**, ali svaki ima zaseban serijski MOSFET; INA219 shunt zajednički na ulazu.
- Struja jednog 10 Ω pri 4,2 V ≈ 0,42 A i gubitak ≈ 1,76 W; svi zajedno ≈ 7,06 W u otpornicima.
- INA219 breakout standardni shunt i kalibraciju treba potvrditi prije 1,68 A.

## Gate drive — ključni uvjet
Infineon za IRF3205 specificira RDS(on) do 8 mΩ pri **VGS=10 V**; VGS(th)=2–4 V definiran je samo pri 250 µA, pa **direktni ESP32 3,3 V nije zajamčen kao uključenje**. Izvor: https://www.infineon.com/assets/row/public/documents/24/49/infineon-irf3205-datasheet-en.pdf

Predložena upravljačka izvedba: **2 × Microchip TC4427 (dvokanalni neinvertirajući gate driver)** na reguliranih 10 V, s četiri odvojena 3,3 V GPIO ulaza ESP32. TC4427 prihvaća VIH ≥2,4 V i radi s VDD 4,5–18 V. Izvor: https://ww1.microchip.com/downloads/en/DeviceDoc/20001422G.pdf
- Gate zasebno preko otpornika za gate (npr. 47–100 Ω) i zasebnog otpornika G-S 47–100 kΩ za reset-off. Gate driver mora imati zajedničku referentnu GND s MOSFET source čvorom; izlaz mora ostati LOW na reset i pri gubitku ESP32, što treba projektirati i testirati.
- 10 V je potrebno osigurati reguliranim zasebnim izvorom/pretvaračem, **ne izravno iz baterije od 3–4,2 V**. TC4427 bez 10 V ne čini IRF3205 zajamčeno uključenim.

## Važno: zajednički aluminijski hladnjak
IRF3205 TO-220 metalna stražnja pločica/tab uobičajeno je električki spojena na **drain**. U četiri zasebne grane drainovi mogu biti različiti čvorovi. **Bez individualne izolacije podloškama i izolacijskim provodnicama vijaka, zajednički hladnjak ih može kratko spojiti.** Fotografija ne potvrđuje izolaciju. Prije bilo kakve montaže/probe provjeriti ohmmetrom vodljivost svaki drain–hladnjak, međusobno drain–drain, bez napajanja.

## Zaštita i blokade
- Osigurač, zaštita od obrnutog polariteta, neovisno isključivanje pri preniskom naponu/temperaturi, zabrana simultanog punjenja i pražnjenja.
- INA219 mjeri ukupnu struju zajedničkom visokostranom granom, ali stavljanje modula u strujni krug ovisi o stvarnom pinoutu, shuntu i dopuštenoj struji.
- TP4056 B− i OUT− NE premostiti, prije spajanja potvrditi stvarnu zaštitu modula i njezin prag opterećenja.
- R42 PCB / R60 as-built shema nisu prikladni za 4 kanala. Projektirati **novu** funkcionalnu shemu sa četiri MOSFET-a i dva TC4427, pa ERC i PCB DRC.
- Ovo je projektni nacrt, ne odobrenje za priključenje 18650 niti za proizvodnju PCB-a.
