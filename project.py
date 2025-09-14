import wikipedia
import nltk
import random
from tabulate import tabulate
nltk.download('punkt_tab')
TOPICS = ["Python","Javascript","C","C++","Rust","Java"]

# fetches the wikipedia page
def wikipedia_fetch(topic):
    content = wikipedia.page(f"{topic}-The Programming Language").content
    return content

def get_topic(t):
    topic = t.strip().capitalize()
    print(topic)
    if topic in TOPICS:
        return topic
    return "Not valid"

def generate_quiz(content,num_questions):
    try:
        sentences = nltk.sent_tokenize(content)
        quiz = []
        for sentence in sentences:
            if len(quiz)>=num_questions:
                break
            keywords = [word for word in sentence.split() if word.title() and len(word)>3]
            if len(keywords) >=1:
                correct_answer = random.choice(keywords)
                question = sentence.replace(correct_answer,"___________")
                options = random.sample(keywords,min(3,len(keywords)))
                if correct_answer not in options:
                    options[0] = correct_answer

                random.shuffle(options)
                quiz.append(
                    {
                        'question' : question,
                        'options' : options,
                        'answer' : correct_answer
                })
        return quiz
    except Exception as e:
        print("Error: ",e)
        return []

def run_quiz(quiz):
    score = 0
    for i,q in enumerate(quiz):
        print(f"Q{i+1}: {q['question']}")
        for idx,opt in enumerate(q['options']):
            print(f"{idx+1}. {opt}")
        try:
            ans = int(input("Your answer (option no.): "))
            if q['options'][ans-1] == q['answer']:
                print("✅ Correct")
                score+=1
            else:
                print(f"❌ Incorrect! Answer: {q['answer']}")
        except:
            print(f"❌ Invalid Input! Answer: {q['answer']}")

    print(f"\n📊 Your Score: {score} / {len(quiz)}")

def main():
    print("Coding Quiz")
    print("""
    *******************************************
    Enter you choice of topic from below options
    ********************************************
        """)
    data = [[topic] for topic in TOPICS]
    print(tabulate(data,headers=["TOPICS"],tablefmt="fancy_grid"))

    while(1):
        try:
            top = input("Topic: ")
            topic = get_topic(top)
            if topic != "Not valid":
                break
            print("Not a valid option")
        except Exception:
            pass

    num_questions = int(input("Enter no of questions you want? "))
    content = wikipedia_fetch(topic)
    quiz = generate_quiz(content,num_questions)
    if quiz:
        run_quiz(quiz)
    else:
        print("No quiz could be generated")

if __name__ == "__main__":
    main()