import pyttsx3 # for text-to-speech
import webbrowser #for opening web pages
import smtplib #for emailing
import random # to pick random
import speech_recognition as sr #for speech-to-text
import wikipedia #to look stuff up
import datetime #to find the date+time
import wolframalpha # to do maths
import os # to open programs
import sys # to use the system
import time #so you can wait
import keyboard #to register a keypress
from pynput.keyboard import Key, Controller #to use the media keys
import pynput
from googlesearch import search # to search google for things
from Passes import * #for the Passes

#setup pynput
pynputkeyboard = Controller()

# Initialize speech 
engine = pyttsx3.init('sapi5')

#set the username
MASTER = 'Name of Master'

#what voice the text to speech will use
american = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0" #Path to the american voice
british = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-GB_HAZEL_11.0" #Path to the british voice
speakingvoice = british # default speaking voice is british

#wolfram setup
client = wolframalpha.Client(wolframappid)

#set the speaking engine
voices = engine.getProperty('voices')
#set the words per minute rate of speech engine
engine.setProperty('voice', speakingvoice)

#definitions
def listallcommands():
    print('Listing commands...')
    #Need to write down all the commands you can say and put them here in text format
 

def todolist():# list the things i have written down to do to improve JARVIS
    print(' ')
    printspeak('Here are the items on your to do list for JARVIS...')
    printspeak('- need to get setup the database')
    printspeak('- need to get the other pis to retrieve the data from the database')
    printspeak('- need to setup the Doorlock on another pi, the Lock,Unlock,Open,Close functions')
    printspeak('- need to add the help command')
    printspeak('- need to add more recipients in the email section')
    printspeak('- need to open settings')
    printspeak('- need to open the folders in File Explorer, not cmd')
    printspeak('- need to somehow get a link to the run command {so that whatever you say it will type into the run window, and if it doesnt work then oh well}')
    printspeak('- need to be able to open power dvd')
    printspeak('- need to be able to open bluetooth settings')
    printspeak('- need to change it so that it is a GPIO input rather than Ctrl + F2 to wake JARVIS so that we can run it headlessley on a pi.')
    print(' ')

def justspeak(audio): #definition for JARVIS to just speak what is inputed: justspeak(what you want him to say)
    engine.say(audio)
    engine.runAndWait()

def printspeak(text): #definition for JARVIS to speak and print what is inputed: printspeak(what you want him to say and print)
    print(text)
    engine.say(text)
    engine.runAndWait()

def lowkey(text): #press a lower case key, or a key without shift added
    pynputkeyboard.press(text)
    pynputkeyboard.release(text)

def highkey(text): #press a higher case key, or a key with shift added
    pynputkeyboard.press(Key.shift)
    pynputkeyboard.press(text)
    pynputkeyboard.release(text)
    pynputkeyboard.release(Key.shift)


def opencd(path):
    os.startfile("C:\\Users\\yourname\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\System Tools\\Command Prompt.lnk")
    time.sleep(4)
    pynputkeyboard.type("cd")
    time.sleep(1)
    pynputkeyboard.type(path)
    lowkey(Key.enter)

def cmdcommand(command):
    os.system(command)
    lowkey(Key.enter)

def gotowebpage(text):
    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
    webbrowser.get(chrome_path).open(text)

def greetMe(): #say either good morning, good afternoon or good evening depending on the time.
    currentH = int(datetime.datetime.now().hour)
    if currentH >= 0 and currentH < 12:
        printspeak('Good Morning!')

    if currentH >= 12 and currentH < 18:
        printspeak('Good Afternoon!')

    if currentH >= 18 and currentH !=0:
        printspeak('Good Evening!')

#startup
printspeak("Initializing Jarvis...")
print("")
print("")
greetMe()
time.sleep(1)
printspeak('Hello ' + MASTER)
todolist() #list the things i need to do to improve JARVIS
printspeak('')
printspeak('I am your digital assistant Jarvis')
printspeak('Press Ctrl + F2 for me to start listening')


def myCommand():
   
    r = sr.Recognizer()                                                                                   
    with sr.Microphone() as source:
        printspeak("Listening...")
        #r.pause_threshold =  1
        audio = r.listen(source) #listen for input
    try:
        query = r.recognize(audio) #query = the words from the recording
        print('User: ' + query + '\n') # print User said: (and then the words from the recording)
        
    except Exception as e: #If it cant understand it, then it will ask for a typed input.
        printspeak(f'Sorry {MASTER} I didn\'t get that! Try typing the command!')
        query = str(input('Command: '))

    return query


        

if __name__ == '__main__':

    while True:
        keyboard.wait('ctrl +F2') # wait for Ctrl + F2 buttons to be pressed
        
        query = myCommand(); #execute myCommand function and the output will be called query
        query = query.lower() #change query to lowercase

#Miscilanious commands.        
        if 'hello' in query:
            printspeak('Hello '+ MASTER, )

        elif 'help' in query:
            listallcommands()

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            printspeak(f"{MASTER} the time is {strTime}")

        elif 'your name' in query:
            printspeak("My name is Jarvis, your digital assistant")

        elif 'my name' in query:
            printspeak("Your name is " +MASTER)

        elif "what\'s up" in query or 'how are you' in query:
            stMsgs = ['Just doing my thing!', 'I am fine!', 'Nice!', 'I am nice and full of energy']
            printspeak(random.choice(stMsgs))

        elif 'to do list' in query or 'to do' in query or 'open to do list' in query:
            todolist()
            
#end of Miscilanious commands.
#
#search commands

        elif 'search google' in query or 'search' in query:
            printspeak("what do you want to search?...")
            thingtosearch = myCommand()
            printspeak("This will return the first item URL")

            for j in search(thingtosearch, tld='co.uk', num=10, stop=1, pause=2):
                print(j)

        elif 'wolfram' in query or 'wolf ram' in query or 'wolf' in query or 'ram' in query:
            try:
                query = query
                res = client.query(query)
                wolframresults = next(res.results).text
                printspeak('WOLFRAM-ALPHA says - ')
                printspeak('Got it.')
                printspeak(wolframresults)  

            except:
                webbrowser.open('www.google.com')

        elif 'wikipedia' in query:
            printspeak("Searching wikipedia...")
            query = query.replace("wikipedia", "")
            wikipediaresults = wikipedia.summary(query, sentences =2)
            printspeak(wikipediaresults)
#end of search commands
#
#music commands

        elif 'play music' in query: #play music from the music folder in your personal onedrive
            songs_dir = "C:\\Users\\yourname\\OneDrive\\Music"
            songs = os.listdir(songs_dir)
            print(songs)
            os.startfile(os.path.join(songs_dir, songs[0]))

        elif 'press play' in query or 'press pause' in query: #press the media play/pause button
            printspeak("Pressing media key...")
            lowkey(Key.media_play_pause)

        elif 'play random music' in query or 'random music' in query: #play random music from your music folder in your personal onedrive
            music_folder = "C:\\User\\yourname\\OneDrive\\Music"
            music = [music1, music2, music3, music4, music5]
            random_music = music_folder + random.choice(music) + '.mp3'
            os.system(random_music)
                  
            printspeak('Okay, here is your music! Enjoy!')    

#end of music commands
#
#email commands

        elif 'email' in query:
            printspeak('Who is the recipient? ')
            recipient = myCommand() #recipient is the voice input

            if 'me' in recipient: #if you want to send an email to yourself
                try:
                    printspeak('What should I say? ')
                    content = myCommand() #content is the voice input
                    server = smtplib.SMTP('smtp.gmail.com', 587)# use the gmail server
                    server.ehlo()
                    server.starttls() 
                    server.login(Your_Username, Your_Password) #use your credentials
                    server.sendmail(Your_Username, Normalemail, content) #send email with the voice recording as content, and send it to yourself
                    server.sendmail(Your_Username, "normalemail@gmail.com", content) #send email with the voice recording as content, and send it to yourself
                    server.close()
                    printspeak('Email sent!')

                except:
                    printspeak(f'Sorry {MASTER} I am unable to send your message at this moment!')

            elif 'code' in recipient or 'coding' in recipient: #if you want to send an email to your coding account
                try:
                    printspeak('What should I say? ')
                    content = myCommand() #content is the voice input
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.ehlo()
                    server.starttls()
                    server.login(Your_Username, Your_Password)
                    server.sendmail(Your_Username, Codingemail, content) #send email with the voice recording as content, and send it to your coding email address
                    server.sendmail(Your_Username, "codingemail@gmail.com", content) #send email with the voice recording as content, and send it to your coding email address
                    server.close()
                    printspeak('Email sent!')

                except:
                    printspeak(f'Sorry {MASTER} I am unable to send your message at this moment!') #error message

#end of email commands
#
#All of the open commands, (Programs and Folders)

        elif 'open youtube' in query: #open youtube
            printspeak('okay')
            gotowebpage('www.youtube.com')

        elif 'open gmail' in query: #open gmail
            printspeak('okay')
            gotowebpage('www.gmail.com')

        elif 'open github' in query or 'open git hub' in query:
            printspeak('opening Github...')
            gotowebpage('github.com')

            
        elif 'open google' in query: #open google
            printspeak('okay')
            gotowebpage('www.google.co.uk')

        elif 'open stackoverflow' in query: #open stack overflow
            gotowebpage("stackoverflow.com")

        elif 'open now tv' in query or 'open nowtv' in query:
            gotowebpage("nowtv.com/gb/watch/home")

        elif 'open disney' in query or 'open disney plus' in query or 'open disne' in query:
            gotowebpage("disneyplus.com/en-gb/")
            
        elif 'open visual studio' in query or 'start visual studio' in query: #open visual studio
            cmdcommand("C:\\Program Files (x86)\\Microsoft Visual Studio\\2019\\Community\\Common7\\IDE\\devenv.exe")
            printspeak("Opening Visual studio Code 2019...")
            

        elif 'open python' in query or 'start python' in query: #open Python IDLE 3
            cmdcommand(idle3)
            printspeak('Opening Python IDLE... ')
            os.system("taskkill /f /im cmd.exe")

        elif 'open android studio' in query or 'android studio' in query or 'start android studio' in query: # open android studio
            os.startfile("C:\\Users\\yourname\\Desktop\\Coding\\Android Studio.lnk")
            printspeak("Opening Android Studio...")

        elif 'open minecraft' in query or 'start minecraft' in query: #open minecraft for windows 10
            os.startfile("C:\\Users\\yourname\\Desktop\\Minecraft\\Minecraft - Shortcut.lnk")
            printspeak("opening Minecraft for Windows 10...")

        elif 'open spotify' in query or 'start spotify' in query: #open spotify
            cmdcommand("C:\\Users\\yourname\\Desktop\\Spotify.lnk")
            printspeak("Opening Spotify...")

        elif 'cmd virtual assistant' in query or 'open virtual assistant folder' in query or 'open virtual assistant' in query: #open the virtual assistant folder in a cmd window
            opencd(" \\users\\yourname\\OneDrive\\Coding\\Projects\\Virtual_assistant")
            print('Opening Virtual Assistant Folder... ')
            
#end of open commands.
#
#door control commands
#door commands are on a different pi
#end of door control commands.
#
#program commands

        elif 'abort' in query or 'stop' in query or 'leave' in query or 'exit' in query or 'bye' in query or 'cancel' in query: #exit the program
            printspeak('okay')
            printspeak(f'Bye  {MASTER} have a good day.')
            cmdcommand("taskkill /f /im python3.8.exe")
            cmdcommand("taskkill /f /im pythonw3.8.exe")
            sys.exit()

        elif 'change voices' in query or 'voice' in query: #switch between british and american voices
            printspeak("what would you like my voice to be, American or British?")
            voicechoice = myCommand()
            voicechoice = voicechoice.lower()
            if 'british' in voicechoice or 'uk' in voicechoice or 'britain' in voicechoice:
                printspeak("Changing voice to british...")
                speakingvoice = british
                engine.setProperty('voice', speakingvoice)

            elif 'american' in voicechoice or 'america' in voicechoice:
                printspeak("Changing voice to american...")
                speakingvoice = american
                engine.setProperty('voice', speakingvoice)
                

        elif 'edit' in query or 'edit this' in query or 'rewrite you' in query: #edit the JARVIS.py script
            os.system("idle3 //users//yourname//OneDrive//Coding//Projects//Virtual_assistant//JARVIS.py")
            print('Opening this file to edit... ')
            

        elif 'shutdown' in query or 'shut down' in query: #shutdown the computer
            printspeak("are you sure you want to shut down?")
            shutdown = myCommand()
            if 'yes' in shutdown:
                printspeak("okay shutting down...")
                cmdcommand("shutdown /s /t 1")

            if 'no' in shutdown:
                printspeak("okay NOT shutting down...")
#end of program commands
#        
                                   
           
        else: #if words in voice recording do not match any of the above ones, say "I didnt catch that" and send the query string to the database where the other pis can access it
            printspeak("I Didnt Catch that.") 
            cloudquery = query

        printspeak('Press Ctrl + F2 for me to start listening again') #print how to wake JARVIS
        

