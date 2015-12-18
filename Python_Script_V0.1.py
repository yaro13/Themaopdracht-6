from lxml import etree
import sys,subprocess
import re
import csv
import os.path
from time import gmtime,strftime

#functie om de aantal regels te tellen
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

#Functie om een commando in cmd uit te voeren
def run_command(command):
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')

#Objecten
tree = etree.parse('c:\scripts\onderwerpen.xml')
xml_uptime_locatie = tree.xpath('/locaties/powershell_scripts/Get_Uptime/locatie[1]/text()')[0]
xml_ftplog_locatie = tree.xpath('/locaties/logs/ftp/locatie[1]/text()')[0]
xml_weblog_locatie = tree.xpath('/locaties/logs/web/locatie[1]/text()')[0]
xml_csv_locatie = tree.xpath('/locaties/csv/locatie[1]/text()')[0]
xml_ftplog_cachelocatie = tree.xpath('/locaties/logs/ftp/cache_locatie[1]/text()')[0]
xml_weblog_cachelocatie = tree.xpath('/locaties/logs/web/cache_locatie[1]/text()')[0]

#Aanmaken CSV
b = os.path.isfile(xml_csv_locatie)
a = open(xml_csv_locatie, ('ab'))

write = csv.writer(a,delimiter=';')
if b == False:
    write.writerow(['Uitgevoerde tijd','Uptime','IP Addres(sen)','Machinenaam','Besturingssysteem','Versie','Transacties','Minimale Transacties','Maximale Transacties','Gemiddelde Transacties','Aantal mislukte inlogpogingen (FTP)','Minimale mislukte inlogpogingen (FTP)','Maximale mislukte inlogpogingen (FTP)','Gemiddelde mislukte inlogpogingen (FTP)'])
else:
    pass
a.close()

#tijd van uitvoeren
uitgevoerde_tijd = strftime('%Y-%m-%d %H:%M', gmtime())

# powershell script uitvoeren, hierbij word de uptime berekend
for line in run_command('powershell.exe -ExecutionPolicy Unrestricted '+ xml_uptime_locatie):
    uptime =  line.split('\n')[0]
print(uptime)


# CMD commando Ipconfig, filter op IPv4 Address
ipaddress = ''
for line in run_command('ipconfig'):
    ipconfig = (re.findall(r"\s+(IPv4 Address.*: [\d\.]+)", line))
    if ipconfig == []:
        pass
    else:
        ipaddress += (ipconfig[0].split(': ')[1])+ ', '
ipaddress = ipaddress[:-2]
print(ipaddress)

# CMD commando Systeminfo, filter op Host Name
for line in run_command('systeminfo'):
    host = (re.findall(r"Host Name:\s+.+", line))
    if host == []:
        pass
    else:
        hostname = host[0].split(':                 ')[1]
print(hostname)

# CMD commando Systeminfo, filter op OS
for line in run_command('systeminfo'):
    OS = (re.findall(r"OS Name:\s+.+", line))
    if OS == []:
        pass
    else:
        besturingssyteem = OS[0].split(':                   ')[1]
print(besturingssyteem)

# CMD commando Systeminfo, filter op OS Version
for line in run_command('systeminfo'):
    versie = (re.findall(r"^OS Version:\s+.+", line))
    if versie == []:
        pass
    else:
        build = versie[0].split(':                ')[1]
print(build)

# Tel hoeveel transacties er gedaan zijn op de Apache webserver
aantal_transacties_web = (file_len(xml_weblog_locatie))

try:
    weblog_lezen = open(xml_weblog_cachelocatie, "r+")
    transacties_last = int(weblog_lezen.read())
except:
    weblog_lezen = open(xml_weblog_cachelocatie, "w")
    transacties_last = 0
verschil_webtransactie = aantal_transacties_web - transacties_last
print verschil_webtransactie
weblog_lezen.close()
weblog_schrijven = open(xml_weblog_cachelocatie, "w")
weblog_schrijven.write(str(aantal_transacties_web))
weblog_schrijven.close()

#minimale transacties van de Apache webserver
csv_lezen = open(xml_csv_locatie, ('r'))
csv_uitlezen = csv_lezen.readlines()
lijst_web = [verschil_webtransactie]
for transactie_data in csv_uitlezen:
    lijst_web.append(transactie_data.split(';')[6])
del lijst_web[1]
lijst_web = [int(i) for i in lijst_web]
try:
    min_transacties =  min(lijst_web)
except:
    min_transacties = verschil_webtransactie
print (min_transacties)

#maximale transacties van de Apache webserver
try:
    max_transacties =  max(lijst_web)
except:
    max_transacties = verschil_webtransactie
print(max_transacties)

#Gemiddelde transacties van de Apache webserver
try:
    gem_transacties =  sum(lijst_web) / len(lijst_web)
except:
    gem_transacties = verschil_webtransactie
print(gem_transacties)

# Tel hoeveel mislukte inlogpogingen er gedaan zijn op de ftp server
aantal_mislukte_ftplogin = 0
ftplog = open(xml_ftplog_locatie, 'r')
for line in ftplog:
    ftpoutput = (re.findall(r"530 Login or password incorrect!$", line))
    if ftpoutput == []:
        pass
    else:
        aantal_mislukte_ftplogin += 1
ftplog.close()

try:
    ftplog_lezen = open(xml_ftplog_cachelocatie, "r+")
    misluke_inlog_last = int(ftplog_lezen.read())
except:
    ftplog_lezen = open(xml_ftplog_cachelocatie, "w")
    misluke_inlog_last = 0
verschil_ftplogin = aantal_mislukte_ftplogin - misluke_inlog_last

ftplog_lezen.close()
ftplog_schrijven = open(xml_ftplog_cachelocatie, "w")
ftplog_schrijven.write(str(aantal_mislukte_ftplogin))
ftplog_schrijven.close()

#minimale mislukte inlogpogingen op de ftp server
lijst_ftp = [verschil_ftplogin]
for ftplogin_data in csv_uitlezen:
    lijst_ftp.append(ftplogin_data.split(';')[10])
del lijst_ftp[1]
lijst_ftp = [int(i) for i in lijst_ftp]
csv_lezen.close()
try:
    min_ftp_mislukt =  min(lijst_ftp)
except:
    min_ftp_mislukt = verschil_ftplogin
print (min_ftp_mislukt)

#maximale foute inlogpogingen op de ftp server
try:
    max_ftp_mislukt =  max(lijst_ftp)
except:
    max_ftp_mislukt = verschil_ftplogin
print(max_ftp_mislukt)

#Gemiddelde foute inlogpogingen op de ftop server
try:
    gem_ftp_mislukt =  sum(lijst_ftp) / len(lijst_ftp)
except:
    gem_ftp_mislukt = verschil_webtransactie
print(gem_ftp_mislukt)

#exporteren naar csv
a = open(xml_csv_locatie, ('ab'))
write = csv.writer(a,delimiter=';')
write.writerow([uitgevoerde_tijd, uptime,ipaddress,hostname,besturingssyteem,build,verschil_webtransactie, min_transacties,max_transacties,gem_transacties,verschil_ftplogin,min_ftp_mislukt,max_ftp_mislukt,gem_ftp_mislukt])
a.close()
