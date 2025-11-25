

import sys
try:
    Gamename = sys.argv[1]
    FirstWord = sys.argv[2]
except:
    print("pls enter name of game and first work from game name")
    quit()
print("GameName", Gamename)
print("FirstWord:", FirstWord)
def check_fodler():
    import os 
    import pathlib
    pathsd = str(pathlib.Path().resolve()) + "/Downloads/"

    if os.path.isdir(pathsd) == False:
        os.makedirs(pathsd)
        
check_fodler()

def get_game(query:str, keywords:list):
    import requests
    import re
    url = "https://fitgirl-repacks.site/"
    params = {"s": query}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
            
        response = requests.get(url, params=params, headers=headers)

        if response.status_code != 200:
            print("Failed to fetch:", response.status_code)
            quit()

            return []

        html = response.text
    except requests.exceptions.ConnectionError:
        import os

        os.system("clear")
        os.execv(sys.executable, ['python'] + sys.argv)
    matches = re.findall(r'<a href="(.*?)".*?>(.*?)</a>', html, re.DOTALL)
    matches = str(matches)
    results = re.findall(r"https://fitgirl-repacks.site/.*?/",matches)
    title = query
    filtered = re.findall(rf"https://fitgirl-repacks.site/{keywords[0]}.*?/",matches)

    filtered = list(dict.fromkeys(filtered))
    filteredsort = list(dict.fromkeys(filtered))
    
    for number, letter in enumerate(filteredsort):
            
        print(number, letter)        
    
    link = input("use number from 0 to chose link ")
    link = filtered[int(link)]

    return link

def get_magnet(link:str):
    import requests
    import re
    url = link  
    import time


    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
    except requests.exceptions.ConnectionError:
        import os
        import time 
        print("server time ou trying again")
        time.sleep(1)
        os.system("clear")
        os.execv(sys.executable, ['python'] + sys.argv)

    if response.status_code != 200:
        print("Failed to fetch:", response.status_code)
        return []

    html = response.text

    matches = re.findall(r'<a href="magnet:(.*?)">magnet</a>', html, re.DOTALL)
    matches = str(matches[0]).replace("['","")
    matches = str(matches).replace("']","")
    matches = "magnet:" + matches
    return matches




def magnet_to_torrent(magnet, save_as):
    import requests
    import re
    import pathlib
    import os
    paths = str(pathlib.Path().resolve()) + "/Downloads/"
    paths = paths + save_as

    if os.path.isfile(paths) == True:
        os.remove(paths)
    


    match = re.search(r"btih:([0-9A-Fa-f]{40}|[0-9A-Fa-f]{32})", magnet)
    if not match:
        raise ValueError("Invalid magnet link: cannot find infohash")

    infohash = match.group(1)
    url = f"https://itorrents.org/torrent/{infohash}.torrent"

    print("Downloading:", url)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/118.0.5993.90 Safari/537.36"
    }

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise Exception(f"Failed to download .torrent file, status code {r.status_code}")

    with open(paths, "wb") as f:
        f.write(r.content)

    print("Saved:", save_as)
    return save_as


def download_magnet(magnet:str):

    import subprocess
    import pathlib
    import os
    paths = str(pathlib.Path().resolve()) + "/Downloads/1.torrent"
    paths1 = str(pathlib.Path().resolve()) + "/Downloads/"
    torrent_file = paths
    save_path = paths1
    subprocess.run([
        "aria2c",
        torrent_file,
        "-d",save_path,
        "--seed-time=0",                  # stop seeding instantly
        "--enable-dht=true",
        "--max-overall-download-limit=0",   # unlimited speed

    ], check=True)


download_magnet(magnet_to_torrent(get_magnet(get_game(Gamename, FirstWord)),"1.torrent"))


   





