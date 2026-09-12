from schema import CandidateResult


def _format_keywords(keywords: list[str]) -> str:
    return ", ".join(keywords) if keywords else "none"


def explain_top3(
    jd_text: str,
    resume_texts: dict[str, str],
    top3: list[CandidateResult],
) -> list[CandidateResult]:
    for candidate in top3:
        candidate.explanation = (
            f"{candidate.name} scored {candidate.final_score * 100:.1f}%. "
            f"Matched skills: {_format_keywords(candidate.matched_keywords)}. "
            f"Missing skills: {_format_keywords(candidate.missing_keywords)}. "
            f"Keyword match: {candidate.keyword_score * 100:.1f}%; "
            f"semantic match: {candidate.semantic_score * 100:.1f}%."
        )
    return top3
