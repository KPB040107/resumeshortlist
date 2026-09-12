from glob import glob

from explainer import explain_top3
from extractor import extract_jd_text, extract_resume_text
from matcher import score_candidates
from schema import CandidateResult


def run(jd_path: str, resume_paths: list[str]) -> list[CandidateResult]:
    jd_text = extract_jd_text(jd_path)
    if not jd_text:
        raise ValueError("No readable text was found in the job description PDF.")

    resume_texts = {path: extract_resume_text(path) for path in resume_paths}
    resume_texts = {path: text for path, text in resume_texts.items() if text}
    results = score_candidates(jd_text, resume_texts)
    results.sort(key=lambda candidate: candidate.final_score, reverse=True)

    for rank, candidate in enumerate(results, start=1):
        candidate.rank = rank

    results[:3] = explain_top3(jd_text, resume_texts, results[:3])
    return results


if __name__ == "__main__":
    jd_path = "data/jd.pdf"
    resume_paths = glob("data/resumes/*.pdf")
    for candidate in run(jd_path, resume_paths):
        print(candidate.rank, candidate.name, candidate.final_score)
