from html import escape

import plotly.graph_objects as go
import streamlit as st

from schema import CandidateResult


def configure_page() -> None:
    st.set_page_config(
        page_title="Candidate OS",
        page_icon="◉",
        layout="wide",
        initial_sidebar_state="expanded",
    )


def apply_theme(dark_mode: bool) -> None:
    if dark_mode:
        colors = {
            "bg": "#0a0a0a",
            "surface": "#121212",
            "surface_alt": "#1a1a1a",
            "text": "#f2f2ee",
            "muted": "#9a9a95",
            "border": "#303030",
            "grid": "rgba(255, 255, 255, 0.035)",
            "accent": "#ff3b30",
        }
    else:
        colors = {
            "bg": "#f4f4f0",
            "surface": "#ffffff",
            "surface_alt": "#ebebe6",
            "text": "#101010",
            "muted": "#686864",
            "border": "#cecec8",
            "grid": "rgba(0, 0, 0, 0.045)",
            "accent": "#d92d24",
        }

    st.markdown(
        f"""
        <style>
        :root {{
            --app-bg: {colors['bg']};
            --surface: {colors['surface']};
            --surface-alt: {colors['surface_alt']};
            --text: {colors['text']};
            --muted: {colors['muted']};
            --border: {colors['border']};
            --grid: {colors['grid']};
            --accent: {colors['accent']};
        }}

        html, body, .stApp {{
            font-family: "Segoe UI", Arial, sans-serif;
        }}

        [data-testid="stIconMaterial"], .material-symbols-rounded {{
            font-family: "Material Symbols Rounded" !important;
            font-weight: normal !important;
            font-style: normal !important;
            letter-spacing: normal !important;
            text-transform: none !important;
            white-space: nowrap !important;
            word-wrap: normal !important;
            direction: ltr !important;
            font-feature-settings: "liga" !important;
            -webkit-font-feature-settings: "liga" !important;
        }}

        .stApp {{
            color: var(--text);
            background-color: var(--app-bg);
            background-image:
                linear-gradient(var(--grid) 1px, transparent 1px),
                linear-gradient(90deg, var(--grid) 1px, transparent 1px);
            background-size: 32px 32px;
        }}

        [data-testid="stHeader"] {{ background: transparent; }}
        [data-testid="stSidebar"] {{
            background: var(--surface);
            border-right: 1px solid var(--border);
        }}
        [data-testid="stSidebar"] * {{ color: var(--text); }}
        .block-container {{
            max-width: 1320px;
            padding-top: 3rem;
            padding-bottom: 4rem;
        }}

        .brand-mark {{
            margin: 0 0 2rem;
            padding: 0.9rem 0;
            border-top: 1px solid var(--border);
            border-bottom: 1px solid var(--border);
            color: var(--text);
            font-family: Consolas, "Courier New", monospace;
            font-weight: 700;
            letter-spacing: 0.16em;
            text-transform: uppercase;
        }}
        .brand-dot {{
            display: inline-block;
            width: 10px;
            height: 10px;
            margin-right: 10px;
            border-radius: 50%;
            background: var(--accent);
            box-shadow: 0 0 16px var(--accent);
        }}

        .hero {{
            position: relative;
            overflow: hidden;
            padding: clamp(2rem, 5vw, 4.5rem);
            margin-bottom: 2rem;
            border: 1px solid var(--border);
            border-radius: 4px;
            background: var(--surface);
        }}
        .hero::after {{
            content: "01";
            position: absolute;
            right: 2rem;
            top: 0.3rem;
            color: var(--surface-alt);
            font-family: Consolas, "Courier New", monospace;
            font-size: clamp(6rem, 15vw, 13rem);
            font-weight: 800;
            line-height: 1;
        }}
        .hero-content {{ position: relative; z-index: 1; }}
        .eyebrow, .section-label {{
            color: var(--accent);
            font-family: Consolas, "Courier New", monospace;
            font-size: 0.75rem;
            font-weight: 700;
            letter-spacing: 0.18em;
            text-transform: uppercase;
        }}
        .hero h1 {{
            max-width: 850px;
            margin: 0.7rem 0 1rem;
            color: var(--text);
            font-family: Consolas, "Courier New", monospace;
            font-size: clamp(2.5rem, 6vw, 5.3rem);
            font-weight: 500;
            line-height: 0.98;
            letter-spacing: -0.065em;
        }}
        .hero p {{
            max-width: 720px;
            margin: 0;
            color: var(--muted);
            font-size: 1.02rem;
            line-height: 1.65;
        }}
        .feature-row {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
            margin-top: 1.5rem;
        }}
        .feature-chip {{
            padding: 0.38rem 0.65rem;
            border: 1px solid var(--border);
            background: var(--surface-alt);
            color: var(--text);
            font-family: Consolas, "Courier New", monospace;
            font-size: 0.68rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }}
        .section-label {{ margin: 2.2rem 0 0.8rem; }}

        .upload-intro, .empty-state {{
            padding: 1.25rem 1.35rem;
            margin-bottom: 1rem;
            border: 1px solid var(--border);
            border-left: 3px solid var(--accent);
            border-radius: 3px;
            background: var(--surface);
        }}
        .upload-intro strong, .empty-state strong {{
            display: block;
            margin-bottom: 0.35rem;
            color: var(--text);
            font-family: Consolas, "Courier New", monospace;
            letter-spacing: 0.04em;
        }}
        .upload-intro span, .empty-state span {{ color: var(--muted); }}
        .empty-steps {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.75rem;
            margin-top: 1.25rem;
        }}
        .empty-step {{
            padding: 1rem;
            border: 1px solid var(--border);
            background: var(--surface-alt);
            color: var(--muted);
            font-size: 0.86rem;
        }}
        .empty-step b {{
            display: block;
            margin-bottom: 0.35rem;
            color: var(--accent);
            font-family: Consolas, "Courier New", monospace;
        }}

        [data-testid="stFileUploader"] {{
            padding: 0.75rem;
            border: 1px solid var(--border);
            border-radius: 4px;
            background: var(--surface);
            transition: transform 160ms ease, border-color 160ms ease;
        }}
        [data-testid="stFileUploader"]:hover {{
            transform: translateY(-2px);
            border-color: var(--accent);
        }}
        .stButton > button {{
            min-height: 3rem;
            border: 1px solid var(--accent);
            border-radius: 2px;
            background: var(--accent);
            color: #ffffff;
            font-family: Consolas, "Courier New", monospace;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            transition: transform 160ms ease, box-shadow 160ms ease;
        }}
        .stButton > button:hover {{
            transform: translateY(-2px);
            border-color: var(--accent);
            color: #ffffff;
            box-shadow: 5px 5px 0 var(--border);
        }}
        .stDownloadButton > button {{
            min-height: 3rem;
            border: 1px solid var(--border);
            border-radius: 2px;
            background: var(--surface);
            color: var(--text);
            font-family: Consolas, "Courier New", monospace;
            font-weight: 700;
            letter-spacing: 0.04em;
            transition: transform 160ms ease, border-color 160ms ease;
        }}
        .stDownloadButton > button:hover {{
            transform: translateY(-2px);
            border-color: var(--accent);
            color: var(--text);
        }}

        [data-testid="stMetric"] {{
            min-height: 118px;
            padding: 1rem 1.1rem;
            border: 1px solid var(--border);
            border-radius: 3px;
            background: var(--surface);
            transition: transform 160ms ease, border-color 160ms ease;
        }}
        [data-testid="stMetric"]:hover {{
            transform: translateY(-3px);
            border-color: var(--accent);
        }}
        [data-testid="stMetricLabel"] {{
            font-family: Consolas, "Courier New", monospace;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }}

        .candidate-card {{
            height: 100%;
            min-height: 500px;
            padding: 1.35rem;
            border: 1px solid var(--border);
            border-top: 3px solid var(--rank-color);
            border-radius: 4px;
            background: var(--surface);
            transition: transform 180ms ease, box-shadow 180ms ease, border-color 180ms ease;
        }}
        .candidate-card:hover {{
            transform: translateY(-7px);
            box-shadow: 8px 8px 0 var(--surface-alt);
            border-color: var(--rank-color);
        }}
        .rank-1 {{ --rank-color: #e7b94f; }}
        .rank-2 {{ --rank-color: #aab0b8; }}
        .rank-3 {{ --rank-color: #bb7448; }}
        .card-kicker {{
            color: var(--rank-color);
            font-family: Consolas, "Courier New", monospace;
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.13em;
            text-transform: uppercase;
        }}
        .candidate-name {{
            min-height: 3.4rem;
            margin: 0.75rem 0 0.7rem;
            color: var(--text);
            font-family: Consolas, "Courier New", monospace;
            font-size: 1.25rem;
            line-height: 1.25;
            text-transform: uppercase;
        }}
        .score-row {{
            display: flex;
            align-items: end;
            justify-content: space-between;
            padding-bottom: 1rem;
            margin-bottom: 1rem;
            border-bottom: 1px solid var(--border);
        }}
        .score-value {{
            color: var(--text);
            font-family: Consolas, "Courier New", monospace;
            font-size: 2.7rem;
            line-height: 1;
        }}
        .fit-label {{ color: var(--rank-color); font-size: 0.75rem; font-weight: 700; }}
        .score-line {{ margin: 0.65rem 0; }}
        .score-line-label {{
            display: flex;
            justify-content: space-between;
            color: var(--muted);
            font-family: Consolas, "Courier New", monospace;
            font-size: 0.7rem;
            text-transform: uppercase;
        }}
        .score-track {{
            height: 5px;
            margin-top: 0.35rem;
            background: var(--surface-alt);
        }}
        .score-fill {{ height: 100%; background: var(--rank-color); }}
        .tag-title {{
            margin: 1rem 0 0.4rem;
            color: var(--muted);
            font-family: Consolas, "Courier New", monospace;
            font-size: 0.65rem;
            letter-spacing: 0.1em;
            text-transform: uppercase;
        }}
        .skill-tag {{
            display: inline-block;
            padding: 0.25rem 0.45rem;
            margin: 0 0.25rem 0.3rem 0;
            border: 1px solid;
            border-radius: 2px;
            font-family: Consolas, "Courier New", monospace;
            font-size: 0.65rem;
        }}
        .skill-match {{ color: #55c98b; border-color: #2b7650; background: rgba(54, 170, 107, 0.08); }}
        .skill-missing {{ color: #ff7168; border-color: #843c37; background: rgba(255, 59, 48, 0.08); }}
        .card-explanation {{
            margin-top: 1rem;
            color: var(--muted);
            font-size: 0.8rem;
            line-height: 1.5;
        }}

        [data-testid="stPlotlyChart"], [data-testid="stDataFrame"], [data-testid="stExpander"] {{
            border: 1px solid var(--border);
            border-radius: 4px;
            background: var(--surface);
        }}
        [data-testid="stPlotlyChart"] {{
            transition: transform 160ms ease, border-color 160ms ease;
        }}
        [data-testid="stPlotlyChart"]:hover {{
            transform: translateY(-3px);
            border-color: var(--accent);
        }}
        [data-testid="stAlert"] {{ border-radius: 2px; }}
        h1, h2, h3, p, label, .stMarkdown {{ color: var(--text); }}

        @media (max-width: 800px) {{
            .empty-steps {{ grid-template-columns: 1fr; }}
            .candidate-card {{ min-height: auto; margin-bottom: 1rem; }}
            .hero::after {{ opacity: 0.45; }}
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_brand() -> None:
    st.markdown(
        '<div class="brand-mark"><span class="brand-dot"></span>Candidate OS</div>',
        unsafe_allow_html=True,
    )


def render_hero() -> None:
    st.markdown(
        """
        <section class="hero">
            <div class="hero-content">
                <div class="eyebrow">Recruitment intelligence / 01</div>
                <h1>Find signal.<br>Shortlist smarter.</h1>
                <p>Rank resumes against a job description with explainable keyword and semantic matching. Built for private, local-first candidate analysis.</p>
                <div class="feature-row">
                    <span class="feature-chip">Local AI</span>
                    <span class="feature-chip">No API keys</span>
                    <span class="feature-chip">Explainable scores</span>
                    <span class="feature-chip">PDF analysis</span>
                </div>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_section_label(number: str, title: str) -> None:
    st.markdown(
        f'<div class="section-label">{escape(number)} / {escape(title)}</div>',
        unsafe_allow_html=True,
    )


def render_upload_intro() -> None:
    st.markdown(
        """
        <div class="upload-intro">
            <strong>ADD SOURCE DOCUMENTS</strong>
            <span>Upload one text-based job description and one or more candidate resumes in PDF format.</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state(jd_ready: bool, resume_count: int) -> None:
    status = "Ready to analyze." if jd_ready and resume_count else "Waiting for source documents."
    st.markdown(
        f"""
        <div class="empty-state">
            <strong>{escape(status)}</strong>
            <span>Your files stay in temporary local storage while the ranking pipeline runs.</span>
            <div class="empty-steps">
                <div class="empty-step"><b>01 / EXTRACT</b>Read selectable text from each PDF.</div>
                <div class="empty-step"><b>02 / MATCH</b>Compare skills and semantic meaning.</div>
                <div class="empty-step"><b>03 / RANK</b>Explain and order the strongest candidates.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def match_category(score: float) -> str:
    if score >= 0.80:
        return "Strong match"
    if score >= 0.65:
        return "Good match"
    if score >= 0.50:
        return "Moderate match"
    return "Low match"


def render_summary_metrics(results: list[CandidateResult]) -> None:
    average = sum(candidate.final_score for candidate in results) / len(results)
    best = results[0]
    columns = st.columns(4)
    columns[0].metric("Resumes analyzed", len(results))
    columns[1].metric("Best candidate", best.name)
    columns[2].metric("Highest score", f"{best.final_score * 100:.1f}%")
    columns[3].metric("Average score", f"{average * 100:.1f}%")


def _chart_style(figure: go.Figure, dark_mode: bool, height: int) -> None:
    text = "#f2f2ee" if dark_mode else "#101010"
    muted = "#9a9a95" if dark_mode else "#686864"
    border = "#303030" if dark_mode else "#cecec8"
    figure.update_layout(
        height=height,
        margin=dict(l=24, r=24, t=56, b=36),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Consolas, Courier New, monospace", color=text),
        title_font=dict(size=15, color=text),
        legend=dict(font=dict(color=muted), orientation="h", y=-0.15),
        hoverlabel=dict(bgcolor="#161616" if dark_mode else "#ffffff", font_color=text),
    )
    figure.update_xaxes(gridcolor=border, zeroline=False)
    figure.update_yaxes(gridcolor=border, zeroline=False)


def render_top5_chart(results: list[CandidateResult], dark_mode: bool) -> None:
    top_five = results[:5]
    custom_data = [
        [
            candidate.keyword_score * 100,
            candidate.semantic_score * 100,
            len(candidate.matched_keywords),
            len(candidate.missing_keywords),
        ]
        for candidate in top_five
    ]
    figure = go.Figure(
        go.Bar(
            x=[candidate.final_score * 100 for candidate in top_five],
            y=[candidate.name for candidate in top_five],
            orientation="h",
            marker=dict(color="#ff3b30"),
            customdata=custom_data,
            text=[f"{candidate.final_score * 100:.1f}%" for candidate in top_five],
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b><br>Final score: %{x:.1f}%"
                "<br>Keyword score: %{customdata[0]:.1f}%"
                "<br>Semantic score: %{customdata[1]:.1f}%"
                "<br>Matched skills: %{customdata[2]}"
                "<br>Missing requirements: %{customdata[3]}<extra></extra>"
            ),
        )
    )
    figure.update_layout(title="TOP 5 CANDIDATES", showlegend=False)
    figure.update_xaxes(title="Final score", range=[0, 105], ticksuffix="%")
    figure.update_yaxes(autorange="reversed", title=None)
    _chart_style(figure, dark_mode, 390)
    st.plotly_chart(figure, use_container_width=True, key="top_five_chart")


def render_score_distribution(results: list[CandidateResult], dark_mode: bool) -> None:
    figure = go.Figure(
        go.Histogram(
            x=[candidate.final_score * 100 for candidate in results],
            xbins=dict(start=0, end=100, size=10),
            marker=dict(color="#ff3b30", line=dict(width=0)),
            hovertemplate="Score range: %{x}<br>Candidates: %{y}<extra></extra>",
        )
    )
    figure.update_layout(title="ALL-RESUME SCORE DISTRIBUTION", showlegend=False, bargap=0.08)
    figure.update_xaxes(title="Final score", range=[0, 100], ticksuffix="%")
    figure.update_yaxes(title="Candidates", dtick=1)
    _chart_style(figure, dark_mode, 360)
    st.plotly_chart(figure, use_container_width=True, key="score_distribution")


def render_fit_donut(results: list[CandidateResult], dark_mode: bool) -> None:
    categories = ["Strong match", "Good match", "Moderate match", "Low match"]
    counts = [sum(match_category(candidate.final_score) == category for candidate in results) for category in categories]
    visible_categories = [category for category, count in zip(categories, counts) if count]
    visible_counts = [count for count in counts if count]
    color_map = {
        "Strong match": "#55c98b",
        "Good match": "#76a9fa",
        "Moderate match": "#e7b94f",
        "Low match": "#ff7168",
    }
    figure = go.Figure(
        go.Pie(
            labels=visible_categories,
            values=visible_counts,
            hole=0.66,
            sort=False,
            marker=dict(colors=[color_map[category] for category in visible_categories]),
            textinfo="percent+label" if len(visible_categories) > 1 else "label",
            textposition="inside",
            hovertemplate="<b>%{label}</b><br>%{value} candidates<br>%{percent}<extra></extra>",
        )
    )
    figure.update_layout(
        title="CANDIDATE FIT CATEGORIES",
        annotations=[dict(text=str(len(results)), x=0.5, y=0.5, showarrow=False, font_size=25)],
    )
    _chart_style(figure, dark_mode, 360)
    st.plotly_chart(figure, use_container_width=True, key="fit_donut")


def _skill_tags(skills: list[str], css_class: str, limit: int = 8) -> str:
    shown = skills[:limit]
    tags = "".join(
        f'<span class="skill-tag {css_class}">{escape(skill)}</span>'
        for skill in shown
    )
    if len(skills) > limit:
        tags += f'<span class="skill-tag {css_class}">+{len(skills) - limit}</span>'
    return tags or f'<span class="skill-tag {css_class}">None</span>'


def render_top3_cards(results: list[CandidateResult]) -> None:
    medals = {1: "GOLD / 01", 2: "SILVER / 02", 3: "BRONZE / 03"}
    columns = st.columns(min(3, len(results)))

    for column, candidate in zip(columns, results[:3]):
        keyword_width = max(0, min(100, candidate.keyword_score * 100))
        semantic_width = max(0, min(100, candidate.semantic_score * 100))
        with column:
            st.markdown(
                f"""
                <article class="candidate-card rank-{candidate.rank}">
                    <div class="card-kicker">{medals[candidate.rank]}</div>
                    <div class="candidate-name">{escape(candidate.name)}</div>
                    <div class="score-row">
                        <span class="score-value">{candidate.final_score * 100:.1f}%</span>
                        <span class="fit-label">{escape(match_category(candidate.final_score).upper())}</span>
                    </div>
                    <div class="score-line">
                        <div class="score-line-label"><span>Keyword match</span><span>{keyword_width:.1f}%</span></div>
                        <div class="score-track"><div class="score-fill" style="width:{keyword_width:.1f}%"></div></div>
                    </div>
                    <div class="score-line">
                        <div class="score-line-label"><span>Semantic match</span><span>{semantic_width:.1f}%</span></div>
                        <div class="score-track"><div class="score-fill" style="width:{semantic_width:.1f}%"></div></div>
                    </div>
                    <div class="tag-title">Matched requirements</div>
                    <div>{_skill_tags(candidate.matched_keywords, 'skill-match')}</div>
                    <div class="tag-title">Missing requirements</div>
                    <div>{_skill_tags(candidate.missing_keywords, 'skill-missing')}</div>
                    <div class="card-explanation">{escape(candidate.explanation)}</div>
                </article>
                """,
                unsafe_allow_html=True,
            )


def render_leaderboard(results: list[CandidateResult]) -> None:
    all_skills = sorted({skill for candidate in results for skill in candidate.matched_keywords})
    filter_columns = st.columns([1.5, 1, 1, 1, 1])
    with filter_columns[0]:
        search = st.text_input("Search candidate", placeholder="Type a name...")
    with filter_columns[1]:
        minimum_score = st.slider("Minimum score", 0, 100, 0, 5)
    with filter_columns[2]:
        category = st.selectbox(
            "Fit category",
            ["All", "Strong match", "Good match", "Moderate match", "Low match"],
        )
    with filter_columns[3]:
        required_skill = st.selectbox("Must match skill", ["All", *all_skills])
    with filter_columns[4]:
        sort_by = st.selectbox("Sort by", ["Rank", "Final score", "Candidate name"])

    filtered = [
        candidate
        for candidate in results
        if search.lower() in candidate.name.lower()
        and candidate.final_score * 100 >= minimum_score
        and (category == "All" or match_category(candidate.final_score) == category)
        and (required_skill == "All" or required_skill in candidate.matched_keywords)
    ]

    if sort_by == "Final score":
        filtered.sort(key=lambda candidate: candidate.final_score, reverse=True)
    elif sort_by == "Candidate name":
        filtered.sort(key=lambda candidate: candidate.name.lower())
    else:
        filtered.sort(key=lambda candidate: candidate.rank)

    st.caption(f"Showing {len(filtered)} of {len(results)} candidates")
    st.dataframe(
        [
            {
                "Rank": candidate.rank,
                "Candidate": candidate.name,
                "Fit": match_category(candidate.final_score),
                "Final score": f"{candidate.final_score * 100:.1f}%",
                "Keyword": f"{candidate.keyword_score * 100:.1f}%",
                "Semantic": f"{candidate.semantic_score * 100:.1f}%",
                "Matched requirements": ", ".join(candidate.matched_keywords) or "None",
                "Missing requirements": ", ".join(candidate.missing_keywords) or "None",
            }
            for candidate in filtered
        ],
        use_container_width=True,
        hide_index=True,
    )
