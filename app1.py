import streamlit as st
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import TreebankWordTokenizer

# Download necessary NLTK resources safely
try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

# Initialize stemmer and tokenizer
ps = PorterStemmer()
tokenizer = TreebankWordTokenizer()

# Text preprocessing function
def transform_text(text):
    text = text.lower()
    text = tokenizer.tokenize(text)  # ✅ Using TreebankWordTokenizer to avoid punkt errors

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(ps.stem(i))

    return " ".join(y)

# Load vectorizer and model
tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

# Streamlit UI
st.set_page_config(page_title="SMS Spam Classifier", layout="centered")
st.markdown("<h1 style='text-align: center; color: #6c63ff;'>SMS Spam Classifier</h1>", unsafe_allow_html=True)

input_sms = st.text_area("Enter the message")

if st.button('Predict'):
    # Preprocess
    transformed_sms = transform_text(input_sms)

    # Vectorize
    vector_input = tfidf.transform([transformed_sms])

    # Predict
    result = model.predict(vector_input.toarray())[0]

    # Output
    if result == 1:
        st.error("Prediction: SPAM ❌")
    else:
        st.success("Prediction: NOT SPAM ✅")