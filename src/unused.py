# --------------BEMÆRK------------
# KODEN I DENNE FIL BLIVER IKKE LÆNGERE BRUGT, DA DENNE KODE BLOT GENERERER ET BILLEDE AF EN GRAF - OG IKKE EN INTERAKTIV GRAF
# Årsagen til jeg har valgt ikke at slette filen, er blot for at demonstrere, at jeg også kan generere grafer med Matplotlib
# --------------BEMÆRK------------

import os
import csv
import matplotlib.pyplot as plt

url = 'uheld_dk.csv'
filename = os.path.basename(url)

STATISTICS = {}

with open(filename) as f:
    reader = csv.reader(f)
    years = next(reader)
    accidents = next(reader)

    STATISTICS = dict(zip(years, accidents))

    plt.xlabel('År')
    plt.ylabel('Uheld')
    plt.title('Trafikuheld i Danmark')

    years = list(map(int, years))
    accidents = list(map(int, accidents))

    plt.xticks(years)
    plt.plot(years, accidents, color='g')
    plt.show()