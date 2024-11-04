import requests

def send_message(message, server_ip, port):
    url = f'http://{server_ip}:{port}/message'  # Wstaw URL serwera
    data = {'message': message}  # Wiadomość jako dane JSON
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Wiadomość została pomyślnie wysłana!")
    else:
        print("Błąd podczas wysyłania wiadomości:", response.status_code)
