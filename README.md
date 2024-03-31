# Convo Insights

Convo Insights is a Streamlit-based web application that leverages cutting-edge AI models to uncover insights from audio conversations. With Convo Insights, you can upload audio files and get transcriptions of conversations, along with sentiment analysis, to gain deeper understanding and valuable insights.

<img width="952" alt="image" src="https://github.com/DennisChangach/Convo_Insight/assets/41690660/8eae5087-2b8a-4b3f-b254-38c5c541cd71">

## Features
- Upload audio files in MP3, M4A, or WAV format.
- Choose between different Language Learning Models (LLMs) such as GPT-3.5 Turbo or Gemini Pro.
- Select transcription mode: Master (uses Deepgram model) or GrandMaster (uses Whisper model)
- Sentiment analysis using LLM models.
- Simple and intuitive user interface powered by Streamlit.

Here's the link to the app on Streamlit Cloud:https://convoinsight.streamlit.app

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
