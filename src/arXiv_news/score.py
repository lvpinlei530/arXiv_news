from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from db_init import Paper  # Import the Paper model from your database initialization script
from utils import DB_LINK

# Initialize database session
engine = create_engine(DB_LINK)
Session = sessionmaker(bind=engine)
session = Session()


def tanh_curve(x, k=5):
    """
    Custom curve function based on scaled tanh.
    Maps 0 to 0 and 1 to 100, with the steepest increase at 0.5.

    Parameters:
    x : float or array-like, input in the range [0, 1]
    k : float, steepness of the curve

    Returns:
    float or array-like, output in the range [0, 100]
    """
    # Scaled tanh function
    return 100 * 0.5 * (np.tanh(k * (x - 0.5)) + 1)


def evaluate_paper(paper, keywords):
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words='english')
    tfidf_matrix = vectorizer.fit_transform([paper])
    # Get keyword vector
    keyword_vector = np.zeros(tfidf_matrix.shape[1])  # Initialize vector
    for word, weight in keywords.items():
        if word in vectorizer.vocabulary_:
            idx = vectorizer.vocabulary_[word]
            keyword_vector[idx] = weight
    keyword_vector = keyword_vector / np.linalg.norm(keyword_vector)
    try:
        similarity = cosine_similarity(tfidf_matrix, keyword_vector.reshape(1, -1))
    except ValueError:
        return np.array(0.0)
    return np.round(tanh_curve(similarity)[0][0], 2)


def update_paper_scores_with_dict(score_dict):
    # Update scores in the database
    for paper_id, score in score_dict.items():
        paper = session.query(Paper).filter_by(paper_id=paper_id).first()
        if paper:
            paper.score = score
            print(f"Updated Paper ID {paper_id} with score {score}")
        else:
            print(f"Paper ID {paper_id} not found in the database.")

    # Commit the changes
    session.commit()
    print("Scores updated successfully.")


# Obsolete function
def update_paper_scores_with_string(score_string):
    # Parse the string to extract paper_id and score pairs
    lines = score_string.strip().split("\n")
    scores = {}
    for line in lines:
        if ";" in line:
            subline = line.split(";")
            for sl in subline:
                print(sl)
                if ":" in sl:
                    parts = sl.split(":")
                    try:
                        paper_id = int(parts[0].strip())
                        score = int(parts[1].strip().replace(";", ""))
                        scores[paper_id] = score
                    except ValueError as e:
                        # raise e
                        print(f"Skipping invalid line: {sl}")

    # Update scores in the database
    for paper_id, score in scores.items():
        paper = session.query(Paper).filter_by(paper_id=paper_id).first()
        if paper:
            paper.score = score
            print(f"Updated Paper ID {paper_id} with score {score}")
        else:
            print(f"Paper ID {paper_id} not found in the database.")

    # Commit the changes
    session.commit()
    print("Scores updated successfully.")


if __name__ == "__main__":
    pass
    # Call the function
