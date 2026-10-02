import streamlit as st
import base64

# 1. Force the page to wide layout
st.set_page_config(layout="wide", page_title="Acader")


# Load your image
try:
    with open("gem.jpeg", "rb") as f:
        image = base64.b64encode(f.read()).decode()
except FileNotFoundError:
    image = ""

# Your HTML structure remains safe
st.html(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>About Acader</title>

    <style>
        @import url('https://googleapis.com');

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            text-decoration: none;
            border: none;
            outline: none;
            font-family: 'Inter', sans-serif;
        }}

        html {{
            font-size: 62.5%;
            scroll-behavior: smooth;
        }}

        body {{
            width: 100%;
            min-height: 100vh;
            background-color: #000;
            color: #fff;
            overflow-x: hidden;
        }}

        .about {{
            height: 100vh;
            padding: 7rem 9%;
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        .about-container {{
            width: 100%;
            max-width: 1200px;
            display: flex;
            align-items: center;
            gap: 8rem;
        }}

        .about-image {{
            flex: 0 0 420px;
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        .about-image img {{
            width: 380px;
            height: 380px;
            object-fit: cover;
            border-radius: 2rem;
            border: 2px solid #b74b4b;
            box-shadow: 0 0 35px rgba(183, 75, 75, 0.3);
            transition: 0.3s ease;
        }}

        .about-image img:hover {{
            transform: scale(1.03);
            box-shadow: 0 0 50px rgba(183, 75, 75, 0.45);
        }}

        .about-content {{
            flex: 1;
        }}

        .about-label {{
            font-size: 1.5rem;
            color: #b74b4b;
            font-weight: 700;
            letter-spacing: 0.3rem;
            text-transform: uppercase;
            margin-bottom: 1.2rem;
        }}

        .about-content h1 {{
            font-size: 5.5rem;
            line-height: 1.1;
            font-weight: 800;
            margin-bottom: 1.5rem;
        }}

        .about-content h1 span {{
            color: #b74b4b;
        }}

        .about-content h2 {{
            font-size: 2.5rem;
            font-weight: 600;
            color: #ddd;
            margin-bottom: 2rem;
        }}

        .about-content p {{
            font-size: 1.7rem;
            line-height: 1.8;
            color: #bdbdbd;
            margin-bottom: 1.8rem;
        }}

        .about-info {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1.5rem;
            margin-top: 3rem;
        }}

        .info-card {{
            padding: 2rem;
            background: #0b0b0b;
            border: 1px solid #242424;
            border-left: 3px solid #b74b4b;
            border-radius: 0.8rem;
            transition: 0.3s ease;
        }}

        .info-card:hover {{
            transform: translateY(-4px);
            border-color: #b74b4b;
            box-shadow: 0 0 20px rgba(183, 75, 75, 0.15);
        }}

        .info-card h3 {{
            font-size: 1.5rem;
            color: #b74b4b;
            font-weight: 700;
            margin-bottom: 0.8rem;
        }}

        .info-card p {{
            font-size: 1.5rem;
            color: #ddd;
            margin: 0;
            line-height: 1.5;
        }}

        .about-btn {{
            display: inline-block;
            margin-top: 3rem;
            padding: 1.2rem 2.8rem;
            border: 2px solid #b74b4b;
            border-radius: 4rem;
            background: transparent;
            color: #b74b4b;
            font-size: 1.5rem;
            font-weight: 600;
            letter-spacing: 0.1rem;
            transition: 0.3s ease;
        }}

        .about-btn:hover {{
            background: #b74b4b;
            color: #000;
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(183, 75, 75, 0.25);
        }}

        @media (max-width: 1000px) {{
            .about-container {{
                gap: 4rem;
            }}

            .about-image {{
                flex: 0 0 320px;
            }}

            .about-image img {{
                width: 300px;
                height: 300px;
            }}

            .about-content h1 {{
                font-size: 4.5rem;
            }}
        }}

        @media (max-width: 800px) {{
            .about {{
                padding: 8rem 6%;
            }}

            .about-container {{
                flex-direction: column;
                text-align: center;
            }}

            .about-image {{
                flex: none;
            }}

            .about-image img {{
                width: 280px;
                height: 280px;
            }}

            .about-content {{
                max-width: 700px;
            }}

            .about-info {{
                text-align: left;
            }}
        }}

        @media (max-width: 500px) {{
            .about {{
                padding: 7rem 5%;
            }}

            .about-image img {{
                width: 220px;
                height: 220px;
            }}

            .about-content h1 {{
                font-size: 3.8rem;
            }}

            .about-content h2 {{
                font-size: 2rem;
            }}

            .about-content p {{
                font-size: 1.5rem;
            }}

            .about-info {{
                grid-template-columns: 1fr;
            }}
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
            font-size: 3rem;
            color: #b74b4b !important;
            font-weight: 800;
            cursor: pointer;
            transition: 0.5s ease;
            text-decoration: none;
        }}

        .logo:hover {{
            transform: scale(1.1);
        }}

        nav {{
            display: flex;
            align-items: center;
            gap: 2.5rem;
        }}

        nav a {{
            font-size: 1.6rem;
            color: white !important;
            font-weight: 500;
            transition: 0.3s ease;
            border-bottom: 3px solid transparent;
            white-space: nowrap;
            text-decoration: none;
        }}

        nav a:hover,
        nav a.active {{
            color: #b74b4b !important;
            border-bottom: 3px solid #b74b4b;
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
                font-size: 2rem;
                margin: 3rem 0;
            }}

            nav a:hover,
            nav a.active {{
                padding: 1rem;
                border-radius: 0.5rem;
                border-bottom: 0.5rem solid #b74b4b;
            }}
        }}

        /* Target the main body and outer container */
        [data-testid="stAppViewContainer"], 
        [data-testid="stHeader"], 
        .main .block-container {{
            padding: 0 !important;
            margin: 0 !important;
            max-width: 100% !important;
            width: 100vw !important;
            background-color: #000000 !important;
        }}
        
        /* Force the specific Streamlit Element block to be full width */
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
    </style>
</head>
<body>
<header>
    <a href="#" class="logo">Acader</a>

    <nav>
        <a href="/">Home</a>
        <a href="/frontend">Services</a>
        <a href="#aboutUs" class="active">Skills</a>
        <a href="#">Education</a>
        <a href="#">Experience</a>
        <a href="/login">Library</a>
    </nav>
</header>
    <section class="about">
        <div class="about-container">
            <div class="about-image">
                <img src="data:image/jpeg;base64,{image}" alt="Acader">
            </div>
            <div class="about-content">
                <div class="about-label">About Acader</div>
                <h1>Study <span>Smarter.</span></h1>
                <h2>AI-powered learning, built for students.</h2>
                <p>Acader is an AI-powered learning platform designed to turn your class materials into personalized study tools...</p>
                <div class="about-info">
                    <div class="info-card"><h3>AI-Powered</h3><p>Uses AI to transform your study materials.</p></div>
                    <div class="info-card"><h3>Flashcards</h3><p>Generate personalized flashcards from your notes.</p></div>
                </div>
                <a href="#" class="about-btn">Start Learning →</a>
            </div>
        </div>
    </section>
</body>
</html>
""")

# Render with 100vh equivalents or generous height allocation
