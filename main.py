print('\033c')

import openai
import subprocess
from STT import recognize_speech
import random
import requests
import time
import os

from elevenlabslib import *
import pydub
import pydub.playback
import io


openai.api_key = "<insert-openai-api-key>"
user = ElevenLabsUser("<insert-elevenlabs-api-key>") 


def play(bytesData):
    sound = pydub.AudioSegment.from_file_using_temporary_files(io.BytesIO(bytesData))
    pydub.playback.play(sound)
    return


###########################Greeting######################
print("""
         88                                                       
         88                                                    
         88                                                     
 ,adPPYb,88  ,adPPYba,   ,adPPYba,  
a8"    `Y88 a8"     "8a a8"     ""   
8b       88 8b       d8 8b               
"8a,   ,d88 "8a,   ,a8" "8a,   ,aa             
 `"8bbdP"Y8  `"YbbdP"'   `"Ybbd8"'           
                                                                 
    """)

print("""

    Medical Chatbot Coding Practice 
    DO NOT USE FOR MEDICAL ADVICE 
    * Not intended to replace the advice of your clinician *
""")

#Stock speech for prompting dialogue

#greetings variables
greetings_list = [
    "Hey there! How can I assist you today? Try and be detailed with your questions",
    "Hi! How may I help you?",
    "Good day! Is there anything specific I can help you with?",
    "Greetings Human! What brings you here today?",
    "Well hello there! How can I be of assistance?",
    "Welcome! How can I assist you on this fine day?",
    "Konnnicheewaaa!, what's up? How can I help you today?",
    "Hey, how's it going. Got any questions?",
    "Ola! How can I be of service to you today?",
    "Howdy! What can I help you with?",
    "Hi! How can I assist you on this lovely day?"
]

selected_greeting = random.choice(greetings_list)

dialogue_prompts = [   
    "Is there anything else you'd like to know?",   
    "Do you have any other questions?",   
    "What other questions do you have?",   
    "Would you like more information on this topic?",   
    "Can I help with anything else?",    
    "Do you need clarification on anything?",    
    "Do you need any further information? We can change topics if you would like?",    
    "Would you like me to go into more detail?"
]


subprocess.run(["say", selected_greeting])


print("Your new assitant is ready!")

#########################

#reply list - for storing replys as text for passing to TTS - not used yet ?could be used to build chat dialogue box
message_list=[]
reply_list =[]
prompt_counter = 0 

#message input from STT
while True:
    message = recognize_speech()
    if message is None:
        continue 
#adds to message list
 #   message_list.insert(0, message)
    print("Your message has been passed to the AI, please give it some time to think")
    #max_tokens= random.randint(100, 200) # adds variety to length of response for more conversational feel
    output = openai.ChatCompletion.create(    
        model="gpt-3.5-turbo-0301",
        messages=[{
        "role": "user", 
        "content": f"You are a medical education chatbot. You should not state you are an AI language model as the user already knows. You do not treat or diagnose. \n\n User: {message}",        
        }],
        max_tokens = 100
    )

#strips the api call output to create text 
    reply = output.choices[0].message.content.strip()


#adds to reply list for potential future chat log
#    reply_list.insert(0, reply) 

    print("\n" + reply + "\n")
    prompt_counter += 1
    voice = user.get_voices_by_name("<insert-voice-model>")[0] 
    play(voice.generate_audio_bytes(f"{reply}")) 

    #subprocess.run(["say", reply]) --- commented out * keep in case of revert * --- old TTS engine 

#segway prompts for dialogue flow
    current_prompt=dialogue_prompts[prompt_counter]
    print(current_prompt)
    subprocess.run(["say", current_prompt])
