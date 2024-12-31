import arxiv
import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db_init import Paper, Author  # Import models from the initialization script
from utils import DB_PATH, DB_LINK, DATE_RANGE

if not os.path.exists(DB_PATH):
    raise FileNotFoundError(f"Database file not found at {DB_PATH}, please run 'db_init.py' to initialize local"
                            f"database")


# Function to populate the database with papers and authors
def populate_paper_db():
    # Initialize database session
    engine = create_engine(f"{DB_LINK}")
    Session = sessionmaker(bind=engine)
    session = Session()

    # Construct the ArXiv API client
    client = arxiv.Client()

    # Search for the latest articles
    search = arxiv.Search(
        query=f"cat:quant-ph AND submittedDate:[{DATE_RANGE}]",  # Quantum physics category
        max_results=200,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Ascending
    )

    for result in client.results(search):
        # Check if the paper is already in the database
        existing_paper = session.query(Paper).filter_by(entry_id=result.entry_id).first()
        print(f"Paper '{result.title}' ")
        if existing_paper:
            print(f"Paper '{result.title}' already exists in the database. Skipping...")
            continue

        # Create a new Paper object
        new_paper = Paper(
            entry_id=result.entry_id,  # ArXiv ID
            title=result.title,
            abstract=result.summary,
            subjects=", ".join(result.categories),
            meta_data="",  # Optional, for any additional metadata
            submitted_time=result.published,  # Submission time
            score=0.0  # Default score
        )

        # Add authors to the paper
        for author in result.authors:
            # Check if the author already exists in the database
            existing_author = session.query(Author).filter_by(name=author.name).first()

            if not existing_author:
                # Create a new Author object if not found
                existing_author = Author(
                    name=author.name,
                    affiliation=author.affiliation if hasattr(author, 'affiliation') else None,
                    citation=0,  # Default value
                    recent_citation=0,
                    h_index=0,
                    recent_h_index=0,
                    i10_index=0,
                    recent_i10_index=0,
                    scores=0.0,
                    tags=""
                )
                session.add(existing_author)

            # Associate the author with the paper
            new_paper.authors.append(existing_author)

        # Add the new paper to the session
        session.add(new_paper)
        print(f"Added new paper: '{result.title}' with authors: {[author.name for author in result.authors]}")

    # Commit the session to save all changes
    session.commit()
    print("Database updated successfully.")


if __name__ == '__main__':
    populate_paper_db()
