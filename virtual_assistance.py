# Description : This is virtual assistant program that gets date,current time,respons back
#              with random greeting and returns information on a person

# Import the libraries
import speech_recognition as sr
import os
from gtts import gTTS
import datetime
import warnings
import calendar
import random
import wikipedia

#Ignore any warning messages
warnings.filterwarnings('ignore')


# Record audio and return as a string
def recordAudio():
    # Record the audio
    r = sr.Recognizer()  # Creating recognizer object

    #open the microphone and start recording

    with sr.Microphone() as source:
            print('say something!')
            audio = r.listen(source)

    # Use Googles speech_recognition
    data = ''
    try:
        data = r.recognize_google(audio)
        print('You said: '+data)
    except sr.UnknownValueError:  # Check for unknown errors
        print('Google Speech Recognition could not understand the audio, unknown error')
    except sr.RequestError as e:
        print('Request result from Google Speech Recognition service error '+e)

    return data



# Function to get the virtual assistance response
def assistantResponse(text):

    print(text)

    # Convert the text to speech
    myobj = gTTS(text=text, lang='en', slow=False)

    # Save the converted audio to a file
    myobj.save('assistant_response.mp3')

    # play the converted file
    os.system('start assistant_response.mp3')


# Function for wake words or phrase
def wakeWord(text):
    WAKE_WORDS = ['hey computer', 'okay computer']  # A list of wake words

    text = text.lower()  # converting the text to all lower case words

    # Check to see if the users command/text contains a wake word/phrase
    for phrase in WAKE_WORDS:
        if phrase in text:
            return True

   #if the wake word isn't found in the text from the loop so it returns false
    return False

# A function to get the current date
def getDate():

    now = datetime.datetime.now()
    my_date = datetime.datetime.today()
    weekday = calendar.day_name[my_date.weekday()]   #e.g. Friday
    monthNum = now.month
    dayNum = now.day

    # A list of months
    month_names = ['January','February','March','April','May','June','July','August','September',
                   'October','November','December']

    # A list of ordinal numbers
    ordinalNumbers = ['1st','2nd','3rd','4th','5th','6th','7th','8th','9th','10th','11th','12th','13th',
                       '14th','15th','16th','17th','18th','19th','20th','21st','22nd','23rd','24th','25th',
                       '26th','27th','28th','29th','30th','31st']

    return 'Today is '+weekday+' '+month_names[monthNum-7]+' the '+ ordinalNumbers[dayNum-1]+' . '

# A function to return a random greeting response
def greeting(text):

    #Greeting inputs
    GREETING_INPUTS = ['hi', 'hey', 'hello', 'hola', 'greetings', 'wassup']

    #Greeting responses
    GREETING_RESPONSES = ['howdy', 'whats good', 'hello', 'hey there']

    # If the users input is a greeting then return a randomly chosen greeting response
    for word in text.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES) +' . '

    # If no greeting was detected then return an empty string
    return ''

# A function to get a persons first and last name from the text
def getPerson(text):

    wordList = text.split()  #splitting the text into a list of words

    for i in range(0, len(wordList)):
        if i + 3 <= len(wordList) - 1 and wordList[i].lower() == 'who' and wordList[i+1].lower() == 'is':
            return wordList[i+2] + ' '+ wordList[i+3]

while True:

    #Record the audio
    text = recordAudio()
    response = ''

    # Check for the wake word/phrase
    if(wakeWord() == True):

        # check for greetings by the user
        response = response + greeting(text)

        # check to see if user said anything having to do with the date
        if('date' in  text):
            get_date = getDate()
            response = response + ' ' + get_date

        # check to see if user said anything having to do with the time
        if('time' in  text):
            now = datetime.datetime.now()
            meridiem = ''
            if now.hour >=12:
                meridiem = 'p.m'  # Post Meridiem (PM) after midday
                hour = now.hour-12
            else:
                meridiem = 'a,m'  # Ante Meridiem (AM) before midday
                hour = now.hour
            # convert minute into a proper string
            if now.minute < 10:
                minute = '0'+str(now.minute)
            else:
                minute = str(now.minute)

            response = response +' '+'It is '+str(hour)+':'+minute+' '+meridiem+' .'


        # check if the user said who is
        if('who is' in text):
            person = getPerson(text)
            wiki = wikipedia.summary(person, sentences=2)
            response = response + ' ' + wiki


        # Have the assistant respond back using audio and text from response
        assistantResponse(response)








