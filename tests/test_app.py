import sys
import types
import importlib
import builtins
import os

import pytest


def load_app(monkeypatch):
    """Import the app module with stubbed dependencies."""
    streamlit_stub = types.SimpleNamespace(
        error=lambda *a, **k: None,
        stop=lambda: None,
        header=lambda *a, **k: None,
        selectbox=lambda *a, **k: None,
        button=lambda *a, **k: False,
        columns=lambda n: [types.SimpleNamespace(text=lambda *a, **k: None,
                                                image=lambda *a, **k: None) for _ in range(n)],
    )
    requests_stub = types.SimpleNamespace()
    monkeypatch.setitem(sys.modules, "streamlit", streamlit_stub)
    monkeypatch.setitem(sys.modules, "requests", requests_stub)
    # Ensure repository root is on sys.path for imports
    repo_root = os.path.dirname(os.path.dirname(__file__))
    monkeypatch.syspath_prepend(repo_root)
    if "app" in sys.modules:
        del sys.modules["app"]
    return importlib.import_module("app")


class DummyMovies:
    class TitleList(list):
        def __eq__(self, other):
            return [x == other for x in self]

    def __init__(self, rows, indexes=None):
        self.rows = list(rows)
        self._indexes = list(range(len(rows))) if indexes is None else indexes

    def __getitem__(self, key):
        if isinstance(key, str):
            if key == "title":
                return DummyMovies.TitleList([row["title"] for row in self.rows])
            raise KeyError(key)
        elif isinstance(key, list):
            selected_rows = [row for row, flag in zip(self.rows, key) if flag]
            selected_idx = [idx for idx, flag in zip(self._indexes, key) if flag]
            return DummyMovies(selected_rows, selected_idx)
        else:
            raise TypeError

    @property
    def index(self):
        return self._indexes

    class _ILoc:
        def __init__(self, outer):
            self.outer = outer
        def __getitem__(self, idx):
            row = self.outer.rows[idx]
            return types.SimpleNamespace(**row)

    @property
    def iloc(self):
        return DummyMovies._ILoc(self)


def test_fetch_poster(monkeypatch):
    app = load_app(monkeypatch)

    class MockResponse:
        def json(self):
            return {"poster_path": "test.jpg"}
        def raise_for_status(self):
            pass

    def mock_get(url):
        return MockResponse()

    monkeypatch.setattr(app.requests, "get", mock_get, raising=False)
    monkeypatch.setenv("TMDB_API_KEY", "dummy")

    assert (
        app.fetch_poster(123)
        == "https://image.tmdb.org/t/p/w500/test.jpg"
    )


def test_recommend(monkeypatch):
    app = load_app(monkeypatch)
    rows = [
        {"movie_id": 1, "title": "A"},
        {"movie_id": 2, "title": "B"},
        {"movie_id": 3, "title": "C"},
    ]
    movies = DummyMovies(rows)
    similarity = [
        [1, 0.1, 0.9],
        [0.1, 1, 0.2],
        [0.9, 0.2, 1],
    ]
    monkeypatch.setattr(app, "movies", movies)
    monkeypatch.setattr(app, "similarity", similarity)
    monkeypatch.setattr(app, "fetch_poster", lambda mid: f"url_{mid}")

    names, posters = app.recommend("A")
    assert names == ["C", "B"]
    assert posters == ["url_3", "url_2"]
