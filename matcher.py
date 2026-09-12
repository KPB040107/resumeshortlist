from pathlib import Path

import numpy as np

from extractor import extract_skills
from schema import CandidateResult


KEYWORD_WEIGHT = 0.5
SEMANTIC_WEIGHT = 0.5
MODEL_NAME = "all-MiniLM-L6-v2"
_model = None


def _get_model():
    global _model
    if _model is None:
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as error:
            raise RuntimeError(
                "Install semantic matching with: pip install sentence-transformers"
            ) from error
        try:
            _model = SentenceTransformer(MODEL_NAME)
        except Exception as error:
            raise RuntimeError(
                f"Could not load {MODEL_NAME}. Connect to the internet for the first model download."
            ) from error
    return _model


def _semantic_scores(jd_text: str, resume_texts: list[str]) -> list[float]:
    if not resume_texts:
        return []
    embeddings = _get_model().encode(
        [jd_text, *resume_texts],
        normalize_embeddings=True,
    )
    jd_embedding = embeddings[0]
    return [
        max(0.0, min(1.0, float(np.dot(jd_embedding, embedding))))
        for embedding in embeddings[1:]
    ]


def score_candidates(
    jd_text: str,
    resume_texts: dict[str, str],
) -> list[CandidateResult]:
    jd_skills = set(extract_skills(jd_text))
    paths = list(resume_texts)
    semantic_scores = _semantic_scores(jd_text, [resume_texts[path] for path in paths])
    results = []

    for path, semantic_score in zip(paths, semantic_scores):
        resume_skills = set(extract_skills(resume_texts[path]))
        matched = sorted(jd_skills & resume_skills)
        missing = sorted(jd_skills - resume_skills)
        keyword_score = len(matched) / len(jd_skills) if jd_skills else 0.0
        final_score = KEYWORD_WEIGHT * keyword_score + SEMANTIC_WEIGHT * semantic_score
        results.append(
            CandidateResult(
                candidate_id=path,
                name=Path(path).stem.replace("_", " ").replace("-", " ").title(),
                keyword_score=round(keyword_score, 4),
                semantic_score=round(semantic_score, 4),
                final_score=round(final_score, 4),
                matched_keywords=matched,
                missing_keywords=missing,
            )
        )
    return results
