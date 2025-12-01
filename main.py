#import request to get info from a website
import requests
#import re to filter and extract links from html elements
import re
#import pathlib easy way to get path
import pathlib
#import os to clear terminal and restart app 
import os

#import sys to handle arguments
import sys
#get arguments full game name and First part of game name
try:
    Gamename = sys.argv[1]
    FirstWord = sys.argv[2]
except:
# if arguments is empty or something, We just give user a hit what is wrong and exit 
    print("pls enter name of game and first work from game name")
    quit()



# Check Does Downloads Folder is Exist
def check_folder():
     
    #make path by pathlib
    pathsd = str(pathlib.Path().resolve()) + "/Downloads/"
    #check does path is exist if not create it
    if os.path.isdir(pathsd) == False:
        os.makedirs(pathsd)
        

#get game link
def get_game(query:str, keywords:list):
    # Fit girl web site URL
    url = "https://fitgirl-repacks.site/"
    params = {"s": query}
    # headers
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    #trying to make request 
    try:
        #making request    
        response = requests.get(url, params=params, headers=headers)
        # if server is not answer we return error
        if response.status_code != 200:
            print("Failed to fetch:", response.status_code)
            quit()

            return []
        # Html elements
        html = response.text
    # if server make 500 kind errors we just restart app with saving arguments    
    except requests.exceptions.ConnectionError:
        
        #clear terminal
        os.system("clear")
        #restart app with arguments
        os.execv(sys.executable, ['python'] + sys.argv)

    #find all links    
    matches = re.findall(r'<a href="(.*?)".*?>(.*?)</a>', html, re.DOTALL)
    matches = str(matches)
    #make simple filtering to get only links with has https://fitgirl-repacks.site/. to ignore pictures and other not needed resources
    results = re.findall(r"https://fitgirl-repacks.site/.*?/",matches)
    title = query
    #make another filtering to show similar links to keyword
    filtered = re.findall(rf"https://fitgirl-repacks.site/{keywords[0]}.*?/",matches)

    filtered = list(dict.fromkeys(filtered))
    filteredsort = list(dict.fromkeys(filtered))
    #make link list more user friendly add number like:
                    ################
                    #    0 link    #
                    #    1 link    #
                    #    2 link    #
                    #    3 link    #
                    ################
    for number, letter in enumerate(filteredsort):
        #print result    
        print(number, letter)        
    #get input with number was chosen
    #Also we check does user put something exempt number, if yes app restart with saving arguments
    try:
     
        link = int(input("use number from 0 to chose link ",))

        link = filtered[link]
        return link
    except:
        #restart app with arguments saved
        print(f"pls Write a number")
        input("Press Enter to Restart: ")
        os.execv(sys.executable, ['python'] + sys.argv)
    

#getting magnet link using game link
def get_magnet(url:str):

    
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Connection": "keep-alive"
    }
    #trying make request
    try:
        response = requests.get(url, headers=headers, timeout=15)
    #if server reject us because of ddos security we just restart 
    except requests.exceptions.ConnectionError:
        
        import time 
        print("server time out trying again")
        time.sleep(1)
        os.system("clear")
        #restart app
        os.execv(sys.executable, ['python'] + sys.argv)
    # check does server still exist
    if response.status_code != 200:
        print("Failed to fetch:", response.status_code)
        return []
    #get html elements
    html = response.text
    #search for a magnet link in page of game
    matches = re.findall(r'<a href="magnet:(.*?)">magnet</a>', html, re.DOTALL)
    #clean URL from [ ]
    matches = str(matches[0]).replace("['","")
    matches = str(matches).replace("']","")
    # connect magnet together 
    matches = "magnet:" + matches
    return matches

#Download game by magnet + aria2c CLI
def download_magnet(magnet:str):
    import textwrap
    import subprocess
    magnet = magnet[0]  # Get the first element of the tuple, which is the magnet string
    magnet = ' '.join(magnet.split())  # Now you can use split
    
    # sav path for games 
    save_path = str(pathlib.Path().resolve()) + "/Downloads/"
    #run aria2c CLI to Download game from magnet
    os.system("clear")
    subprocess.run([
        "aria2c",
        magnet,
        "-d",save_path,
        "--seed-time=0",                  # stop seeding instantly
        "--enable-dht=true",
        "--max-overall-download-limit=0",   # unlimited speed

    ], check=True)
#check does folder is exists 
check_folder()
# connect all together 
download_magnet((get_magnet(get_game(Gamename, FirstWord)),"1.torrent"))


   





