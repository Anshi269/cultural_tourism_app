import streamlit as st

st.set_page_config(page_title="More Responsible Tourism Info", layout="wide", initial_sidebar_state="collapsed")
st.title("📘 More Responsible Tourism Info")

# Define the card data
info_cards = [
    {
        "title": "🌱 Sustainable Travel",
        "content": """Choose eco-friendly transportation, pack light, and stay in green-certified accommodations to reduce your environmental footprint.
       <ul>
            <li>Use public transport, walk, or cycle.</li>  
            <li>Choose eco-certified stays.</li>  
            <li>Carry reusable items (bottle, bag, utensils).</li>  
            <li>Offset carbon emissions for flights.</li>
        </ul>""",
        "color": "#90be6d",
        "image": "Responsible_Tourism/images/sustainable_travel.png"
    },
    {
        "title": "🤝 Community Support",
        "content": """Support local communities by booking local guides, eating at family-run restaurants, and staying in homestays or locally owned lodges.
        <ul>
            <li>Eat at local restaurants and food stalls.</li>  
            <li>Hire local guides for authentic insights.</li>  
            <li>Stay in community-run homestays.</li>  
            <li>Join cultural events or village tours.</li>
        </ul>""",
        "color": "#f9844a",
        "image": "Responsible_Tourism/images/community.png"
    },
    {
        "title": "🧶 Local Handicrafts",
        "content": """Purchase handmade crafts and souvenirs directly from local artisans to promote traditional skills and boost the local economy.
        <ul>
            <li>Buy directly from artisans or cooperatives.</li>  
            <li>Choose handmade, eco-friendly goods.</li>  
            <li>Avoid items from endangered species.</li>  
            <li>Take local workshops to learn a craft.</li>
        </ul>""",
        "color": "#43aa8b",
        "image": "Responsible_Tourism/images/handicrafts.png"
    }
]

# Create dynamic columns
cols = st.columns(len(info_cards))

# Render each card
for i, card in enumerate(info_cards):
    with cols[i]:
        try:
            st.markdown(
                f"""
                <div style="background-color:{card['color']}; padding: 20px; border-radius: 20px; margin: 10px; 
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); color: white; font-size: 16px; line-height: 1.6; text-align: center;">
                """,
                unsafe_allow_html=True
            )

            st.image(card["image"], use_container_width=True)

            st.markdown(
                f"""
                <h3 style="margin-top: 15px;">{card['title']}</h3>
                <p>{card['content']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

        except Exception as e:
            st.error(f"Error rendering card: {e}")

# Back button
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="display: flex; justify-content: center; margin-top: 30px;">
    <a href="/" target="_self">
    <button style="background-color:#f9c74f; border:none; border-radius:50%; 
    padding:15px 20px; font-size:20px; font-weight:bold; color:#262730; 
    cursor:pointer; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);">⬅</button>
    </a>
    </div>
    """,
    unsafe_allow_html=True
)
