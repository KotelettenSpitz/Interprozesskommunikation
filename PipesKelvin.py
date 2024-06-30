import os
import time
import random


# Pfade_Pipes
conv_zu_log_pipe = "/tmp/conv_zu_log_pipe"
conv_zu_stat_pipe = "/tmp/conv_zu_stat_pipe"
stat_zu_report_pipe = "/tmp/stat_zu_report_pipe"

# Conv: Generiert zufällige Messwerte und schickt 
def conv_process():
    os.mkfifo(conv_zu_log_pipe) #Pipes erstellen
    os.mkfifo(conv_zu_stat_pipe)
    with open(conv_zu_log_pipe, 'w') as conv_zu_log, open(conv_zu_stat_pipe, 'w') as conv_zu_stat: #Pipes öffnen
        try:
            while True: #Schleife um Prozess endlos laufen zu lassen
                value = random.randint(0, 1000)  #Zufallswert erzeugen
                if value is not None:  #Wenn Datenwert erstellt
                    conv_zu_log.write(f"{value}\n") #In Pipes schreiben und sofortiges schreiben erzwingen
                    conv_zu_log.flush()
                    conv_zu_stat.write(f"{value}\n")
                    conv_zu_stat.flush()
                time.sleep(1)  # 1 Sekunden warten, bevor der nächste Wert generiert wird
        finally:
            os.remove(conv_zu_log_pipe) #Bei Prozessende Pipes löschen
            os.remove(conv_zu_stat_pipe)

# Log: Empfängt Messwerte/schreibt sie in Datei
def log_process():
    with open("log.txt", 'a') as log_datei, open(conv_zu_log_pipe, 'r') as log_recv: #Log Datei und Pipe öffnen
        try:
            while True:
                value = log_recv.readline().strip() #Zeilenweise auslesen
                if value: #Wenn Wert
                    log_datei.write(f"{value}\n") #In Pipe schreiben
                    log_datei.flush() #sofortiges schreiben erzwingen
                time.sleep(1)
        finally:
            pass 

# Stat: Empfängt Messwerte, berechnet Statistiken und sendet diese 
def stat_process():
    os.mkfifo(stat_zu_report_pipe) #Pipe erstellen
    values = []
    with open(conv_zu_stat_pipe, 'r') as stat_recv, open(stat_zu_report_pipe, 'w') as stat_to_report: #Pipes öffnen
        try:
            while True: #Schleife um Prozess endlos laufen zu lassen
                value = stat_recv.readline().strip() #Zeilenweise auslesen
                if value:
                    values.append(int(value)) #Datenwert in Array eingeben
                    mean = sum(values) / len(values) #Summe und Mittelwert berechnen
                    total_sum = sum(values)
                    stats = {'mean': round(mean, 2), 'sum': total_sum} #Als stats abspeichern
                    stat_to_report.write(f"{stats['mean']} {stats['sum']}\n") #Statistik in Pipe schreiben
                    stat_to_report.flush() #sofortiges schreiben erzwingen
                time.sleep(1)  
        finally:
            os.remove(stat_zu_report_pipe) #Bei Prozessende Pipe löschen

# Report: Empfängt Statistiken und gibt sie aus
def report_process():

    with open(stat_zu_report_pipe, 'r') as report_recv: #Pipe öffnen
        try:
            while True: #Schleife um Prozess endlos laufen zu lassen
                stats = report_recv.readline().strip().split() #Zeilenweise auslesen
                if stats: #Wenn Datenwert
                    mean, total_sum = float(stats[0]), int(stats[1]) #Daten auslesen
                    print(f"| {time.strftime('%H:%M:%S')} | {total_sum} | {mean} |") #Daten ausgeben
                time.sleep(1) 
        finally:
            pass