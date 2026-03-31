# quiz_logic
import wikipedia
from transformers import pipeline
import random
import streamlit as st # Import Streamlit for caching decorators

TOPICS = ["Python","Javascript","C","C++","Rust","Java"]

# Cache the pipelines so they only load once when the app starts
@st.cache_resource
def load_pipelines():
    ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
    qg_pipeline = pipeline("text2text-generation", model="valhalla/t5-base-qg-hl")
    return ner_pipeline, qg_pipeline

# Load pipelines once
ner_pipeline, qg_pipeline = load_pipelines()

# Cache the data fetching to avoid re-downloading on every UI interaction
@st.cache_data
def wikipedia_fetch(topic):
    try:
        # Try the programming language page first
        page = wikipedia.page(f"{topic} (programming language)")
    except wikipedia.exceptions.PageError:
        # Fallback to regular page
        try:
            page = wikipedia.page(topic)
        except Exception as e:
            print(f"⚠️ Couldn't find a page for {topic}: {e}")
            return ""
    except wikipedia.exceptions.DisambiguationError as e:
        for option in e.options:
            if "programming" in option.lower():
                page = wikipedia.page(option)
                break
        else:
            page = wikipedia.page(e.options[0])
    return page.content


def get_topic(t):
    topic = t.strip().capitalize()
    if topic in TOPICS:
        return topic
    return "Not valid"


def generate_quiz(text, num_questions):
    sentences = [s.strip() for s in text.split(".") if len(s.split()) >= 4]
    if not sentences:
        return []

    # Step 1: divide questions by type
    base = num_questions // 3
    remainder = num_questions % 3

    num_mcq = base
    num_one_word = base
    num_true_false = base

    if remainder == 1:
        num_mcq += 1
    elif remainder == 2:
        num_mcq += 1
        num_one_word += 1

    quiz = []

    # Step 2: Dividing the sentences according to type
    random.shuffle(sentences)

    # Step 3: Create MCQ questions
    mcq_created = 0
    for sent in sentences:
        if mcq_created >= num_mcq:
            break
        entities = ner_pipeline(sent)
        if not entities:
            continue
        answer_entity = random.choice(entities)
        answer = answer_entity['word']

        # Other entities of the same type for options
        same_type_entities = [e['word'] for e in entities if e != answer_entity]
        options = [answer] + random.sample(same_type_entities, min(3, len(same_type_entities)))

        # If less than 3 distractors, fill with random words from sentence
        words = [w for w in sent.split() if w.isalpha() and w != answer]
        while len(options) < 4 and words:
            options.append(words.pop(random.randint(0, len(words)-1)))

        random.shuffle(options)

        highlighted_text = sent.replace(answer, f"<hl>{answer}<hl>")
        result = qg_pipeline(f"generate question: {highlighted_text}", max_length=64)
        question = result[0]["generated_text"]

        quiz.append({
        "question": question,
        "options": options,
        "answer": answer,
        "type": "mcq"
        })
        mcq_created += 1

    # Step 4: Create one-word questions
    random.shuffle(sentences)
    one_word_created = 0
    for sent in sentences:
        if one_word_created >= num_one_word:
            break
        entities = ner_pipeline(sent)
        if not entities:
            continue

        entity = random.choice(entities)
        answer = entity['word']

        # Highlight the answer in the sentence for QG
        highlighted_text = sent.replace(answer, f"<hl>{answer}<hl>")

        try:
            # Generate a question using QG pipeline
            result = qg_pipeline(f"generate question: {highlighted_text}", max_length=64)
            question_text = result[0]['generated_text']
        except Exception as e:
            # fallback if QG fails
            question_text = f"What is the {entity['entity_group'].lower()} in this sentence: '{sent}'?"

        quiz.append({
            "question": question_text,
            "answer": answer,
            "context": sent,
            "type": "one_word"
        })
        one_word_created += 1


    # Step 5: Create true/false questions
    random.shuffle(sentences)
    true_false_created = 0
    for sent in sentences:
        if true_false_created >= num_true_false:
            break
        entities = ner_pipeline(sent)
        if not entities:
            continue
        entity = entities[0]
        answer = entity['word']
        is_true = random.choice([True, False])
        if not is_true:
            fake_entity = "XYZ123"  # make it false
            question_text = sent.replace(answer, fake_entity)
            answer_text = "False"
        else:
            question_text = sent
            answer_text = "True"
        quiz.append({
            "question": question_text,
            "answer": answer_text,
            "context": sent,
            "type": "true_false"
        })
        true_false_created += 1

    return quiz
