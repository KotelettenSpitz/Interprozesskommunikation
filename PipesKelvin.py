import os
import time
import random


# Pfade_Pipes
conv_zu_log_pipe = "/tmp/conv_zu_log_pipe"
conv_zu_stat_pipe = "/tmp/conv_zu_stat_pipe"
stat_zu_report_pipe = "/tmp/stat_zu_report_pipe"

# Conv: Generiert zufällige Messwerte und schickt 
def conv_process():
    os.mkfifo(conv_zu_log_pipe)
    os.mkfifo(conv_zu_stat_pipe)
    with open(conv_zu_log_pipe, 'w') as conv_zu_log, open(conv_zu_stat_pipe, 'w') as conv_zu_stat:
        try:
            while True:
                value = random.randint(0, 1000)  
                if value is not None:  
                    conv_zu_log.write(f"{value}\n")
                    conv_zu_log.flush()
                    conv_zu_stat.write(f"{value}\n")
                    conv_zu_stat.flush()
                time.sleep(1)  # 0,5 Sekunden warten, bevor der nächste Wert generiert wird
        except KeyboardInterrupt:
            os.remove(conv_zu_log_pipe)
            os.remove(conv_zu_stat_pipe)

# Log: Empfängt Messwerte/schreibt sie in Datei
def log_process():
    with open("/tmp/werte.log", 'a') as log_datei, open(conv_zu_log_pipe, 'r') as log_recv:
        try:
            while True:
                value = log_recv.readline().strip()
                if value:
                    log_datei.write(f"{value}\n")
                    log_datei.flush()
                time.sleep(1)
        except KeyboardInterrupt:
            pass 

# Stat: Empfängt Messwerte, berechnet Statistiken und sendet diese 
def stat_process():
    os.mkfifo(stat_zu_report_pipe)
    values = []
    with open(conv_zu_stat_pipe, 'r') as stat_recv, open(stat_zu_report_pipe, 'w') as stat_to_report:
        try:
            while True:
                value = stat_recv.readline().strip()
                if value:
                    values.append(int(value))
                    mean = sum(values) / len(values)
                    total_sum = sum(values)
                    stats = {'mean': round(mean, 2), 'sum': total_sum}
                    stat_to_report.write(f"{stats['mean']} {stats['sum']}\n")
                    stat_to_report.flush()
                time.sleep(1)  
        except KeyboardInterrupt:
            os.remove(stat_zu_report_pipe)

# Report: Empfängt Statistiken und gibt sie aus
def report_process():
    with open(stat_zu_report_pipe, 'r') as report_recv:
        try:
            while True:
                stats = report_recv.readline().strip().split()
                if stats:
                    mean, total_sum = float(stats[0]), int(stats[1])
                    print(f"Mittelwert: {mean:.2f}, Summe: {total_sum:.2f}")
                time.sleep(1) 
        except KeyboardInterrupt:
            pass