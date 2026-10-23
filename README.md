# ResumeShortlist (Candidate OS)

A local Streamlit app that compares PDF resumes with a PDF job description, ranks candidates, and shows why each candidate received their score. It is intended to help a recruiter review a shortlist, not to make a hiring decision automatically.

## What you can do

- Upload one job description PDF and one or more resume PDFs.
- See a ranked leaderboard, top-three candidate cards, score charts, and fit categories.
- Search and filter candidates by name, minimum score, category, or matched skill.
- Download the full ranking as CSV and a one-page PDF report for each of the top three candidates.
- Switch between dark and light themes.

## How it works

1. **Extract text:** `pdfplumber` reads selectable text from each PDF. Resumes with no readable text are skipped; a job description with no readable text stops the analysis.
2. **Find skills:** The app searches the text for a defined vocabulary of technical skills and normalizes a few aliases (for example, `reactjs` to `react`). The keyword score is the share of detected job-description skills also found in the resume.
3. **Compare meaning:** The `all-MiniLM-L6-v2` sentence-transformer model creates embeddings for the job description and resumes. Their normalized dot product gives the semantic score, clamped to 0–1.
4. **Rank:** The final score is **50% keyword score + 50% semantic score**. Candidates are sorted by that score. The top three get a text explanation listing matched and missing skills.
5. **Review and export:** The dashboard shows the scores and candidate fit categories. CSV and PDF downloads are generated from the results.

Scores are comparison aids, not calibrated probabilities or proof that a candidate is qualified. The skill list is limited, so a relevant skill outside the vocabulary will not appear in the keyword matches. Candidate names are derived from PDF filenames.

## Run locally

You need Python and an internet connection for the first download of the sentence-transformer model. Later runs can use the cached model. No API key is required.

```bash
git clone https://github.com/KPB040107/resumeshortlist.git
cd resumeshortlist
python -m venv .venv
```

Activate the environment:

- Windows PowerShell: `.venv\Scripts\Activate.ps1`
- macOS/Linux: `source .venv/bin/activate`

Then install the packages and start the app:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Open the local URL Streamlit prints (usually `http://localhost:8501`), upload a text-based job description PDF and at least one text-based resume PDF, and click **Analyze candidates**.

## Project files

| File | Purpose |
| --- | --- |
| `app.py` | Streamlit entry point, uploads, analysis flow, and downloads |
| `extractor.py` | PDF text extraction and skill detection |
| `matcher.py` | Keyword and semantic scores |
| `pipeline.py` | Extraction, ranking, and top-three explanations |
| `explainer.py` | Top-three explanation text |
| `ui.py` | Dashboard, charts, filters, and visual theme |
| `report_generator.py` | CSV leaderboard and candidate PDF reports |
| `schema.py` | Candidate result data structure |

## Data handling and limitations

The app writes uploaded PDFs to a temporary directory while an analysis runs and removes that directory afterward. The code does not save the uploaded PDFs to a database or send them to an external scoring API. If you deploy the app, review the hosting platform's upload, logging, and retention behavior separately.

Scanned or image-only PDFs need OCR before this app can read them. The scoring depends on extracted text and the built-in skill vocabulary; review the source resumes and job requirements before making any hiring decision.
