import os
import random
from pyowm import OWM
import requests
from datetime import datetime

from textblob import Word
from bs4 import BeautifulSoup
from apiclient.discovery import build
from urllib.parse import urlencode, quote_plus


def check_weather(place):
    """Uses Pyowm API to check weather results for specified region"""
    try:
        fluff_words = ["out", "in", "over", "there", "like", "here"]
        place = place.replace("?", "").split('weather')[1].split(", ")
        place = ",".join(filter(lambda x: x not in fluff_words, place)).strip()

        if place:
            key = os.environ.get('PYOWM_KEY')
            owm = OWM(key)

            observation = owm.weather_at_place(place)
            w = observation.get_weather()

            rise=datetime.fromtimestamp(w.get_sunrise_time())
            sset=datetime.fromtimestamp(w.get_sunset_time())

            report = f"It's {w.get_temperature(unit='fahrenheit')['temp']} degrees F, with {w.get_detailed_status()}.\n"
            report += f"Winds {w.get_wind()}, sunrise at {rise}, Sunset at {sset}.\n"
            return report
    except:
        return "Please specify name of a place or a zipcode." if key else "Please set PYOWM_KEY environment variable."


def comic(_):
    """Fetches random XKCD comic"""
    response = requests.get("https://xkcd.com/{}/info.0.json".format(random.randint(1, 1837)))
    return response.json()["img"]


def define(command):
    """Word definitions from textblob"""
    word = Word(command.split("define")[1].strip())
    return word.definitions[0]


def get_pic(command):
    """Queries Google custom search API for image"""
    query = command.split('pics')[1].strip()

    #params = {
    #    "cx": os.environ.get("GOOGLE_IMAGE_CX"),
    #    "key": os.environ.get("GOOGLE_IMAGE_KEY"),
    #    "searchType": "image", "tab":0,"page":1,
    #    "q": query
    #}
    #resp = requests.get('https://www.googleapis.com/customsearch/v1', params=params)

    params = {
            "cx": os.environ.get("GOOGLE_IMAGE_CX"),
            "key": os.environ.get("GOOGLE_IMAGE_KEY"),
            "searchType": "image",
            "q": query+"#gsc.tab=1",
            "gsc.page": 1
            }

    #https://cse.google.com/cse?cx=<>&key=<>&searchType=image&q=dogs#gsc.tab=1&gsc.q=dogs&gsc.page=1

    resp.raise_for_status()
    images = [im['link'] for im in resp.json()['items']]
    return random.choice(images)


def get_quote(command):
    """Gets real time financial data for a ticker or benchmarks"""

    secret = os.environ["IEX_API_TOKEN"]
    ticker = command.split('quote ')[1].split()[0].upper()

    # make request
    response = requests.get(f"https://cloud-sse.iexapis.com/stable/stock/{ticker}/quote?token={secret}")

    data = response.json()

    # parse price data
    price = data['latestPrice']
    pct_change = 100. * data['changePercent']
    mkt_cap = data['marketCap']

    result = f"{ticker} is trading at ${price}. That's a {pct_change:.2f}% move since the last open, which now values " \
             f"the company at ${mkt_cap:,}"

    return result


def get_video(command):
    """Uses Google API to query for youtube results, and then returns the top result"""

    # standardize and clean input
    command = command.replace("youtube", "play").split("play")[-1].replace("of", "")

    # Set developerKey to the API key value from the APIs & auth > Registered apps at https://cloud.google.com/console
    youtube = build("youtube", "v3", developerKey=os.environ.get('GOOGLE_DEVELOPER_KEY'), cache_discovery=False)

    # Call the search.list method to retrieve results matching the specified query term.
    search_response = youtube.search().list(
        q=command,
        part="id,snippet",
        maxResults=5
    ).execute()

    videos = [v for v in search_response["items"] if "videoId" in v["id"]]
    url = "https://www.youtube.com/watch?v={}".format(random.choice(videos)["id"]["videoId"])
    return url


def joke(_):
    """Scrapes randome joke from theoatmeal.com"""
    url = requests.get('http://theoatmeal.com/djtaf/')
    soup = BeautifulSoup(url.content, 'lxml')
    random_joke = soup.find(class_='part1').get_text()
    random_answer = soup.find(id='part2_0').get_text()
    return "\n".join([random_joke, random_answer])


def search_words(command):
    """Direct link to top Google Search for given input"""
    searchcmd = command.replace("look up", "search").replace('google', 'search')
    query = command if command==searchcmd else command.split('search ')[1]
    goog = requests.get('https://www.google.com/search?{}'.format(urlencode({'q': query}, quote_via=quote_plus)))
    soup = BeautifulSoup(goog.content, 'lxml')

    all_text = ""

    for i in range(3, 5):
        text_candidate = soup.select_one("div:nth-of-type({})".format(i))
        if text_candidate:
            all_text += '\n' + text_candidate.get_text(separator=' ')

    return all_text


def synonyms(command):
    """Synonyms from textblob"""
    word = Word(command.split("synonyms")[1].strip())
    syns = {l for syn in word.synsets for l in syn.lemma_names()}
    return "\n".join(syns)


def word_count(command):
    """Simple word count"""
    text = command.split("count")[1].strip().split()
    return len(text)
