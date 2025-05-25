import streamlit as st
import time

# Page config
st.set_page_config(
    page_title="Cultural Tourism India - Discover the Soul of Bharat", 
    layout="wide", 
    page_icon="🇮🇳",
    initial_sidebar_state="expanded"
)

# Enhanced interactive storytelling theme
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;900&family=Inter:wght@300;400;500;600&family=Cinzel:wght@400;500;600&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
        color: #f8f9fa;
        font-family: 'Inter', sans-serif;
        overflow-x: hidden;
    }

    /* Floating particles effect */
    .stApp::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: 
            radial-gradient(2px 2px at 20px 30px, #fbbf24, transparent),
            radial-gradient(2px 2px at 40px 70px, rgba(255, 154, 158, 0.8), transparent),
            radial-gradient(1px 1px at 90px 40px, #60a5fa, transparent),
            radial-gradient(1px 1px at 130px 80px, #34d399, transparent);
        background-repeat: repeat;
        background-size: 200px 150px;
        animation: sparkle 20s linear infinite;
        pointer-events: none;
        z-index: -1;
    }
    
    @keyframes sparkle {
        0% { transform: translateY(0px) translateX(0px); opacity: 0.3; }
        50% { opacity: 0.8; }
        100% { transform: translateY(-100px) translateX(50px); opacity: 0.1; }
    }

    h1 {
        font-family: 'Cinzel', serif !important;
        font-size: 4.5rem !important;
        font-weight: 600 !important;
        background: linear-gradient(45deg, #fbbf24, #f59e0b, #d97706, #92400e);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 2rem 0 !important;
        animation: shimmer 4s ease-in-out infinite, pulse 2s ease-in-out infinite alternate;
        text-shadow: 0 0 50px rgba(251, 191, 36, 0.5);
        letter-spacing: 2px;
    }
    
    @keyframes shimmer {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes pulse {
        from { filter: drop-shadow(0 0 20px rgba(251, 191, 36, 0.3)); }
        to { filter: drop-shadow(0 0 40px rgba(251, 191, 36, 0.8)); }
    }
    
    @keyframes typewriter {
        from { width: 0; }
        to { width: 100%; }
    }
    
    @keyframes fadeInScale {
        0% { 
            opacity: 0; 
            transform: scale(0.8) translateY(30px); 
        }
        100% { 
            opacity: 1; 
            transform: scale(1) translateY(0); 
        }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px) rotate(0deg); }
        25% { transform: translateY(-10px) rotate(1deg); }
        50% { transform: translateY(-5px) rotate(0deg); }
        75% { transform: translateY(-12px) rotate(-1deg); }
    }
    
    @keyframes cardHover {
        0% { transform: translateY(0) scale(1); }
        50% { transform: translateY(-10px) scale(1.05); }
        100% { transform: translateY(-8px) scale(1.02); }
    }
    
    .main-container {
        background: rgba(15, 23, 42, 0.6);
        border-radius: 30px;
        padding: 4rem 3rem;
        margin: 2rem auto;
        backdrop-filter: blur(25px) saturate(180%);
        -webkit-backdrop-filter: blur(25px) saturate(180%);
        border: 2px solid rgba(251, 191, 36, 0.2);
        box-shadow: 
            0 25px 80px -12px rgba(0, 0, 0, 0.7),
            inset 0 1px 0 rgba(255, 255, 255, 0.2),
            0 0 100px rgba(251, 191, 36, 0.1);
        animation: fadeInScale 1.5s ease-out;
        position: relative;
        overflow: hidden;
    }
    
    .main-container::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg, transparent, rgba(251, 191, 36, 0.1), transparent);
        animation: rotate 20s linear infinite;
        pointer-events: none;
    }
    
    @keyframes rotate {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .chapter-header {
        position: relative;
        z-index: 10;
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .chapter-number {
        font-family: 'Cinzel', serif;
        font-size: 1.2rem;
        color: #fbbf24;
        font-weight: 500;
        letter-spacing: 3px;
        margin-bottom: 0.5rem;
        opacity: 0;
        animation: fadeInScale 2s ease-out 0.5s forwards;
    }
    
    .gateway-title {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 50%, #d97706 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        position: relative;
        opacity: 0;
        animation: fadeInScale 2s ease-out 1s forwards;
    }
    
    .gateway-title::after {
        content: '';
        position: absolute;
        bottom: -15px;
        left: 50%;
        transform: translateX(-50%);
        width: 0;
        height: 3px;
        background: linear-gradient(135deg, #fbbf24, #f59e0b);
        border-radius: 2px;
        animation: expandWidth 2s ease-out 1.5s forwards;
    }
    
    @keyframes expandWidth {
        to { width: 200px; }
    }
    
    .story-quote {
        font-family: 'Playfair Display', serif;
        font-style: italic;
        font-size: 1.4rem;
        color: #e2e8f0;
        text-align: center;
        margin: 3rem auto;
        padding: 3rem 2rem;
        background: rgba(30, 41, 59, 0.8);
        border-radius: 20px;
        border: 1px solid rgba(251, 191, 36, 0.3);
        max-width: 85%;
        position: relative;
        overflow: hidden;
        opacity: 0;
        animation: fadeInScale 2s ease-out 2s forwards;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }
    
    .story-quote::before {
        content: '"';
        position: absolute;
        top: -10px;
        left: 30px;
        font-size: 5rem;
        color: #fbbf24;
        font-family: 'Playfair Display', serif;
        opacity: 0.7;
        animation: float 4s ease-in-out infinite;
    }
    
    .story-quote::after {
        content: '"';
        position: absolute;
        bottom: -30px;
        right: 30px;
        font-size: 5rem;
        color: #fbbf24;
        font-family: 'Playfair Display', serif;
        opacity: 0.7;
        animation: float 4s ease-in-out infinite 2s;
    }
    
    .typewriter-text {
        overflow: hidden;
        white-space: nowrap;
        border-right: 3px solid #fbbf24;
        width: 0;
        animation: typewriter 4s steps(40) 2.5s forwards, blink 1s infinite 6.5s;
    }
    
    @keyframes blink {
        0%, 50% { border-color: #fbbf24; }
        51%, 100% { border-color: transparent; }
    }
    
    .welcome-text {
        text-align: center;
        font-size: 1.2rem;
        line-height: 1.8;
        color: #cbd5e1;
        margin-bottom: 3rem;
        opacity: 0;
        animation: fadeInScale 2s ease-out 3s forwards;
        position: relative;
        z-index: 10;
    }
    
    .cards-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 2rem;
        margin: 3rem 0;
        position: relative;
        z-index: 10;
        padding: 1rem 0;
    }
    
    .journey-card {
        background: rgba(51, 65, 85, 0.6);
        border-radius: 20px;
        padding: 2rem;
        border: 1px solid rgba(148, 163, 184, 0.3);
        backdrop-filter: blur(15px);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: pointer;
        position: relative;
        overflow: hidden;
        opacity: 0;
        transform: translateY(50px);
        animation: fadeInScale 1s ease-out forwards;
        min-height: 200px;
        width: 100%;
        box-sizing: border-box;
    }
    
    .journey-card:nth-child(1) { animation-delay: 4s; }
    .journey-card:nth-child(2) { animation-delay: 4.2s; }
    .journey-card:nth-child(3) { animation-delay: 4.4s; }
    .journey-card:nth-child(4) { animation-delay: 4.6s; }
    .journey-card:nth-child(5) { animation-delay: 4.8s; }
    .journey-card:nth-child(6) { animation-delay: 5s; }
    .journey-card:nth-child(7) { animation-delay: 5.2s; }
    
    .journey-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(251, 191, 36, 0.2), transparent);
        transition: left 0.7s ease;
        pointer-events: none;
    }

    .journey-card:hover::before {
        left: 100%;
    }
    
    .journey-card:hover {
        box-shadow: 
            0 20px 40px rgba(0, 0, 0, 0.4),
            0 0 30px rgba(251, 191, 36, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.2);
        border-color: rgba(251, 191, 36, 0.6);
        transform: translateY(-5px) scale(1.02);
    }
    
    .card-icon {
        font-size: 3rem;
        margin-bottom: 1.5rem;
        display: block;
        animation: float 6s ease-in-out infinite;
        filter: drop-shadow(0 5px 15px rgba(0, 0, 0, 0.3));
        pointer-events: none;
    }
    
    .card-title {
        color: #f8fafc;
        font-size: 1.4rem;
        font-weight: 600;
        margin-bottom: 1rem;
        font-family: 'Playfair Display', serif;
        position: relative;
        z-index: 2;
    }
    
    .card-description {
        color: #cbd5e1;
        font-size: 1rem;
        line-height: 1.6;
        opacity: 0.9;
        z-index: 2;
        position: relative;
    }
    
    .interactive-hint {
        position: absolute;
        top: 10px;
        right: 15px;
        background: rgba(251, 191, 36, 0.2);
        color: #fbbf24;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        border: 1px solid rgba(251, 191, 36, 0.4);
        animation: pulse 3s infinite;
        z-index: 3;
        pointer-events: none;
    }
    
    .final-message {
        text-align: center;
        margin-top: 4rem;
        font-size: 1.2rem;
        color: #e2e8f0;
        padding: 3rem 2rem;
        background: rgba(30, 41, 59, 0.5);
        border-radius: 20px;
        border: 1px solid rgba(251, 191, 36, 0.2);
        position: relative;
        opacity: 0;
        animation: fadeInScale 2s ease-out 6s forwards;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
    }
    
    .namaste {
        font-size: 1.8rem;
        color: #fbbf24;
        font-weight: 600;
        margin-top: 2rem;
        font-family: 'Cinzel', serif;
        animation: float 3s ease-in-out infinite 1s;
        text-shadow: 0 5px 15px rgba(251, 191, 36, 0.3);
    }
    
    .sound-wave {
        display: inline-block;
        margin: 0 3px;
        width: 3px;
        height: 15px;
        background: #fbbf24;
        animation: soundWave 1s ease-in-out infinite;
    }
    
    .sound-wave:nth-child(2) { animation-delay: 0.1s; }
    .sound-wave:nth-child(3) { animation-delay: 0.2s; }
    .sound-wave:nth-child(4) { animation-delay: 0.3s; }
    
    @keyframes soundWave {
        0%, 100% { height: 15px; }
        50% { height: 5px; }
    }
    
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    #MainMenu {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Interactive title with sound effect simulation
st.markdown('''
<h1>
    🇮🇳 Journey Through Bharat's Eternal Soul 
    <span class="sound-wave"></span>
    <span class="sound-wave"></span>
    <span class="sound-wave"></span>
    <span class="sound-wave"></span>
    🇮🇳
</h1>
''', unsafe_allow_html=True)

# Main container with storytelling elements
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Chapter introduction
st.markdown('''
<div class="chapter-header">
    <div class="chapter-number">✦ CHAPTER I ✦</div>
    <h2 class="gateway-title">The Sacred Threshold</h2>
</div>
''', unsafe_allow_html=True)

# Interactive story quote with typewriter effect
st.markdown('''
<div class="story-quote">
    <div class="typewriter-text">
        Where ancient whispers meet modern dreams, India awaits...
    </div>
    <br><br>
    <em>Every temple bell that rings, every prayer flag that flutters, 
    every step on sacred ground—they all sing the same eternal song of belonging.</em>
</div>
''', unsafe_allow_html=True)

# Welcome narrative
st.markdown('''
<p class="welcome-text">
    🌟 <strong>Welcome, Soul Seeker</strong> 🌟<br><br>
    You are not just a visitor here—you are a protagonist in an unfolding story 
    that began 5,000 years ago and continues through your very presence. 
    This digital sanctuary holds the keys to understanding not just India's heritage, 
    but your own connection to the timeless human journey of seeking meaning, beauty, and truth.
</p>
''', unsafe_allow_html=True)

# Interactive cards with enhanced storytelling
st.markdown('<div class="cards-container">', unsafe_allow_html=True)

# Enhanced cards data with interactive elements
cards_data = [
    ("📊", "Insights Dashboard", "Step into the Oracle's chamber where numbers dance into stories. Witness tourism patterns transform into tales of human longing, discovery, and connection across India's sacred landscape.", "EXPLORE PATTERNS"),
    ("🌍", "Journey Trends", "Follow the ancient pilgrim routes now walked by modern seekers. See how the eternal human desire for spiritual and cultural awakening flows like rivers across our vast nation.", "TRACE JOURNEYS"),
    ("🎨", "Kreative Traditions", "Enter the artist's workshop where time stands still. Watch as paint becomes prayer, clay becomes consciousness, and every creative act becomes a bridge between the mortal and divine.", "CREATE STORIES"),
    ("🏛️", "Living Heritage", "Walk through doorways that have witnessed empires rise and fall. These stones hold memories of lovers' whispers, warriors' valor, and saints' revelations—all waiting to speak to you.", "HEAR WHISPERS"),
    ("🏛️", "Ministry Programs", "Discover the modern guardians of ancient wisdom. See how contemporary India nurtures its soul while embracing tomorrow—a delicate dance between preservation and progress.", "JOIN GUARDIANS"),
    ("🌱", "Preserve Tourism", "Learn the sacred art of treading lightly on holy ground. Become a protector-traveler who leaves only footprints of respect and takes only memories of wonder.", "BECOME GUARDIAN"),
    ("📚", "Quick Guide", "Your mystical compass for navigating India's cultural cosmos. These aren't just tips—they're secrets whispered by generations of wise travelers who've walked this path before you.", "UNLOCK SECRETS")
]

for i, (icon, title, description, action) in enumerate(cards_data):
    st.markdown(f'''
    <div class="journey-card">
        <div class="interactive-hint">CLICK TO {action}</div>
        <span class="card-icon">{icon}</span>
        <h3 class="card-title">{title}</h3>
        <p class="card-description">{description}</p>
    </div>
    ''', unsafe_allow_html=True)

# Close cards container
st.markdown('</div>', unsafe_allow_html=True)  

# Epic conclusion with call to adventure - FIXED VERSION
st.markdown('''
<div class="final-message">
    <strong>🔮 Your Quest Begins Now 🔮</strong>
    <br><br>
    The sidebar awaits your choice, dear traveler. But remember—this is not merely navigation; 
    this is destiny calling. Each path you choose will reveal different facets of India's soul, 
    and in discovering them, you discover parts of yourself you never knew existed.
    <br><br>
    <em>The ancients believed that every journey changes both the traveler and the destination. 
    Your digital pilgrimage through India's cultural heritage begins with a single click, 
    but its effects will ripple through your understanding forever.</em>
    <br><br>    
    <strong>Choose your path. The adventure of a lifetime awaits.</strong>    
    <div class="namaste">
        🙏 सत्यमेव जयते • Satyameva Jayate • Truth Alone Triumphs 🙏
    </div>
</div>
''', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close main container

# Add a hidden audio element for immersion (visual representation)
st.markdown('''
<div style="position: fixed; bottom: 20px; right: 20px; background: rgba(251, 191, 36, 0.1); 
     padding: 1rem; border-radius: 50%; border: 2px solid rgba(251, 191, 36, 0.3); 
     backdrop-filter: blur(10px); cursor: pointer; z-index: 1000;">
    <span style="font-size: 1.5rem; animation: pulse 2s infinite;">🎵</span>
</div>
''', unsafe_allow_html=True)