# Convo Insights

Convo Insights is a Streamlit-based web application that leverages cutting-edge AI models to uncover insights from audio conversations. With Convo Insights, you can upload audio files and get transcriptions of conversations, along with sentiment analysis, to gain deeper understanding and valuable insights.

<img width="952" alt="image" src="https://github.com/DennisChangach/Convo_Insight/assets/41690660/8eae5087-2b8a-4b3f-b254-38c5c541cd71">

## Features
- Upload audio files in MP3, M4A, or WAV format.
- Choose between different Language Learning Models (LLMs) such as GPT-3.5 Turbo, GPT-4 or Gemini Pro.
- Select transcription mode: Master (uses Deepgram model) or GrandMaster (uses Whisper model)
- Sentiment analysis using LLM models.
- Simple and intuitive user interface powered by Streamlit.

<img width="940" alt="image" src="https://github.com/DennisChangach/Convo_Insight/assets/41690660/aef1c73a-3b63-4dac-9684-54c5c960b86b">

Here's how to use the app on streamlit 
1. **Open the Web App**: Access the web app through the provided link. 🌐:https://convoinsight.streamlit.app

2. **Upload Audio File**:
   - Click on the "Browse Files" button.
   - Select an audio file in MP3, M4A, or WAV format from your device.
   - Ensure the file size is less than 25 MB to minimize latency. 🎵

3. **Select Large Language Model (LLM)**:
   - Choose the desired LLM from the drop-down menu.
   - Options include GPT-3.5 Turbo, GPT-4, or Gemini Pro. 🧠

4. **Select Transcription Mode**:
   - Choose the transcription mode:
     - **Master**: Uses the Deepgram model for transcription.
     - **GrandMaster**: Employs the Whisper model for transcription.
   - Select the appropriate mode based on your preference and requirements. 🎙️

5. **Initiate Transcription**:
   - Click on the "Transcribe" button to start the transcription process.
   - The selected audio file will be transcribed according to the chosen LLM and transcription mode.
   - Allow some time for the transcription to complete, depending on the size and complexity of the audio file. ⏳

6. **View Transcription Results**:
   - Once the transcription is complete, the results will be displayed on the web app interface.
   - Sentiment analysis using the selected LLM models will also be provided, offering insights into the emotional tone of the conversation. 📜

7. **Interpret and Analyze**:
   - Review the transcription and sentiment analysis provided by the web app.
   - You can also listen to the audio file uplaoded to cross check the analysis.
   - Analyze the sentiment, identify key insights, and extract valuable information from the conversation transcript. 💡

8. **Repeat as Needed**:
   - Feel free to upload additional audio files and run the transcription process again as needed.
   - Experiment with different LLMs and transcription modes to compare results and gain deeper insights into the conversation content. 🔁

9. **Enjoy the User-Friendly Interface**:
   - Streamlit provides a simple and intuitive user interface, making it easy to navigate and interact with the web app.
   - Enjoy the seamless experience while exploring conversation transcripts and sentiment analysis results. 🚀


## Challenges Faced
- Audio Transcription: Implementing audio transcription with the Whisper model posed challenges due to resource constraints (CPU & GPU) and latency issues.
- Error Handling: Ensuring robust error handling and exception management during audio transcription and sentiment analysis was crucial to provide a seamless user experience.
- Documentation for Open-source Models: Obtaining detailed documentation and understanding the intricacies of open-source models like WhisperX was challenging, requiring extensive experimentation and research.

## How to Run Locally
To run Convo Insights locally on your machine, follow these steps:

1. Clone the repository to your local machine:
```git clone https://github.com/your-username/convo-insights.git```

2. Install the required dependencies:
```pip install -r requirements.txt```

3. Install '``ffmpeg'`` on your device. 

4. Set up environment variables:
  - Create a ```.env``` file in the project directory.
  - Add the following environment variables and replace the placeholder values with your API keys:
    ```
    DEEPGRAM_API_KEY=your_deepgram_api_key
    GOOGLE_API_KEY=your_google_api_key
    OPENAI_API_KEY=your_openai_api_key
    LANGCHAIN_API_KEY=your_langchain_api_key```

5. Run the Streamlit app: ```streamlit run app.py```
6. Access the web application in your browser at http://localhost:8501
