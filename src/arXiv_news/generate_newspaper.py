import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from openai import OpenAI
from db_init import Paper  # Import the Paper model from your database initialization script
from dotenv import load_dotenv, dotenv_values
from utils import DB_LINK, ENV_PATH
load_dotenv(ENV_PATH)

# Initialize database session
engine = create_engine(DB_LINK)
Session = sessionmaker(bind=engine)
session = Session()


# OpenAI API setup
def analyze_text(prompt):
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content


# Get yesterday's date range
def get_yesterday_date_range():
    today = datetime.utcnow().date()
    if today.weekday() == 0:  # Monday
        yesterday = today - timedelta(days=3)  # Go back to Friday
    else:
        yesterday = today - timedelta(days=1)
    start_time = datetime(yesterday.year, yesterday.month, yesterday.day)
    end_time = start_time + timedelta(days=1)
    return start_time, end_time


# Fetch top 5 papers from yesterday
def get_top_5_papers():
    # start_time, end_time = get_yesterday_date_range()
    from get_from_db import load_config
    config = load_config()
    # Retrieve the last processed date
    oldest_processed_str = config.get('oldest_submission')
    last_processed_str = config.get('last_processed')
    oldest_processed = datetime.strptime(oldest_processed_str, '%Y-%m-%d %H:%M:%S')
    last_processed = datetime.strptime(last_processed_str, '%Y-%m-%d %H:%M:%S')
    papers = session.query(Paper).filter(
        Paper.submitted_time.between(oldest_processed, last_processed)
    ).order_by(Paper.score.desc()).limit(5).all()
    return papers


def generate_summary_for_papers(papers=None):
    if not papers:
        papers = get_top_5_papers()

    if not papers:
        return "No papers were found for yesterday."

    # Prepare collective information for the prompt
    paper_details = ""
    entry_ids = []
    for paper in papers:
        paper_details += (
            f"Title: {paper.title}\n"
            f"Abstract: {paper.abstract}\n"
            f"Subjects: {paper.subjects}\n\n"
        )
        entry_ids.append(paper.entry_id)

    # Design a collective prompt
    prompt = (
        f"Summarize the following five research papers for physicist audience (but not necessary same field) in "
        f"a newspaper-style summary (500-1000 characters). Include the collective "
        f"importance of these works, thread them together logically, and highlight "
        f"their overall significance in advancing knowledge. If you summarize these papers "
        f"in separate sentences for each one, I want you add '-' at first. \n\n"
        f"{paper_details}"
    )

    # Get the summary from OpenAI
    summary = analyze_text(prompt)
    text_sentence = summary.split("\n- ")
    new_summary = text_sentence[0]
    for i in range(1, len(text_sentence)):
        paper = papers[i - 1]
        new_summary += f"\n {i}. {paper.title}; {paper.entry_id}, {text_sentence[i]}"
    return new_summary


# Main function
if __name__ == "__main__":
    print("Generating newspaper for yesterday's top papers...")
    papers = get_top_5_papers()
    newspaper = generate_summary_for_papers(papers=papers)
    print(newspaper)
