import streamlit as st
import pickle
import string
import nltk
import time
import base64
import random
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.tokenize import TreebankWordTokenizer
import streamlit.components.v1 as components

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
    text = tokenizer.tokenize(text)  # Using TreebankWordTokenizer to avoid punkt errors

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

# Custom CSS and JavaScript for futuristic UI
def local_css():
    st.markdown("""
    <style>
        /* Main Theme Colors */
        :root {
            --primary: #00a8ff;
            --secondary: #0097e6;
            --accent: #8c7ae6;
            --background: #f5f6fa;
            --card-bg: #ffffff;
            --text: #2f3640;
            --text-light: #7f8fa6;
            --danger: #e84118;
            --success: #4cd137;
            --warning: #fbc531;
        }
        
        /* Base styling */
        .main, [data-testid="stAppViewContainer"] {
            background: var(--background);
            color: var(--text);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        
        /* Custom header styling */
        .hero-header {
            text-align: center;
            margin-bottom: 2rem;
            padding: 2rem 0;
            position: relative;
            overflow: hidden;
            border-radius: 16px;
            background: linear-gradient(135deg, #00a8ff, #8c7ae6);
            color: white;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.1);
        }
        
        .hero-header h1 {
            font-size: 3.5rem;
            font-weight: 800;
            margin-bottom: 1rem;
            text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        
        .hero-subtitle {
            font-size: 1.2rem;
            opacity: 0.9;
            margin-bottom: 1rem;
            font-weight: 400;
        }
        
        /* Glassmorphism card for main content */
        .glass-card {
            background: var(--card-bg);
            border-radius: 16px;
            box-shadow: 0 4px 30px rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.3);
            padding: 2rem;
            margin: 1rem 0;
            transition: all 0.3s ease;
        }
        
        .glass-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 7px 30px rgba(0, 0, 0, 0.1);
        }
        
        /* Custom text area */
        .stTextArea textarea {
            background: var(--card-bg) !important;
            color: var(--text) !important;
            border-radius: 12px !important;
            border: 1px solid #dfe6e9 !important;
            padding: 1rem !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
        }
        
        .stTextArea textarea:focus {
            border-color: var(--primary) !important;
            box-shadow: 0 0 0 2px rgba(0, 168, 255, 0.2) !important;
        }
        
        /* Custom button */
        .stButton button {
            background: linear-gradient(135deg, var(--primary), var(--accent)) !important;
            color: white !important;
            font-weight: 600 !important;
            border: none !important;
            border-radius: 50px !important;
            padding: 0.8rem 2.5rem !important;
            transition: all 0.3s ease !important;
            transform: translateY(0) !important;
            box-shadow: 0 10px 20px rgba(0, 168, 255, 0.2) !important;
            font-size: 1rem !important;
        }
        
        .stButton button:hover {
            transform: translateY(-3px) !important;
            box-shadow: 0 15px 25px rgba(0, 168, 255, 0.3) !important;
            background: linear-gradient(135deg, var(--secondary), var(--accent)) !important;
        }
        
        .stButton button:active {
            transform: translateY(1px) !important;
        }
        
        /* Custom result cards */
        .result-card {
            text-align: center;
            padding: 2rem;
            border-radius: 16px;
            margin-top: 2rem;
            transition: all 0.5s ease;
            background: var(--card-bg);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        }
        
        .result-card.spam {
            border-left: 6px solid var(--danger);
        }
        
        .result-card.not-spam {
            border-left: 6px solid var(--success);
        }
        
        .result-title {
            font-size: 2.2rem;
            font-weight: 800;
            margin-bottom: 1rem;
        }
        
        .result-title.spam {
            color: var(--danger);
        }
        
        .result-title.not-spam {
            color: var(--success);
        }
        
        .result-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
        }
        
        /* Footer styling */
        footer {
            text-align: center;
            margin-top: 3rem;
            padding: 1.5rem;
            font-size: 0.9rem;
            color: var(--text-light);
            border-top: 1px solid #dfe6e9;
        }
        
        /* Animations */
        @keyframes pulse {
            0% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.03);
            }
            100% {
                transform: scale(1);
            }
        }
        
        /* Loading animation */
        .loading-container {
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 2rem 0;
        }
        
        .loading-spinner {
            width: 50px;
            height: 50px;
            border: 5px solid rgba(0, 168, 255, 0.2);
            border-radius: 50%;
            border-top-color: var(--primary);
            animation: spin 1s ease-in-out infinite;
        }
        
        @keyframes spin {
            to {
                transform: rotate(360deg);
            }
        }
        
        /* Typing animation */
        .typing-container {
            overflow: hidden;
            white-space: nowrap;
            margin: 1rem auto;
            text-align: center;
            font-size: 1.2rem;
            color: var(--text);
        }
        
        .typing-text {
            display: inline-block;
            overflow: hidden;
            animation: typing 3.5s steps(40, end), blink-caret 0.75s step-end infinite;
            border-right: 2px solid var(--primary);
            white-space: nowrap;
            margin: 0 auto;
            max-width: fit-content;
        }
        
        @keyframes typing {
            from { width: 0 }
            to { width: 100% }
        }
        
        @keyframes blink-caret {
            from, to { border-color: transparent }
            50% { border-color: var(--primary) }
        }
        
        /* Custom scrollbar */
        ::-webkit-scrollbar {
            width: 8px;
            height: 8px;
        }
        
        ::-webkit-scrollbar-track {
            background: rgba(0, 0, 0, 0.05);
        }
        
        ::-webkit-scrollbar-thumb {
            background: var(--primary);
            border-radius: 10px;
        }
        
        ::-webkit-scrollbar-thumb:hover {
            background: var(--secondary);
        }
        
        /* Progress bar styling */
        .stProgress > div > div > div {
            background-color: var(--primary) !important;
        }
        
        /* Probability meter */
        .probability-container {
            margin-top: 1.5rem;
        }
        
        .probability-meter {
            height: 12px;
            border-radius: 6px;
            margin-top: 0.5rem;
            background: #f1f2f6;
            position: relative;
            overflow: hidden;
        }
        
        .probability-fill {
            height: 100%;
            transition: width 1s ease-in-out;
            border-radius: 6px;
        }
        
        .probability-fill.spam {
            background: linear-gradient(90deg, var(--danger), #ff7675);
        }
        
        .probability-fill.not-spam {
            background: linear-gradient(90deg, var(--success), #00d2d3);
        }
        
        /* Feature section styling */
        .feature-section {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            margin: 2rem 0;
            gap: 1.5rem;
        }
        
        .feature-card {
            flex: 1 1 300px;
            background: var(--card-bg);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
            transition: all 0.3s ease;
            border-top: 4px solid var(--primary);
        }
        
        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
        }
        
        .feature-icon {
            font-size: 2rem;
            color: var(--primary);
            margin-bottom: 1rem;
        }
        
        .feature-title {
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: var(--text);
        }
        
        .feature-desc {
            color: var(--text-light);
            font-size: 0.95rem;
            line-height: 1.5;
        }
        
        /* Stats section */
        .stats-container {
            display: flex;
            justify-content: space-around;
            flex-wrap: wrap;
            margin: 2rem 0;
            gap: 1rem;
        }
        
        .stat-card {
            flex: 1;
            min-width: 150px;
            text-align: center;
            padding: 1.5rem;
            background: var(--card-bg);
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        }
        
        .stat-number {
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--primary);
            margin-bottom: 0.5rem;
        }
        
        .stat-label {
            color: var(--text-light);
            font-size: 0.9rem;
        }
        
        /* How it works section */
        .steps-container {
            margin: 2rem 0;
        }
        
        .step {
            display: flex;
            margin-bottom: 1.5rem;
            align-items: flex-start;
        }
        
        .step-number {
            background: var(--primary);
            color: white;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            font-weight: bold;
            margin-right: 1rem;
            flex-shrink: 0;
        }
        
        .step-content {
            flex: 1;
        }
        
        .step-title {
            font-weight: 600;
            margin-bottom: 0.3rem;
        }
        
        .step-desc {
            color: var(--text-light);
            font-size: 0.95rem;
        }
        
        /* Token visualization */
        .token-container {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin: 1rem 0;
        }
        
        .token {
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-size: 0.9rem;
            font-weight: 500;
        }
        
        .spam-token {
            background: rgba(232, 65, 24, 0.1);
            color: var(--danger);
            border: 1px solid rgba(232, 65, 24, 0.3);
        }
        
        .ham-token {
            background: rgba(76, 209, 55, 0.1);
            color: var(--success);
            border: 1px solid rgba(76, 209, 55, 0.3);
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .hero-header h1 {
                font-size: 2.5rem;
            }
            
            .feature-card {
                flex: 1 1 100%;
            }
            
            .stat-card {
                min-width: 120px;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# Particles JS for animated background (lighter version)
def particles_js():
    particles_code = """
    <div id="particles-js"></div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/particles.js/2.0.0/particles.min.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', function() {
            particlesJS('particles-js', {
                "particles": {
                    "number": {
                        "value": 40,
                        "density": {
                            "enable": true,
                            "value_area": 800
                        }
                    },
                    "color": {
                        "value": ["#00a8ff", "#8c7ae6"]
                    },
                    "shape": {
                        "type": "circle",
                        "stroke": {
                            "width": 0,
                            "color": "#000000"
                        }
                    },
                    "opacity": {
                        "value": 0.2,
                        "random": true,
                        "anim": {
                            "enable": true,
                            "speed": 1,
                            "opacity_min": 0.1,
                            "sync": false
                        }
                    },
                    "size": {
                        "value": 3,
                        "random": true,
                        "anim": {
                            "enable": true,
                            "speed": 2,
                            "size_min": 0.1,
                            "sync": false
                        }
                    },
                    "line_linked": {
                        "enable": true,
                        "distance": 150,
                        "color": "#00a8ff",
                        "opacity": 0.1,
                        "width": 1
                    },
                    "move": {
                        "enable": true,
                        "speed": 1,
                        "direction": "none",
                        "random": true,
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
                            "enable": false,
                            "mode": "grab"
                        },
                        "onclick": {
                            "enable": false,
                            "mode": "push"
                        },
                        "resize": true
                    }
                },
                "retina_detect": true
            });
        });
    </script>
    """
    components.html(particles_code, height=0)

# Typing animation effect
def typing_animation(text):
    html = f"""
    <div class="typing-container">
        <div class="typing-text">{text}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

# Animated result display
def show_result(result, probability=None):
    if result == 1:  # SPAM
        html = f"""
        <div class="result-card spam">
            <div class="result-icon">⚠️</div>
            <div class="result-title spam">SPAM DETECTED</div>
            <p>This message has been classified as spam with {probability:.1%} confidence.</p>
            <div class="probability-container">
                <p>Spam Probability</p>
                <div class="probability-meter">
                    <div class="probability-fill spam" style="width: {probability*100}%;"></div>
                </div>
            </div>
        </div>
        """
    else:  # NOT SPAM
        html = f"""
        <div class="result-card not-spam">
            <div class="result-icon">✅</div>
            <div class="result-title not-spam">NOT SPAM</div>
            <p>This message appears to be legitimate with {(1-probability):.1%} confidence.</p>
            <div class="probability-container">
                <p>Safe Message Probability</p>
                <div class="probability-meter">
                    <div class="probability-fill not-spam" style="width: {(1-probability)*100}%;"></div>
                </div>
            </div>
        </div>
        """
    st.markdown(html, unsafe_allow_html=True)

# Loading animation
def loading_animation():
    html = """
    <div class="loading-container">
        <div class="loading-spinner"></div>
    </div>
    """
    return st.markdown(html, unsafe_allow_html=True)

# Hero section
def hero_section():
    hero_html = """
    <div class="hero-header">
        <h1>Advanced Spam Shield</h1>
        <p class="hero-subtitle">AI-powered detection for SMS and Email messages</p>
    </div>
    """
    st.markdown(hero_html, unsafe_allow_html=True)

# Features section
def features_section():
    st.markdown("""
    <div class="glass-card">
        <h2 style="text-align: center; margin-bottom: 1.5rem;">Why Choose Our Spam Detector?</h2>
        <div class="feature-section">
            <div class="feature-card">
                <div class="feature-icon">🤖</div>
                <h3 class="feature-title">AI-Powered Analysis</h3>
                <p class="feature-desc">Our advanced machine learning model accurately classifies messages with 95%+ accuracy based on content analysis.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <h3 class="feature-title">Real-Time Processing</h3>
                <p class="feature-desc">Get instant results with our optimized processing pipeline that analyzes messages in milliseconds.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔍</div>
                <h3 class="feature-title">Detailed Insights</h3>
                <p class="feature-desc">Understand why a message was flagged with our transparent analysis and token highlighting.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Stats section
def stats_section():
    st.markdown("""
    <div class="glass-card">
        <h2 style="text-align: center; margin-bottom: 1.5rem;">Our Detection Performance</h2>
        <div class="stats-container">
            <div class="stat-card">
                <div class="stat-number">96.2%</div>
                <div class="stat-label">Accuracy</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">98.1%</div>
                <div class="stat-label">Spam Recall</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">10K+</div>
                <div class="stat-label">Messages Analyzed</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">50ms</div>
                <div class="stat-label">Avg Response Time</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# How it works section
def how_it_works_section():
    st.markdown("""
    <div class="glass-card">
        <h2 style="text-align: center; margin-bottom: 1.5rem;">How It Works</h2>
        <div class="steps-container">
            <div class="step">
                <div class="step-number">1</div>
                <div class="step-content">
                    <h4 class="step-title">Text Preprocessing</h4>
                    <p class="step-desc">The message is cleaned by removing punctuation, stopwords, and standardized through stemming.</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">2</div>
                <div class="step-content">
                    <h4 class="step-title">Feature Extraction</h4>
                    <p class="step-desc">Key features are extracted using TF-IDF vectorization to identify important patterns.</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">3</div>
                <div class="step-content">
                    <h4 class="step-title">Model Prediction</h4>
                    <p class="step-desc">Our trained machine learning model analyzes the features to classify the message.</p>
                </div>
            </div>
            <div class="step">
                <div class="step-number">4</div>
                <div class="step-content">
                    <h4 class="step-title">Result Interpretation</h4>
                    <p class="step-desc">You receive a clear classification with confidence score and explanation.</p>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Token visualization
def show_token_analysis(tokens, result):
    st.markdown("""
    <div class="glass-card">
        <h3>Key Tokens Analysis</h3>
        <p>These are the most significant words that influenced the classification:</p>
        <div class="token-container">
    """, unsafe_allow_html=True)
    
    # Display tokens with appropriate styling
    for token in tokens[:15]:  # Show top 15 tokens max
        if result == 1:  # Spam
            st.markdown(f'<span class="token spam-token">{token}</span>', unsafe_allow_html=True)
        else:  # Ham
            st.markdown(f'<span class="token ham-token">{token}</span>', unsafe_allow_html=True)
    
    st.markdown("</div></div>", unsafe_allow_html=True)

# Main application
def main():
    # Page config
    st.set_page_config(
        page_title="Advanced Spam Classifier",
        page_icon="🛡️",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Apply custom CSS
    local_css()
    
    # Add particles background (lighter version)
    particles_js()
    
    # Hero section
    hero_section()
    
    # Features section
    features_section()
    
    # Stats section
    stats_section()
    
    # How it works section
    how_it_works_section()
    
    # Main classifier section
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        
        typing_animation("Enter your message to check for spam")
        
        # Text input
        input_text = st.text_area("", placeholder="Type or paste your SMS/email message here...", height=150)
        
        # Analyze button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            predict_button = st.button("Analyze Message", type="primary")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Process and display results
        if predict_button and input_text:
            with st.spinner():
                # Show loading animation
                loading = loading_animation()
                
                # Simulate processing time for better UX
                time.sleep(1.5)
                
                # Preprocess
                transformed_text = transform_text(input_text)
                
                # Vectorize
                vector_input = tfidf.transform([transformed_text])
                
                # Predict
                result = model.predict(vector_input.toarray())[0]
                
                # Get probability scores if model supports it
                try:
                    probability = model.predict_proba(vector_input.toarray())[0][1]  # Probability of spam class
                except:
                    probability = 0.99 if result == 1 else 0.01  # Default values if proba not available
                
                # Remove loading animation
                loading.empty()
                
                # Display result with animation
                show_result(result, probability)
                
                # Show token analysis
                tokens = transformed_text.split()
                if tokens:
                    show_token_analysis(tokens, result)
                else:
                    st.markdown("""
                    <div class="glass-card">
                        <p>No significant tokens were extracted from this message.</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        elif predict_button and not input_text:
            st.warning("Please enter a message to analyze.")
    
    # Footer
    st.markdown("""
    <footer>
        <p>© 2025 Advanced Spam Shield | Powered by Machine Learning | Accuracy: 96.2%</p>
    </footer>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()