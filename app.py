from flask import Flask, request,render_template
import spacy
from PyPDF2 import PdfReader
from spacy.lang.en.stop_words import STOP_WORDS
from jinja2 import Template

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

def extract_data():

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
        # list of data
        skills = []
        degree = []
        instutute = []
        field = []

        doc_num = len(doc.ents)

        # get data
        for i,ent in enumerate(doc.ents):

            # check for institute and field if we find degree (degree usally come frist before institute and field)
            if len(degree) > len(instutute) or len(degree) > len(field):

                # append institute that found after degree and if not field before institute make it blank (institute came last)
                if ent.label_ == "INSTITUTE" and len(degree) > len(instutute):
                    instutute.append(ent.text)
                    if len(degree) > len(field):
                        field.append("-") 
                elif ent.label_ == "FIELD" and  len(degree) > len(field):
                    field.append(ent.text)

                # if found degree again just fill all blank
                elif ent.label_ == "DEGREE" or i == (doc_num -1):
                    if len(degree) > len(instutute):
                        instutute.append("-")
                    
                    if len(degree) > len(field):
                        field.append("-") 

            # extract skill and degree
            if ent.label_ == "SKILL":
                skills.append(ent.text)
            elif ent.label_ == "DEGREE":
                degree.append(ent.text)

        
        skills = list(set(skills))

        # Return the extracted information
        return skills,degree,field,instutute
  


@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':

        # Call the extract_data function and pass the pdf_file as an argument
        skills, degree, field, institute = extract_data()
        # Render the result template and pass the extracted data as arguments
        return render_template('result.html', skills=skills, degree=degree, field=field, institute=institute)
    return render_template('upload.html')


if __name__ == "__main__":
    app.run(debug=True)
