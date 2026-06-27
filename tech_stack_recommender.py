"""
==========================================================
 DecodeLabs Industrial Training Kit - Artificial Intelligence
 Project 3: AI Recommendation Logic
 Capstone: Tech Stack Recommender
==========================================================

GOAL:
Build a content-based recommendation engine that maps a user's
raw skills/interests to the most relevant career role (job role),
using TF-IDF vectorization + Cosine Similarity (no historical
user data required -> avoids the "Cold Start" problem).

PIPELINE (Input -> Process -> Output):
 1. Ingestion  -> Take at least 3 user skills as input
 2. Scoring    -> Convert text into TF-IDF vectors, compute Cosine Similarity
 3. Sorting    -> Rank job roles by similarity score (descending)
 4. Filtering  -> Return Top-3 most relevant job roles
"""

import csv
import math
import re
from collections import Counter


# ----------------------------------------------------------
# STEP 0: Helper - text cleaning / tokenization
# ----------------------------------------------------------
def tokenize(text):
    """Lowercase and split text into clean word tokens."""
    text = text.lower()
    tokens = re.findall(r"[a-z0-9\+\#]+", text)
    return tokens


# ----------------------------------------------------------
# STEP 1: INGESTION - Load the job-role dataset (the "items")
# ----------------------------------------------------------
def load_dataset(csv_path):
    """
    Reads raw_skills.csv and returns:
        roles       -> list of job role names
        documents   -> list of tokenized skill-lists (one per role)
    """
    roles = []
    documents = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            roles.append(row["job_role"])
            documents.append(tokenize(row["skills"]))
    return roles, documents


# ----------------------------------------------------------
# STEP 2: PROCESS - Build TF-IDF vectors (shared vocabulary space)
# ----------------------------------------------------------
def build_vocabulary(documents):
    """Creates the master list of unique terms across all documents."""
    vocab = sorted(set(term for doc in documents for term in doc))
    return vocab


def compute_tf(doc, vocab):
    """Term Frequency: count(term) / total terms in the document."""
    total_terms = len(doc)
    counts = Counter(doc)
    return [counts[term] / total_terms if total_terms > 0 else 0 for term in vocab]


def compute_idf(documents, vocab):
    """
    Inverse Document Frequency:
        idf(t) = log(Total Documents / Documents containing t)
    Penalizes generic terms that appear in many job roles.
    """
    n_docs = len(documents)
    idf_scores = []
    for term in vocab:
        doc_count = sum(1 for doc in documents if term in doc)
        idf = math.log(n_docs / doc_count) + 1  # +1 smoothing avoids idf = 0
        idf_scores.append(idf)
    return idf_scores


def build_tfidf_vector(doc, vocab, idf_scores):
    """Combines TF and IDF -> a single weighted vector for one document."""
    tf = compute_tf(doc, vocab)
    return [tf[i] * idf_scores[i] for i in range(len(vocab))]


# ----------------------------------------------------------
# STEP 3: SCORING - Cosine Similarity (angle-based, magnitude-independent)
# ----------------------------------------------------------
def cosine_similarity(vec_a, vec_b):
    """
    cos(theta) = (A . B) / (||A|| * ||B||)
    Returns 0 if either vector has zero magnitude (handles Cold Start safely).
    """
    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    mag_a = math.sqrt(sum(a * a for a in vec_a))
    mag_b = math.sqrt(sum(b * b for b in vec_b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot_product / (mag_a * mag_b)


# ----------------------------------------------------------
# MAIN ENGINE - Tech Stack Recommender
# ----------------------------------------------------------
class TechStackRecommender:
    def __init__(self, csv_path):
        self.roles, self.documents = load_dataset(csv_path)
        self.vocab = build_vocabulary(self.documents)
        self.idf_scores = compute_idf(self.documents, self.vocab)
        # Pre-compute TF-IDF vectors for every job role ("item")
        self.role_vectors = [
            build_tfidf_vector(doc, self.vocab, self.idf_scores)
            for doc in self.documents
        ]

    def recommend(self, user_skills, top_n=3):
        """
        Steps 1-4 of the ranking pipeline applied to a single user query.
        user_skills: list of strings, e.g. ["Python", "Cloud Computing", "Automation"]
        """
        if len(user_skills) < 3:
            raise ValueError("Please provide at least 3 skills for accurate matching.")

        # Step 1: Ingestion - tokenize the user's raw input
        user_tokens = tokenize(" ".join(user_skills))

        # Step 2: Process/Scoring - vectorize user profile + compute similarity
        user_vector = build_tfidf_vector(user_tokens, self.vocab, self.idf_scores)

        scores = []
        for role, role_vector in zip(self.roles, self.role_vectors):
            score = cosine_similarity(user_vector, role_vector)
            scores.append((role, round(score, 4)))

        # Step 3: Sorting - descending by similarity score
        scores.sort(key=lambda x: x[1], reverse=True)

        # Step 4: Filtering - return only the Top-N
        return scores[:top_n]


# ----------------------------------------------------------
# DEMO / TEST RUN
# ----------------------------------------------------------
if __name__ == "__main__":
    engine = TechStackRecommender("raw_skills.csv")

    test_cases = [
        ["Python", "Cloud Computing", "Automation"],
        ["JavaScript", "React", "Web Design"],
        ["SQL", "Excel", "Statistics"],
        ["Python", "Machine Learning", "Deep Learning"],
    ]

    for skills in test_cases:
        print(f"\nUser Skills: {skills}")
        recommendations = engine.recommend(skills, top_n=3)
        for rank, (role, score) in enumerate(recommendations, start=1):
            print(f"  {rank}. {role:<28} -> Similarity Score: {score}")
