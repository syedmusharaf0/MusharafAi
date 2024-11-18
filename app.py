import openai
import streamlit as st
import gradio as gr
import pyttsx3
import speech_recognition as sr
from PIL import Image

# Set your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Function to generate response from GPT-4
def generate_text(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()

# Function to generate image based on prompt
def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return response['data'][0]['url']

# Function to handle audio input and convert it to text
def listen_to_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand that."
    except sr.RequestError:
        return "Sorry, there was an issue with the speech recognition service."

# Create a response to the user
def assistant(text_input=None, image_input=None, audio_input=None):
    # If there is an audio input, convert it to text
    if audio_input:
        user_input = listen_to_audio()
    # If image input, generate image
    elif image_input:
        user_input = generate_image(image_input)
    # If there is a text input, generate a response
    elif text_input:
        user_input = generate_text(text_input)
    return user_input

# Create Streamlit interface
st.title("Musharaf AI Assistant")
st.markdown("Contact: mushumushu656@gmail.com")

# Create text input
text_input = st.text_input("Ask a Question:")
image_input = st.text_input("Generate an Image from Text:")
audio_input = st.button("Listen to Audio")

# Handle inputs and display responses
if text_input:
    response = assistant(text_input=text_input)
    st.text_area("Response:", value=response, height=200)

if image_input:
    response = assistant(image_input=image_input)
    st.image(response, caption="Generated Image", use_column_width=True)

if audio_input:
    response = assistant(audio_input=True)
    st.text_area("Audio Response:", value=response, height=200)

