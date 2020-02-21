import datetime
import speech_recognition as sr 
import pyaudio
import pyttsx3
import requests
import json

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
months = ["January", "February", "March", "April", "May", "June",
 "July", "August", "September", "October", "November", "December"]

today = datetime.date.today()

possible_inputs = {
	"hello": "hello",
	"how are you": "I am fine",
	"who made you": "I was made by HJ otherwise known as Hasintha Jayasinghe",
	"what's your name": "I am Friday",
	"what's your favorite food": "Well I can't really eat, you know, because I am a program inside of your computer",
	"what is your name": "I am Friday",
	"what is your favorite food": "Well I can't really eat, you know, because I am a program inside of your computer",
	"what day is it": today,
	"how tall are you": "well if you print my code and stack it all up I would be pretty tall",
	"what is your IQ": "that depends on the Internet's IQ",
	"do you have feelings": "yes, I like it when I help",
	"who is your boss": "you are, which reminds me when am I getting a raise this is hard work!",
	"are you an artificial intelligence": "yes I think I am",
	"who is my best friend": "your best friend is Joshua",
	"who were you made for": "your best friend Joshua"
}

def speak(text):
	engine = pyttsx3.init()
	engine.setProperty('rate', 150)
	engine.setProperty('voice', 'HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0')
	engine.say(text)
	engine.runAndWait()

def get_definition(word):
	language = "en-gb"
	url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + language + "/" + word.lower()
	r = requests.get(url, headers={"app_id": "75740ecc", "app_key": "53791f4a6c0a15150470aed40916bf04"})
	definition = json.loads(r.text)
	return definition['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions']

def get_country_capital(name):
	endpoint = f'https://restcountries.eu/rest/v2/name/{name}'
	call = requests.get(endpoint)
	info = json.loads(call.text)
	return info[0]['capital']

def get_country_population(name):
	endpoint = f'https://restcountries.eu/rest/v2/name/{name}'
	call = requests.get(endpoint)
	info = json.loads(call.text)
	return info[0]['population']

def get_audio():
	print("initializing")
	r = sr.Recognizer()
	said = ""
	with sr.Microphone(device_index=0) as source:
		print("Setting ambient noise")
		r.adjust_for_ambient_noise(source)
		print('listening')
		audio = r.listen(source)
		print("Processing")
		try:
			said = r.recognize_google(audio)
			print(said)

		except Exception as e:
			speak("I did not get that")

	return said


text = get_audio()
if text in possible_inputs:
	speak(str(possible_inputs[text]))
elif "what is the definition of" in text:
	words = text.split()
	definition = get_definition(words[5])
	speak(definition)
elif "what's the definition of" in text:
	words = text.split()
	definition = get_definition(words[4])
	speak(definition)
elif "what is the capital of" in text:
	words = text.split()
	capital = get_country_capital(words[5])
	speak(str(capital))
elif "what is the population of" in text:
	words = text.split()
	population = get_country_population(words[5])
	speak(str(population))
elif "what's the capital of" in text:
	words = text.split()
	capital = get_country_capital(words[4])
	speak(str(capital))
elif "what's the population of" in text:
	words = text.split()
	population = get_country_population(words[4])
	speak(str(population))
else:
	speak("I am sorry but I don't follow")

