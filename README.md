# 🎬 MovieMinds – Smart Movie Recommender

![Python](https://img.shields.io/badge/python-3.10-blue.svg)
![License](https://img.shields.io/badge/license-MIT-brightgreen)
![Last Commit](https://img.shields.io/github/last-commit/Adityarajsingh2904/MovieMinds-Movie-Recommender)
![Platform](https://img.shields.io/badge/Platform-Jupyter-lightgrey)

MovieMinds is a content-based movie recommender system that suggests similar movies using metadata and cosine similarity on TMDB dataset features.
The training data comes from the TMDB 5000 Movie Dataset available on Kaggle.

---

## 📂 Folder Structure

```
MovieMinds/
├── app.py                     # Script for standalone inference (if used)
├── model/                    # Saved model pickle files
├── notebook86c26b4f17.ipynb          # Main Jupyter notebook
├── requirements.txt           # Dependencies
├── README.md                  # Project documentation
└── .gitignore
```

---

## 🧠 How It Works

This system calculates cosine similarity between movie vectors derived from:
- Keywords
- Genres
- Director
- Cast

It then recommends top-N similar movies based on input.

---

## 🛠 Tech Stack

- **Python 3.10**
- **Pandas**, **Scikit-learn**, **Numpy**
- **Jupyter Notebook**
- TMDB 5000 Movie Dataset (Kaggle)

## 🔧 Generating the Similarity Model

1. Download `tmdb_5000_movies.csv` and `tmdb_5000_credits.csv` from Kaggle.
2. Run `notebook86c26b4f17.ipynb` to build the similarity matrix.
3. Save the resulting `movie_list.pkl` and `similarity.pkl` files in the `model/` folder.

---

## 🚀 Running Locally

1. 📦 Install dependencies

```bash
pip install -r requirements.txt
```

2. 📓 Open the notebook:

```bash
jupyter notebook
```

3. Run `notebook86c26b4f17.ipynb` and follow the input prompts
4. Ensure the `model/` directory contains `movie_list.pkl` and `similarity.pkl`

5. Launch the Streamlit app:
```bash
streamlit run app.py
```

---

## 🌟 Features

- Clean recommendations using cosine similarity
- Content-based, no login required
- 100% offline usage

---

## 🖼 Sample Screenshots

> 📌 _(Add actual screenshots below once app is run)_

| Input Movie | Top 5 Recommendations |
|-------------|------------------------|
| Inception   | Interstellar, Matrix…  |
| Avatar      | Titanic, Avengers…     |

---

## 📄 License

This project is licensed under the MIT License.

---

> ✨ Built with passion by Aditya Raj Singh


