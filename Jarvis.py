##########################
#    JARVIS_PROYECT      #
#        V 0.1           #
#   DATE: 12.10.2021     #
#  CREATOR: Anze Kovac   #
##########################
import webbrowser
import random
import json
import pickle
import numpy as np
import nltk
import pyttsx3
import requests
import bs4
import urllib.request
from nltk.stem import WordNetLemmatizer
import speech_recognition as sr
import time
import datetime
from tensorflow.keras.models import load_model
# initialize elements
lematizer = WordNetLemmatizer()
intents = json.loads(open("intents.json").read())
words = pickle.load(open("words.skl", "rb"))
classes = pickle.load(open("classes.skl", "rb"))
model = load_model("chatbotmodel.h5")

#cleaning up sentence function
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lematizer.lemmatize(word) for word in sentence_words]
    return sentence_words

#sentence convert to bag of words (in binary 0 or 1)
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

#predict function
def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

#goodmorning protocol
def good_morning_pt():
    #tell you the time
    Now_time = time.asctime(time.localtime(time.time()))
    r = requests.get("https://ipinfo.io/")
    datas = r.json()
    city = datas["city"]
    # weather
    url = 'ADD CITY LINK FROM WEBSITE ABOVE'.format(city)
    res = requests.get(url)
    data = res.json()

    temp = data['main']['temp']
    wind_speed = data['wind']['speed']
    description = data['weather'][0]['description']

    #what will bot return
    jarvis_say = "Good morning sir today is " + Now_time + " currently in " + city + " {} degrees celsius".format(
        temp) + " and {}".format(description) + " and the Wind Speed is {} Meters per second".format(
        wind_speed) + "have a wonderful day."

    return jarvis_say
#crypto stats
def Crypto_PY():
    url1 = 'https://digitalcoinprice.com/coins/polymath-network'
    url2 = 'https://digitalcoinprice.com/coins/bitcoin'
    url3 = 'https://digitalcoinprice.com/coins/ethereum'

    # POLY
    sauce = urllib.request.urlopen(url1).read()
    soup = bs4.BeautifulSoup(sauce, "html.parser")
    prices = soup.find(id="quote_price").get_text()

    # BTC
    sauce2 = urllib.request.urlopen(url2).read()
    soup2 = bs4.BeautifulSoup(sauce2, "html.parser")
    prices2 = soup2.find(id="quote_price").get_text()

    # ETH
    sauce3 = urllib.request.urlopen(url3).read()
    soup3 = bs4.BeautifulSoup(sauce3, "html.parser")
    prices3 = soup3.find(id="quote_price").get_text()

    Crypto_price = "Price of Raven coin is " + prices + " ,price of Bitcoin is " + prices2 + " ,price of Ethereum is " + prices3 + " ."
    return Crypto_price
#tell you what is the current time
def jarvis_time():
    seconds = time.time()
    local_time = time.ctime(seconds)
    result_time = "It is:" + local_time
    return result_time
#tell you what is the current weather
def jarvis_weather():
    r = requests.get("https://ipinfo.io/")
    datas = r.json()
    city = datas["city"]

    # weather
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=a4887dd4c4e8f0b06ea59c6f1e5623ed&units=metric'.format(city)
    res = requests.get(url)
    data = res.json()

    temp = data['main']['temp']
    wind_speed = data['wind']['speed']

    description = data['weather'][0]['description']

    jarvis_say ="Currently in " + city + " {} degrees celsius".format(
        temp) + " and {}".format(description) + " and the Wind Speed is {} Meters per second".format(
        wind_speed) + "."

    return jarvis_say
# show you what you want to see in browser
def jarvis_search():
    engine.say("what do you want to search")
    engine.runAndWait()
    search = record_audio()
    url = "https://www.google.com/search?q=" + search
    webbrowser.get().open(url)
    resoult = "Here is what i found of" + search
    return resoult
#tell you what are he's specifications
def Specification():
    spec = "PUT YOUR SPECIFICATIONS HERE"
    return spec
#tell you current date
def Datum():
    date_object = datetime.date.today()
    return date_object
#found best answer for you
def get_response(intents_list, intents_json):
    tag = intents_list[0]["intent"]
    list_of_intents = intents_json["intents"]
    for i in list_of_intents:
        if i["tag"] == tag:
            result = random.choice(i['responses'])
            if result == "Goodmorning=True":
                result = good_morning_pt()
            elif result == "Stoks=True":
                result = Crypto_PY()
            elif result == "Time=True":
                result = jarvis_time()
            elif result == "Weather=True":
                result = jarvis_weather()
            elif result == "Search=True":
                result = jarvis_search()
            elif result == "Specification=True":
                result = Specification()
            elif result == "Datum=True":
                result = Datum()
            else:
                pass
            break
    return result
#record audio function
def record_audio(ask=False):
    # use microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        if ask:
            print(ask)
        # use microphone in element and record voice
        audio = r.listen(source, 10, 3)
        voice_data = ""
        try:
            voice_data = r.recognize_google(audio)
        # if found any error
        except sr.UnknownValueError:
            print("SYSTEM: UnknownValueError")
        return voice_data

print("Jarvis is ready")

while True:
    #voice generation
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    engine.setProperty('volume', 2.0)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    #listening
    mesage = record_audio()
    print("YOU: ", mesage)
    if mesage == "hey Jarvis":
        Ask_word = "What can I do for you sir"
        engine.say(Ask_word)
        engine.runAndWait()
        engine.stop()
        engine.runAndWait()
        print("BOT: ", Ask_word)
        mesage = record_audio()
        print("YOU: ", mesage)
        ints = predict_class(mesage)
        try:
            res = get_response(ints, intents)
        except:
            mesage = record_audio()
            print("YOU: ", mesage)
            ints = predict_class(mesage)
        try:
            engine.say(res)
            print("BOT: ", res)
        except:
            print(" ")
        engine.runAndWait()
        engine.stop()
        engine.runAndWait()
    else:
        pass