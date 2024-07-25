from flask import Flask, request, render_template
import spacy

app = Flask(__name__)

# Muat model bahasa Inggris dan model multibahasa (yang mencakup bahasa Indonesia)
try:
    nlp_en = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp_en = spacy.load("en_core_web_sm")

try:
    nlp_multi = spacy.load("xx_ent_wiki_sm")
except OSError:
    from spacy.cli import download
    download("xx_ent_wiki_sm")
    nlp_multi = spacy.load("xx_ent_wiki_sm")

def extract_names(text, language="en"):
    if language == "en":
        nlp = nlp_en
    else:
        nlp = nlp_multi

    doc = nlp(text)
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    return names

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/prediksi_nama', methods=['POST'])
def extract_names_endpoint():
    text = request.form.get('text', '')
    language = request.form.get('language', 'en')
    names = extract_names(text, language)
    is_name = len(names) > 0
    print(f"Input text: {text}")
    print(f"Detected names: {names}")
    return render_template('index.html', text=text, language=language, is_name=is_name, names=names)

if __name__ == '__main__':
    app.run(debug=True)
