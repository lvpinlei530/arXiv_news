from arxiv_fetch import populate_paper_db
from get_from_db import grab_recent_papers, grab_since_last_processed
from score import evaluate_paper
from score import update_paper_scores_with_dict
from generate_newspaper import generate_summary_for_papers
from utils import send_slack_message

keywords = {"quantum": 1.0, "quantum computation": 1.0, "quantum information": 1.0, "circuit QED": 1.0,
            "superconducting qubit": 1.0, "dual-rail qubit": 1.0}

if __name__ == '__main__':
    # Populate the database with arXiv publication, default to check last 7 days and skip the populated ones
    populate_paper_db()
    # Read from the config file to get the last processed date, and grab new paper since then.
    # Otherwise, grab recent papers (yesterday's papers)
    papers = grab_since_last_processed()
    papers_score = {}
    for paper_id, paper in papers.items():
        print(f"Paper ID: {paper_id}")
        papers_score[paper_id] = evaluate_paper(paper, keywords)
    update_paper_scores_with_dict(papers_score)
    newspaper = generate_summary_for_papers()
    send_slack_message(
        newspaper,
        f"#arxiv-newspaper",
    )
