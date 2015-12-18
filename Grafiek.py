import csv
import numpy as np
import matplotlib.pyplot as plt
from lxml import etree

#Objecten
tree = etree.parse('c:\scripts\onderwerpen.xml')
xml_uptime_locatie = tree.xpath('/locaties/powershell_scripts/Get_Uptime/locatie[1]/text()')[0]
xml_ftplog_locatie = tree.xpath('/locaties/logs/ftp/locatie[1]/text()')[0]
xml_weblog_locatie = tree.xpath('/locaties/logs/web/locatie[1]/text()')[0]
xml_csv_locatie = tree.xpath('/locaties/csv/locatie[1]/text()')[0]
xml_ftplog_cachelocatie = tree.xpath('/locaties/logs/ftp/cache_locatie[1]/text()')[0]
xml_weblog_cachelocatie = tree.xpath('/locaties/logs/web/cache_locatie[1]/text()')[0]

csv_lezen = open(xml_csv_locatie, ('r'))
csv_uitlezen = csv_lezen.readlines()

#normale transacties uitlezen
lijst_web = []
for transactie_data in csv_uitlezen:
    lijst_web.append(transactie_data.split(';')[6])
del(lijst_web)[0]
lijst_web = [int(i) for i in lijst_web]
print (lijst_web)
csv_lezen.close()

#minimale transacties uitlezen
lijst_web_min = []
for transactie_data in csv_uitlezen:
    lijst_web_min.append(transactie_data.split(';')[7])
del(lijst_web_min)[0]
lijst_web_min = [int(i) for i in lijst_web_min]
print (lijst_web_min)

#maximale transacties uitlezen
lijst_web_max = []
for transactie_data in csv_uitlezen:
    lijst_web_max.append(transactie_data.split(';')[8])
del(lijst_web_max)[0]
lijst_web_max = [int(i) for i in lijst_web_max]
print (lijst_web_max)

#maximale transacties uitlezen
lijst_web_gem = []
for transactie_data in csv_uitlezen:
    lijst_web_gem.append(transactie_data.split(';')[9])
del(lijst_web_gem)[0]
lijst_web_gem = [int(i) for i in lijst_web_gem]
print (lijst_web_gem)

#uitgevoerde tijd
uitgevoerd_tijd = []
for transactie_data in csv_uitlezen:
    uitgevoerd_tijd.append(transactie_data.split(';')[0])
del(uitgevoerd_tijd)[0]
print (uitgevoerd_tijd)

aantal_tijden = (len(uitgevoerd_tijd))
lijst = []
nummer = -1
for i in range (aantal_tijden):
    nummer +=1
    lijst.extend([nummer])
delen = max(lijst_web_max) / nummer
print(delen)
yaxis_lijst = []
nummer_y = 1
for i in range (nummer):
    nummer_y += 1
    max_nummer = delen * nummer_y
    yaxis_lijst.extend([max_nummer])
print(lijst)
print(yaxis_lijst)

x = np.array(lijst)
y = np.array(yaxis_lijst)
my_xticks = uitgevoerd_tijd
plt.xticks(x, my_xticks)
plt.plot(lijst_web, label ='Aantal Transacties')
plt.plot(lijst_web_min, label ='Minimale transacties')
plt.plot(lijst_web_max, label ='Maximale transacties')
plt.plot(lijst_web_gem, label ='Gemiddelde transacties')
plt.show()






##plt.grid(True)
##plt.title('Transacties (min, max, gem)')
##plt.ylabel('Aantal transacties')

##plt.bar(lijst, lijst_web, align='center')
##plt.bar(lijst, lijst_web_min, align='center')
##plt.bar(lijst, lijst_web_max, align='center')
##plt.bar(lijst, lijst_web_gem, align='center')
##plt.xticks(lijst, uitgevoerd_tijd)
####plt.axis([1200, 1500, 0, 9000])
##plt.legend(loc='upper left')
##
##
##plt.show()