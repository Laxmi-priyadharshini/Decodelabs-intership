# AI Recommendation Logic — Tech Stack Recommender
**DecodeLabs Industrial Training Kit | Artificial Intelligence | Project 3**

## Overview
A content-based recommendation engine that maps a user's raw skills to the
most relevant job role, using **TF-IDF vectorization** + **Cosine Similarity**.
No historical user data needed — pure similarity logic between user input and
item (job role) attributes.

## Files
| File | Purpose |
|---|---|
| `tech_stack_recommender.py` | Main recommendation engine (run this) |
| `raw_skills.csv` | Dataset of 15 job roles and their associated skills |
| `make_chart.py` | Generates the similarity score bar chart |
| `similarity_chart.png` | Output visualization |
| `Project_3_AI_Recommendation_Logic_Report.pdf` / `.docx` | Full submission report |

## Setup
1. Put `tech_stack_recommender.py` and `raw_skills.csv` in the **same folder**.
2. Make sure you're running Python from that folder (or use the full file path
   inside the script — see Troubleshooting below).
3. No external libraries required to run the core engine (uses only Python's
   built-in `csv`, `math`, `re`, `collections`).
   - Optional: `pip install matplotlib` if you want to regenerate the chart.

## How to Run
```bash
python tech_stack_recommender.py
```

This runs 4 built-in test cases and prints the Top-3 recommended job roles
for each, with similarity scores.

## How to Use With Your Own Skills
```python
from tech_stack_recommender import TechStackRecommender

engine = TechStackRecommender("raw_skills.csv")
results = engine.recommend(["Python", "Cloud Computing", "Automation"], top_n=3)

for rank, (role, score) in enumerate(results, start=1):
    print(f"{rank}. {role} -> {score}")
```
**Note:** You must provide at least 3 skills.

## How It Works (Pipeline)
1. **Ingestion** — take at least 3 user skills as input
2. **Scoring** — convert user profile + every job role into TF-IDF vectors,
   compute Cosine Similarity between them
3. **Sorting** — rank job roles by similarity score (descending)
4. **Filtering** — return only the Top-3 highest-scoring roles

## Troubleshooting
**`FileNotFoundError: raw_skills.csv`**
The CSV isn't in the folder Python is looking in. Fix by either:
- Moving `raw_skills.csv` into the same folder as the script, **or**
- Using the full path:
  ```python
  engine = TechStackRecommender(r"C:\path\to\your\folder\raw_skills.csv")
  ```
- Check your current working directory with:
  ```python
  import os
  print(os.getcwd())
  ```

## Author
Priya — DecodeLabs Industrial Training Kit, AI Track, Batch 2026
