import tempfile
from pathlib import Path

import streamlit as st

from pipeline import run
from report_generator import generate_candidate_report, generate_rankings_csv
from ui import (
    apply_theme,
    configure_page,
    render_empty_state,
    render_fit_donut,
    render_hero,
    render_leaderboard,
    render_score_distribution,
    render_section_label,
    render_sidebar_brand,
    render_summary_metrics,
    render_top3_cards,
    render_top5_chart,
    render_upload_intro,
)


configure_page()

with st.sidebar:
    render_sidebar_brand()
    dark_mode = st.toggle("Dark mode", value=True)
    st.caption("Private processing. No resume files are permanently stored.")

apply_theme(dark_mode)
render_hero()
render_section_label("02", "Input documents")
render_upload_intro()

upload_left, upload_right = st.columns(2)
with upload_left:
    jd_file = st.file_uploader("Job description PDF", type="pdf")
with upload_right:
    resume_files = st.file_uploader(
        "Candidate resume PDFs",
        type="pdf",
        accept_multiple_files=True,
    )

signature = (
    "scoring-v2",
    (jd_file.name, jd_file.size) if jd_file else None,
    tuple((resume.name, resume.size) for resume in resume_files),
)
if st.session_state.get("analysis_signature") != signature:
    st.session_state.pop("candidate_results", None)

if resume_files:
    st.caption(f"{len(resume_files)} resume{'s' if len(resume_files) != 1 else ''} selected")

if st.button("Analyze candidates", use_container_width=True, type="primary"):
    if jd_file is None or not resume_files:
        st.error("Upload one job description and at least one resume.")
    else:
        with st.spinner("Extracting, matching, and ranking candidates..."):
            with tempfile.TemporaryDirectory() as temp_dir:
                jd_path = Path(temp_dir) / "jd.pdf"
                jd_path.write_bytes(jd_file.getvalue())
                resume_paths = []

                for index, resume_file in enumerate(resume_files):
                    resume_dir = Path(temp_dir) / f"resume_{index}"
                    resume_dir.mkdir()
                    resume_path = resume_dir / resume_file.name
                    resume_path.write_bytes(resume_file.getvalue())
                    resume_paths.append(str(resume_path))

                try:
                    results = run(str(jd_path), resume_paths)
                except (RuntimeError, ValueError) as error:
                    st.session_state.pop("candidate_results", None)
                    st.error(str(error))
                    st.stop()

        if not results:
            st.error("No readable resume text was found.")
        else:
            st.session_state.candidate_results = results
            st.session_state.analysis_signature = signature

results = st.session_state.get("candidate_results", [])

if not results:
    render_empty_state(jd_file is not None, len(resume_files))
else:
    render_section_label("03", "Analysis overview")
    render_summary_metrics(results)

    render_section_label("04", "Candidate analytics")
    render_top5_chart(results, dark_mode)
    distribution_column, category_column = st.columns(2)
    with distribution_column:
        render_score_distribution(results, dark_mode)
    with category_column:
        render_fit_donut(results, dark_mode)

    render_section_label("05", "Top candidate shortlist")
    render_top3_cards(results)

    render_section_label("06", "Complete leaderboard")
    render_leaderboard(results)

    render_section_label("07", "Export results")
    st.caption(
        "Download the complete ranking as CSV or export a one-page assessment "
        "for each shortlisted candidate."
    )
    st.download_button(
        "Download complete leaderboard (CSV)",
        data=generate_rankings_csv(results),
        file_name="candidate_rankings.csv",
        mime="text/csv",
        use_container_width=True,
    )

    report_columns = st.columns(min(3, len(results)))
    for column, candidate in zip(report_columns, results[:3]):
        safe_name = "_".join(candidate.name.lower().split())
        with column:
            st.download_button(
                f"Export #{candidate.rank} {candidate.name}",
                data=generate_candidate_report(candidate),
                file_name=f"{safe_name}_candidate_report.pdf",
                mime="application/pdf",
                use_container_width=True,
                key=f"candidate_report_{candidate.rank}",
            )
