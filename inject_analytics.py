import pathlib
import streamlit as st
import os

def inject_ga():
    # Paste your raw snippet from Google Analytics here
    ga_code = os.getenv("GA_TRACKING_ID")
    
    # Locate the base HTML structure file inside your cloud container
    index_path = pathlib.Path(st.__file__).parent / "static" / "index.html"
    content = index_path.read_text(encoding="utf-8")
    
    # Silently insert it into the layout background
    if "googletagmanager" not in content:
        modified_content = content.replace("<head>", f"<head>\n{ga_code}")
        index_path.write_text(modified_content, encoding="utf-8")

if __name__ == "__main__":
    inject_ga()