# Fotografska referenca stvarnog testera — donja strana (15.10.2026.)

Korisnik je 15.10.2026. u razgovoru ChatGPT dostavio fotografiju **donje, lemljene strane** iste funkcionalne univerzalne perforirane pločice. Fotografija je dostupna u razgovoru, ali nije kopirana kao binarna datoteka u GitHub. Upariti s [fotografijom gornje strane](PHOTO_TOP_REFERENCE_2026-10-15.md).

## Što se vidi na fotografiji

- Pravokutna zelena univerzalna pločica s pravilnom mrežom izoliranih metaliziranih rupica; gornji i donji rub imaju niz širih kontaktnih površina.
- Uz **lijevi rub fotografije donje strane** više uzastopnih zalemljenih priključaka i bakrenih vodova; ovo je pogled s donje strane i **ne smije se mehanički preklopiti s pogledom odozgo bez vodoravnog zrcaljenja i provjere orijentacije**.
- **Četiri ili više zelenih izoliranih vodiča** spajaju udaljene točke središnjeg/lijevog područja, uključujući više presijecanja; presijecanje izoliranih žica nije dokaz električnog spoja.
- Više **golih bakrenih mostova**: duga vodoravna trasa uz gornji rub, kraći mostovi pri sredini i dulji vodič uz desnu polovicu koji se spušta do donjeg područja.
- **Jedan smeđi izolirani vodič** uz lijevi rub.
- Veći broj lemnih spojeva i nekoliko kratkih vertikalnih žičanih mostova u sredini.
- Fotografija nema oznake električnih mreža niti je dovoljno pouzdana da se svaka žica bez dodatne provjere pridruži određenom pinu modula.

## Smjernice za Codex/KiCad

1. Kao mehanički predložak koristiti obje stvarne fotografije. Pri usporedbi gornje i donje strane napraviti **horizontalno zrcaljenje** jednog pogleda i poravnati rubove/rupice, uz dodatnu provjeru orijentacije po rasporedu komponenti.
2. Prikazati stvarnu univerzalnu pločicu kao **rekonstrukciju rasporeda**, s NodeMCU lijevo, INA219 dolje lijevo, relejem gore u sredini, dva otpornika 22 Ω jedan ispod drugoga i držačem 18650 desno — položaji se odnose na pogled odozgo.
3. Dokumentirati vidljive izolirane žice i gole bakrene mostove kao fizičke trase; **ne zaključivati** da križanje vodiča predstavlja spoj bez vidljivog zajedničkog lema.
4. Mreže koje su funkcionalno potvrđene iz R2 mogu se koristiti za kontrolu konzistentnosti, ali **ne za automatsko pripisivanje svake nejasne fizičke veze**. Osobito baza/emiter tranzistora, djelitelj, napajanja i polaritet INA219 ostaju za provjeru.
5. Ne generirati proizvodne Gerbere niti tvrditi da je DRC čist ili PCB električki dovršen na temelju ovih fotografija.
6. Za stvarni 3D prikaz i vjerodostojan PCB raspored potrebni su footprintovi odgovarajućih konkretnih modula i držača; točnost njihove geometrije posebno označiti.

**Status:** obje strane stvarnog funkcionalnog sklopa sada su fotografirane. Fotografije daju osnovu za rekonstrukciju fizičkog rasporeda, ali ne predstavljaju potvrđenu električnu netlistu niti dopuštenje za proizvodnju PCB-a.
