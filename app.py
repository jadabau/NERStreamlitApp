import streamlit as st
import spacy
from spacy.pipeline import EntityRuler
from spacy import displacy

st.set_page_config(page_title="🍀 Notre Dame NER 🎓", layout="wide")

# Theme styles
st.markdown("""
    <style>
        body {
            background: linear-gradient(to bottom right, #b3dac5, #fefefe);
        }
        .title-text {
            font-size: 2.7em;
            font-weight: 800;
            color: #0c2340;
            font-family: 'Georgia', serif;
        }
        .subheader {
            font-size: 1.2em;
            color: #0a843d;
            font-style: italic;
        }
        .stTextArea, .stFileUploader {
            background-color: #f8f8f8 !important;
            border: 1px solid #0a843d;
            border-radius: 10px;
            padding: 10px;
        }
        .block-container {
            padding-top: 2rem;
        }
        .stMarkdown h3 {
            color: #0c2340;
            margin-top: 1.5rem;
        }
        .highlight-box {
            background-color: #f5f5f5;
            padding: 10px;
            border-left: 4px solid #0a843d;
            border-radius: 6px;
        }
        .stButton>button {
            background-color: #0a843d !important;
            color: white !important;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #096b31 !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="title-text">🎓🍀 Notre Dame NER Explorer</p>', unsafe_allow_html=True)
st.markdown('<p class="subheader">Made with love & leprechauns. Upload your own stories or customize with Irish spirit!</p>', unsafe_allow_html=True)

# Session state initializing
if "text_input" not in st.session_state:
    st.session_state.text_input = (
        "The University of Notre Dame is home to the Golden Dome and the Fighting Irish. "
        "It was founded by Father Sorin in 1842, envisioning it as a force for good in the world. "
    )

if "pattern_input" not in st.session_state:
    st.session_state.pattern_input = '''{ "label": "ICON", "pattern": "Golden Dome" }
{ "label": "BEST SCHOOL IN THE WORLD", "pattern": "Notre Dame" }
{ "label": "MASCOT", "pattern": "Fighting Irish" }'''

# Load model
@st.cache(allow_output_mutation=True)
def load_model():
    return spacy.load("en_core_web_sm")

nlp = load_model()

# Text Input
st.markdown("### 🖋 Paste or Upload Your Text")
uploaded_file = st.file_uploader("📂 Upload a .txt file", type=["txt"])
if uploaded_file:
    st.session_state.text_input = uploaded_file.read().decode("utf-8")
else:
    st.session_state.text_input = st.text_area(
        "📝 Your text here:",
        value=st.session_state.text_input,
        height=160
    )

# Pattern input
st.markdown("### 🌳 Define Custom Entity Patterns")
st.session_state.pattern_input = st.text_area(
    "📚 Enter patterns (one per line):",
    value=st.session_state.pattern_input,
    height=150
)

# Run NER Button
run_ner = st.button("Run NER 🍀")

if run_ner:
    text = st.session_state.text_input
    try:
        patterns = [eval(line.strip()) for line in st.session_state.pattern_input.strip().split("\n") if line.strip()]
    except Exception:
        st.error("⚠️ Pattern format error. Make sure each line is a valid Python dictionary.")
        patterns = []

    if text.strip() and patterns:
        if "custom_ruler" in nlp.pipe_names:
            nlp.remove_pipe("custom_ruler")
        ruler = nlp.add_pipe("entity_ruler", before="ner", name="custom_ruler")
        ruler.add_patterns(patterns)

        doc = nlp(text)

        # Recognized entities
        st.markdown("### 📜 Recognized Entities")
        if doc.ents:
            for ent in doc.ents:
                st.markdown(
                    f"<div class='highlight-box'>"
                    f"<strong style='color:#0a843d'>{ent.text}</strong> "
                    f"→ <code style='color:#ae9142'>{ent.label_}</code> "
                    f"<small>(start: {ent.start_char}, end: {ent.end_char})</small>"
                    f"</div>",
                    unsafe_allow_html=True
                )
        else:
            st.info("No entities found. Try adjusting your text or patterns.")

        # Entity visualizer
        st.markdown("### 📚 Visualizer")
        colors = {
            "ORG": "#b3dac5", "PERSON": "#ae9142", "GPE": "#0a843d",
            "DATE": "#ae9142", "NAME": "#0a843d", "PLACE": "#b3dac5",
            "SCHOOL": "#ae9142", "MASCOT": "#0a843d", "BUILDING": "#b3dac5"
        }
        options = {"colors": colors}
        html = displacy.render(doc, style="ent", options=options)
        st.components.v1.html(html, scrolling=True, height=250)
    else:
        st.warning("Start by pasting some text and adding at least one valid pattern.")