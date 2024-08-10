import os
import pickle
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer, util

# Initialize the SentenceTransformer model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Load the dataset
file_path = 'asana_qa_dataset.csv'
asana_qa_df = pd.read_csv(file_path)

# Preprocessing: Convert to lowercase
asana_qa_df['Question'] = asana_qa_df['Question'].str.lower()

# Step 1: Vectorize the questions using TF-IDF
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(asana_qa_df['Question'])

# Load or compute sentence embeddings and cache them
cache_file = 'question_embeddings_cache.pkl'
if os.path.exists(cache_file):
    with open(cache_file, 'rb') as f:
        question_embeddings = pickle.load(f)
else:
    question_embeddings = model.encode(asana_qa_df['Question'], convert_to_tensor=True)
    with open(cache_file, 'wb') as f:
        pickle.dump(question_embeddings, f)

def find_closest_answer(user_query):
    user_query = user_query.lower()
    user_vector = vectorizer.transform([user_query])
    cosine_similarities = cosine_similarity(user_vector, vectors).flatten()
    best_match_index = np.argmax(cosine_similarities)
    best_match_score = cosine_similarities[best_match_index]

    if best_match_score < 0.2:
        return "I'm not sure I understand the question. Can you please rephrase?"
    else:
        return asana_qa_df.iloc[best_match_index]['Answer']

def find_closest_answer_enhanced(user_query):
    user_embedding = model.encode(user_query, convert_to_tensor=True)
    cosine_similarities = util.pytorch_cos_sim(user_embedding, question_embeddings)

    # Convert to numpy array and extract the best match index
    best_match_index = int(cosine_similarities.argmax().item())
    best_match_score = cosine_similarities[0][best_match_index].item()

    if best_match_score < 0.4:
        return "I'm not sure I understand the question. Can you please rephrase?"
    else:
        return asana_qa_df.iloc[best_match_index]['Answer']


def get_related_questions(best_match_index, top_n=3):
    related_scores = cosine_similarity([vectors[best_match_index]], vectors).flatten()
    related_indices = related_scores.argsort()[-top_n - 1:-1][::-1]
    return asana_qa_df.iloc[related_indices]['Question'].tolist()


def collect_feedback():
    """
    Collects user feedback on whether the answer was helpful.
    """
    feedback = input("Was this answer helpful? (Yes/No): ").strip().lower()
    if feedback == 'no':
        print("I'm sorry the answer wasn't helpful. Let me try to assist you further.")
        # Logic for further assistance (e.g., suggesting more questions, asking for clarification)
    else:
        print("Great! I'm glad I could help.")


def fallback_clarification(user_query, best_match_score, best_match_index):
    """
    Handles fallback and clarification when the chatbot is unsure about the answer.
    """
    if best_match_score < 0.4:  # Low confidence threshold
        # Fallback response
        clarification_question = "I'm not sure I understand your question. Could you clarify? Are you asking about tasks, projects, or something else?"
        return clarification_question
    else:
        # Confident response
        return asana_qa_df.iloc[best_match_index]['Answer']


def ask_for_clarification(user_query):
    """
    Suggests a clarification question based on the initial user query.
    """
    if "task" in user_query.lower():
        clarification = "Are you asking about adding files to a task, completing a task, or something else?"
    elif "project" in user_query.lower():
        clarification = "Are you asking about setting up a project, managing a project, or something else?"
    else:
        clarification = "Could you please specify what you're asking about?"

    return clarification



def respond_with_context(user_query, session):
    # Check for context
    last_question = session.get_context('last_question')

    if last_question and "task" in last_question:
        if "assign" in user_query.lower():
            return "Yes, after creating the task, you can assign it to a team member by selecting their name in the 'Assignee' field."
        elif "due date" in user_query.lower():
            return "You can set a due date by selecting the date in the 'Due Date' field when creating the task."

    # If no context or new question, follow the regular flow
    return find_closest_answer_enhanced(user_query)


last_action = None

def handle_multi_turn_dialogue(user_query):
    global last_action

    # Check if the user has changed the topic
    if last_action and "task" not in user_query.lower() and "assign" not in user_query.lower():
        last_action = None  # Reset the context

    # Respond based on the previous context
    if last_action == 'creating_task':
        if "yes" in user_query.lower():
            last_action = 'assigning_task'
            return "You can assign the task by selecting a team member in the 'Assignee' field."
        else:
            last_action = None
            return "Okay, let me know if you need help with something else!"

    if last_action == 'assigning_task':
        if "due date" in user_query.lower():
            last_action = None
            return "You can set a due date by selecting the date in the 'Due Date' field."
        else:
            last_action = None
            return "Task assigned! Do you need help with anything else?"

    # Handle the initial request
    if "create" in user_query.lower() and "task" in user_query.lower():
        last_action = 'creating_task'
        return "To create a task, click on the 'Add Task' button in your project. Would you like to assign it to someone?"

    # Default to enhanced answer finding
    last_action = None
    return find_closest_answer_enhanced(user_query)



