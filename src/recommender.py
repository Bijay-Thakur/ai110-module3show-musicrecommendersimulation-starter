import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def _song_to_dict(self, song: Song) -> Dict:
        return {
            "id": song.id,
            "title": song.title,
            "artist": song.artist,
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
            "tempo_bpm": song.tempo_bpm,
            "valence": song.valence,
            "danceability": song.danceability,
            "acousticness": song.acousticness,
        }

    def _profile_to_dict(self, user: UserProfile) -> Dict:
        return {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        user_prefs = self._profile_to_dict(user)
        scored = []
        for song in self.songs:
            song_dict = self._song_to_dict(song)
            score, _ = score_song(user_prefs, song_dict)
            scored.append((song, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        user_prefs = self._profile_to_dict(user)
        song_dict = self._song_to_dict(song)
        _, reasons = score_song(user_prefs, song_dict)
        return "; ".join(reasons) if reasons else "This song is in our catalog"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"]           = int(row["id"])
            row["energy"]       = float(row["energy"])
            row["tempo_bpm"]    = float(row["tempo_bpm"])
            row["valence"]      = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.

    Weights:
      genre match     0.35  (binary)
      mood match      0.30  (binary)
      energy distance 0.25  (1 - |user_energy - song_energy|)
      acousticness    0.10  (boolean preference vs. threshold 0.6)

    Returns:
      (score, reasons) where score is in [0, 1] and reasons explains the match.
    """
    score = 0.0
    reasons = []

    # Genre match
    if song["genre"] == user_prefs.get("genre"):
        score += 0.35
        reasons.append(f"Matches your favorite genre ({song['genre']})")

    # Mood match
    if song["mood"] == user_prefs.get("mood"):
        score += 0.30
        reasons.append(f"Matches your preferred mood ({song['mood']})")

    # Energy similarity
    target_energy = user_prefs.get("energy", 0.5)
    energy_sim = 1.0 - abs(song["energy"] - target_energy)
    score += 0.25 * energy_sim
    if energy_sim >= 0.85:
        reasons.append("Energy level closely matches your target")
    else:
        reasons.append("Energy level is somewhat near your target")

    # Acousticness preference (only applied when preference is specified)
    likes_acoustic = user_prefs.get("likes_acoustic")
    if likes_acoustic is not None:
        is_acoustic = song["acousticness"] > 0.6
        if likes_acoustic == is_acoustic:
            score += 0.10
            label = "acoustic" if is_acoustic else "electric"
            reasons.append(f"Fits your {label} preference")

    return round(score, 4), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py

    Returns a list of (song_dict, score, explanation) tuples sorted by score descending.
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "No strong match found"
        scored.append((song, score, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
