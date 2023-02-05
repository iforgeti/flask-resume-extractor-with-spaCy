from flask import Flask, request
import spacy
from PyPDF2 import PdfReader
from spacy.lang.en.stop_words import STOP_WORDS

app = Flask(__name__)

def read_pdf(file):
    pdf_text = ''
    pdf = PdfReader(file)
    for page in pdf.pages:
        pdf_text +=  ' '+page.extract_text()

    return pdf_text



#before that, let's clean our resume.csv dataframe
def preprocessing(doc):
    
    stopwords = list(STOP_WORDS)
    cleaned_tokens = []
    
    for token in doc:
        if token.text not in stopwords and token.pos_ != 'PUNCT' and token.pos_ != 'SPACE' and \
            token.pos_ != 'SYM':
                cleaned_tokens.append(token.lemma_.lower().strip())
                
    return " ".join(cleaned_tokens)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Load the PDF file
        file = request.files["pdf_file"]

        # Load the spaCy model
        nlp = spacy.load("en_core_web_sm")

        # load skill and eduducation
        skill_path = "skills.jsonl"
        ruler = nlp.add_pipe("entity_ruler",before="ner")
        ruler.from_disk(skill_path)

        # Convert the PDF to text
        pdf_text = read_pdf(file)

        # Process the text with spaCy
        doc = nlp(pdf_text)

        # preprocess
        doc = nlp(preprocessing(doc))

        # Extract skills and education information
        skills = []
        degree = []
        instutute = []
        field = []

        doc_num = len(doc.ents)
        for i,ent in enumerate(doc.ents):
            if len(degree) > len(instutute) or len(degree) > len(field):
                if ent.label_ == "INSTITUTE" and len(degree) > len(instutute):
                    instutute.append(ent.text)
                    if len(degree) > len(field):
                        field.append("-") 
                elif ent.label_ == "FIELD" and  len(degree) > len(field):
                    field.append(ent.text)

                elif ent.label_ == "DEGREE" or i == (doc_num -1):
                    if len(degree) > len(instutute):
                        instutute.append("-")
                    
                    if len(degree) > len(field):
                        field.append("-") 

            if ent.label_ == "SKILL":
                skills.append(ent.text)
            elif ent.label_ == "DEGREE":
                degree.append(ent.text)

        # Return the extracted information
        skills = list(set(skills))
  
        combined_table = "<table><tr><th>Skills</th><th>Degree</th><th>Field</th><th>Instutute</th></tr>"
        for i in range(max(len(skills), len(degree))):
            combined_table += "<tr><td>" + (skills[i] if i < len(skills) else "") + "</td><td>" +\
                 (degree[i] if i < len(degree) else "")+ "</td><td>" +\
                     (field[i] if i < len(field) else "")+ "</td><td>" + (instutute[i] if i < len(instutute) else "")+ "</td></tr>"
        combined_table += "</table>"

        return """
    <html>
    <head>
        <style>
            table {
                margin: 0 auto;
                text-align: center;
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid black;
                padding: 8px;
            }
            th {
                background-color: #dddddd;
            }
        </style>
    </head>
    <body>
        """ + combined_table + """
    </body>
    </html>
"""

    return """
        <form method="post" enctype="multipart/form-data">
            <input type="file" name="pdf_file">
            <input type="submit" value="Extract">
        </form>
    """

if __name__ == "__main__":
    app.run(debug=True)
