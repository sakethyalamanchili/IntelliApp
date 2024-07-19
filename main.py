import os
import streamlit as st
from streamlit_option_menu import option_menu
from gemini_utility import load_gemini_pro_model, gemini_pro_vision_response, embedding_model_response, gemini_pro_response
from PIL import Image

# Get the working directory
working_directory = os.path.dirname(os.path.abspath(__file__))

# Setting up the page config
st.set_page_config(
    page_title="IntelliApp",
    page_icon="🧠",
    layout="centered"
)

# Sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title="IntelliApp",
        options=["ChatBot", "Image Captioning", "Embed Text", "Ask me Anything", "Coding Assistant", "Sentiment Analysis", "Summarize Text", "Help"],
        menu_icon='robot',
        icons=['chat-dots-fill', 'image-fill', 'textarea-t', 'patch-question-fill', 'code-slash', 'emoji-smile-fill', 'file-text-fill', 'info-circle'],
        default_index=0
    )

# Function to translate role between gemini-pro and streamlit terminology
def translate_role_for_streamlit(role):
    return "assistant" if role == 'model' else role

# ChatBot Page
if selected == "ChatBot":
    st.title("🤖 ChatBot")
    st.markdown("**Hint:** Ask anything related to general knowledge, trivia, or specific information you need.")
    
    model = load_gemini_pro_model()
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])
    
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)
    
    user_prompt = st.chat_input("Ask IntelliApp...")
    if user_prompt:
        with st.spinner('Generating response...'):
            st.chat_message("user").markdown(user_prompt)
            gemini_response = st.session_state.chat_session.send_message(user_prompt)
            with st.chat_message("assistant"):
                st.markdown(gemini_response.text)

# Image Captioning Page
if selected == "Image Captioning":
    st.title("📸 Snap Narrate")
    st.markdown("**Hint:** Upload an image file to generate a descriptive caption.")
    
    uploaded_image = st.file_uploader("", type=["jpg", "jpeg", "png"])
    if uploaded_image:
        if st.button("Generate Caption"):
            with st.spinner('Generating caption...'):
                image = Image.open(uploaded_image)
                col1, col2 = st.columns(2)
                with col1:
                    st.image(image)
                default_prompt = """Analyze the content of this image and generate a 
                                    detailed and descriptive caption that highlights 
                                    the main objects, scene, and context. 
                                    Make the caption engaging and informative, 
                                    capturing the essence of the moment shown in the image."""
                caption = gemini_pro_vision_response(default_prompt, image)
                with col2:
                    st.info(caption)
    else:
        st.warning("Please upload an image file.")

# Text Embedding Page
if selected == "Embed Text":
    st.title("🔡 Embed Text")
    st.markdown("**Hint:** Enter a block of text for which you need embeddings. Embeddings can be used for tasks like semantic search, clustering, and classification.")
    
    input_text = st.text_area(label="", placeholder="Enter the text to get the embeddings")
    if st.button("Get Embeddings"):
        with st.spinner('Generating embeddings...'):
            response = embedding_model_response(input_text)
            st.markdown(response)

# Question Answering Page
if selected == "Ask me Anything":
    st.title("❓ Ask me Anything")
    st.markdown("**Hint:** Ask any question to get a detailed and informative answer.")
    
    user_prompt = st.text_area(label="", placeholder="Ask IntelliApp...")
    if st.button("Get an answer"):
        with st.spinner('Generating answer...'):
            response = gemini_pro_response(user_prompt)
            st.markdown(response)

# Coding Assistant Page
if selected == "Coding Assistant":
    st.title("💻 Coding Assistant")
    st.markdown("**Hint:** Describe the coding problem or task you need help with. Be as detailed as possible.")
    
    coding_task = st.text_area(label="", placeholder="Describe the coding task or problem...")
    language = st.selectbox("Select programming language", ["Python", "JavaScript", "Java", "C++", "Go", "Ruby", "Swift", "PHP", "C#", "Other"], help="Choose the programming language for the code snippet.")
    if st.button("Generate Code"):
        with st.spinner('Generating code...'):
            prompt = f"Generate a unique code snippet in {language} for the following task:\n{coding_task}"
            response = gemini_pro_response(prompt)
            code = response.strip().replace(f"```{language.lower()}", "").replace("```", "")
            st.code(code)

# Sentiment Analysis Page
if selected == "Sentiment Analysis":
    st.title("😊 Sentiment Analysis")
    st.markdown("**Hint:** Enter text to analyze its sentiment (positive, negative, neutral).")
    
    input_text = st.text_area(label="", placeholder="Enter the text to analyze sentiment")
    if st.button("Analyze Sentiment"):
        with st.spinner('Analyzing sentiment...'):
            prompt = f"Analyze the sentiment of the following text:\n{input_text}"
            response = gemini_pro_response(prompt)
            st.markdown(response)

# Summarize Text Page
if selected == "Summarize Text":
    st.title("📝 Summarize Text")
    st.markdown("**Hint:** Enter a block of text to get a concise summary.")
    
    input_text = st.text_area(label="", placeholder="Enter the text to summarize")
    if st.button("Summarize"):
        with st.spinner('Summarizing text...'):
            prompt = f"Please summarize the following text in a brief and concise manner:\n\n{input_text}"
            response = gemini_pro_response(prompt)
            st.markdown(response)

# Help Page
if selected == "Help":
    st.title("Help & Documentation")
    
    st.markdown("""
        ### Welcome to IntelliApp!

        IntelliApp provides various AI-powered functionalities to assist with tasks ranging from chatting with an AI model to generating code snippets and analyzing text. Below you'll find detailed information on how to use each feature.

        ## Features Overview
        
        **1. ChatBot**
        - **What you can ask:** General knowledge questions, trivia, specific information you need, or just have a conversation.
        - **What you should avoid:** Asking for sensitive personal advice or highly specialized professional advice.
        - **Example Question:** "Can you explain the theory of relativity?"
        
        **2. Image Captioning**
        - **How it works:** Upload an image to generate a descriptive caption.
        - **What you should avoid:** Uploading images with sensitive or personal content.
        - **Example Image:** A photo of a sunset for which the AI will generate a descriptive caption.
        
        **3. Embed Text**
        - **How it works:** Input a block of text to obtain embeddings which can be used for tasks like semantic search or classification.
        - **What you should avoid:** Providing excessively long texts as it may affect performance.
        - **Example Text:** "Machine learning is a method of data analysis that automates analytical model building."
        
        **4. Ask me Anything**
        - **What you can ask:** Any question you have, whether it's a factual query or a general topic.
        - **What you should avoid:** Asking for specific medical, legal, or financial advice.
        - **Example Question:** "What are the benefits of exercise?"
        
        **5. Coding Assistant**
        - **How it works:** Describe the coding problem or task, and select the programming language to generate a code snippet.
        - **What you should avoid:** Asking for code related to sensitive data handling or security vulnerabilities.
        - **Example Task:** "Generate a Python function that sorts a list of numbers in ascending order."
        
        **6. Sentiment Analysis**
        - **How it works:** Analyze the sentiment of a given text.
        - **What you should avoid:** Providing text with unclear or ambiguous sentiment.
        - **Example Text:** "I love using IntelliApp because it makes my work easier."
        
        **7. Summarize Text**
        - **How it works:** Enter a block of text to get a concise summary.
        - **What you should avoid:** Providing extremely long texts as it might not capture the full context.
        - **Example Text:** "IntelliApp provides a range of AI functionalities including chat, text analysis, and code generation. It's designed to be user-friendly and versatile."
        
        ## Frequently Asked Questions (FAQs)

        **Q1: How do I start using IntelliApp?**
        - A: Simply select the feature you are interested in from the sidebar menu and follow the on-screen instructions.

        **Q2: Can I use IntelliApp for commercial purposes?**
        - A: Please review the terms of service for any usage restrictions related to commercial purposes.

        **Q3: What should I do if I encounter an issue?**
        - A: If you experience any issues, please contact our support team or check the help section for troubleshooting tips.

        **Q4: Is there a limit to how much text or how many images I can process?**
        - A: While there are no strict limits, processing large texts or images may impact performance. It’s best to keep inputs within reasonable sizes.

        **Q5: How do I provide feedback or suggest improvements?**
        - A: Feedback can be sent via the contact form in the support section or through our feedback email address.

        ## Tips for Using IntelliApp

        - **Be Specific:** The more specific your input, the better the responses. For example, instead of asking "Tell me about Python," ask "How do I use Python for data analysis?"
        - **Keep Inputs Clear:** Avoid overly complex or ambiguous queries for better results.
        - **Explore Features:** Try different features to fully understand what IntelliApp can do for you.

        ## Contact Support

        If you have any further questions or need additional help, please reach out to our support team at [saketh.engineer@gmail.com](mailto:saketh.engineer@gmail.com).

        Thank you for using IntelliApp!
    """)
