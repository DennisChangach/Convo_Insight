import os
import httpx
import whisper
import torch
from dotenv import load_dotenv
import streamlit as st
from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    PrerecordedOptions,
    FileSource,
)
# Load environment variables
load_dotenv()

#Checking if NVIDIA GPU is available
torch.cuda.is_available()
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


class Transcribe:
    def __init__(self,audio_file):
        self.audio_file = audio_file
    #Function to transcribe audio file
    def transcribe_audio_file_dpg(self,DEEPGRAM_API_KEY):
        try:
            if DEEPGRAM_API_KEY is not None:
                # Configuring user's Deepgram API KEY
                api_key = DEEPGRAM_API_KEY
            else:
                api_key = os.getenv("DEEPGRAM_API_KEY")
            
            if not api_key:
                st.error("No API key provided. Please provide a valid Deepgram API key.")
                exit()
            
            #iCreating a deepgram client
            deepgram: DeepgramClient = DeepgramClient(DEEPGRAM_API_KEY)
        except Exception as e:
            st.error("Please ensure you have provide the correct API key")
            exit()
            
        #buffer data: audio_file onkect
        buffer_data = self.audio_file
        
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
            payload,options,timeout=httpx.Timeout(300.0, connect=10.0)
        )
        #after = datetime.now()

        #print(file_response)

        #Formatting to get the output
        return file_response['results']['channels'][0]['alternatives'][0]['paragraphs']['transcript']

    #Function to generate transcript using Whisper X
    def transcribe_audio_file_wsp(self):
        #Loading whisper model
        model = whisper.load_model("base",device = DEVICE)
        #audio transcription
        result = model.transcribe(self.audio_file,fp16=False)

        # Print the transcription
        #print(result["text"])

        # return speaker information
        return result["text"]