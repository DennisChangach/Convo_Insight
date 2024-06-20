#importing the necessary dependencies:
import streamlit as st
from src.components.transcribe import Transcribe
from src.components.insights import Insights
from tempfile import NamedTemporaryFile

#Main function
def main():
    #page config
    st.set_page_config(page_title = "Convo Insights",page_icon = "🧠")

    st.title("💬 Uncovering Insights from your Conversations.💡")

    #Uploading Audio Files
    with st.sidebar:
        st.title("🛠️ Configuration:⚙️")
        #Uploading your audiofile
        st.text("Please upload your audio file: 🔊")
        audio_file = st.file_uploader("Upload audio file",type=["mp3","m4a","wav"])
        #Give a listen to your uploaded file:
        st.text("Listen to your uploaded audio: 🎧")
        st.audio(audio_file)
        
        #Selecting Mode of transacription: Either using Deepgram or Whisper Model
        mode = st.selectbox(
                            "Please select the Transcription Model",
                            ('Deepgram','Whisper'),index=0)
        
        if mode == 'Deepgram':
            #Get Deepgram API key here
            st.markdown("[Get Your Deepgram API key here](https://console.deepgram.com/signup?jump=keys)")
            DEEPGRAM_API_KEY = st.text_input('Please add your Deepgram API key',placeholder='Paste your API key here',type = 'password')
            
        elif mode == 'Whisper':
            st.markdown("*Please upload files under 25MB in size to ensure optimal processing with the Whisper model.*")
        
        
        #selecting LLM to use
        llm_type = st.selectbox(
                            "Please select LLM",
                            ('gpt-3.5-turbo','gemini-pro'),index=0)
        #Getting the LLMs keys
       
        LLM_API_KEY = st.text_input('Please add your LLM API key',placeholder='Paste your API key here',type = 'password')

        transcribe = st.button("Get Insights✨")
        
    if audio_file and transcribe:
        with st.spinner("Transcribing..."):
            # When the file is uploaded: Pass the UploadFile object
            try: 
                #Getting the transcription from the function
                if mode == 'Deepgram':
                    #getting the transcript using Deepgram
                    #Intializing the objects
                    transcribe = Transcribe(audio_file)
                    transcript = transcribe.transcribe_audio_file_dpg(DEEPGRAM_API_KEY)
                    
                elif mode == "Whisper":
                    with NamedTemporaryFile(delete=False) as temp:
                        # Write the user's uploaded file to the temporary file.
                        with open(temp.name, "wb") as temp_file:
                            temp_file.write(audio_file.read())
                    # Getting the transcript using Whisper Model.
                    #st.write("🔊 Our current Whisper model doesn't support speaker diarization yet. Each transcription will be provided as a single, unified text. We appreciate your understanding and patience as we continue to improve our services! 🚀")
                    transcribe = Transcribe(temp.name)
                    transcript = transcribe.transcribe_audio_file_wsp()     
            except Exception as e:
                #Error handling
                st.error(e)
                st.error(f"An error occurred: {type(e).__name__}: {str(e)}")
        #Summarization
        with st.spinner("Generating Transcript Summary..."):
            try:
                insights = Insights(transcript,mode,llm_type,LLM_API_KEY)
                summary = insights.generate_summary()
                #st.markdown(summary) 
            except Exception as e:
                #Error handling
                #st.error(e)
                st.error(f"An error occurred: {type(e).__name__}: {str(e)}")
      
        with st.spinner("Generating Insights..."):
            try:
                #Getting the sentiments from the LLM
                insights = Insights(transcript,mode,llm_type,LLM_API_KEY)
                insights = insights.generate_insights()   
            
            except Exception as e:
                #Error handling
                #st.error(e)
                st.error(f"An error occurred: {type(e).__name__}: {str(e)}")

        tab1,tab2,tab3 = st.tabs(['Transcript','Summarization','Conversation Insights'])
        with tab1:
            st.markdown(transcript)
        with tab2:
            st.markdown(summary)
        with tab3:
            st.markdown(insights)


    #if user hasn't uploaded audio file
    elif transcribe and audio_file is None:
        st.error("Please upload an audio file first!")



if __name__ == "__main__":
    main()
