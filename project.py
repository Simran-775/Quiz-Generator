import wikipedia
from transformers import pipeline 
import nltk
import random
from tabulate import tabulate

nltk.download('punkt')

TOPICS = ["Python","Javascript","C","C++","Rust","Java"]

# Pipelines
ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", aggregation_strategy="simple")
qg_pipeline = pipeline("text2text-generation", model="valhalla/t5-base-qg-hl")

# Fetch Wikipedia page safely
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
        # Pick the option containing "programming"
        for option in e.options:
            if "programming" in option.lower():
                page = wikipedia.page(option)
                break
        else:
            page = wikipedia.page(e.options[0])
    return page.content


# Validate topic
def get_topic(t):
    topic = t.strip().capitalize()
    if topic in TOPICS:
        return topic
    return "Not valid"

# Generate quiz
def generate_quiz(text, num_questions):
    sentences = [s.strip() for s in text.split(".") if len(s.split()) >= 6]
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

    total_needed = num_mcq + num_one_word + num_true_false
    random.shuffle(sentences)

    # If not enough sentences, allow reuse by cycling through
    if len(sentences) < total_needed:
        extended_sentences = sentences * ((total_needed // len(sentences)) + 1)
    else:
        extended_sentences = sentences

    mcq_sentences = extended_sentences[:num_mcq]
    one_word_sentences = extended_sentences[num_mcq:num_mcq+num_one_word]
    true_false_sentences = extended_sentences[num_mcq+num_one_word:num_mcq+num_one_word+num_true_false]


    # Step 2: Create blank questions
    mcq_created = 0
    for sent in mcq_sentences:
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

    # Step 3: Create one-word questions
    one_word_created = 0
    for sent in one_word_sentences:
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


    # Step 4: Create true/false questions
    true_false_created = 0
    for sent in true_false_sentences:
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


# Run quiz interactively
def run_quiz(quiz):
    score = 0

    # Separate quiz by type
    mcq = [q for q in quiz if q['type'] == 'mcq']
    one_word = [q for q in quiz if q['type'] == 'one_word']
    true_false = [q for q in quiz if q['type'] == 'true_false']

    print("\n========== MCQ (1 marks each)==========")
    for i, q in enumerate(mcq):
        print(f"\nQ{i+1}: {q['question']}")
        for idx, opt in enumerate(q['options']):
            print(f"{idx+1}. {opt}")
        try:
            ans = int(input("Your answer (option no.): "))
            if q['options'][ans-1] == q['answer']:
                print("✅ Correct")
                score += 1
            else:
                print(f"❌ Incorrect! Answer: {q['answer']}")
        except:
            print(f"❌ Invalid Input! Answer: {q['answer']}")

    # ----- ONE-WORD -----
    print("\n========== ONE-WORD QUESTIONS (2 marks each) ==========")
    for i, q in enumerate(one_word):
        print(f"\nQ{i+1}: {q['question']}")
        ans = input("Your answer: ").strip()
        if ans.lower() == q['answer'].lower():
            print("✅ Correct")
            score += 2
        else:
            print(f"❌ Incorrect! Answer: {q['answer']}")

    # ----- TRUE/FALSE -----
    print("\n========== TRUE/FALSE QUESTIONS (1 mark each) ==========")
    for i, q in enumerate(true_false):
        print(f"\nQ{i+1}: {q['question']}")
        ans = input("Your answer (True/False): ").strip().lower()
        if (ans == "true" and q['answer'] == "True") or (ans == "false" and q['answer'] == "False"):
            print("✅ Correct")
            score += 1
        else:
            print(f"❌ Incorrect! Answer: {q['answer']}")

    total_marks = len(mcq)*1 + len(one_word)*2 + len(true_false)*1
    print(f"\n📊 Your Score: {score} / {total_marks}")


# Main function
def main():
    print("Coding Quiz")
    print("""
*******************************************
Enter your choice of topic from below options
********************************************
    """)
    data = [[topic] for topic in TOPICS]
    print(tabulate(data, headers=["TOPICS"], tablefmt="fancy_grid"))

    while True:
        top = input("Topic: ")
        topic = get_topic(top)
        if topic != "Not valid":
            break
        print("Not a valid option")

    num_questions = int(input("Enter no of questions you want? "))
    text = wikipedia_fetch(topic)
    if not text:
        print("No Wikipedia content found for this topic.")
        return

    quiz = generate_quiz(text, num_questions)
    if quiz:
        run_quiz(quiz)
    else:
        print("No quiz could be generated.")

if __name__ == "__main__":
    main()
