# 🧠 AI Quiz Generator

An intelligent quiz generation web app powered by NLP Transformer models.
Automatically generates quizzes from Wikipedia content using BERT (NER) 
and T5 (Question Generation) — no manual question writing needed!

Built as a Python project submission for B.Tech CSE AIML at DAVIET, PTU.

## Screenshots
### Homepage
<img width="798" height="424" alt="image" src="https://github.com/user-attachments/assets/b5f2480d-72cd-4f0f-aeee-465ebbf0eed8" />
### Quiz Generated
<img width="796" height="423" alt="image" src="https://github.com/user-attachments/assets/30f38b1b-22ad-491b-883f-02c418b94335" />
<img width="786" height="418" alt="image" src="https://github.com/user-attachments/assets/9444c20b-947d-4991-bf01-725e37c16ac4" />
<img width="773" height="410" alt="image" src="https://github.com/user-attachments/assets/832d3609-bbf3-4b64-86de-f11ad3187055" />
<img width="756" height="402" alt="image" src="https://github.com/user-attachments/assets/3d6df586-b78f-4112-8d28-cff8f7ab5559" />
<img width="765" height="406" alt="image" src="https://github.com/user-attachments/assets/ef530d5b-c2f6-4d6e-9a01-79b48b654b40" />
### End of Quiz
<img width="940" height="499" alt="image" src="https://github.com/user-attachments/assets/2fe18be9-c0ae-4665-958e-7691c56bf010" />

<!-- Add a screenshot of the Streamlit app here -->

---

## ✨ Features

- 📖 Auto-fetches Wikipedia content by topic
- 🤖 **BERT NER** (dslim/bert-base-NER) identifies key entities from text
- ❓ **T5 transformer** (valhalla/t5-base-qg-hl) generates natural language questions
- 3 question types generated automatically:
  - 🔵 Multiple Choice Questions (MCQ) with 4 options
  - 🟢 One-word answer questions
  - 🟡 True / False questions
- 🎛️ Choose number of questions to generate
- ⚡ Cached model loading for fast performance
- 🌐 Streamlit web interface — runs in browser

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD21E?style=flat&logo=huggingface&logoColor=black)

**Models:** `dslim/bert-base-NER` · `valhalla/t5-base-qg-hl`  
**Libraries:** `transformers` · `wikipedia` · `streamlit` · `random`

## 🧠 How It Works
```
User selects topic
       ↓
Wikipedia content fetched
       ↓
Text cleaned & split into sentences
       ↓
BERT NER → identifies key entities (people, dates, places, concepts)
       ↓
T5 QG model → generates questions from highlighted entities
       ↓
Quiz displayed on Streamlit UI (MCQ + One-word + True/False)
```

## 📚 Supported Topics

`Python` · `JavaScript` · `C` · `C++` · `Rust` · `Java`

## 🚀 How to Run
```bash
# Clone the repo
git clone https://github.com/Simran-775/Quiz-Generator.git
cd Quiz-Generator

# Install dependencies
pip install transformers wikipedia streamlit

# Run the app
streamlit run streamlit_app.py
```

> ⚠️ First run will download the BERT and T5 models (~500MB). 
> After that, models are cached for fast loading.

## 📁 Project Structure
```
Quiz-Generator/
├── streamlit_app.py   # Streamlit UI
├── project.py         # Quiz logic (NER + QG pipelines)
└── README.md
```

## 📬 Contact
Made with 💙 by [Simranjeet Kaur](https://www.linkedin.com/in/simrandadiala775/)



