# arXiv_news
Tags: arXiv, science-newsletter, research-curation, python

**arXiv_news** is a Python-based project designed to advertise arXiv preprints into an accessible and curated scientific newsletter. It extracts, processes, and formats recent submissions across various disciplines, making them suitable for an audience of researchers, students, and enthusiasts.

## Features

- Automated fetching of arXiv preprints using keywords and categories.
- Database integration for efficient storage and retrieval of metadata.
- Formatting tools to generate newsletters from selected research papers.
- Integration-ready for email or web-based delivery systems.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/lvpinlei530/arXiv_news.git
   cd arXiv_news
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the database:
   Run the initialization script to create the database structure:
   ```bash
   python src/arXiv_news/db_init.py
   ```

## Usage

1. Configure settings in the `config/.env` file for openAI API and sending Slack message.
2. Run the main script to fetch and process arXiv data:
   ```bash
   python src/arXiv_news/main.py
   ```
   Particularly, the following functions are mainly used in the main script:
   ```python
   keywords = {"quantum": 1.0, "quantum computation": 1.0, "quantum information": 1.0, "circuit QED": 1.0,
                "superconducting qubit": 1.0, "dual-rail qubit": 1.0}
   from arxiv_fetch import populate_paper_db  # populate database from arXiv
   from get_from_db import grab_recent_papers, grab_since_last_processed  # grab papers from database
   from score import evaluate_paper  # calculate paper scores based on keywords provided
   from score import update_paper_scores_with_dict  # update paper scores from the grabbed paper
   from generate_newspaper import generate_summary_for_papers  # generate summary for papers using OpenAI API
   from utils import ENV_PATH, send_slack_message  # utils for functions
   ```

## License

This project is licensed under the terms of the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Commit your changes and push to your fork.
4. Submit a pull request.

## Contact

For questions or suggestions, feel free to reach out at [lvpinlei530@gmail.com](mailto:lvpinlei530@gmail.com).
