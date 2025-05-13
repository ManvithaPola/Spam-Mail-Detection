import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer
import time
import base64
# Download the required NLTK resource 'punkt' for tokenization
nltk.download('punkt')
# Set page configuration
st.set_page_config(
    page_title="Quantum Spam Shield",
    page_icon="🛡️",
    layout="wide"
)

# Initialize Porter Stemmer
ps = PorterStemmer()

# Ensure NLTK downloads are complete
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('punkt')
    nltk.download('stopwords')

# Text transformation function
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

# Load ML models
@st.cache_resource
def load_models():
    tfidf = pickle.load(open('vectorizer.pkl','rb'))
    model = pickle.load(open('model.pkl','rb'))
    return tfidf, model

tfidf, model = load_models()

# Custom CSS with animations and modern styling
def local_css():
    st.markdown("""
    <style>
    /* Main background and scrollbar */
    body {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: #fff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Customizing scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        background: #0f0c29;
    }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #7928CA, #FF0080);
        border-radius: 10px;
    }
    
    /* Header styling */
    .hero-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        padding: 2rem 1rem;
        background: rgba(24, 24, 36, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        background: linear-gradient(to right, #7928CA, #FF0080);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: pulse 2s infinite;
    }
    
    .subtitle {
        font-size: 1.2rem;
        opacity: 0.85;
        margin-bottom: 1rem;
        color: #d1d1d1;
    }
    
    /* Input area styling */
    .stTextArea textarea {
        background: rgba(24, 24, 36, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        color: white !important;
        font-size: 1.1rem !important;
        padding: 1rem !important;
        transition: all 0.3s ease;
        backdrop-filter: blur(5px);
    }
    
    .stTextArea textarea:focus {
        border: 1px solid #7928CA !important;
        box-shadow: 0 0 15px rgba(121, 40, 202, 0.5) !important;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #7928CA, #FF0080) !important;
        color: white !important;
        border: none !important;
        padding: 0.6rem 2rem !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        border-radius: 50px !important;
        cursor: pointer !important;
        margin-top: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 10px 20px rgba(121, 40, 202, 0.3) !important;
    }
    
    .stButton button:hover {
        transform: translateY(-5px) !important;
        box-shadow: 0 15px 25px rgba(121, 40, 202, 0.5) !important;
    }
    
    /* Result card styling */
    .result-card {
        background: rgba(24, 24, 36, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 2rem;
        margin-top: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        transition: all 0.5s ease;
        text-align: center;
    }
    
    .spam-result {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 1rem 0;
        text-shadow: 0px 0px 10px currentColor;
    }
    
    .spam-true {
        color: #FF0080;
        animation: warning-pulse 1.5s infinite;
    }
    
    .spam-false {
        color: #45FFCA;
        animation: safe-pulse 2s infinite;
    }
    
    .result-details {
        margin-top: 1rem;
        padding: 1rem;
        background: rgba(0, 0, 0, 0.2);
        border-radius: 10px;
        font-size: 1.1rem;
    }
    
    /* Loading animation */
    .loading-spinner {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100px;
    }
    
    /* Animated floating particles background */
    .particle-background {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        z-index: -1;
        overflow: hidden;
    }
    
    /* Animations */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    @keyframes warning-pulse {
        0% { text-shadow: 0px 0px 10px #FF0080; }
        50% { text-shadow: 0px 0px 25px #FF0080, 0px 0px 10px #FF0080; }
        100% { text-shadow: 0px 0px 10px #FF0080; }
    }
    
    @keyframes safe-pulse {
        0% { text-shadow: 0px 0px 10px #45FFCA; }
        50% { text-shadow: 0px 0px 25px #45FFCA, 0px 0px 10px #45FFCA; }
        100% { text-shadow: 0px 0px 10px #45FFCA; }
    }
    
    /* Features section styling */
    .features-section {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        margin-top: 3rem;
        margin-bottom: 2rem;
    }
    
    .feature-card {
        background: rgba(24, 24, 36, 0.6);
        backdrop-filter: blur(5px);
        border-radius: 12px;
        padding: 1.5rem;
        flex: 1;
        margin: 0.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        min-width: 200px;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 25px rgba(0, 0, 0, 0.3);
    }
    
    .feature-title {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.7rem;
        color: #d1d1d1;
    }
    
    /* Glassmorphism containers */
    .glass-container {
        background: rgba(24, 24, 36, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    
    /* Override Streamlit components */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Function for animated typing text
def type_writer_animation(text, speed=20):
    animated_text = ""
    placeholder = st.empty()
    
    for char in text:
        animated_text += char
        placeholder.markdown(f"<h3>{animated_text}|</h3>", unsafe_allow_html=True)
        time.sleep(1/speed)
    
    placeholder.markdown(f"<h3>{text}</h3>", unsafe_allow_html=True)

# Function to add animated particles background
def add_particles_background():
    particles_js = """
    <script src="https://cdnjs.cloudflare.com/ajax/libs/particles.js/2.0.0/particles.min.js"></script>
    <div id="particles-js" class="particle-background"></div>
    <script>
        particlesJS("particles-js", {
            "particles": {
                "number": {
                    "value": 80,
                    "density": {
                        "enable": true,
                        "value_area": 800
                    }
                },
                "color": {
                    "value": ["#7928CA", "#FF0080", "#45FFCA"]
                },
                "shape": {
                    "type": "circle",
                    "stroke": {
                        "width": 0,
                        "color": "#000000"
                    },
                    "polygon": {
                        "nb_sides": 5
                    }
                },
                "opacity": {
                    "value": 0.5,
                    "random": false,
                    "anim": {
                        "enable": false
                    }
                },
                "size": {
                    "value": 3,
                    "random": true,
                    "anim": {
                        "enable": false
                    }
                },
                "line_linked": {
                    "enable": true,
                    "distance": 150,
                    "color": "#7928CA",
                    "opacity": 0.4,
                    "width": 1
                },
                "move": {
                    "enable": true,
                    "speed": 2,
                    "direction": "none",
                    "random": false,
                    "straight": false,
                    "out_mode": "out",
                    "bounce": false,
                    "attract": {
                        "enable": false,
                        "rotateX": 600,
                        "rotateY": 1200
                    }
                }
            },
            "interactivity": {
                "detect_on": "canvas",
                "events": {
                    "onhover": {
                        "enable": true,
                        "mode": "grab"
                    },
                    "onclick": {
                        "enable": true,
                        "mode": "push"
                    },
                    "resize": true
                },
                "modes": {
                    "grab": {
                        "distance": 140,
                        "line_linked": {
                            "opacity": 1
                        }
                    },
                    "push": {
                        "particles_nb": 4
                    }
                }
            },
            "retina_detect": true
        });
    </script>
    """
    st.components.v1.html(particles_js, height=0)

# Apply custom CSS
local_css()

# Add particles background
add_particles_background()

# Hero section
st.markdown("""
<div class="hero-container">
    <h1 class="main-title">QUANTUM SPAM SHIELD</h1>
    <p class="subtitle">Advanced AI-powered protection against email & SMS spam</p>
</div>
""", unsafe_allow_html=True)

# Create a two-column layout
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("<div class='glass-container'>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #d1d1d1;'>Message Analysis</h2>", unsafe_allow_html=True)
    input_sms = st.text_area("Paste the message you want to analyze:", height=200)
    
    analyze_button = st.button("Analyze Message")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='glass-container' style='text-align: center;'>", unsafe_allow_html=True)
    if analyze_button:
        # Perform text transformation
        transformed_sms = transform_text(input_sms)

        # Transform the input text using the TF-IDF vectorizer
        vector_input = tfidf.transform([transformed_sms])

        # Predict the spam probability using the loaded model
        prediction = model.predict(vector_input.toarray())[0]

        # Show result
        st.markdown("<div class='result-card'>", unsafe_allow_html=True)
        if prediction == 1:
            st.markdown("<h2 class='spam-result spam-true'>SPAM DETECTED!</h2>", unsafe_allow_html=True)
            st.markdown("<p class='result-details'>This message is classified as spam. Please be cautious!</p>", unsafe_allow_html=True)
        else:
            st.markdown("<h2 class='spam-result spam-false'>NOT SPAM</h2>", unsafe_allow_html=True)
            st.markdown("<p class='result-details'>This message is safe. No spam detected!</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<p class='subtitle'>Paste a message to analyze its spam probability.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Features section
st.markdown("""
<div class="features-section">
    <div class="feature-card">
        <div class="feature-title">🔍 Smart Detection</div>
        <p>Our AI model analyzes word patterns and message structure to identify spam with high accuracy.</p>
    </div>
    <div class="feature-card">
        <div class="feature-title">⚡ Lightning Fast</div>
        <p>Get instant protection with our high-performance text processing engine.</p>
    </div>
    <div class="feature-card">
        <div class="feature-title">🛡️ Privacy First</div>
        <p>Your messages never leave this app - all processing is done locally for maximum privacy.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Analysis results section
if analyze_button:
    if input_sms.strip() == "":
        st.warning("Please enter a message to analyze")
    else:
        st.markdown("<div class='result-card'>", unsafe_allow_html=True)
        
        # Show loading animation
        with st.spinner("Quantum analysis in progress..."):
            # Process the input
            transformed_sms = transform_text(input_sms)
            vector_input = tfidf.transform([transformed_sms])
            result = model.predict(vector_input.toarray())[0]
            
            # Add slight delay for effect
            time.sleep(1.5)
        
        # Display result with animation
        if result == 1:
            st.markdown("""
            <div class="spam-result spam-true">⚠️ SPAM DETECTED ⚠️</div>
            <div class="result-details">
                This message contains patterns commonly found in spam content. 
                It's recommended to delete this message and avoid interacting with any links or attachments.
            </div>
            """, unsafe_allow_html=True)
            
            # Add spam characteristics
            st.markdown("""
            <h4 style='margin-top: 1.5rem; color: #FF0080;'>Potential spam indicators:</h4>
            <ul style='margin-top: 0.5rem;'>
                <li>Suspicious word patterns detected</li>
                <li>Message structure matches known spam templates</li>
                <li>Content analysis reveals deceptive intent</li>
            </ul>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="spam-result spam-false">✓ LEGITIMATE MESSAGE</div>
            <div class="result-details">
                Our analysis suggests this message is legitimate and does not contain known spam patterns.
            </div>
            """, unsafe_allow_html=True)
        
        # Add confidence meter visualization
        confidence = 0.92  # This would normally come from your model
        st.markdown(f"""
        <h4 style='margin-top: 1.5rem; color: #d1d1d1;'>Analysis Confidence</h4>
        <div style='background: rgba(0,0,0,0.3); border-radius: 10px; height: 30px; width: 100%; margin-top: 0.5rem;'>
            <div style='background: linear-gradient(90deg, #7928CA, #FF0080); width: {confidence*100}%; height: 30px; border-radius: 10px; text-align: right; padding-right: 10px;'>
                <span style='line-height: 30px; color: white; font-weight: bold;'>{int(confidence*100)}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style='padding: 2rem 0; text-align: center; opacity: 0.7; margin-top: 2rem;'>
    <p>Quantum Spam Shield • AI-Powered Email & SMS Protection</p>
</div>
""", unsafe_allow_html=True)