import requests
import os
import re
from bs4 import BeautifulSoup
import concurrent.futures
import httpx
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.dummy import Pool as ThreadPool
from colorama import Fore, Style, init

init(autoreset=True)

def free(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G892A Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.107 Mobile Safari/537.36'
        }
        
        with httpx.Client() as client:
            response = client.get("http://de-datacenter.xreverselabs.my.id:1337/reverse-ip?apikey=1337deborahyoung15900&ip="+url, headers=headers)
            
        get_r = response.json()
        result = get_r["domains"]
        for results in result:
            print("[>] {} >> {} Domains".format(Fore.LIGHTCYAN_EX + url + Fore.RESET, Fore.LIGHTYELLOW_EX + str(len(results))))
            open('xReverseResult.txt', 'a').write(results+"\n")
        else:
            print("BAD IP " + url)
    except:
        pass

def revip(url):
    try:
        free(url)
    except Exception as e:
        print("Error in revip:", e)

def Main():
    os.system('cls' if os.name == 'nt' else 'clear')
    try:
        response = requests.get('https://google.com/')
        if response.status_code == 200:
            print("{}   xReverse | {}#No_Identity - @xxyz4".format(Fore.CYAN, Fore.GREEN))
            print("\t{} IP Reverse {}Private API !\n".format(Fore.GREEN, Fore.YELLOW))
            print("{} Copyright : #No_Identity - {}t.me/xxyz4 !".format(Fore.WHITE, Fore.YELLOW))
            print("{} Site : https://xreverselabs.my.id{} - the best all in one hacking tools !\n".format(Fore.WHITE, Fore.YELLOW))
            try:
                list = input(" root@youez[ip list]:~# ")
                url = open(list, 'r').read().splitlines()
                with concurrent.futures.ThreadPoolExecutor(max_workers=int(50)) as executor:
                        executor.map(revip, url)
            except Exception as e:
                print("Error in Main:", e)
        else:
            print(f"\n{y}[-] {r}CHECK YOUR NETWORK CONNECTION{o}")
    except requests.exceptions.SSLError:
        print("Opps, fuck you.")

if __name__ == '__main__':
    Main()