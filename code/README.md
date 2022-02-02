# Code
## Algorithms
![schematische weergave](https://github.com/JappieeeT/Chiptuners/blob/main/doc/Schermafbeelding%202022-02-02%20om%2009.50.06.png)
Zoals op de schematische weergave te zien is, hebben wij gekozen voor een bepaalde structuur in het oplossen van de case. Wij hebben namelijk gevonden dat het sorteren van de paden binnen een netlist uitmaakt en sommige sorteermethodes lagere kosten brengen dan anderen, daarom doen wij dit vóór elk algoritme. Daarnaast hebben wij gekozen om eerst met een sterk "basisalgoritme" (a*) oplossingen te vinden die vervolgens verbeterd kunnen worden door een iteratief algoritme (hillclimber). Onze voorkeur gaat niet uit naar het simulated annealing algoritme, aangezien deze slechtere oplossingen vind dan de hillclimber. Toch hebben we hem erbij gezet.

## Classes

Wij hebben drie soorten klassen gebruikt om de objecten binnen onze chip te representeren: de gates die verbonden moeten worden, de "net" ofwel het stuk pad wat gates verbind en de grid zelf waarbinnen alles plaatsvind (deze bevat dus ook de gehele netlist). 

## Visualize

Voor de visualisatie voor de paden in de chip hebben wij ten eerste een 3D plot met matplotlib gemaakt. Hier is het mogelijk om de legenda aan of uit te zetten. Echter werkte deze visualisatie niet bij alle besturingsystemen optimaal. Daarom hebben wij ook eenzelfde 3D plot gemaakt in plotly. Deze visualisatie wordt automatisch geopend in je browser. Ook is het mogelijk om door dubbel te klikken op paden in de legenda, te selecteren wat je wel of niet wilt zien.