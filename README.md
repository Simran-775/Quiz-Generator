# 🧠 AI Quiz Generator

An intelligent quiz generation web app powered by NLP Transformer models.
Automatically generates quizzes from Wikipedia content using BERT (NER) 
and T5 (Question Generation) — no manual question writing needed!

Built as a Python project submission for B.Tech CSE AIML at DAVIET, PTU.

## Screenshots

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



