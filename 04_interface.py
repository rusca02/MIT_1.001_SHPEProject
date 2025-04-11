import streamlit as st
from prompting import ask_gpt

# 1. Set Page Configuration
st.set_page_config(
    page_title="SHPE GPT Assistant",
    page_icon=":rocket:",  # or a local image file or something else
    layout="centered"
)

# 2. Define Your Custom SHPE Colors
# Pick the ones you'd like to use for background, heading, etc.
SHPE_ORANGE = "#D32A02"  # from your palette
SHPE_LIGHT_ORANGE = "#F46F3B"
SHPE_BLUE = "#0070CD"
SHPE_LIGHT_BLUE = "#72A9BE"

# 3. Inject Custom CSS with SHPE Colors
custom_css = f"""
<style>
/* Set a background color for the main page */
body {{
    background-color: #F5F5F5; /* Light neutral background, or pick a SHPE color if you want a stronger look */
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}}

/* Style the main title */
h1 {{
    color: {SHPE_BLUE};  /* A bold blue for headings */
    font-weight: 700;
}}

/* Style the subtext or other elements in a complementary color */
h2, h3, .stMarkdown p {{
    color: {SHPE_ORANGE};
}}

/* Customize the text input box */
div.stTextInput > div > input {{
    font-size: 1.1em;
    padding: 10px;
    border: 2px solid {SHPE_BLUE};
    border-radius: 5px;
}}

/* Style the 'Answer' box or the st.success elements, etc. */
.reportview-container .main .block-container {{
    border-left: 5px solid {SHPE_LIGHT_ORANGE};
    padding: 1em;
    border-radius: 5px;
}}

/* Customize Streamlit's success message color (for st.success) */
.stAlert > div[data-baseweb="block"] {{
    background-color: {SHPE_LIGHT_BLUE}1A; /* Adding 1A for some transparency or use a solid color if you want */
    border-left: 5px solid {SHPE_LIGHT_BLUE};
}}
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# 4. Optional Logo
# If you have a SHPE logo, place it at the top. Example:
# st.image("shpe_logo.png", width=200)

# 5. Title and Description
st.title("SHPE GPT Assistant")
st.markdown(f"""
Welcome to the **SHPE GPT Assistant** – your tool for exploring our indexed documents.  
Ask your questions below, and let our AI help you extract insights from the data!
""")

# 6. Query Input
query = st.text_input("Enter your question:")

# 7. If user typed something, process it
if query:
    try:
        with st.spinner("Processing your question..."):
            answer = ask_gpt(query)
        st.success("Answer:")
        st.markdown(answer)
    except Exception as e:
        st.error(f"An error occurred while processing your query: {e}")
