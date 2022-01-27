# Chiptuners

Jasper Timmer, Rick Cornelisse, Ariella Hiele

## Case: Chips and Circuits

### Introductie
Onze case gaat over een chip waarbinnen onderdelen, gates, met elkaar verbonden moeten met draad om de chip werkend te krijgen.
Het uiteindelijke doel van onze case is om dit zo goedkoop mogelijk te doen. De chip in kwestie is 3D en bevat 7 lagen, wij hebben aangenomen dat alle gates op de onderste laag liggen. De juiste volgorde waarin gates met elkaar verbonden moeten worden wordt een netlist genoemd, enkele voorbeelden hiervan zijn te vinden in de map "data". Het rooster waarbinnen draad wordt aangelegd wordt vanaf nu de "grid" genoemd.

De case kent ook enkele constraints; zo mogen stukken draad niet over hetzelfde segment binnen de grid lopen (een "collisie"). Ze mogen elkaar wel kruisen (een "intersectie"), dit kost alleen wel meer geld, zoals onder in de kostenformule te zien is.

De kostenfunctie: TK = aantal segmenten + 300 * aantal intersecties

![visualisatie voorbeeld]()

### Usage
```bash
python main.py netlistnummer (-h) (-c naam algoritme) (-i naam algoritme) (-vis) (-n N) (-m N verbeteringen) (-file bestandsnaam)
```
In de commandline is het mogelijk om verschillende functies aan te roepen:
- "-h" of "--help" : laat informatie zien over de positionele en optionele argumenten
- "-c" : kiest algoritme om te gebruiken, opties: "baseline", "a-star"
- "-i" : kiest algoritme om eerdere oplossing te verbeteren, opties: "hillclimber", "simulated annealing"
- "-vis" of "--visualize" : plot een 3D visualizatie van een oplossing
- "-n" : hoeveel oplossingen moeten er worden gegenereerd?
- "-m" : hoeveel verbeterde oplossingen moeten er zijn voor elke oplossing?
- "-file" : wanneer een al bestaand bestand gebruikt moet worden, voorbeeld: wanneer de bestandsnaam "paths_netlist_4_C_19655" is, gebruik dan "C_19655"

### Requirements