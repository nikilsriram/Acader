import streamlit as st

st.set_page_config(layout="wide", page_title="Frequently Asked Questions", page_icon="./gem.jpeg")
st.markdown(
    """
    <style>
    div[data-testid="stStatusWidget"],
    .stAppViewerFooter,
    div[class*="ViewerBadge"],
    div[class*="viewerBadge"],
    [data-testid="stActionButton"],
    footer {
        display: none !important;
        visibility: hidden !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.html(f"""
<style>
html, body {{
    background-color: #050505 !important;
    color: white !important;
}}

[data-testid="stAppViewContainer"] {{
    background-color: #050505 !important;
}}

[data-testid="stMain"] {{
    background-color: #050505 !important;
}}


   [data-testid="stHeader"], 
[data-testid="stStatusWidget"], 
#MainMenu {{
    display: none !important;
    height: 0 !important;
}}


header {{
            position: fixed;
            top: 20px;
            left: 0;
            width: 100%;
            height: 80px;
            padding: 0 5%;
            background-color: transparent;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 100;
        }}

        .logo {{
            font-size: 1.8rem; /* Scaled down further from 2.4rem */
            color: #b74b4b !important;
            font-weight: 800;
            cursor: pointer;
            transition: 0.5s ease;
            text-decoration: none;
        }}

        .logo:hover {{
            transform: scale(1.05);
        }}

        nav {{
            display: flex;
            align-items: center;
            gap: 1.8rem; /* Tightened gap spacing */
        }}

        nav a {{
            font-size: 1.1rem; /* Scaled down further from 1.3rem */
            color: white !important;
            font-weight: 500;
            transition: 0.3s ease;
            border-bottom: 2px solid transparent; /* Lightened border line scale */
            white-space: nowrap;
            text-decoration: none;
        }}

        nav a:hover,
        nav a.active {{
            color: #b74b4b !important;
            border-bottom: 2px solid #b74b4b;
        }}

        @media (max-width: 995px) {{
            nav {{
                position: absolute;
                display: none;
                top: 0;
                right: 0;
                width: 40%;
                border-left: 3px solid #b74b4b;
                border-bottom: 3px solid #b74b4b;
                border-bottom-left-radius: 2rem;
                padding: 1rem;
                background-color: #161616;
                border-top: 0.1rem solid rgba(0, 0, 0, 0.1);
            }}

            nav .active {{
                display: block;
            }}

            nav a {{
                display: block;
                font-size: 1.3rem; /* Scaled down mobile text */
                margin: 1.5rem 0;
            }}

            nav a:hover,
            nav a.active {{
                padding: 0.6rem;
                border-radius: 0.5rem;
                border-bottom: 0.4rem solid #b74b4b;
            }}
        }}

         [data-testid="stElementContainer"], .element-container {{
                    max-width: 100% !important;
                    width: 100vw !important;
                }}
        
                /* Make sure the iframe itself drops all borders and fills the space */
                iframe {{
                    display: block;
                    width: 100vw !important;
                    height: 100vh !important;
                    border: none !important;
                }}
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    .faq-wrapper {{
        width: 100%;
        max-width: 800px;
        margin: 0 auto;
        padding: 4rem 3%;
        font-family: 'Inter', sans-serif;
        color: white;
    }}

    .faq-wrapper > p {{
        text-align: center;
        color: #b74b4b;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }}

    .faq-wrapper > h1 {{
        text-align: center;
        color: white;
        font-size: 3rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        margin-bottom: 3rem;
    }}

    .faq {{
        border: 2px solid #b74b4b;
        border-radius: 0.8rem;
        margin: 1rem 0;
        background-color: #0a0a0a;
        overflow: hidden;
        transition: 0.3s ease;
    }}

    .faq:hover {{
        box-shadow: 0 0 15px rgba(183, 75, 75, 0.2);
        transform: translateY(-1px);
    }}

    .question {{
        padding: 1.5rem 2rem;
        cursor: pointer;
        font-size: 1.5rem;
        font-weight: 600;
        color: white;
        display: flex;
        justify-content: space-between;
        align-items: center;
        list-style: none;
        transition: 0.3s ease;
    }}

    .question::-webkit-details-marker {{
        display: none;
    }}

    .question:hover {{
        color: #b74b4b;
    }}

    .question i {{
        color: #b74b4b;
        font-size: 1.4rem;
        transition: transform 0.3s ease;
    }}

    details[open] .question {{
        color: #b74b4b;
        border-bottom: 1px solid rgba(183, 75, 75, 0.4);
    }}

    details[open] .question i {{
        transform: rotate(180deg);
    }}

    .answer {{
        padding: 1.5rem 2rem 2rem;
        color: rgba(255, 255, 255, 0.7);
        font-size: 1.3rem;
        line-height: 1.5;
        background-color: #050505;
    }}

    @media (max-width: 995px) {{
        .faq-wrapper {{
            max-width: 90%;
            padding: 3rem 2%;
        }}

        .faq-wrapper > h1 {{
            font-size: 2.5rem;
            margin-bottom: 2.5rem;
        }}

        .question {{
            font-size: 1.4rem;
            padding: 1.3rem 1.5rem;
        }}

        .answer {{
            padding: 1.3rem 1.5rem 1.7rem;
            font-size: 1.2rem;
        }}
    }}
    
</style>
<header>
    <a href="#" class="logo">Acader</a>

    <nav>
        <a href="/">Home</a>
        <a href="/aboutme">About Us</a>
        <a href="/faq" class="active">Frequently Asked Questions</a>
        <a href="/contact">Contact Us</a>
        <a href="/login">Login/Sign up</a>
    </nav>
</header>
<div class="faq-wrapper">

    <h1>Frequently Asked Questions</h1>

    <details class="faq">
        <summary class="question">
            What is Acader?
            <i class="fa-solid fa-chevron-down"></i>
        </summary>

        <div class="answer">
            Acader is an AI-powered study platform that helps students
            turn their learning materials into personalized study resources,
            including notes, flashcards, and practice tests.
        </div>
    </details>

    <details class="faq">
        <summary class="question">
            How does Acader work?
            <i class="fa-solid fa-chevron-down"></i>
        </summary>

        <div class="answer">
            Simply upload your study material, choose what you want to create,
            and Acader's AI analyzes your content to generate personalized
            study resources.
        </div>
    </details>

    <details class="faq">
        <summary class="question">
            What can I create with Acader?
            <i class="fa-solid fa-chevron-down"></i>
        </summary>

        <div class="answer">
            Acader can transform your study materials into AI-generated
            notes, flashcards, and practice tests.
        </div>
    </details>

    <details class="faq">
        <summary class="question">
            What types of files can I upload?
            <i class="fa-solid fa-chevron-down"></i>
        </summary>

        <div class="answer">
            Acader is designed to work with common study materials such as
            images and documents. Supported file types may expand as new
            features are added.
        </div>
    </details>

    <details class="faq">
        <summary class="question">
            Do I need an account to use Acader?
            <i class="fa-solid fa-chevron-down"></i>
        </summary>

        <div class="answer">
            Yes. Creating an account allows Acader to securely save your
            study materials and generated resources so you can access them
            again later.
        </div>
    </details>

    <details class="faq">
        <summary class="question">
            Is Acader free to use?
            <i class="fa-solid fa-chevron-down"></i>
        </summary>

        <div class="answer">
            Acader is focused on making AI-powered studying accessible
            to students. Feature availability and usage limits may change
            as the platform continues to develop.
        </div>
    </details>

</div>
""")