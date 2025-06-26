import pytest
from types import SimpleNamespace

class FakeSeries(list):
    def __eq__(self, other):
        return [item == other for item in self]

class FakeILoc:
    def __init__(self, rows):
        self._rows = rows
    def __getitem__(self, idx):
        return SimpleNamespace(**self._rows[idx])

class FakeDataFrame:
    def __init__(self, rows, indices=None):
        self._rows = rows
        self._indices = indices if indices is not None else list(range(len(rows)))
    def __getitem__(self, key):
        if isinstance(key, str):
            return FakeSeries([row[key] for row in self._rows])
        elif isinstance(key, list):
            subset_rows = [r for r, m in zip(self._rows, key) if m]
            subset_idx = [i for i, m in zip(self._indices, key) if m]
            return FakeDataFrame(subset_rows, subset_idx)
        raise NotImplementedError
    @property
    def index(self):
        return self._indices
    @property
    def iloc(self):
        return FakeILoc(self._rows)

def make_sample_dataset():
    rows = [
        {'movie_id': 1, 'title': 'Movie A'},
        {'movie_id': 2, 'title': 'Movie B'},
        {'movie_id': 3, 'title': 'Movie C'},
        {'movie_id': 4, 'title': 'Movie D'},
        {'movie_id': 5, 'title': 'Movie E'},
        {'movie_id': 6, 'title': 'Movie F'},
    ]
    movies = FakeDataFrame(rows)
    similarity = [
        [1.0, 0.9, 0.8, 0.7, 0.6, 0.5],
        [0.9, 1.0, 0.7, 0.6, 0.5, 0.4],
        [0.8, 0.7, 1.0, 0.6, 0.5, 0.4],
        [0.7, 0.6, 0.6, 1.0, 0.5, 0.4],
        [0.6, 0.5, 0.5, 0.5, 1.0, 0.4],
        [0.5, 0.4, 0.4, 0.4, 0.4, 1.0],
    ]
    return movies, similarity

@pytest.fixture
def sample_data():
    return make_sample_dataset()
