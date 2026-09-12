import csv
from html import escape
from io import BytesIO, StringIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from schema import CandidateResult


def _fit_label(score: float) -> str:
    if score >= 0.80:
        return "Strong match"
    if score >= 0.65:
        return "Good match"
    if score >= 0.50:
        return "Moderate match"
    return "Low match"


def _keyword_summary(keywords: list[str], limit: int = 18) -> str:
    if not keywords:
        return "None detected"
    shown = keywords[:limit]
    summary = ", ".join(shown)
    if len(keywords) > limit:
        summary += f" and {len(keywords) - limit} more"
    return summary


def _shorten(text: str, limit: int = 700) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def generate_candidate_report(candidate: CandidateResult) -> bytes:
    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=14 * mm,
        title=f"{candidate.name} - Candidate Match Report",
        author="Candidate OS",
    )

    styles = getSampleStyleSheet()
    eyebrow = ParagraphStyle(
        "Eyebrow",
        parent=styles["Normal"],
        fontName="Courier-Bold",
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#E13A30"),
        alignment=TA_CENTER,
        spaceAfter=6,
    )
    title = ParagraphStyle(
        "CandidateTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=23,
        leading=28,
        textColor=colors.HexColor("#111111"),
        alignment=TA_CENTER,
        spaceAfter=4,
    )
    subtitle = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontName="Courier",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#666666"),
        alignment=TA_CENTER,
        spaceAfter=16,
    )
    heading = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontName="Courier-Bold",
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#E13A30"),
        spaceBefore=10,
        spaceAfter=5,
    )
    body = ParagraphStyle(
        "ReportBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#2B2B2B"),
    )
    note = ParagraphStyle(
        "Note",
        parent=body,
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#777777"),
    )

    score_data = [
        ["FINAL SCORE", "KEYWORD MATCH", "SEMANTIC MATCH"],
        [
            f"{candidate.final_score * 100:.1f}%",
            f"{candidate.keyword_score * 100:.1f}%",
            f"{candidate.semantic_score * 100:.1f}%",
        ],
    ]
    score_table = Table(score_data, colWidths=[55 * mm, 55 * mm, 55 * mm])
    score_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F5F5F2")),
                ("BOX", (0, 0), (-1, -1), 0.8, colors.HexColor("#CCCCCC")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#DDDDDD")),
                ("FONTNAME", (0, 0), (-1, 0), "Courier-Bold"),
                ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 7.5),
                ("FONTSIZE", (0, 1), (-1, 1), 18),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#666666")),
                ("TEXTCOLOR", (0, 1), (-1, 1), colors.HexColor("#111111")),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, 0), 9),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 4),
                ("TOPPADDING", (0, 1), (-1, 1), 4),
                ("BOTTOMPADDING", (0, 1), (-1, 1), 11),
            ]
        )
    )

    story = [
        Paragraph("CANDIDATE OS / SHORTLIST REPORT", eyebrow),
        Paragraph(escape(candidate.name), title),
        Paragraph(
            f"RANK {candidate.rank:02d} &nbsp;&nbsp;/&nbsp;&nbsp; {_fit_label(candidate.final_score).upper()}",
            subtitle,
        ),
        score_table,
        Paragraph("MATCHED REQUIREMENTS", heading),
        Paragraph(escape(_keyword_summary(candidate.matched_keywords)), body),
        Paragraph("MISSING REQUIREMENTS", heading),
        Paragraph(escape(_keyword_summary(candidate.missing_keywords)), body),
        Paragraph("JOB-FIT SUMMARY", heading),
        Paragraph(
            escape(_shorten(candidate.explanation or "No explanation was generated.")),
            body,
        ),
        Spacer(1, 12),
        Paragraph(
            "This report is generated from local keyword and semantic matching. "
            "It is decision support and should be reviewed by a recruiter before making hiring decisions.",
            note,
        ),
    ]

    document.build(story)
    return buffer.getvalue()


def generate_rankings_csv(results: list[CandidateResult]) -> bytes:
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(
        [
            "Rank",
            "Candidate",
            "Fit category",
            "Final score",
            "Keyword score",
            "Semantic score",
            "Matched requirements",
            "Missing requirements",
            "Explanation",
        ]
    )

    for candidate in results:
        writer.writerow(
            [
                candidate.rank,
                candidate.name,
                _fit_label(candidate.final_score),
                f"{candidate.final_score * 100:.1f}%",
                f"{candidate.keyword_score * 100:.1f}%",
                f"{candidate.semantic_score * 100:.1f}%",
                ", ".join(candidate.matched_keywords),
                ", ".join(candidate.missing_keywords),
                candidate.explanation,
            ]
        )

    return output.getvalue().encode("utf-8-sig")
