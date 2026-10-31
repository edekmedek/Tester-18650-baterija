# R34 — provjera topologije prije spajanja baterije

## Potvrđeno
- R33: korisnički KiCad DRC 0 violations, 0 unconnected pads, 0 footprint errors.
- INA219 kabelsko sučelje J4: 1=3V3, 2=GND, 3=SDA, 4=SCL; to je naš odabrani raspored, ne fizički pinout modula.
- J3 ESP32 kabelsko sučelje: 1=PWM, 2=3V3, 3=GND, 4=SDA, 5=SCL.
- Preostali nedodijeljeni pinovi: J1.1, J1.2, J2.1..J2.6, J3.6..J3.8, Q1.2 = 12, ne 14.

## Kritične projektne činjenice
- Q1 IRF3205 je N-MOSFET, drain Q1.2 je nedodijeljen.
- U1 MCP6002 radi na 3.3 V; izlazno upravljanje gateom IRF3205 i DC SOA nisu potvrđeni.
- RSH1 0.5 ohm je niskostrani mjerni otpornik regulacije; INA219 ima vlastiti mjerni otpornik i treba ga staviti u točno definiranu serijsku granu.
- TP4056 USB-C modul s B+/B-/OUT+/OUT- nije fizički jednak J2 1x06; J2 može biti samo ožičeni adapter, s eksplicitnim označavanjem.
- Punjenje i pražnjenje preko modula zahtijevaju potvrdu zaštite i izolacije puta opterećenja. Ne pretpostavljati da OUT+/- i B+/- imaju očekivano ponašanje.
- Za test kapaciteta treba pouzdano očitanje napona baterije i uvjet prekida, zaštita od previsoke temperature i neovisno isključivanje opterećenja pri kvaru ESP32.

## Blokade
1. Potvrditi fizičke oznake i raspored INA219 modula te ESP32 GPIO koji nije zauzet OLED-om.
2. Potvrditi tip i zaštitnu izvedbu TP4056 modula i priključke baterije.
3. Odabrati MOSFET prikladan za DC linearni režim ili promijeniti topologiju na prekidačko opterećenje.
4. Izraditi izvornu shemu i pokrenuti ERC; postojeći PCB bez sheme i s nedodijeljenim pinovima nije proizvodno spreman.

## Sigurnost
Ne spajati 18650, ne naručivati PCB i ne pokretati punjenje/pražnjenje dok se gore navedeno ne riješi.
