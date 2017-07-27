# MazeNetStats
Statistische Auswertungsskripte für das Rechnernetze Projekt MazeNet

## How-To
Mit dem Skript __arena.py__ können per Schleife automatisch Spiele gespielt werden. 
Eine modifizierte maze-server.jar erzeugt dabei Log-Dateien, die dann mit dem Skript
__Evaluation.py__ ausgewertet werden können.

1. Die antretenden Spieler müssen in der _arena.py_ noch hardgecodet werden (steht auf der TODO).
2. Schleifenvariable ist gleichzeitig der Boardseed (Testboard = true, hardgecodet im Server)
3. Log-Dateien werden in das selbe Verzeichnis geschrieben in dem auch die Server-Jar ist.
4. neues/leeres Verzeichnis erstellen, die Log-Dateien reinkopieren
5. _Evaluation.py_ mit dem Verzeichnis als Parameter starten (wertet alle Dateien im Verzeichnis aus,
 wenn nicht-Log-Dateien dabei sind gibt's 'n Fehler -> TODO)
6. Die erzeugten Grafiken geniessen...   oder auch nicht.  hehe

### bekannte Probleme
* Log-Dateien von Spielen die nicht durchgelaufen sind, bereiten Probleme in den Auswertungsskripten
* Falls ein Computerspieler ein Labyrinth nicht löst, wird das vom Server nicht erkannt (endlos-Schleife) 
-> muss im Spieler implementiert sein (Züge zählen + Begrenzung)
* Server-Port ist hardgecodet, d. h. es kann nur ein Spiel laufen (keine Parallelisierung) 
-> mögl. Lsg.: Port beim Serverstart per Kommandozeile übergeben (mögliche Parallelisierung - yeepiee!)


### TODO
* Spieler nicht mehr hardgecodet
* nicht durchgelaufene Spiele erkennen, nicht auswerten und in die Logfile (Log-File der Log-Files!) schreiben
* Benennungsschema für Logfiles angeben und nur diese Auswerten
* nicht Log-Files, bzw. kaputte Log-Files erkennen und entsprechend vermerken
* Server-Port per Kommandozeile
