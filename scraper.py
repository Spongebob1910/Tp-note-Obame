import json
import re
import time
import requests_html

import bs4
import requests
from bs4 import BeautifulSoup  # importing BeautifulSoup
from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession

# sample youtube video url
url = "https://www.youtube.com/watch?v=y-yPttAx77I"


def likes_of_video(soup):
    # Récupérer le nombre de like
    data = re.search(r"var ytInitialData = ({.*?});", soup.prettify()).group(1)  
    data_json = json.loads(data)
    videoPrimaryInfoRendererBuilder = data_json['contents']['twoColumnWatchNextResults']['results']['results']['contents']
    indice = 0
    if 'videoPrimaryInfoRenderer' in videoPrimaryInfoRendererBuilder[0]:
        indice = 0
    elif 'videoPrimaryInfoRenderer' in videoPrimaryInfoRendererBuilder[1]:
        indice = 1
    else :
        indice = 2
    videoPrimaryInfoRenderer = videoPrimaryInfoRendererBuilder[indice]['videoPrimaryInfoRenderer']

    likes_label = videoPrimaryInfoRenderer['videoActions']['menuRenderer']['topLevelButtons'][0]['segmentedLikeDislikeButtonRenderer']['likeButton']['toggleButtonRenderer']['defaultText']['accessibility']['accessibilityData']['label']

    likes_str = likes_label.split(' ')[0].replace(' ','')  # on supprime les espaces

    likes_tab = re.findall('\d+', likes_str) # on recupères les chiffres

    likes = ""

    for e in likes_tab:

        likes = likes + e
    return likes


def get_video_info(url):
    # download HTML code
    response = requests.get(url)

    # create beautiful soup object to parse HTML
    web_soup = bs(response, "html.parser")
    # open("index.html", "w").write(response.html.html)
    # initialize the result
    if response.ok:
        result = {}
        title = web_soup.find("meta", itemprop="name")['content']
        result["title"] = title
        result["author"] = web_soup.find("span", itemprop="author").findChildren("link",itemprop="name",recursive=False)[0]['content']
        result["views"] = web_soup.find("meta", itemprop="interactionCount")['content']
        # video description
        result["description"] = web_soup.find("meta", itemprop="description")['content']
        result["video_id"] = web_soup.find("meta", itemprop="videoId")["content"]
        # nombre de likes
        #result["likes"] = likes_of_video(web_soup)
    return result

# Création de ma vidéothèque correspondant à mon fichier

def create_fichier_json(nom_fichier):
    if type(nom_fichier) == str :
        nom_fichier = nom_fichier + ".json"
        with open(nom_fichier, "w") as file:
            print("fichier créé")
    else:
        print("Vous n'avez pas rentrer un string, le fichier n'a pas pu être créé")
    return nom_fichier

def get_video_id(url):
    response = requests.get(url)
    # create beautiful soup object to parse HTML
    web_soup = bs(response, "html.parser")
    # open("index.html", "w").write(response.html.html)
    # initialize the result
    if response.ok:
        result = {}
        result = web_soup.find("meta", itemprop="videoId")["content"]
    return result


def ecrire_json(fileName,result):
    nom_fichier = fileName
    tmp = json.dumps(result)
    jsonString = json.loads(tmp)
    file = open(fileName, "a")
    tmp2 = get_video_info(jsonString)
    tmp2 = str(tmp2)+ "\n"
    file.write(tmp2)
    file.close()

#def lire_fichier_json(nom_fichier):
    #with open(nom_fichier) as mon_fichier:
        #data = json.load(mon_fichier)
        #print(data)
    #return data


def combine_url(l):
    liste_url = []
    for i in range(len(l)):
        liste_url.append("https://www.youtube.com/watch?v=" + l[i])
    return liste_url

def ecrire_tous_les_url(fileName,liste_id):
    for i in range(len(liste_id)):
        ecrire_json(fileName,liste_id[i])
    return fileName

def nb_lignes(nom_fichier):
    with open(nom_fichier, 'r') as fp:
        lines = len(fp.readlines())
        print('Total Number of lines:', lines)
    return lines

def verif_youtube_video(nom_fichier_entree,nom_fichier_sortie):
    urls = []
    url_video = 0
    nom = create_fichier_json(nom_fichier_sortie)

    # Ouvrir le fichier en lecture seule
    file = open(nom_fichier_entree, "r")
    # utilisez readline() pour lire la première ligne
    line = file.readline()
    line = json.dumps(line)
    url_ligne = line
    url_id = combine_url(url_ligne)
    info_video = get_video_id(url_id)
    print("info_video",info_video)
    urls.append(info_video)

    while line:
        # utilisez readline() pour lire la ligne suivante
        line = json.dumps(line)
        url_ligne = line
        url_id = combine_url(url_ligne)
        info_video = get_video_id(url_id)
        urls.append(info_video)
    ecrire_tous_les_url(nom_fichier_sortie,urls)
    file.close()
    return 0

verif_youtube_video(test,"videotheque")