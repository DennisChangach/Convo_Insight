import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from src.components.prompts import gd_prompt_0,prompt_coe,prompt_summary

# Load environment variables
load_dotenv()

#Configuring Langsmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")


class Insights:
    def __init__(self,transcript,mode,llm_type,LLM_API_KEY):
        self.transcript = transcript
        self.mode = mode
        self.llm_type = llm_type
        self.llm_api_key = LLM_API_KEY
    #generating sentiment
    def generate_insights(self):
        #Selecting the prompt based on the transcription mode
        if self.mode == 'Deepgram':
            my_prompt = prompt_coe
        elif self.mode == "Whsiper":
            my_prompt = gd_prompt_0

        llm = get_LLM(llm_type = self.llm_type,llm_api_key = self.llm_api_key)
    
        #Defining the prompt template
        prompt = PromptTemplate(input_variables=['transcript'],template=my_prompt)

        #Defining the LLM Chain
        chain = LLMChain(llm=llm,prompt=prompt,verbose=True)

        response = chain.run(transcript=self.transcript,
                            )
        return response
    
    #Generating Transcript Summary
    def generate_summary(self):
        my_prompt = prompt_summary

        llm = get_LLM(llm_type = self.llm_type,llm_api_key = self.llm_api_key)
    
        #Defining the prompt template
        prompt = PromptTemplate(input_variables=['transcript'],template=my_prompt)

        #Defining the LLM Chain
        chain = LLMChain(llm=llm,prompt=prompt,verbose=True)

        response = chain.run(transcript=self.transcript,
                            )
        return response
    
#Getting LLM
def get_LLM(llm_type,llm_api_key):
    #selecting the LLM based on the LLM selected
    if llm_type == "gpt-3.5-turbo":
        if llm_api_key:
            llm = ChatOpenAI(temperature=0, openai_api_key= llm_api_key,model_name = "gpt-3.5-turbo-0125")
        else:
            #Loading openai models
            OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")
            llm = ChatOpenAI(temperature=0, openai_api_key= OPENAI_API_KEY,model_name = "gpt-3.5-turbo-0125")

        
    elif llm_type == "gemini-pro":
        if llm_api_key:
            genai.configure(api_key=llm_api_key)
        
        else:
            # Configure the API key
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            
        llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3,google_api_key = llm_api_key)

    return llm