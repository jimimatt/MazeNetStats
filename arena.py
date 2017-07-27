#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
author: Matthias Telöken

Automatisches erzeugen von Test-Log-Dateien von mazeNet-Spielen

!!! Achtung !!!
Erzeugte Daten liegen im gleichen Ordner wie das Skript
und werden bei wiederholter Ausführung des Skripts überschrieben!
"""

import subprocess
import sys


def circus(number_of_players, end, begin=0):
	"""
	player1-4 sind hardgecodet -> hier müssen vorerst manuell die jars
	mit entsprechenden Parametern aufgerufen werden.
	
	TODO Spieler-jars variabel aufrufbar (aus einem Pool)
	"""
    for i in range(begin, end):
        arena = subprocess.Popen(["java", "-jar", "maze-server-v2017.2-jar-with-dependencies.jar",
                                  "-t", str(number_of_players), str(i),
                                  "test_{}_seed{}.txt".format(number_of_players, i)],
                                 shell=True, universal_newlines=True)

        player1 = subprocess.Popen(["java", "-jar", "aMAZEing.jar", "localhost", "5123"])
        if number_of_players > 1:
            player2 = subprocess.Popen(["java", "-jar", "jelicado.jar"])
            if number_of_players > 2:
                player3 = subprocess.Popen(["java", "-jar", "AI Tobias.jar"])
                if number_of_players > 3:
                    player4 = subprocess.Popen(["java", "-jar", "AI Marvin.jar"])
        arena.wait()


if __name__ == "__main__":
    """
    mögliche Kommandozeilen-Parameter:
     - Anzahl der Spieler
     - Ende der For-Schleife (seed)
     - Beginn der For-Schleife
    """
    number_of_players = 3
    begin = 0
    end = 200
    if len(sys.argv) == 2:
        number_of_players = int(sys.argv[1])
    if len(sys.argv) == 3:
        number_of_players = int(sys.argv[1])
        end = int(sys.argv[2])
    if len(sys.argv) == 4:
        number_of_players = int(sys.argv[1])
        end = int(sys.argv[2])
        begin = int(sys.argv[3])
    print("Mögen die Spiele beginnen...")
    circus(number_of_players, end, begin)
    print("Fin.")
