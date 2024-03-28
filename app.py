#importing the necessary dependencies:
import streamlit as st
from dotenv import load_dotenv
#from datetime import datetime
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from prompts import prompt_0,prompt_1
import os
import requests
import httpx
import whisperx

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

# Load the WhisperX model


# Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#Configuring Langsmith
#os.environ["LANGCHAIN_TRACING_V2"] = "true"
#os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# Load the LLM - Gemini Pro
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)

#Initilializing the output parser
#output_parser = StrOutputParser()

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
        mode = st.selectbox(
                            "Please select Mode",
                            ('Master','GrandMaster'),index=0)
        
        transcribe = st.button("Transcribe 📜")
    
    if audio_file and transcribe:
        with st.spinner("Transcribing..."):
            # When the file is uploaded: Pass the buffered audio file object
            try: 
               #Getting the transcription from the function
                if mode == 'Master':
                    #getting the transcript using Deepgram
                    transcript = transcribe_audio_file_dpg(audio_file)
                    #Getting the sentiments from the LLM
                    sentiment = generate_sentiment(transcript)
                    st.success("Done")
                elif mode == "GrandMaster":
                    transcript = transcribe_audio_file_wsp(audio_file)
                    st.success("Done")
                st.markdown(transcript)
                #st.markdown(sentiment)
            except Exception as e:
                st.write(e)


#Function to transcribe audio file
def transcribe_audio_file_dpg(audio_file):
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

#Function to generate transcript using Whisper X
def transcribe_audio_file_wsp(audio_file):
    #Specify the path to your local audio file
    # = "path/to/your/audio/file.wav"
    model = whisperx.load_model("MODELS")

    # Transcribe the audio file with speaker diarization
    result = model.transcribe(audio_file, language="en", task="transcribe,diarize")

    # Print the transcription
    print(result["text"])

    # Print the speaker information
    for segment in result["segments"]:
        speaker = segment["speaker"]
        start = segment["start"]
        end = segment["end"]
        text = segment["text"]
        print(f"Speaker {speaker} ({start:.2f} - {end:.2f}): {text}")

    return result

#generating sentiment
def generate_sentiment(transcript):
    my_prompt = prompt_0
  
    #Defining the prompt template
    prompt = PromptTemplate(input_variables=['transcript'],template=my_prompt)

    #Defining the LLM Chain
    chain = LLMChain(llm=llm,prompt=prompt,verbose=True)

    response = chain.run(transcript=transcript,
                         )
    return response

if __name__ == "__main__":
    main()
