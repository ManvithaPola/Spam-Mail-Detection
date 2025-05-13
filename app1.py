import streamlit as st
import pickle
import string
import nltk
import os
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import word_tokenize

# Ensure nltk_data path is added correctly
nltk_data_path = os.path.join(os.path.dirname(__file__), 'nltk_data')
nltk.data.path.append(nltk_data_path)

# Download required resources to the local directory
nltk.download('punkt', download_dir=nltk_data_path)
nltk.download('stopwords', download_dir=nltk_data_path)

ps = PorterStemmer()

def transform_text(text):
    text = text.lower()
    
    # Force language to 'english' to avoid punkt_tab issue
    tokens = word_tokenize(text, language="english")

    filtered_tokens = []
    for token in tokens:
        if token.isalnum():
            filtered_tokens.append(token)

    cleaned_tokens = []
    for token in filtered_tokens:
        if token not in stopwords.words('english'):
            cleaned_tokens.append(ps.stem(token))

    return " ".join(cleaned_tokens)

# Load pre-trained models
tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

# Streamlit UI
st.title("Email/SMS Spam Classifier")

input_sms = st.text_area("Enter the message")

if st.button('Predict'):
    # 1. Preprocess
    transformed_sms = transform_text(input_sms)
    # 2. Vectorize
    vector_input = tfidf.transform([transformed_sms])
    # 3. Predict
    result = model.predict(vector_input.toarray())[0]
    # 4. Display
    st.header("Spam" if result == 1 else "Not Spam")