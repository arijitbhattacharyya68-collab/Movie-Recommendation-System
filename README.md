# Movie Recommendation System

A Content-Based Movie Recommendation System built using Python, Pandas, and Scikit-Learn. It recommends movies similar to a given movie by analyzing genres, cast, crew, keywords, and movie overview using Natural Language Processing (NLP).

---

## Project Overview

This recommendation system uses content-based filtering instead of user ratings. It compares movie features such as genres, actors, directors, keywords, and plot summaries to find similar movies.

Movie information is converted into numerical vectors using CountVectorizer, and similarity between movies is computed using Cosine Similarity.

---

## Features

- Data preprocessing and cleaning
- Feature extraction from multiple columns
- Text vectorization using CountVectorizer
- Cosine similarity computation
- Movie recommendation function
- Model serialization using Pickle

---

## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Pickle

---

## Dataset

This project uses the TMDB 5000 Movie Dataset.

Files used:
- tmdb_5000_movies.csv
- tmdb_5000_credits.csv

---

## Project Workflow

1. Load the movie and credits datasets.
2. Merge both datasets.
3. Select the required features.
4. Clean and preprocess the text data.
5. Create a combined `tags` column.
6. Convert the text into vectors using CountVectorizer.
7. Compute cosine similarity.
8. Recommend the top similar movies.

---

## How to Run

1. Clone this repository.
2. Install the required libraries using:

   `pip install -r requirements.txt`

3. Download the TMDB 5000 Movie Dataset.
4. Open the Jupyter Notebook.
5. Run all the cells.

---

## Sample Recommendation

Example:

recommend("Avatar")

Output:

- Avatar
- John Carter
- Guardians of the Galaxy
- Star Trek
- The Avengers

---



