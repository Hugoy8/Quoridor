import nmap
import socket

class ScanNetwork:
    def __init__(self, firstPort : int, endPort : int) -> None:
        self.listIp = []
        self.firstPort = firstPort
        self.endPort = endPort
        
    def scan(self) -> None:
        # Récupération de l'ip local et création de la plage d'ip à scanner.
        adresse_ip_locale = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][0]
        self.firstIp = '.'.join(adresse_ip_locale.split('.')[:3])
        self.firstIp += '.1'
        self.endIp = self.firstIp[:-1] + '255'

        # Plage de port à scanner
        plaguePort = str(self.firstPort) + "-" + str(self.endPort)

        # Scan du réseau en mode furtif
        print("Scan du réseau en cours ...")
        scan = nmap.PortScanner()
        scan.scan(hosts=f"{self.firstIp}-255", arguments="-sS -n -T4 -PN -p " + str(plaguePort))

        # Récupération des adresses IP des serveurs actifs
        print("Traitement des données ...")
        
        for host in scan.all_hosts():
            if scan[host].state() == "up":
                for proto in scan[host].all_protocols():
                    lport = scan[host][proto].keys()
                    for port in lport:
                        if port >= self.firstPort and port <= self.endPort:
                            port_info = scan[host][proto][port]
                            if port_info['state'] == 'open':
                                self.listIp.append(str(host) + ":" + str(port))
        
    def getIp(self) -> list:
        return self.listIp
