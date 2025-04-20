# Resume Parser for Indian Candidates

## Project Overview
This project is a **Resume Parser** built to extract structured information from multiple PDF/DOCX resumes. It's fine‑tuned to recognise **Indian names** using a custom **spaCy NER model**, and provides a clean, user‑friendly frontend using **Streamlit**.


## ✨ Features

- 🔍 **Name Extraction**: Uses a fine-tuned **spaCy NER model** to accurately identify Indian names.
- 📞 **Contact Info**: Extracts mobile phone numbers from resumes.
- 🌐 **Links**: Automatically fetches LinkedIn and GitHub links.
- 💼 **Skills**: Parses and lists skills mentioned in the resume.
- 📂 **Batch Processing**: Handles multiple PDF or DOCX resumes in one go.
- 📊 **Streamlit UI**:
  - View the extracted details for each resume.
  - Download all the results in a CSV format.

---

## Clone the Repository
To clone the project repository, run:  
``` bash
git clone https://github.com/Vivek9411/Resume-information-extractor.git
cd  Resume-information-extractor
```

## Install Dependencies
Install the required Python packages: 
``` bash
pip install -r requirements.txt
```
or 
```bash
pip install pandas spacy streamlit pymupdf
```

Ensure to load the fine‑tuned spaCy model  **person_only_model** trained to recognise **Indian names**.

## Run the Application
Start the Streamlit app: 
``` bash
streamlit run app.py
```

The app will open in your default web browser, allowing you to upload resumes and view/download parsed results.

## Output Format
The CSV output contains:  
- **Name**  
- **Contact Number**
- **Email** 
- **LinkedIn**  
- **GitHub**  
- **Skills**  

## Sample CSV Output
| Name         | Email         | Contact Number | LinkedIn               | GitHub                  | Skills               |
|--------------|--------------|----------------|------------------------|-------------------------|----------------------|
| Ramesh Singh | Ramesh@gmail.com | 9999999999    | linkedin.com/in/ramesh | github.com/rameshsingh  | Python, SQL, NumPy   |
| Anjali Rao   |anjali@gmail.com|9123456789    | linkedin.com/in/anjalirao | github.com/anjalirao  | Data Analysis, Excel |

## 🚀 Live Demo

Try it now: **[Open Demo](https://resume-information-extractor-svo6wf8b8jtj7qdngds9dj.streamlit.app/)**

---
