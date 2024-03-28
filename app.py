#importing the necessary dependencies:
import streamlit as st
from dotenv import load_dotenv
#from datetime import datetime
import os
import tempfile
#import requests
#import logging, verboselogs

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    PrerecordedOptions,
    FileSource,
)

# Load environment variables
load_dotenv()

#Configuring Deepgram API
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

#iCreating a deepgram client
deepgram: DeepgramClient = DeepgramClient(DEEPGRAM_API_KEY)



#Main function
def main():
    #page config
    st.set_page_config(page_title = "Convo Insights",page_icon = "🧠")

    st.title("💬 Uncovering Insights from your Conversations 🕵️‍♂️💡")

    
    
    #Uploading Audio Files
    with st.sidebar:
        st.title("🛠️ Configuration:⚙️")
        #Activating Demo Data
        st.text("Please upload your audio file: 🔊")
        audio_file = st.file_uploader("Upload audio file")
        #Selecting Mode of transacription: Master or Grand Master: & Call the appropriate function for transacription
        transcribe = st.button("Transcribe")
        demo_on = st.toggle("📈")

    
    if audio_file and transcribe:
        # When the file is uploaded: Pass the buffered audio file object
        response = transcribe_audio(audio_file)
        st.markdown(response)
        
           
   
    if transcribe and demo_on:
        #audio_file = 'Test recording.m4a'
        audio_url = "https://www.youtube.com/watch?v=4Q8R0JXFXZE"
        #returns the response as a json file
        response = transcribe_audio_URL(audio_url)
        
        st.markdown(response)


    

#Function to transcribe audio
def transcribe_audio(audio_file):
    #buffer data: audio_file onkect
    buffer_data = audio_file
    
    payload: FileSource = {
        "buffer": buffer_data,
    }
    #providing transcription options
    options: PrerecordedOptions = PrerecordedOptions(
        model="nova",
        smart_format=True,
        utterances=False,
        paragraphs=True,
        punctuate=True,
        diarize=True,

    )

    #before = datetime.now()
    file_response = deepgram.listen.prerecorded.v("1").transcribe_file(
        payload,options
    )
    #after = datetime.now()

    #print(file_response)

    #getting the response in a json format: Formatting to get the output
    st.write("completed printing on console")
    return file_response['results']['channels'][0]['alternatives'][0]['paragraphs']['transcript']


#transctibe from URL
def transcribe_audio_URL(audio_url):
    st.write("Entered here!")
    #Defiing the audio URL
    AUDIO_URL = {
    "url": audio_url
    }
    
    
    options = PrerecordedOptions(
        model="nova",
        smart_format=True,
        utterances=False,
        paragraphs=True,
        punctuate=True,
        diarize=True,
    )
    st.write("starting this")
    url_response = deepgram.listen.prerecorded.v("1").transcribe_url(
        AUDIO_URL, options
    )
    st.write("Completed the transcription")
    print(url_response)

    st.write("completed printing on console")


    #getting the response in a json format
    json_response = url_response.to_json(indent=4)

    return url_response['results']['channels'][0]['alternatives'][0]['paragraphs']['transcript']

      
        
if __name__ == "__main__":
    main()
