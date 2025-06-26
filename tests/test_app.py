import sys
import types

# stub out external modules that are not installed
requests_stub = types.ModuleType('requests')
requests_stub.get = lambda *args, **kwargs: None
sys.modules['requests'] = requests_stub

# create a minimal stub for streamlit so app can be imported
st_stub = types.ModuleType('streamlit')
# provide minimal attributes used in app.py
st_stub.header = lambda *args, **kwargs: None
st_stub.selectbox = lambda *args, **kwargs: None
st_stub.button = lambda *args, **kwargs: False
st_stub.columns = lambda n: [None]*n
st_stub.text = lambda *args, **kwargs: None
st_stub.image = lambda *args, **kwargs: None
sys.modules['streamlit'] = st_stub

import app

class MockResponse:
    def __init__(self, data):
        self._data = data
    def json(self):
        return self._data

def test_fetch_poster(monkeypatch):
    def mock_get(url):
        return MockResponse({'poster_path': 'test.jpg'})
    monkeypatch.setattr(app.requests, 'get', mock_get)
    poster = app.fetch_poster(1)
    assert poster == 'https://image.tmdb.org/t/p/w500/test.jpg'

def test_recommend(monkeypatch, sample_data):
    movies, similarity = sample_data
    monkeypatch.setattr(app, 'movies', movies, raising=False)
    monkeypatch.setattr(app, 'similarity', similarity, raising=False)

    calls = []
    def mock_get(url):
        calls.append(url)
        return MockResponse({'poster_path': 'path.jpg'})
    monkeypatch.setattr(app.requests, 'get', mock_get)

    names, posters = app.recommend('Movie A')
    assert names == ['Movie B', 'Movie C', 'Movie D', 'Movie E', 'Movie F']
    assert posters == ['https://image.tmdb.org/t/p/w500/path.jpg'] * 5
    assert len(calls) == 5
