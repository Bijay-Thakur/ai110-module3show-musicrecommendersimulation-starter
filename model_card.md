# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**MoodMatch 1.0**

---

## 2. Intended Use

MoodMatch is designed to suggest songs from a small catalog based on how well each song fits a user's stated preferences. It is built for classroom exploration, not a real product. It assumes the user knows their preferred genre, mood, and energy level. It should not be used to make recommendations for real listeners in a production app, and it should not be used to draw conclusions about what music people "should" like based on demographic data.

---

## 3. How the Model Works

The system scores every song in the catalog against the user's preferences and returns the top 5. Each song gets points in up to four areas:

- **Genre match** — if the song's genre exactly matches what the user asked for, it earns points.
- **Mood match** — same idea: exact match earns points, anything else earns nothing.
- **Energy proximity** — songs closer to the user's target energy score higher. A perfect match scores full points; a song far away scores less.
- **Acoustic preference** — if the user said they like acoustic or electric music, songs that fit that preference earn a small bonus.

Energy is currently weighted the highest, at 50% of the total score. Genre is worth about 17.5% and mood is worth 30%. The acoustic bonus is worth 10%. Songs are ranked from highest to lowest score and the top 5 are returned.

---

## 4. Data

The catalog has 18 songs. Each song has a title, artist, genre, mood, energy level (0 to 1), tempo, and a few other audio features. The genres covered include pop, rock, lofi, jazz, hip-hop, electronic, metal, folk, classical, ambient, synthwave, indie pop, country, r&b, and reggae. Moods include happy, chill, intense, sad, relaxed, melancholic, angry, euphoric, peaceful, focused, moody, nostalgic, romantic, and uplifting.

The dataset was not modified. It has real limits: most genres have only one song, "chill" is the only mood with three songs, and there are no low-energy hip-hop, rock, or pop songs. Features like tempo, danceability, and valence are loaded but not used in scoring at all.

---

## 5. Strengths

The system works best for users whose preferences align with what the catalog actually contains. A user who wants high-energy pop or chill lofi will get reasonable results because those genres have songs that match both the mood and energy expectations. The energy scoring gives partial credit for near-matches instead of treating everything as pass or fail, which helps when no song is a perfect fit. The explanation output is useful — it tells the user exactly why each song was recommended, which makes the scoring logic easy to inspect and debug.

---

## 6. Limitations and Bias

The system has a strong low-energy filter bubble. Because energy accounts for half of the total score, any user who prefers calm or quiet music gets funneled into the same small group of ambient, lofi, jazz, and folk songs — regardless of what genre they actually asked for. A user who wants chill hip-hop and a user who wants chill classical will receive nearly identical recommendations, because no low-energy hip-hop exists in the catalog and energy dominates the score. The genre preference simply cannot compete.

Genre matching is also case-sensitive and exact. Typing "Pop" instead of "pop" results in zero genre credit. There is no fuzzy matching, no synonym handling, and no warning when a preference goes unrecognized. Users whose input doesn't match the catalog vocabulary are silently treated as if they had no preference at all.

Finally, energy values are never validated. Setting energy to 10.0 or -1.0 produces negative scores across the board, but the system still returns confident-sounding recommendations. There is no indication to the user that anything went wrong.

---

## 7. Evaluation

Eight adversarial profiles were tested against all 18 songs to look for edge cases and scoring failures. The profiles tested conflicting preferences (high energy + sad mood), out-of-range inputs (energy 10.0 and -1.0), incomplete profiles (genre only), capitalization mismatches ("Pop" vs "pop"), synonym mismatches ("relaxed" vs "chill"), missing optional fields, and self-contradictory preferences (electronic genre + acoustic preference).

The most surprising result was that every score went negative when energy was set to 10.0 — including the song that matched both genre and mood perfectly. The system returned those results with full explanations and no warnings. The capitalization test was also surprising: the correct pop/happy song ranked 4th behind three songs with zero genre or mood credit, just because of a capital letter. Both failures are silent — a user would have no way to know the recommendations were wrong.

---

## 8. Ideas for Improvement

- **Clamp and validate energy.** The energy input should be restricted to 0.0–1.0 before scoring. Any value outside that range should either be rejected or snapped to the nearest valid value. This would prevent negative scores entirely.
- **Normalize genre and mood input.** Converting both the user's input and the catalog values to lowercase before comparing would fix the capitalization bug with one line of code. Adding a small set of known synonyms (e.g., "chill" = "relaxed") would catch the most common vocabulary mismatches.
- **Expand the catalog and balance it.** Adding low-energy songs across more genres (hip-hop, rock, pop) would break the low-energy filter bubble. Ensuring each mood has at least two or three songs would reduce the "chill dominance" problem. A richer catalog makes the scoring logic more meaningful regardless of how the weights are set.

---

## 9. Personal Reflection

**Biggest learning moment:** The biggest thing I learned is that a recommender can be completely broken and still look like it's working. When energy was set to 10.0, every score went negative — but the system still printed "Matches your favorite genre" and returned a ranked list. Nothing crashed. Nothing warned. That moment made it clear that correctness and confidence are two different things, and a system can have a lot of the second without any of the first.

**How AI tools helped, and when I had to double-check:** AI tools were useful for spotting failure modes quickly — things like the energy dead zone between 0.62 and 0.74, or the fact that incomplete profiles are structurally disadvantaged because the max score changes depending on which fields are filled in. But I still had to run the actual code and read the real output to confirm those predictions. The analysis said Profile 5 would surface a jazz song as the top result for a hip-hop user, and it did — but I wouldn't have trusted that without seeing the numbers. AI tools are good at reasoning about logic; they still need you to verify against reality.

**What surprised me about simple algorithms feeling like recommendations:** The output looks convincing even when the logic is just four weighted conditions. Phrases like "Energy level closely matches your target" or "Fits your electric preference" read like the system understands you. But it doesn't — it just filled in a template. That gap between what the output sounds like and what actually happened under the hood is probably the most important thing I'll take away from this. Real recommenders have the same gap, just harder to see.

**What I'd try next:** I would add catalog coverage checking — before scoring, the system should tell the user if their genre or mood has fewer than two matching songs, so they know the results are constrained by the data and not just their preferences. I'd also try replacing the binary mood match with a small similarity map (e.g., "chill" and "relaxed" both count as partial matches) to see if it produces more intuitive results without much added complexity.
