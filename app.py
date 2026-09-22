import streamlit as st
from google import genai
from google.genai import types

# Page setup
st.set_page_config(page_title="AI Smart Lecture Notes", page_icon="🎓", layout="centered")

st.title("🎓 Smart Lecture Note-Taking Assistant")
st.write("Upload your lecture audio and whiteboard snapshot to generate revision notes.")

# API Key input in sidebar
with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.caption("Get your key at [Google AI Studio](https://aistudio.google.com/)")

# File Uploaders
audio_file = st.file_uploader("Upload Lecture Audio (.mp3, .wav)", type=["mp3", "wav", "m4a"])
image_file = st.file_uploader("Upload Whiteboard / Slide Photo (.jpg, .png)", type=["jpg", "jpeg", "png"])

if st.button("Generate Smart Notes", type="primary"):
    if not api_key:
        st.error("Please provide a Gemini API key in the sidebar.")
    elif not audio_file and not image_file:
        st.warning("Please upload at least an audio file or a whiteboard photo.")
    else:
        with st.spinner("Processing lecture contents with AI..."):
            try:
                # Initialize Gemini client
                client = genai.Client(api_key=api_key)

                contents = []

                # Attach whiteboard image if uploaded
                if image_file:
                    image_bytes = image_file.read()
                    contents.append(
                        types.Part.from_bytes(
                            data=image_bytes,
                            mime_type=image_file.type,
                        )
                    )

                # Attach lecture audio if uploaded
                if audio_file:
                    audio_bytes = audio_file.read()
                    contents.append(
                        types.Part.from_bytes(
                            data=audio_bytes,
                            mime_type=audio_file.type,
                        )
                    )

                # Prompt instructions for the AI
                prompt = """
                You are an expert academic tutor. Analyze the provided lecture audio and/or whiteboard snapshot.
                Generate a structured study guide with the following sections:

                1. **Executive Summary**: A concise 3-4 sentence overview of the topic discussed.
                2. **Key Concepts & Definitions**: Bulleted list explaining core formulas, terms, or ideas.
                3. **Detailed Lecture Notes**: Structured, well-formatted notes with clear headings.
                4. **5-Question Revision Quiz**: 5 multiple-choice questions with answers revealed at the bottom to test student comprehension.
                """
                contents.append(prompt)

                # Generate notes
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=contents,
                )

                st.success("Notes generated successfully!")
                st.markdown(response.text)

                # Download button for notes
                st.download_button(
                    label="Download Notes as Markdown",
                    data=response.text,
                    file_name="lecture_notes.md",
                    mime="text/markdown"
                )

            except Exception as e:
                st.error(f"Error processing lecture: {e}")