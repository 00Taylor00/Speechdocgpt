import speech_recognition as sr
import re
import subprocess
import random

no_input_responses = [
    "I'm sorry, I didn't hear anything. Could you please speak louder?",
    "I didn't catch that. Can you please try speaking more clearly?",
    "Hmm, I didn't quite understand you. Can you please repeat what you said?",
    "Sorry, I'm having trouble hearing you. Could you please speak closer to the microphone?",
    "I'm not sure what you said. Can you please try speaking more slowly?"
]

#manual entry func
retries = 0
error_counter=0

#manual entry function - if inputting >1 response then will switch input text 
def manual_entry():
    global retries
    if retries == 0:
        retries += 1
        message = input("What would you like help with?")
    else:
        message = input("Do you have any further questions?")
    return message

def recognize_speech():
    # create a speech recognition object
    r = sr.Recognizer()
    global error_counter


    while True:
        

        while error_counter < 3: #nested while loop for speech recog.
            # use the default microphone as the audio source
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source)
                print("Speak now...")
                audio = r.listen(source, timeout=0)

            try:
                # recognize speech using Google Speech Recognition
                message = r.recognize_google(audio)
                message = f"{message}."
                print(f"You said: {message}")

                # check if the message is related to medical issues
                if re.search(r"\bmedical\b|\bhealth\b|\bdoctor\b|\bsymptoms?\b", message, re.IGNORECASE):
                    message = f"medical: {message}"
                return message
            
            except sr.UnknownValueError:
                print("Oops! Didn't catch that")
                error_counter += 1 
                response = random.choice(no_input_responses)
                subprocess.run(["say", response])
                pass
            
            except sr.RequestError as e:
                print(f"Uh oh! Couldn't request results from Google Speech Recognition service; {e}")
                return None
        
        print('I am sorry I think this may not be the correct method of interaction for you with my program. Shall we try using text input instead?')
        
            
        message = manual_entry()
        return message
