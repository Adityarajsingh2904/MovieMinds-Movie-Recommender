# 🎬 MovieMinds – Smart Movie Recommender

![Python](https://img.shields.io/badge/python-3.10-blue.svg)
![License](https://img.shields.io/badge/license-MIT-brightgreen)
![Last Commit](https://img.shields.io/github/last-commit/Adityarajsingh2904/MovieMinds-Movie-Recommender)
![Platform](https://img.shields.io/badge/Platform-Jupyter-lightgrey)

MovieMinds is a content-based movie recommender system that suggests similar movies using metadata and cosine similarity on TMDB dataset features.

---

## 📂 Folder Structure

```
MovieMinds/
├── app.py                     # Script for standalone inference (if used)
├── notebookXYZ.ipynb          # Main Jupyter notebook
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
- **Streamlit**, **Requests**
- **Jupyter Notebook**
- TMDB Dataset

---

## 🚀 Running Locally

1. 📦 Install dependencies

```bash
pip install -r requirements.txt
```

2. 🚀 Launch the Streamlit app (optional):

```bash
streamlit run app.py
```

3. 📓 Or open the notebook:

```bash
jupyter notebook
```

4. Run `notebook86c26b4f17.ipynb` and follow the input prompts

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


