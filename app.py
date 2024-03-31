#importing the necessary dependencies:
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from prompts import prompt_0,gd_prompt_0,prompt_1,prompt_coe
import os
import httpx
import whisper
import torch
from tempfile import NamedTemporaryFile
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

# Checking if NVIDIA GPU is available
torch.cuda.is_available()
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


# Load the LLM - Gemini Pro
# Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
gemini_llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)

#Loading openai models
OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")
gpt3_5_llm = ChatOpenAI(temperature=0.3, openai_api_key= OPENAI_API_KEY,model_name = "gpt-3.5-turbo-0125")
#gpt 4
gpt4_llm = ChatOpenAI(temperature=0.3, openai_api_key= OPENAI_API_KEY,model_name = "gpt-4")

#Configuring Langsmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

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
        #Uploading your audiofile
        st.text("Please upload your audio file: 🔊")
        audio_file = st.file_uploader("Upload audio file",type=["mp3","m4a","wav"])
        #Give a listen to your uploaded file:
        st.text("Listen to your uploaded audio: 🎧")
        st.audio(audio_file)
        
        #selecting LLM to use
        llm_type = st.selectbox(
                            "Please select LLM",
                            ('gpt-3.5-turbo','gpt-4','gemini-pro'),index=0)
        #Selecting Mode of transacription: Master or Grand Master: & Call the appropriate function for transacription
        mode = st.selectbox(
                            "Please select Mode",
                            ('Master','GrandMaster'),index=0)
        
        if mode == 'GrandMaster':
            st.write("Please upload files under 25MB in size to ensure optimal processing with our Whisper model.")
        
        transcribe = st.button("Transcribe 📜")
        
    if audio_file and transcribe:
        with st.spinner("Transcribing..."):
            # When the file is uploaded: Pass the UploadFile object
            try: 
               #Getting the transcription from the function
                if mode == 'Master':
                    #getting the transcript using Deepgram
                    transcript = transcribe_audio_file_dpg(audio_file)
                    
                elif mode == "GrandMaster":
                    with NamedTemporaryFile(delete=False) as temp:
                        # Write the user's uploaded file to the temporary file.
                        with open(temp.name, "wb") as temp_file:
                            temp_file.write(audio_file.read())
                    # Getting the transcript using Whisper Model.
                    st.write("🔊 Our current GrandMaster model doesn't support speaker diarization yet. Each transcription will be provided as a single, unified text. We appreciate your understanding and patience as we continue to improve our services! 🚀")
                    transcript = transcribe_audio_file_wsp(temp.name)
                    
                #Getting the sentiments from the LLM
                sentiment = generate_sentiment(transcript,mode,llm_type)   
                st.success("Done")
                #st.markdown(transcript)
                st.markdown(sentiment)
            except Exception as e:
                #Error handling
                st.error(f"An error occurred: {type(e).__name__}: {str(e)}")

    #if user hasn't uploaded audio file
    elif transcribe and audio_file is None:
        st.error("Please upload an audio file first!")



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
    #Loading whisper model
    model = whisper.load_model("base",device = DEVICE)

    #audio transcription
    result = model.transcribe(audio_file,fp16=False)

    # Print the transcription
    #print(result["text"])

    # return speaker information
    return result["text"]

#generating sentiment
def generate_sentiment(transcript,mode,llm_type):
    #Selecting the prompt based on the transcription mode
    if mode == 'Master':
        my_prompt = prompt_coe
    elif mode == "GrandMaster":
        my_prompt = gd_prompt_0

    #selecting the LLM based on the LLM selected
    if llm_type == "gpt-3.5-turbo":
        llm = gpt3_5_llm
    elif llm_type == 'gpt-4':
        llm = gpt4_llm
    elif llm_type == "gemini-pro":
        llm = gemini_llm
  
    #Defining the prompt template
    prompt = PromptTemplate(input_variables=['transcript'],template=my_prompt)

    #Defining the LLM Chain
    chain = LLMChain(llm=llm,prompt=prompt,verbose=True)

    response = chain.run(transcript=transcript,
                         )
    return response

if __name__ == "__main__":
    main()
