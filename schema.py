from dataclasses import dataclass, field
from typing import List


@dataclass
class CandidateResult:
    candidate_id: str
    name: str
    keyword_score: float
    semantic_score: float
    final_score: float
    matched_keywords: List[str] = field(default_factory=list)
    missing_keywords: List[str] = field(default_factory=list)
    rank: int = 0
    explanation: str = ""
