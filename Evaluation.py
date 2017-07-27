#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
author: Matthias Telöken

Auswerten von Test-Log-Dateien von mazeNet-Spielen
"""

import os
import sys
from datetime import date, datetime
import matplotlib.pyplot as plt
import numpy as np


class PlayerStats(object):
	"""
	Die Klasse speichert die Statistikdaten eines Spielers.
	
	Mit der eval() Funktion können die ausgewertenten Daten abgerufen werden.
	Der Aufruf ändert die gespeicherten Daten nicht, es kann also theoretisch auch 
	zwischendurch ein Zwischenergebnis abgefragt werden.
	
	Effektivität: 	# gewonnene Spiele / # alle Spiele
	
	Effizienz:		# gefundene Schätze / # Züge
		(ein akademisches Bsp.: pro Zug 1 Schatz gefunden -> 100 %)
		
	"zurückgelassene" Schätze:
		Eine Art Platz 2 Ranking - hier werden nur Spiele gewertet, die nicht gewonnene
		wurden. Daher auch die extra Variable game_count_treasure.
	"""
	
	"""
	Die Dictionary-Konstante enthält die Information wieviele Schätze pro Spieler
	gefunden werden müssen in einem n-Spieler-Spiel.
	Die krummen Werte kommen zustande, da bspw. in einem 3-Spieler-Spiel
	2 Spieler 8 Schätze finden müssen und 1 Spieler 9 Schätze
	-> gewichtetes arithmetischen Mittel: 8.33...
	
	Werte ggf. anpassen!
	"""
    TREASURES_PER_PLAYER = {1: 25., 2: 12.5, 3: 8.33, 4: 7.}

    def __init__(self, name, number_of_players):
        self.name = name
        self.number_of_players = number_of_players
        self.treasures = PlayerStats.TREASURES_PER_PLAYER.get(number_of_players)
        self.game_count = 0
		self.game_count_treasure = 0
        self.efficiency = 0
        self.effectivity = 0
        self.average_left_treasures = 0

    def inc_win(self):
        self.effectivity += 1
		self.game_count_treasure -= 1

    def add_game_data(self, left_treasures, move_count):
        self.average_left_treasures += left_treasures
        self.efficiency += (self.treasures - left_treasures) / move_count
        self.game_count += 1

    def eval(self):
        """

        :return: name, effectivity, efficiency, average left treasures
        """
        return self.name,\
                self.effectivity/self.game_count,\
                self.efficiency/self.game_count,\
                self.average_left_treasures/self.game_count

    def __str__(self):
        return self.name


class Evaluator(object):
	"""
	Die Klasse ist ein Parser für die von dem modifizierten maze-server erstellten Logfiles.
	
	Spieler müssen unterschiedliche Namen! (player ist ein Dictionary!)
	Also wenn Tests mit einem mehrfach vorhandenem Computerspieler gemacht werden,
	muss darauf geachtet werden, dass die Spieler sich mit unterschiedlichen Namen anmelden!
	"""

    def __init__(self, path):
		"""
		
		:param path: Pfad zu den auszuwertenden Dateien
		"""
        if not os.path.isdir(path):
            raise Exception
        self.path = path
        self.basedir = os.getcwd()
        self.logfilename = "{}_{}.txt".format(path, date.today())
        logfile = open(self.logfilename, "w")
        logfile.write("Logfile for {}, Date: {}, Time: {}\n\n".format(path, date.today(), datetime.now().time()))
        logfile.close()
        self.player = {}
        self.eval()

    def eval(self):
        os.chdir(self.path)
        files = os.listdir()
        f0 = open(files[0], "r")
        number_of_players = int(f0.readline()[18:])
        for file in files:
            f = open(file, "r")
            content = f.readlines()
            testboardseed = int(content[1][14:])
            if len(content) > number_of_players + 4:
                log = open(os.path.join("..", self.logfilename), "a")
                log.write("Fehler bei Seed {}\n".format(testboardseed))
                log.close()
                continue
            movecount = int(content[2][11:])
            winner = content[3][7:-1]
            for i in range(4, number_of_players+4):
                name, treasures_to_go = content[i].split('=')
                if name in self.player:
                    stats = self.player.get(name)
                    stats.add_game_data(int(treasures_to_go)-1, movecount)
                else:
                    p = PlayerStats(name, number_of_players)
                    p.add_game_data(int(treasures_to_go)-1, movecount)
                    self.player[name] = p
            self.player.get(winner).inc_win()

    def show_stats(self):
	"""
	grafische Aufbereitung der Statistiken
	
	TODO Anzahl der Spiele, die ausgewerten wurde muss noch mit in die Grafiken!
	"""
        labels = []
        effe = []
        effi = []
        left_treasures = []
        dings = self.player.values()
        for p in dings:
            name, effectivity, efficiency, average_left_treasures = p.eval()
            labels.append(name)
            effe.append(round(effectivity * 100, 1))
            effi.append(round(efficiency * 100, 1))
            left_treasures.append(average_left_treasures)

        maxi = effe.index(max(effe))
        explode = [0 for i in range(len(effe))]
        explode[maxi] += 0.1
        fig1, ax1 = plt.subplots()
        ax1.pie(effe, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')
        ax1.set_title("Effektivität")

        plt.rcdefaults()
        fig2, ax2 = plt.subplots()
        y_pos = np.arange(len(labels))
        ax2.barh(y_pos, effi, align='center',
                color='green', ecolor='black')
        ax2.set_yticks(y_pos)
        ax2.set_yticklabels(labels)
        ax2.invert_yaxis()  # labels read top-to-bottom
        ax2.set_xlabel('Effizienz in %')
        ax2.set_title('Wahrscheinlichkeit pro Zug einen Schatz zu erreichen')

        ind = np.arange(len(labels))  # the x locations for the groups
        width = 0.35  # the width of the bars

        fig, ax = plt.subplots()
        ax.bar(ind, left_treasures, width, color='r')
        ax.set_ylabel('Durschnitt pro Spiel')
        ax.set_title('nicht erreichte Schätze')
        ax.set_xticks(ind + width / 2)
        ax.set_xticklabels(labels)

        plt.show()


if __name__ == "__main__":
    """
    Auszuwertende Daten liegen idealerweise in einem Unterordner zu diesem Skript.
    Name des Unterordners als Kommandozeilenargument übergeben.
    """
    DIR_NAME = 'default'
    if len(sys.argv) == 2:
        DIR_NAME = sys.argv[1]
    print("processing data in directory: " + DIR_NAME)
    dings = Evaluator(DIR_NAME)
    dings.show_stats()
