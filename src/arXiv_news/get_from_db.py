import json
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db_init import Paper  # Import the Paper model
from utils import DB_LINK, CONFIG_FILE

# Initialize database session
engine = create_engine(DB_LINK)
Session = sessionmaker(bind=engine)
session = Session()


# Function to load configuration
def load_config():
    try:
        with open(CONFIG_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"last_processed": None}


# Function to save configuration
def save_config(config):
    with open(CONFIG_FILE, 'w') as file:
        json.dump(config, file, indent=4)


# Function to get all papers submitted on the most recent working day
def grab_recent_papers():
    # Load the configuration file
    config = load_config()

    # Calculate the target date
    today = datetime.utcnow().date()

    # Determine the last working day
    if today.weekday() == 0:  # Monday
        target_date = today - timedelta(days=4)  # Go back to Friday
    elif today.weekday() == 1:  # Tuesday
        target_date = today - timedelta(days=3)
    else:
        target_date = today - timedelta(days=2)  # Go back to yesterday

    # Query the database for papers submitted on the target date
    papers = session.query(Paper).filter(
        Paper.submitted_time.between(
            datetime(target_date.year, target_date.month, target_date.day),
            datetime(target_date.year, target_date.month, target_date.day, 23, 59, 59)
        )
    ).all()

    # Print and return the results
    results = {}
    if papers:
        print(f"Papers submitted on {target_date}:")
        for paper in papers:
            results[paper.paper_id] = f"Title: {paper.title}; Abstract: {paper.abstract}\n"
            print(f"ID: {paper.paper_id}; Title: {paper.title}")

        # Update the last processed date in the configuration to the latest submission time
        latest_submission = max(paper.submitted_time for paper in papers)
        oldest_submission = min(paper.submitted_time for paper in papers)
        config['last_processed'] = latest_submission.strftime('%Y-%m-%d %H:%M:%S')
        config['oldest_submission'] = oldest_submission.strftime('%Y-%m-%d %H:%M:%S')
    else:
        print(f"No papers were submitted on {target_date}.")

    save_config(config)
    return results


# Function to get papers since the last processed date
def grab_since_last_processed():
    # Load the configuration file
    config = load_config()

    # Retrieve the last processed date
    last_processed_str = config.get('last_processed')
    if not last_processed_str:
        grab_recent_papers()
        return ""

    last_processed = datetime.strptime(last_processed_str, '%Y-%m-%d %H:%M:%S')
    today = datetime.utcnow()

    # Query the database for papers submitted since the last processed date
    papers = session.query(Paper).filter(
        Paper.submitted_time >= last_processed,
        Paper.submitted_time <= today
    ).all()

    # Print and return the results
    results = {}
    if papers:
        print(f"Papers submitted since {last_processed}:")
        for paper in papers:
            results[paper.paper_id] = f"Title: {paper.title}; Abstract: {paper.abstract}\n"
            print(f"ID: {paper.paper_id}; Title: {paper.title}")

        # Update the last processed date to the latest submission time
        latest_submission = max(paper.submitted_time for paper in papers)
        oldest_submission = min(paper.submitted_time for paper in papers)
        config['last_processed'] = latest_submission.strftime('%Y-%m-%d %H:%M:%S')
        config['oldest_submission'] = oldest_submission.strftime('%Y-%m-%d %H:%M:%S')
    else:
        print(f"No papers were submitted since {last_processed}.")

    save_config(config)
    return results


if __name__ == '__main__':
    # print("Running grab_recent_papers...")
    # grab_recent_papers()
    print("\nRunning grab_since_last_processed...")
    grab_since_last_processed()
