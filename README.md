# 🎬 MovieMinds – Smart Movie Recommender

![Python](https://img.shields.io/badge/python-3.10-blue.svg)
![License](https://img.shields.io/badge/license-MIT-brightgreen)
![Last Commit](https://img.shields.io/github/last-commit/Adityarajsingh2904/MovieMinds-Movie-Recommender)
![Platform](https://img.shields.io/badge/Platform-Jupyter-lightgrey)

MovieMinds is a content-based movie recommender system that suggests similar movies using metadata and cosine similarity on TMDB dataset features.
The training data comes from the TMDB 5000 Movie Dataset available on Kaggle.

---

## 📂 Folder Structure

```text
.
├── app.py
├── model/
├── notebook86c26b4f17.ipynb
├── requirements.txt
├── LICENSE
└── README.md
```


## 📝 Repo Setup

The `.gitignore` file ensures that generated folders like `__pycache__/` and
`.ipynb_checkpoints/` aren't committed to version control. Keep this file intact
after cloning so your repository stays clean.

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
- **Streamlit**, **Requests**
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

2. 🔑 Set your TMDB API key as an environment variable so posters can be fetched

```bash
export TMDB_API_KEY=<your-tmdb-key>
```

On Windows PowerShell use:

```powershell
$env:TMDB_API_KEY="<your-tmdb-key>"
```

3. ▶️ Start the application

```bash
streamlit run app.py
```

4. 📝 (Optional) Explore the notebook

```bash
jupyter notebook
```



---

## 🌟 Features

- Clean recommendations using cosine similarity
- Content-based, no login required
- Requires an internet connection for movie poster retrieval
- Offline mode possible only if poster images are cached or disabled

---

## 🖼 Sample Screenshots

> 📌 _(Add actual screenshots below once app is run)_

| Input Movie | Top 5 Recommendations |
|-------------|------------------------|
| Inception   | Interstellar, Matrix…  |
| Avatar      | Titanic, Avengers…     |

---

## 🔮 Future Enhancements

- **Transformer-based embeddings**: Explore models like `sentence-transformers` to represent movies with rich semantic vectors for better similarity.
- **GPT-powered tooling**: Investigate GPT-based document generation or code explanation utilities to help maintain the project.

## 📄 License

This project is licensed under the MIT License.

---

> ✨ Built with passion by Aditya Raj Singh


