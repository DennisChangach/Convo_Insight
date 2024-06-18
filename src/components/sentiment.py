import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from src.components.prompts import prompt_0,gd_prompt_0,prompt_1,prompt_coe

# Load environment variables
load_dotenv()

# Load the LLM - Gemini Pro
# Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
gemini_llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.3)

#Loading openai models
OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")
gpt3_5_llm = ChatOpenAI(temperature=0, openai_api_key= OPENAI_API_KEY,model_name = "gpt-3.5-turbo-0125")
#gpt 4
gpt4_llm = ChatOpenAI(temperature=0, openai_api_key= OPENAI_API_KEY,model_name = "gpt-4")

#Configuring Langsmith
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")


class Sentiment:
    def __init__(self,transcript,mode,llm_type):
        self.transcript = transcript
        self.mode = mode
        self.llm_type = llm_type
    #generating sentiment
    def generate_sentiment(self):
        #Selecting the prompt based on the transcription mode
        if self.mode == 'Deepgram':
            my_prompt = prompt_coe
        elif self.mode == "Whsiper":
            my_prompt = gd_prompt_0

        #selecting the LLM based on the LLM selected
        if self.llm_type == "gpt-3.5-turbo":
            llm = gpt3_5_llm
        elif self.llm_type == 'gpt-4':
            llm = gpt4_llm
        elif self.llm_type == "gemini-pro":
            llm = gemini_llm
    
        #Defining the prompt template
        prompt = PromptTemplate(input_variables=['transcript'],template=my_prompt)

        #Defining the LLM Chain
        chain = LLMChain(llm=llm,prompt=prompt,verbose=True)

        response = chain.run(transcript=self.transcript,
                            )
        return response