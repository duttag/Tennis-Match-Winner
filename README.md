# Tennis Match Winner — Python Solution

Determines the winner of a tennis match from the given sequence of point-by-point results, using
official tennis scoring rules including deuce, advantage, tiebreaks, and set logic.

---

## Table of Contents

- [Approach](#approach)
- [Project Structure](#project-structure)
- [How to Run](#how-to-run)
- [Scoring Rules Implemented](#scoring-rules-implemented)
- [Output](#output)
- [Test Cases](#test-cases)
- [Trade-offs & Design Decisions](#trade-offs--design-decisions)

---

## Approach

The solution considers a single tennis set by decomposing the match into three layers of
scoring — **points → games → set** — each handled by a dedicated function:

```
Input: ["A", "A", "B", "A", ...]
         │
         ▼
   play_game()          ← Handles 0/15/30/40, deuce & advantage
         │
         ▼
   play_tiebreak()      ← Triggered only at 6-6; first to 7 with 2-point margin
         │
         ▼
   determine_tennis_winner()  ← Orchestrates set logic, returns final result
```

**Key design insight:** 
The 6-6 tiebreak check is placed before `play_game()` is called, 
ensuring tiebreak points are never accidentally consumed as a regular game. 

---

## Project Structure

```
tennis_winner.py      ← Main solution file (all logic + test cases)
README.md             ← This file
```

---

## How to Run

### Prerequisites

- Python 3.7 or higher
- No external libraries required — uses only the Python standard library

### Run the solution with built-in tests

```bash
python tennis_winner.py
```

### Call as an API
If you want to use this solution from any other scripts:

```python
from tennis_winner import determine_tennis_winner

points = ["A", "A", "B", "A", "B", "B", "A", "A", "A", "A"]
result = determine_tennis_winner(points)

print(result["winner"])        # "A" or "B"
print(result["final_score"])   # e.g. "6-4"
print(result["tiebreak_played"])  # True / False
print(result["tiebreak_score"])   # e.g. "7-5" (only present if tiebreak was played)
```

---

## Scoring Rules Implemented

| Rule | Implementation |
|------|----------------|
| Points: 0 → 15 → 30 → 40 → Game | Integer counter (0,1,2,3,4) mapped to tennis terms |
| Deuce (40-40) | Both players at score `3`; require 2-point lead to win |
| Advantage | Natural outcome of deuce logic; no separate state needed |
| Game win | First to reach 4 points with a 2-point lead at or after deuce |
| Set win | First to 6 games with ≥ 2 game advantage (e.g. 6-4, 7-5) |
| Tiebreak trigger | Exactly at 6-6 in games |
| Tiebreak win | First to 7 points with ≥ 2 point advantage (e.g. 7-3, 8-6) |

---

## Output

`determine_tennis_winner()` returns a dictionary:

```python
{
    "winner": "A",               # Match winner
    "final_score": "7-6",        # Games won by each player
    "games_A": 7,
    "games_B": 6,
    "tiebreak_played": True,
    "tiebreak_score": "7-3"      # Only included if tiebreak was played
}
```

Console output (via `format_result()`):

```
========================================
  MATCH WINNER: Player A
========================================
  Final Score : 7-6 (games)
  Tiebreak    : 7-3
========================================
```

---

## Test Cases

| # | Scenario | Expected Result |
|---|----------|----------------|
| 1 | A wins every game cleanly | A wins 6-0 |
| 2 | B wins every game cleanly | B wins 0-6 |
| 3 | Alternating runs, A pulls ahead | A wins 7-5 |
| 4 | 6-6 tiebreak, A wins 7-6 | A wins 7-6, tiebreak 7-3 |
| 5 | All games go to deuce | A wins 6-4 |
| 6 | Extended tiebreak B wins 7-6 | B wins 7-6, tiebreak 6-8 |

Run `python tennis_winner.py` to execute all six tests with assertions.

---

## Design Decisions

###  Integer counters over string labels
Tennis points (0, 15, 30, 40) are represented as integers (0, 1, 2, 3) internally.
This keeps the deuce/advantage logic simple (`score >= 3`) without needing string
comparisons or a separate state machine.

###  Tiebreak check before game loop, not after
Checking for `6-6` at the **start** of each iteration (before calling
`play_game`) ensures tiebreak points are never misread as regular game points. 

###  Single-pass streaming over the points array
The solution reads the `points` list exactly once, left to right, passing an index
(`point_index`) between functions. There is no slicing or copying of sub-arrays, keeping
memory usage O(1) relative to input size.

---

## Assumptions

###  One set only
The problem specifies a single set, as given in the requirement. 

**Note:** Extending to best-of-3 or best-of-5 would require
wrapping the current set logic in an outer loop — the internal `play_game` and
`play_tiebreak` functions are already reusable and would not need changes.

###  No input validation
The solution assumes the input is a valid tennis match sequence (only `"A"` / `"B"` values,
and a sequence that always resolves to a winner), as given in the requirement. Adding input validation (empty array,
invalid characters, incomplete match) would be a natural next step for production use.

###  Tiebreak always at 6-6 (no final-set super-tiebreak)
This implementation uses the standard 7-point tiebreak at 6-6, consistent with the
one-set match format specified in the problem.