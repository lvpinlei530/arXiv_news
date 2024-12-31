import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base
from eralchemy import render_er
from utils import DB_LINK

# Base class for the database models
Base = declarative_base()

# Many-to-Many Relationship Table
AuthorsPapers = Table(
    'authors_papers', Base.metadata,
    Column('author_id', Integer, ForeignKey('authors.author_id'), primary_key=True),
    Column('paper_id', Integer, ForeignKey('papers.paper_id'), primary_key=True)
)


# Authors Table
class Author(Base):
    __tablename__ = 'authors'
    author_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    affiliation = Column(String)
    citation = Column(Integer, default=0)
    recent_citation = Column(Integer, default=0)
    h_index = Column(Integer, default=0)
    recent_h_index = Column(Integer, default=0)
    i10_index = Column(Integer, default=0)
    recent_i10_index = Column(Integer, default=0)
    scores = Column(Float, default=0.0)
    tags = Column(Text)
    last_updated = Column(DateTime)
    # Relationship with Papers
    papers = relationship('Paper', secondary=AuthorsPapers, back_populates='authors')


# Papers Table
class Paper(Base):
    __tablename__ = 'papers'
    paper_id = Column(Integer, primary_key=True, autoincrement=True)  # Local unique ID
    entry_id = Column(String, unique=True, nullable=False)  # ArXiv entry ID (unique globally)
    title = Column(String, nullable=False)
    abstract = Column(Text)
    subjects = Column(Text)
    meta_data = Column(String)  # Additional metadata (if any)
    score = Column(Float, default=0.0)
    submitted_time = Column(DateTime, nullable=False)  # Submission time from ArXiv

    # Relationship with Authors
    authors = relationship('Author', secondary=AuthorsPapers, back_populates='papers')


# Initialize the database
def initialize_database(db_path='sqlite:///local_database.db'):
    engine = create_engine(db_path)
    Base.metadata.create_all(engine)
    print(f"Database initialized at {db_path}.")


# Generate an ER Diagram
def generate_er_diagram(db_path='sqlite:///arXiv_news/data/local_database.db', output_file='er_diagram.png'):
    try:
        # Render the ER diagram
        render_er(db_path, output_file)
        print(f"ER diagram generated and saved to {output_file}.")
    except Exception as e:
        print(f"Error generating ER diagram: {e}")


if __name__ == '__main__':
    print('Feel free to run this script to initialize the database and generate the ER diagram.')
    initialize_database(DB_LINK)  # Initialize the database
    # generate_er_diagram(DB_LINK)  # Generate the ER diagram
