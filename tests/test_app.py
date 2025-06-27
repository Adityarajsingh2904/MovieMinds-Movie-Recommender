import sys
import types

import importlib
import builtins
import os
import io
import pickle

import pytest


def load_app(monkeypatch):
    """Import the app module with stubbed dependencies."""
    streamlit_stub = types.SimpleNamespace(
        error=lambda *a, **k: None,
        stop=lambda: None,
        header=lambda *a, **k: None,
        selectbox=lambda *a, **k: None,
        button=lambda *a, **k: False,
        columns=lambda n: [
            types.SimpleNamespace(
                text=lambda *a, **k: None, image=lambda *a, **k: None
            )
            for _ in range(n)
        ],
        secrets=types.SimpleNamespace(get=lambda *a, **k: None),
        cache_data=lambda **d: (lambda f: f),
    )
    requests_stub = types.SimpleNamespace()
    monkeypatch.setitem(sys.modules, "streamlit", streamlit_stub)
    monkeypatch.setitem(sys.modules, "requests", requests_stub)
    monkeypatch.setattr(os.path, "exists", lambda *a, **k: True)
    monkeypatch.setattr(builtins, "open", lambda *a, **k: io.BytesIO())
    class FakeMovies:
        def __getitem__(self, key):
            return types.SimpleNamespace(values=[])
    fake_movie_obj = FakeMovies()
    load_counter = {"i": 0}
    def fake_load(f):
        load_counter["i"] += 1
        return fake_movie_obj if load_counter["i"] == 1 else []
    monkeypatch.setattr(pickle, "load", fake_load)
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
        @property
        def values(self):
            return self

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

    def mock_get(url, **kwargs):
        assert kwargs.get("timeout") == 5
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


def test_ui_handles_short_results(monkeypatch):
    app = load_app(monkeypatch)

    # Configure streamlit stub to run the UI code
    st_mod = sys.modules["streamlit"]

    class Column:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            pass

        def text(self, *args, **kwargs):
            pass

        def image(self, *args, **kwargs):
            pass

    st_mod.button = lambda *a, **k: True
    st_mod.selectbox = lambda *a, **k: "A"
    st_mod.columns = lambda n: [Column() for _ in range(n)]
    st_mod.text = lambda *a, **k: None
    st_mod.image = lambda *a, **k: None

    rows = [
        {"movie_id": 1, "title": "A"},
        {"movie_id": 2, "title": "B"},
    ]
    movies = DummyMovies(rows)
    similarity = [
        [1, 0.9],
        [0.9, 1],
    ]

    load_counter = {"i": 0}

    def fake_load(_):
        load_counter["i"] += 1
        return movies if load_counter["i"] == 1 else similarity

    monkeypatch.setattr(pickle, "load", fake_load)
    monkeypatch.setattr(
        sys.modules["requests"],
        "get",
        lambda *a, **k: types.SimpleNamespace(
            json=lambda: {"poster_path": "test.jpg"},
            raise_for_status=lambda: None,
        ),
        raising=False,
    )
    monkeypatch.setenv("TMDB_API_KEY", "dummy")

    import importlib

    importlib.reload(app)

