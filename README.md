# Chiptuners

Jasper Timmer, Rick Cornelisse, Ariella Hiele

## Case: Chips and Circuits

### Introductie
Onze case gaat over het werkend krijgen van een chip, door onderdelen van deze chip (gates) op de juiste manier met elkaar te verbinden. Het uiteindelijke doel van onze case is om dit zo goedkoop mogelijk te doen. De chip in kwestie is drie-dimensionaal en bevat 8 lagen. Wij hebben aangenomen dat alle gates op de onderste laag liggen. De juiste volgorde waarin gates met elkaar verbonden moeten worden, wordt een netlist genoemd. Enkele voorbeelden hiervan zijn te vinden in de map "data". Het rooster waarbinnen draad wordt aangelegd, wordt vanaf nu de "grid" genoemd.

De case kent ook enkele constraints; zo mogen stukken draad niet over hetzelfde segment binnen de grid lopen (een "collisie"). Ze mogen elkaar wel kruisen (een "intersectie"), dit kost alleen wel meer geld, zoals in de onderstaande kostenformule te zien is.

De kostenfunctie: TK = aantal segmenten + 300 * aantal intersecties

> Ook hebben wij de grootte van de state-space van onze case als volgt berekent:
>
> 2^ N
>
> N = l * [m(n - 1) + n(m - 1)] + mn(l − 1)
>
> N =  totale aantal segmenten
>
> l = aantal lagen
>
> m = breedte grid
>
> n = lengte grid


<!-- ![visualisatie voorbeeld](https://github.com/JappieeeT/Chiptuners/blob/main/photos/vis.png) -->
<p float="center">
  <img align="center" src="/doc/Example_Solved_grid.png" width="512"/>
</p>


### Usage
```bash
python3 main.py netlistnummer (-h) (-c naam algoritme) (-i naam algoritme) (-vis) (-leg) (-plotly) (-iter N) (-n N) (-m N verbeteringen) (-file bestandsnaam) (-pop indexnummer) (-gs lagen) (-random netlistnummer)
```
In de commandline is het mogelijk om verschillende functies aan te roepen:

| functies               | beschrijving                                                        |
| :--------------------- | :------------------------------------------------------------------ |
| `-h` of `--help`       | Laat informatie zien over de positionele en optionele argumenten.   |
| `-c`                   | Kiest algoritme om te gebruiken, opties: baseline, a_star.          |
| `-i`                   | Kiest iteratief algoritme, keuze uit: hillclimber of simulated_annealing.                           |
| `-sort_c`              | Kiest sorteermethode voor basis algoritme, keuze uit: random, length_a, length_d, middle, outside, gate_a, gate_d, intersections_a, intersections_d. Wanneer er geen methode is gekozen wordt automatisch lengte oplopend gekozen. Wanneer er geen volgorde is gekozen, wordt er automatisch gekozen voor oplopend. |
| `-sort_i`              | Kiest sorteermethode voor iteratief algoritme, keuze uit bovenstaande. Wanneer er geen methode is gekozen wordt automatisch lengte oplopend gekozen. Wanneer er geen volgorde is gekozen, wordt er automatisch gekozen voor oplopend. |
| `-vis` of `--visualize`| Plot een 3D visualizatie van een oplossing in matplotlib.                         |
| `-leg`of `--legend`    | Geeft een legenda bij de 3D visualisatie van matplotlib.                           |
| `-plotly`              | Genereert een 3D visualizatie in plotly, die opent in je browser.             |
| `-iter`                | Hoeveel iteraties zijn er nodig bij het iteratief algoritme? Wanneer deze niet wordt ingevuld staat hij automatisch op 1000. |
| `-n`                   | Hoeveel oplossingen moeten er worden gegenereerd?                   |
| `-m`                   | Hoeveel verbeterde oplossingen moeten er zijn voor elke oplossing?  |
| `-file`                | Wanneer een al bestaand bestand gebruikt moet worden, voorbeeld: wanneer de bestandsnaam "paths_netlist_4_C_19655" is, gebruik dan "C_19655". |
|  `-pop`                | Geef aan welk item verwijdert wordt in het a* algoritme, wanneer er meerdere staten dezelfde prioriteit hebben. Wanneer niks ingevuld wordt kiest hij 1|
|  `-gs`                 | Minimale hoogte boven een gate die vrij moet blijven van paden, zodat de gate niet onnodig geblokkeerd wordt. Wanneer niks ingevuld wordt is dit 2. |
|  `-random`, `--randomized`| Maakt random netlists aan in plaats van de al bestaande. Hij gebruikt hiervoor de al bestaande coordinaten van de netlisten uit de data map. Daarvoor is het wel nodig om een al bestaande netlist op te geven.|


### Structuur
- data/ - 

- doc/ -

- results/

    - figures_and_plots/
    - results_a_star/
    - results_annealing/
    - results_baseline/
    - results_hillclimber/

- code/ -

    - algorithms/ -
    - classes/ - 
    - visualize.py

### Requirements
Om het programma werkend te laten draaien, zullen enkele dingen geïnstalleerd moeten zijn. Deze kun je automatisch installeren door: 

```bash
pip3 install -r requirements.txt
```
