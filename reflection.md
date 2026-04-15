# Profile Comparison Reflections

---

## Profiles 1 & 3 — High-Energy Sad vs. Ghost User

Profile 1 (pop/sad/energy 0.9) and Profile 3 (jazz only, no other fields) both failed to
get what they asked for, but for opposite reasons. Profile 1 gave the system too much
conflicting information: the sad mood pointed toward low-energy songs, but the 0.9 energy
target pointed away from them. The system resolved the conflict by siding with energy —
the top two results were pop songs with "intense" and "happy" moods, not sad ones. The
only sad song in the catalog ranked third because its energy (0.33) was so far from 0.9
that the mood match couldn't compensate.

Profile 3 gave the system almost nothing to work with. With only genre specified, energy
silently defaulted to 0.5 and mood was skipped entirely. The jazz song came first because
it matched genre, but the next four results were country, r&b, lofi, and hip-hop — chosen
purely because their energy happened to sit near 0.5. This shows that the default energy
value doesn't represent "no preference" — it actively biases results toward mid-energy
songs as if the user had asked for them.

---

## Profiles 2 & 8 — Energy Extremist (10.0) vs. Negative Energy (-1.0)

Both profiles used energy values outside the valid 0.0–1.0 range, but they produced
different failure modes. Profile 2 (energy 10.0) caused every score to go negative — even
the perfect genre and mood match ("Storm Runner") topped out at -1.27. The energy penalty
was so large it swamped everything else. Profile 8 (energy -1.0) was less catastrophic:
the correct pop/happy song still ranked first at +0.165, because genre and mood together
(+0.475) partially offset the energy penalty. But songs ranked 4th and 5th had negative
scores, and the system described a song at energy 0.55 as "somewhat near" a target of
-1.0 — a gap of 1.55 — without any indication that the claim was nonsense.

The key difference: with energy weight at 0.50, an out-of-range value completely breaks
the scale, but a strong genre+mood match can still survive a moderately bad energy value.
Neither case produces an error or warning. Both demonstrate that the formula needs
clamping before it can be trusted with real user input.

---

## Profiles 4 & 5 — Case Typo vs. Synonym Trap

These two profiles both received zero credit for one or both categorical preferences, but
the reasons were different. Profile 4 ("Pop"/"Happy") was a pure input normalization
failure: the user's intent was clear and correct, but capitalization caused both genre and
mood to miss. The actual pop/happy song ("Sunrise City") ranked 4th, beaten by a
synthwave song that had no genre or mood match at all. This is the most fixable bug in the
system — a single `.lower()` call on both sides of the comparison would resolve it.

Profile 5 ("hip-hop"/"relaxed") was a harder problem. The genre value "hip-hop" did match
the catalog exactly, but "relaxed" did not appear on any hip-hop song. The only "relaxed"
song was jazz. So the top result was a jazz song (right mood, wrong genre) and second
place was a hip-hop song (right genre, wrong mood). Neither satisfied both preferences.
Unlike Profile 4, this isn't a bug — it's a genuine catalog gap. No normalization fix
helps here; the catalog simply doesn't have a hip-hop/relaxed song. The system should
ideally surface that gap rather than silently returning a best-effort result.

---

## Profiles 6 & 7 — Acoustic Ambivalence vs. Contradictory Acoustic

Profile 6 (folk/chill/energy 0.3, no acoustic preference) and Profile 7 (electronic/
energetic/energy 0.95, likes_acoustic: True) both involve the acousticness field, but in
opposite ways. Profile 6 omitted it entirely, which meant the maximum score any song could
achieve was 0.975 instead of 1.025. The folk song with a genre match ("Faded Photographs")
ranked 4th — three chill-mood songs from other genres beat it because their energy was
closer to 0.3 and they couldn't be penalized for missing an acoustic preference that
wasn't specified. Omitting a preference didn't stay neutral; it changed the ranking.

Profile 7 set a preference the catalog couldn't satisfy. The best electronic song
("Overdrive") has acousticness of 0.03 — solidly non-acoustic — so it could never earn
the acoustic bonus. Its score was 0.675 rather than the 0.775 it would have received if
the user's preference matched what electronic music actually sounds like. A country song
("Dirt Road Memory") crept into 4th place not because it was relevant but because it was
acoustic. The contradiction between genre preference and acoustic preference created a
situation where the system rewarded irrelevant songs for satisfying a preference the user
shouldn't have set in the first place.
