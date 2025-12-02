import socket  # Importiert das socket-Modul. Damit können wir TCP/UDP-Verbindungen erstellen.
import sys     # Importiert das sys-Modul. sys.exit() ermöglicht sauberes Beenden des Programms.

# ------------------------------------------------------------
# FUNKTION: scan_port()
# Aufgabe:
#   - prüft ob ein bestimmter Port an einer Ziel-IP offen ist
#   - wenn offen: versucht „Banner Grabbing“ (Service-Informationen lesen)
# ------------------------------------------------------------
def scan_port(target_ip, port):    # target_ip = String ("8.8.8.8"), port = Integer (80)
    # Ein Socket ist wie ein virtueller Telefonhörer für das Netzwerk.
    # AF_INET  = IPv4
    # SOCK_STREAM = TCP (verbindungsorientiert)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Erstellt ein TCP-Socket

    s.settimeout(0.5)  # Setzt maximale Wartezeit auf 0.5 Sekunden. Verhindert „Hängenbleiben“.

    try:
        # connect_ex() versucht eine Verbindung aufzubauen.
        # Vorteil: gibt Statuscode zurück statt Fehler zu werfen.
        # Rückgabewert:
        #   0  → Verbindung erfolgreich → Port offen
        #   >0 → Fehlercode → Port geschlossen oder gefiltert
        result = s.connect_ex((target_ip, port))  # Übergabe eines Tupels: (IP, Port)

        if result == 0:  # 0 bedeutet: Port ist offen
            print(f"[+] Port {port} ist offen")  # Ausgabe für Anwender

            # ------------------------------------------------------
            # Banner Grabbing:
            # Viele Netzwerkdienste wie FTP/SMTP/SSH/Webserver senden
            # direkt nach Verbindung oder nach minimalem Input
            # ein sogenanntes „Banner“:
            # → Versionsnummer
            # → Servertyp
            # → Produktname (z. B. OpenSSH_8.2, Apache/2.4)
            # ------------------------------------------------------
            try:
                # Manche Server senden erst ein Banner, wenn man etwas schickt.
                # Deshalb senden wir eine harmlose Anfrage:
                s.sendall(b"HELLO\r\n")  # sendall() sendet garantiert ALLE Bytes

                # recv(1024) liest max. 1024 Bytes Antwort.
                # Kein Limit = unkontrollierte Daten = Gefahr für Speicher.
                banner = s.recv(1024)

                # banner ist in Bytes – wir müssen es in Text (String) umwandeln.
                # decode(errors="ignore") ignoriert kaputte Zeichen.
                print(f"    Banner: {banner.decode(errors='ignore').strip()}")

            except Exception:  # Falls ein Server NICHT antwortet → Fehler abfangen
                print("    Banner konnte nicht abgefragt werden.")

        # Wenn Port geschlossen ist → keine Ausgabe. Scanner bleibt leise.

    except Exception as e:
        # Falls es beim Verbindungsversuch zu technischen Fehlern kommt.
        print(f"Fehler bei Port {port}: {e}")

    finally:
        # Egal ob Erfolg oder Fehler → Socket schließen.
        # Wichtig für Ressourcenmanagement.
        s.close()


# ------------------------------------------------------------
# FUNKTION: main()
# Aufgabe:
#   - Benutzer nach Ziel fragen
#   - DNS-Auflösung
#   - Ports definieren
#   - jeden Port scannen
# ------------------------------------------------------------
def main():
    target = input("Ziel-IP oder Domain eingeben: ")  # Fragt Benutzer nach Ziel
                                                      # z. B. "scanme.nmap.org"

    print(f"\nStarte Scan für {target}...\n")
    #Aktiviert Variablen-Interpolation
    # \n am Anfang → Leerzeile vor dem Text (visuelle Trennung)
    # \n am Ende → Leerzeile nach der Ausgabe (Spacing für folgenden Output)

    # DNS-Auflösung: Domain → IP
    # gethostbyname() liefert eine IPv4-Adresse zu einem Domainnamen.
    try:
        target_ip = socket.gethostbyname(target)
    except Exception:
        print("Ungültige Domain oder DNS-Problem.")
        sys.exit()  # bricht das Programm sauber ab

    print(f"Aufgelöste IP: {target_ip}\n")  # Zeigt echte IP

    # Typische Ports für Einsteiger-Training:
    # 21   FTP
    # 22   SSH
    # 23   Telnet
    # 25   SMTP
    # 53   DNS
    # 80   HTTP
    # 110  POP3
    # 143  IMAP
    # 443  HTTPS
    # 3306 MySQL
    # 8080 Web-Server/Proxy
    ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080]

    # Jeder Port wird einzeln geprüft
    for p in ports:
        scan_port(target_ip, p)  # Ruft die Scan-Funktion für jeden Port auf


# ------------------------------------------------------------
# STARTPUNKT DES PROGRAMMS
# Dieser Block wird NUR ausgeführt, wenn die Datei direkt gestartet wird
# (z. B. python scanner.py)
# Nicht beim importieren.
# ------------------------------------------------------------
if __name__ == "__main__":
    main()  # Startet das Programm
# Nie ohne (.ven) starten
