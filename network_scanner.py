import socket
import threading

class NetworkScanner:
    def __init__(self):
        self.devices = []
        self.lock = threading.Lock()  # Lock do synchronizacji dostępu do listy urządzeń
        self.running = False

    def is_port_open(self, ip, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.05)  # Zmniejszony timeout
        try:
            result = sock.connect_ex((ip, port))
            return result == 0
        finally:
            sock.close()

    def scan_ip(self, ip):
        ports = [21, 22, 23, 25, 53, 67, 68, 69, 70, 79, 80, 110, 111, 115, 123, 137, 138, 139, 143, 161, 162, 179, 194, 220, 389, 443, 445, 465, 514, 515, 543, 548, 554, 587, 631, 636, 646, 669, 688, 690, 700, 707, 720, 749, 750, 780, 818, 830, 843, 873, 880, 888, 990, 993, 995, 1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1012, 1013, 1014, 1015, 1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023, 1024, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033, 1034, 1035, 1036, 1037, 1038, 1039, 1040, 1041, 1042, 1043, 1044, 1045, 1046, 1047, 1048, 1049, 1050, 1051, 1052, 1053, 1054, 1055, 1056, 1057, 1058, 1059, 1060, 1061, 1062, 1063, 1064, 1065, 1066, 1067, 1068, 1069, 1070, 1071, 1072, 1073, 1074, 1075, 1076, 1077, 1078, 1079]  # Typowe porty dla urządzeń
        for port in ports:
            if self.is_port_open(ip, port):
                with self.lock:  # Użyj locka do synchronizacji
                    self.devices.append({"ip": ip, "port": port})
                    print(f"Znaleziono otwarty port {port} na {ip}")

    def scan_network_for_devices(self):
        self.devices.clear()  # Wyczyść poprzednie wyniki

        # Ustawiam prefix automatycznie
        def get_ip():
            # Biorę adres lokalnego interfejsu przy użyciu socketów
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.settimeout(0)
            try:
                s.connect(('8.8.8.8', 80))  # Łączymy się z dnsem googla żeby mieć ten adres którym komp się łączy z internetem a nie np adres wirtualnej karty sieciowej wirtualboxa albo adres pętli zwrotnej
                ip = s.getsockname()[0]
            except Exception:
                ip = '127.0.0.1'  # Jak się z niczym nie połączy ustawia na pętle zwrotną żeby nie wywaliło błędu i żeby nie zcrashowało programu
            finally:
                s.close()  # Zamyka socket bo nie będzie już nam potrzebny
            return ip

        # Ustawiam sobie zmienną na adres ip
        ip_address = get_ip()

        # Dzielę go na 4 oktety
        octets = ip_address.split(".")

        # Łącze oktety ze sobą ale tu już bez ostatniego
        network_prefix = ".".join(octets[:-1]) + "."

        print("Rozpoczynam skanowanie sieci...")

        self.running = True  # Rozpocznij skanowanie
        threads = []

        for i in range(1, 255):
            if not self.running:
                print("Skanowanie przerwane.")
                break
            ip = f"{network_prefix}{i}"
            thread = threading.Thread(target=self.scan_ip, args=(ip,))
            threads.append(thread)
            thread.start()  # Uruchom skanowanie w nowym wątku

        for thread in threads:
            thread.join()  # Czekaj na zakończenie wszystkich wątków

        print("Skanowanie zakończone.")

# Umożliwienie importu z tego pliku
if __name__ == "__main__":
    scanner = NetworkScanner()
    scanner.scan_network_for_devices()
