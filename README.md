
## How to do flask pdf resume extractor by yourself 



- step1 install nessesery library PyPDF2 spacy and flask

- step2 copy skill pattern for nlp entity ruler from microsoft
https://github.com/microsoft/SkillsExtractorCognitiveSearch.git

- step3 add other pattern as you want (in this work i only add pattern for extrct data from someone_cv.pdf)
![image](https://user-images.githubusercontent.com/78832408/217266187-6f09236d-c8ee-49df-a380-54388c875924.png)

- step4 write program to extract data

  In brief, program receive pdf file from user. Pdf file convert to text . preprocessing text by remove symbol punctuation stopword... use spacy to label entity . select only entity we need (SKILLS,DEGREE,FIELD,INSTITUTE). if find degree in text get field and institute too (work in case input cv looklike someone_cv)

- Step5 create web page with html 

- Step6 decorate with css

---
## review

- ### Upload page 

minimal webpage black and white theme  

![image](https://user-images.githubusercontent.com/78832408/217243876-ca98b248-8591-4ef4-8104-2c855a91a5c4.png)

upload by drop file in drop area

![image](https://user-images.githubusercontent.com/78832408/217249788-95887d93-5008-41cd-9e17-4bec4fc5e307.png)

upload bottom pop up, Let extract our cv.

![image](https://user-images.githubusercontent.com/78832408/217249911-4494aaee-d14e-4f3f-91a3-409782e53abd.png)

- ### 2. Result page

result page show table of skill and table of education

![image](https://user-images.githubusercontent.com/78832408/217249517-77cea6ba-c365-483c-a18d-ae2fdf71322b.png)

table of education consist of degree, field of study and Institute 

![image](https://user-images.githubusercontent.com/78832408/217249616-6dc26cb6-8b7e-4337-9852-41f1137919fc.png)

---
