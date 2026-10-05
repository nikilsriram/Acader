import os
import pathlib
import streamlit as st

def inject_ga():
    ga_id = os.getenv("GA_TRACKING_ID")

    if not ga_id:
        print("Warning: GA_TRACKING_ID not found.")
        return

    ga_code = f"""
    <!-- Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){{dataLayer.push(arguments);}}
      gtag('js', new Date());
      gtag('config', '{ga_id}');
    </script>
    """

    index_path = pathlib.Path(st.__file__).parent / "static" / "index.html"

    if not index_path.exists():
        print(f"Warning: Streamlit HTML file not found: {index_path}")
        return

    content = index_path.read_text(encoding="utf-8")

    if "googletagmanager.com/gtag/js" not in content:
        if "<head>" in content:
            modified_content = content.replace(
                "<head>", f"<head>\n{ga_code}", 1
            )
            index_path.write_text(modified_content, encoding="utf-8")
        else:
            print("Warning: Could not find <head> tag.")

if __name__ == "__main__":
    inject_ga()
