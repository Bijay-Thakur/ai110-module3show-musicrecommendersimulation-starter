# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommenders like Spotify or YouTube learn from massive amounts of behavioral data — skips, replays, playlist adds — to predict what a listener wants next without ever asking them directly. They also layer in collaborative filtering, meaning they surface songs that people with similar taste histories have enjoyed, even if those songs share no obvious features with what you just played. This version takes a simpler, fully transparent approach: instead of learning from behavior, it asks the user to describe their preferences directly (favorite genre, mood, energy level, and whether they prefer acoustic or electric sounds), then scores every song in the catalog using a weighted formula. Genre and mood carry the most weight because they represent the clearest categorical preferences — a lofi listener getting a rock track is a worse miss than a small energy mismatch. Energy similarity is scored continuously so that near-matches still get partial credit rather than being treated as complete misses. The result is a recommender that is easy to reason about and explain, at the cost of personalization depth: it cannot discover that you sometimes break your own patterns, and it treats every user with the same preference shape as equally served.

### Algorithm Recipe

The user provides a taste profile with four fields:

| Field | Type | Example |
|---|---|---|
| `genre` | string | `"jazz"` |
| `mood` | string | `"relaxed"` |
| `energy` | float 0–1 | `0.40` |
| `likes_acoustic` | boolean | `True` |

Every song in the catalog is then judged by the same four-step formula:

```
score = 0.0

1. Genre match      if song.genre == user.genre       → +0.35
2. Mood match       if song.mood  == user.mood         → +0.30
3. Energy distance  +0.25 × (1 − |song.energy − user.energy|)
4. Acoustic pref    if user.likes_acoustic matches     → +0.10
                    song.acousticness > 0.6

Maximum possible score: 1.00
```

After all songs are scored, they are sorted in descending order and the top K are returned alongside a plain-language explanation built from whichever conditions fired.

### Potential Biases

- **Genre over-dominance.** With a weight of 0.35, genre is the single largest factor. A song that perfectly matches every other preference — mood, energy, acousticness — can still score below a genre-matched song with nothing else in common. Great songs from adjacent genres (e.g., soul for a jazz user) will be systematically under-ranked.
- **Mood is binary.** "Relaxed" and "chill" feel very similar, but the algorithm treats them as a complete miss. Any song tagged with a near-synonym of the user's preferred mood receives zero credit for that field.
- **Catalog skew.** The dataset was hand-curated and does not represent all genres or cultures equally. Genres that happen to have more entries (lofi has three songs; reggae has one) give users of popular genres more good matches to choose from, while niche-genre users get fewer high-scoring options even if their profile is equally valid.
- **Static profile.** The user profile never updates. If a listener's mood shifts mid-session, the recommendations do not adapt — the system will keep returning the same ranked list.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```
![alt text]({2B1B667A-C780-49CD-9F55-1619A4289DBD}.png)
### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

