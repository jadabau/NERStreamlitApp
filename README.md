# 🎓 Notre Dame NER Explorer

Welcome to the **Notre Dame NER Explorer**: a custom-built Named Entity Recognition (NER) web app powered by **spaCy** and **Streamlit**, with the shamrock-studded Notre Dame spirit ☘️

This app allows users to upload or paste their own text, define custom NER patterns, and visually explore highlighted entities in real-time using spaCy’s `EntityRuler`. Whether you're working with stories, campus history, or just experimenting with language, this tool makes entity recognition both easy, educational, and efficient.

View it here: https://ndnerexplorer.streamlit.app/

---

## Project Overview

NER (Named Entity Recognition) is a key task in Natural Language Processing that identifies and classifies entities such as people, locations, organizations, and more. This app uses **spaCy**, a popular Python NLP library, to:

- Parse user-submitted text (typed or .txt file)
- Apply*custom rules through `EntityRuler`
- Visualize recognized entities with label-specific styling

I built this with **Streamlit** to create an intuitive interface with subtle accents of **Notre Dame navy, gold, and green**.

---

## How to Run the App Locally

### ☘️ Requirements

Make sure you have Python **3.7–3.10** installed.

### Setup

```bash
# Clone this repo
git clone https://github.com/jadabau/NERStreamlitApp.git
cd NERStreamlitApp

# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm

# Run the app!
streamlit run app.py
