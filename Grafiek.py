import csv
import numpy as np
import matplotlib.pyplot as plt
from lxml import etree

#Objecten
tree = etree.parse('c:\scripts\onderwerpen.xml')
xml_csv_locatie = tree.xpath('/locaties/csv/locatie[1]/text()')[0]

csv_lezen = open(xml_csv_locatie, ('r'))
csv_uitlezen = csv_lezen.readlines()

#normale transacties uitlezen
lijst_web = []
for transactie_data in csv_uitlezen:
    lijst_web.append(transactie_data.split(';')[6])
del(lijst_web)[0]
lijst_web = [int(i) for i in lijst_web]
print (lijst_web)


#Totaal mislukte ftp login pogingen uitlezen
lijst_ftp = []
for mis_ftp_data in csv_uitlezen:
    lijst_ftp.append(mis_ftp_data.split(';')[10])
del(lijst_ftp)[0]
lijst_ftp = [int(i) for i in lijst_ftp]
print (lijst_ftp)
csv_lezen.close()

#minimale transacties uitlezen
lijst_web_min = []
for transactie_data in csv_uitlezen:
    lijst_web_min.append(transactie_data.split(';')[7])
del(lijst_web_min)[0]
lijst_web_min = [int(i) for i in lijst_web_min]
print (lijst_web_min)

#minimale mislukte ftp pogingen uitlezen
lijst_ftp_min = []
for mis_ftp_data in csv_uitlezen:
    lijst_ftp_min.append(mis_ftp_data.split(';')[11])
del(lijst_ftp_min)[0]
lijst_ftp_min = [int(i) for i in lijst_ftp_min]
print (lijst_ftp_min)

#maximale transacties uitlezen
lijst_web_max = []
for transactie_data in csv_uitlezen:
    lijst_web_max.append(transactie_data.split(';')[8])
del(lijst_web_max)[0]
lijst_web_max = [int(i) for i in lijst_web_max]
print (lijst_web_max)

#maximale mislukte ftp pogingen uitlezen
lijst_ftp_max = []
for mis_ftp_data in csv_uitlezen:
    lijst_ftp_max.append(mis_ftp_data.split(';')[12])
del(lijst_ftp_max)[0]
lijst_ftp_max = [int(i) for i in lijst_ftp_max]
print (lijst_ftp_max)

#Gemiddelde transacties uitlezen
lijst_web_gem = []
for transactie_data in csv_uitlezen:
    lijst_web_gem.append(transactie_data.split(';')[9])
del(lijst_web_gem)[0]
lijst_web_gem = [int(i) for i in lijst_web_gem]
print (lijst_web_gem)

#Gemiddelde mislukte ftp inlog pogingen uitlezen
lijst_ftp_gem = []
for mis_ftp_data in csv_uitlezen:
    lijst_ftp_gem.append(mis_ftp_data.split(';')[13])
del(lijst_ftp_gem)[0]
lijst_ftp_gem = [int(i) for i in lijst_ftp_gem]
print (lijst_ftp_gem)

#uitgevoerde tijd
uitgevoerd_tijd = []
for transactie_data in csv_uitlezen:
    uitgevoerd_tijd.append(transactie_data.split(';')[0])
del(uitgevoerd_tijd)[0]
print (uitgevoerd_tijd)

#Bereking xas-waardes web
aantal_tijden = (len(uitgevoerd_tijd))
tijden_lijst = []
nummer = -1
for i in range (aantal_tijden):
    nummer +=1
    tijden_lijst.extend([nummer])
print(tijden_lijst)


#Gegevens web omzetten naar grafiek
xas = np.array(tijden_lijst)
plt.xticks(xas, uitgevoerd_tijd)
plt.plot(lijst_web, label ='Aantal Transacties')
plt.plot(lijst_web_min, label ='Minimale Transacties')
plt.plot(lijst_web_max, label ='Maximale Transacties')
plt.plot(lijst_web_gem, label ='Gemiddelde Transacties')
plt.legend(loc='upper right')
plt.gcf().set_size_inches(30, 10.5)
plt.savefig('C:\inetpub\wwwroot\Thema6\grafiek_web.png')
plt.show()


#Gegevens FTP omzetten naar grafiek
plt.xticks(xas, uitgevoerd_tijd)
plt.plot(lijst_ftp, label ='Aantal Mislukte FTP Inlogpogingen')
plt.plot(lijst_ftp_min, label ='Minimale Mislukte FTP Inlogpogingen')
plt.plot(lijst_ftp_max, label ='Maximale Mislukte FTP Inlogpogingen')
plt.plot(lijst_ftp_gem, label ='Gemiddelde Mislukte FTP Inlogpogingen')
plt.legend(loc='upper right')
plt.gcf().set_size_inches(30, 10.5)
plt.savefig('C:\inetpub\wwwroot\Thema6\grafiek_ftp.png')



