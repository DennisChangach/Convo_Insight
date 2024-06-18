#API FILE: Taking the audio file as input & generating the transcriots from the audio file
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import uvicorn
import httpx
import requests
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

# Define FastAPI app
app = FastAPI()


#Function to transcribe audio file
def transcribe_audio_file(audio_file):
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
        payload,options,timeout=httpx.Timeout(300.0, connect=10.0)
    )
    #after = datetime.now()

    #print(file_response)

    #gFormatting to get the output
    return file_response['results']['channels'][0]['alternatives'][0]['paragraphs']['transcript']

#index route: Opens automaticaly on http://127.0.0.1:8000
@app.get('/')
async def index():
    return {'message':'Get Started: Uncovering Insights from your conversations'}


# Defining the API endpoint: that listens for POST requests at the '/generate_response
@app.post("/transcribe_audio")
async def transcribe_audio(audio_file:UploadFile = File(...)):
    try:
        #buffer_data = await audio_file.read()
        transcription = transcribe_audio_file(audio_file)
        return {"transcription": transcription}
    
    except Exception as e:
        return {"error": str(e)}
    
#Run with: uvicorn api:app --reload
    
#Errors:
#AuthenticationError:
