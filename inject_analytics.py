import os
import pathlib
import streamlit as st

def inject_ga():
    # 1. Pull the secret ID from the environment setup
    ga_id = os.getenv("GA_TRACKING_ID")
    
    if not ga_id:
        print("Warning: GA_TRACKING_ID environment variable not found.")
        return

    # FIXED: This now injects the proper JavaScript tags instead of raw text
    ga_code = f"""
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://googletagmanager.com{ga_id}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{ga_id}');
    </script>
    """
    
    # 2. Locate the base HTML structure file inside your cloud container
    index_path = pathlib.Path(st.__file__).parent / "static" / "index.html"
    content = index_path.read_text(encoding="utf-8")
    
    # 3. Insert it into the layout background safely
    if "googletagmanager" not in content:
        modified_content = content.replace("<head>", f"<head>\n{ga_code}")
        index_path.write_text(modified_content, encoding="utf-8")

if __name__ == "__main__":
    inject_ga()
