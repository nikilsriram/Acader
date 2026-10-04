import streamlit as st

st.set_page_config(layout="wide")

st.html(f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Us</title>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">

    <style>
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
            overflow-x: hidden;
            background-color: #050505;
            color: #ffffff;
        }}

        /* ================= STREAMLIT OVERRIDES ================= */

        [data-testid="stHeader"],
        [data-testid="stStatusWidget"],
        #MainMenu {{
            display: none !important;
            height: 0 !important;
        }}

        .stMainBlockContainer {{
            padding: 0 !important;
            max-width: 100% !important;
        }}

        /* ================= NAVBAR ================= */

        [data-testid="stHeader"], 
        [data-testid="stStatusWidget"], 
        #MainMenu {{
            display: none !important;
            height: 0 !important;
        }}
        
        header {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 110px; /* Increased height from 80px */
            padding: 0 6%;
            background-color: transparent;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 100;
        }}
        
        .logo {{
            font-size: 2.6rem; /* Scaled up from 1.8rem */
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
            gap: 2.8rem; /* Increased spacing between items */
        }}
        
        nav a {{
            font-size: 1.5rem; /* Scaled up from 1.1rem */
            color: white !important;
            font-weight: 500;
            transition: 0.3s ease;
            border-bottom: 3px solid transparent;
            padding-bottom: 0.3rem;
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
                width: 45%;
                border-left: 3px solid #b74b4b;
                border-bottom: 3px solid #b74b4b;
                border-bottom-left-radius: 2rem;
                padding: 1.5rem;
                background-color: #161616;
                border-top: 0.1rem solid rgba(0, 0, 0, 0.1);
            }}
        
            nav .active {{
                display: block;
            }}
        
            nav a {{
                display: block;
                font-size: 1.6rem; /* Scaled up mobile text */
                margin: 1.8rem 0;
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

        /* ================= CONTACT SECTION ================= */

        .content {{
            min-height: 100vh;
            width: 100%;
            background-color: #050505;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 12rem 8% 6rem;
        }}

        .container {{
            width: 100%;
            max-width: 1100px;
            margin: 0 auto;
        }}

        .container h2 {{
            text-align: center;
            font-size: 4rem;
            font-weight: 800;
            margin-bottom: 4rem;
            color: white;
            letter-spacing: -0.5px;
        }}

        .container h2 span {{
            color: #b74b4b;
        }}

        .contact-wrapper {{
            width: 100%;
            display: grid;
            grid-template-columns: 1.2fr 0.8fr;
            gap: 4rem;
            align-items: start;
        }}

        /* ================= CONTACT FORM ================= */

        .contact-form {{
            width: 100%;
            background-color: #111111;
            border: 1px solid #222222;
            border-radius: 1.6rem;
            padding: 4rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        }}

        .contact-form h3 {{
            font-size: 2.2rem;
            margin-bottom: 2.5rem;
            color: white;
            font-weight: 700;
        }}

        .form-group {{
            width: 100%;
            margin-bottom: 2rem;
        }}

        input,
        textarea {{
            width: 100%;
            padding: 1.4rem 1.6rem;
            border-radius: 0.8rem;
            border: 1px solid #2a2a2a;
            background-color: #181818;
            color: white;
            font-size: 1.4rem;
            transition: all 0.3s ease;
        }}

        input::placeholder,
        textarea::placeholder {{
            color: #777777;
        }}

        input:focus,
        textarea:focus {{
            border-color: #b74b4b;
            box-shadow: 0 0 12px rgba(183, 75, 75, 0.25);
            background-color: #1c1c1c;
        }}

        textarea {{
            min-height: 140px;
            resize: vertical;
        }}

        button {{
            display: inline-block;
            width: 100%;
            padding: 1.4rem;
            background-color: #b74b4b;
            border-radius: 0.8rem;
            font-size: 1.5rem;
            color: white;
            font-weight: 600;
            transition: 0.3s ease;
            cursor: pointer;
        }}

        button:hover {{
            background-color: #a33e3e;
            box-shadow: 0 0 20px rgba(183, 75, 75, 0.4);
        }}

        /* ================= CONTACT INFO ================= */

        .contact-info {{
            width: 100%;
            background-color: #111111;
            border: 1px solid #222222;
            border-radius: 1.6rem;
            padding: 4rem;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        }}

        .contact-info h3 {{
            font-size: 2.2rem;
            margin-bottom: 3rem;
            color: white;
            font-weight: 700;
        }}

        .contact-info p {{
            display: flex;
            align-items: center;
            margin-bottom: 2.5rem;
            color: #bbbbbb;
            font-size: 1.5rem;
        }}

        .contact-info i {{
            display: inline-flex;
            justify-content: center;
            align-items: center;
            width: 4.2rem;
            height: 4.2rem;
            margin-right: 1.8rem;
            background-color: rgba(183, 75, 75, 0.1);
            border: 1px solid rgba(183, 75, 75, 0.3);
            border-radius: 50%;
            color: #b74b4b;
            font-size: 1.6rem;
        }}

        /* ================= MEDIA QUERIES ================= */

        @media (max-width: 900px) {{
            .contact-wrapper {{
                grid-template-columns: 1fr;
                gap: 3rem;
            }}

            header {{
                padding: 0 5%;
            }}

            nav {{
                gap: 1.5rem;
            }}

            nav a {{
                font-size: 1.2rem;
            }}
        }}

    </style>
</head>

<body>

<header>
    <a href="#" class="logo">Acader</a>

    <nav>
        <a href="/">Home</a>
        <a href="/aboutme">About Us</a>
        <a href="/faq">Frequently Asked Questions</a>
        <a href="/contact" class="active">Contact Us</a>
        <a href="/login">Login/Sign up</a>
    </nav>
</header>

<section class="content">

    <div class="container">

        <h2>Contact <span>Us</span></h2>

        <div class="contact-wrapper">

            <div class="contact-form">
                <h3>Send us a message</h3>

                <form action="#" method="POST">
                    <div class="form-group">
                        <input type="text" name="name" placeholder="Your Name" required>
                    </div>

                    <div class="form-group">
                        <input type="email" name="email" placeholder="Your Email" required>
                    </div>

                    <div class="form-group">
                        <textarea name="message" placeholder="Your Message" required></textarea>
                    </div>

                    <button type="submit">
                        Send Message
                    </button>
                </form>
            </div>

            <div class="contact-info">
                <h3>Contact Information</h3>

                <p>
                    <i class="fas fa-envelope"></i>
                    info@acader.com
                </p>

                <p>
                    <i class="fas fa-map-marker-alt"></i>
                    Acader HQ, San Francisco, CA
                </p>
            </div>

        </div>

    </div>

</section>

</body>
</html>
""")