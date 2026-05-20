"""
VERA-NV: Verification Engine for Results & Accountability - Nevada
Type 4 Dyslexia Screening using ACCESS for ELLs and SBAC Assessment Data

H-EDU.Solutions | https://h-edu.solutions
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ============================================================================
# CONFIGURATION
# ============================================================================

APP_PASSWORD = "vera2026"

# Nevada colors
NV_BLUE = "#003366"  # Nevada blue
NV_SILVER = "#C0C0C0"  # Silver state
NV_GOLD = "#FFD700"  # Gold accent

# ============================================================================
# SAMPLE DATA - Nevada Districts
# ============================================================================

def load_districts():
    """Load Nevada district data."""
    districts_data = [
        ("02", "Clark County School District", 305000, 54900, 18.0, 82.1, 52.5),
        ("16", "Washoe County School District", 62000, 11160, 18.0, 84.3, 58.2),
        ("01", "Carson City School District", 7500, 1125, 15.0, 86.5, 55.8),
        ("04", "Elko County School District", 10000, 1200, 12.0, 88.2, 61.3),
        ("09", "Lyon County School District", 8500, 1020, 12.0, 85.7, 54.2),
        ("03", "Douglas County School District", 5800, 464, 8.0, 90.1, 65.4),
        ("12", "Nye County School District", 4200, 378, 9.0, 79.5, 48.6),
        ("05", "Churchill County School District", 3500, 350, 10.0, 87.3, 57.1),
        ("08", "Lincoln County School District", 950, 76, 8.0, 91.2, 62.8),
        ("17", "White Pine County School District", 1200, 108, 9.0, 85.4, 53.9),
    ]

    df = pd.DataFrame(districts_data, columns=[
        'district_id', 'district_name', 'total_students',
        'ell_count', 'ell_percent', 'graduation_rate', 'nspf_score'
    ])
    return df

def load_access_data():
    """Load sample ACCESS for ELLs data (Nevada is a WIDA state)."""
    access_data = []

    districts = [
        ("02", "Clark County School District"),
        ("16", "Washoe County School District"),
        ("01", "Carson City School District"),
        ("04", "Elko County School District"),
        ("09", "Lyon County School District"),
        ("03", "Douglas County School District"),
        ("12", "Nye County School District"),
        ("05", "Churchill County School District"),
        ("08", "Lincoln County School District"),
        ("17", "White Pine County School District"),
    ]

    for district_id, district_name in districts:
        for grade in range(3, 9):
            for year in [2024, 2025]:
                # Generate realistic ACCESS scores (scale 100-600)
                base_speaking = 340 + (grade * 8)
                base_writing = 295 + (grade * 6)

                # Add district-specific variation
                if district_id == "02":  # Clark County - largest, diverse
                    speaking_adj = 30
                    writing_adj = -5
                elif district_id == "16":  # Washoe - second largest
                    speaking_adj = 25
                    writing_adj = 0
                elif district_id == "12":  # Nye County - rural, lower performing
                    speaking_adj = 35
                    writing_adj = -15
                elif district_id in ["03", "08"]:  # Higher performing rural
                    speaking_adj = 15
                    writing_adj = 10
                else:
                    speaking_adj = 20
                    writing_adj = 5

                access_data.append({
                    'district_id': district_id,
                    'district_name': district_name,
                    'grade': grade,
                    'year': year,
                    'total_tested': 200 + (grade * 15) if district_id == "02" else 50 + (grade * 5),
                    'listening_avg': base_speaking + speaking_adj - 5,
                    'speaking_avg': base_speaking + speaking_adj,
                    'reading_avg': base_writing + writing_adj + 15,
                    'writing_avg': base_writing + writing_adj,
                    'composite_avg': (base_speaking + speaking_adj + base_writing + writing_adj) / 2 + 20
                })

    return pd.DataFrame(access_data)

def load_sbac_data():
    """Load sample SBAC (Smarter Balanced) assessment data."""
    sbac_data = []

    districts = [
        ("02", "Clark County School District"),
        ("16", "Washoe County School District"),
        ("01", "Carson City School District"),
        ("04", "Elko County School District"),
        ("09", "Lyon County School District"),
        ("03", "Douglas County School District"),
        ("12", "Nye County School District"),
        ("05", "Churchill County School District"),
        ("08", "Lincoln County School District"),
        ("17", "White Pine County School District"),
    ]

    for district_id, district_name in districts:
        for grade in range(3, 9):
            for year in [2024, 2025]:
                for subject in ['ELA', 'Math']:
                    # Generate realistic SBAC proficiency distributions
                    if district_id in ["03", "08", "04"]:  # Higher performing
                        level_4 = 22 + (grade * 0.5)
                        level_3 = 32 + (grade * 0.3)
                        level_2 = 28 - (grade * 0.3)
                        level_1 = 18 - (grade * 0.5)
                    elif district_id in ["12"]:  # Lower performing
                        level_4 = 8 + (grade * 0.3)
                        level_3 = 22 + (grade * 0.2)
                        level_2 = 38 - (grade * 0.2)
                        level_1 = 32 - (grade * 0.3)
                    elif district_id == "02":  # Clark - large urban
                        level_4 = 14 + (grade * 0.4)
                        level_3 = 28 + (grade * 0.2)
                        level_2 = 32 - (grade * 0.2)
                        level_1 = 26 - (grade * 0.4)
                    else:  # Average
                        level_4 = 16 + (grade * 0.4)
                        level_3 = 30 + (grade * 0.2)
                        level_2 = 30 - (grade * 0.2)
                        level_1 = 24 - (grade * 0.4)

                    sbac_data.append({
                        'district_id': district_id,
                        'district_name': district_name,
                        'grade': grade,
                        'subject': subject,
                        'year': year,
                        'total_tested': 3000 + (grade * 100) if district_id == "02" else 300 + (grade * 20),
                        'level_1_pct': max(5, level_1),
                        'level_2_pct': max(10, level_2),
                        'level_3_pct': min(45, level_3),
                        'level_4_pct': min(35, level_4),
                        'mean_scale_score': 2420 + (level_3 + level_4) * 2.5
                    })

    return pd.DataFrame(sbac_data)

# ============================================================================
# AUTHENTICATION
# ============================================================================

def check_password():
    st.session_state.authenticated = True
    return True

# ============================================================================
# TYPE 4 DETECTION
# ============================================================================

def compute_type4_analysis(access_df, district_id, grade, year):
    """
    Compute Type 4 (oral-written delta) analysis for a district.

    Type 4 candidates show strong oral skills but weak written skills.
    Delta = Speaking Score - Writing Score
    Flag threshold: Delta > 8 points (on normalized scale)
    """
    filtered = access_df[
        (access_df['district_id'] == district_id) &
        (access_df['grade'] == grade) &
        (access_df['year'] == year)
    ]

    if filtered.empty:
        return None

    row = filtered.iloc[0]

    # Calculate delta (Speaking - Writing)
    speaking = row['speaking_avg']
    writing = row['writing_avg']
    delta = speaking - writing

    # Normalize to 0-100 scale for threshold comparison
    delta_normalized = delta / 5  # Approximate normalization

    # Flag if delta exceeds threshold
    flagged = delta_normalized > 8

    return {
        'district_id': district_id,
        'district_name': row['district_name'],
        'grade': grade,
        'year': year,
        'speaking_avg': speaking,
        'writing_avg': writing,
        'delta': delta,
        'delta_normalized': delta_normalized,
        'flagged': flagged,
        'total_tested': row['total_tested'],
        'estimated_flagged': int(row['total_tested'] * 0.15) if flagged else int(row['total_tested'] * 0.05)
    }

# ============================================================================
# DASHBOARD PAGES
# ============================================================================

def render_overview(districts_df, access_df, sbac_df):
    """Render the overview dashboard."""
    st.header("Nevada Education Overview")

    # Key metrics
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Districts", len(districts_df))
    with col2:
        st.metric("Total Students", f"{districts_df['total_students'].sum():,}")
    with col3:
        st.metric("English Learners", f"{districts_df['ell_count'].sum():,}")
    with col4:
        avg_nspf = districts_df['nspf_score'].mean()
        st.metric("Avg NSPF Score", f"{avg_nspf:.1f}")

    st.divider()

    # District overview table
    st.subheader("Pilot Districts")

    display_df = districts_df.copy()
    display_df['ell_percent'] = display_df['ell_percent'].apply(lambda x: f"{x:.1f}%")
    display_df['graduation_rate'] = display_df['graduation_rate'].apply(lambda x: f"{x:.1f}%")
    display_df['nspf_score'] = display_df['nspf_score'].apply(lambda x: f"{x:.1f}")
    display_df.columns = ['District ID', 'District Name', 'Total Students', 'EL Count', 'EL %', 'Grad Rate', 'NSPF']

    st.dataframe(display_df, use_container_width=True, hide_index=True)

    # EL Population chart
    st.subheader("English Learner Population by District")

    fig = px.bar(
        districts_df.sort_values('ell_count', ascending=True),
        x='ell_count',
        y='district_name',
        orientation='h',
        color='ell_percent',
        color_continuous_scale=[[0, NV_SILVER], [1, NV_BLUE]],
        labels={'ell_count': 'English Learners', 'district_name': 'District', 'ell_percent': 'EL %'}
    )
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def render_access_analysis(access_df, districts_df):
    """Render ACCESS for ELLs assessment analysis."""
    st.header("ACCESS for ELLs Analysis")

    st.markdown("""
    **ACCESS for ELLs** (WIDA) measures English learners' proficiency across four domains:
    Listening, Speaking, Reading, and Writing. Nevada is a WIDA consortium member state.
    """)

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        district = st.selectbox(
            "Select District",
            options=districts_df['district_name'].tolist(),
            key="access_district"
        )

    with col2:
        grade = st.selectbox("Select Grade", options=list(range(3, 9)), key="access_grade")

    with col3:
        year = st.selectbox("Select Year", options=[2025, 2024], key="access_year")

    # Get district ID
    district_id = districts_df[districts_df['district_name'] == district]['district_id'].values[0]

    # Filter data
    filtered = access_df[
        (access_df['district_id'] == district_id) &
        (access_df['grade'] == grade) &
        (access_df['year'] == year)
    ]

    if not filtered.empty:
        row = filtered.iloc[0]

        st.divider()

        # Domain scores
        st.subheader("ACCESS Domain Scores")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Listening", f"{row['listening_avg']:.0f}")
        with col2:
            st.metric("Speaking", f"{row['speaking_avg']:.0f}")
        with col3:
            st.metric("Reading", f"{row['reading_avg']:.0f}")
        with col4:
            st.metric("Writing", f"{row['writing_avg']:.0f}")

        # Domain comparison chart
        domains = ['Listening', 'Speaking', 'Reading', 'Writing']
        scores = [row['listening_avg'], row['speaking_avg'], row['reading_avg'], row['writing_avg']]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=domains,
            y=scores,
            marker_color=[NV_BLUE, NV_GOLD, NV_SILVER, NV_BLUE],
            text=[f"{s:.0f}" for s in scores],
            textposition='outside'
        ))
        fig.update_layout(
            title=f"ACCESS Domain Scores - {district} - Grade {grade} ({year})",
            yaxis_title="Scale Score",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

        # Oral vs Written gap highlight
        oral_avg = (row['listening_avg'] + row['speaking_avg']) / 2
        written_avg = (row['reading_avg'] + row['writing_avg']) / 2
        gap = oral_avg - written_avg

        st.subheader("Oral vs Written Gap")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Oral Average", f"{oral_avg:.0f}", help="(Listening + Speaking) / 2")
        with col2:
            st.metric("Written Average", f"{written_avg:.0f}", help="(Reading + Writing) / 2")
        with col3:
            delta_color = "normal" if gap < 25 else "inverse"
            st.metric("Gap", f"{gap:+.0f}", delta=f"{'Flag' if gap > 30 else 'OK'}", delta_color=delta_color)

def render_type4_detection(access_df, districts_df):
    """Render Type 4 detection analysis."""
    st.header("Type 4 Detection")

    st.markdown("""
    **Type 4 dyslexia candidates** demonstrate strong oral communication abilities but
    significant challenges with written expression. VERA-NV identifies these students by
    analyzing the delta between ACCESS Speaking and Writing domain scores.

    **Flag Threshold:** Speaking - Writing delta > 8 points (normalized scale)
    """)

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        district = st.selectbox(
            "Select District",
            options=districts_df['district_name'].tolist(),
            key="type4_district"
        )

    with col2:
        grade = st.selectbox("Select Grade", options=list(range(3, 9)), key="type4_grade")

    with col3:
        year = st.selectbox("Select Year", options=[2025, 2024], key="type4_year")

    # Get district ID
    district_id = districts_df[districts_df['district_name'] == district]['district_id'].values[0]

    # Run analysis
    result = compute_type4_analysis(access_df, district_id, grade, year)

    if result:
        st.divider()

        # Results
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Speaking Score", f"{result['speaking_avg']:.0f}")
        with col2:
            st.metric("Writing Score", f"{result['writing_avg']:.0f}")
        with col3:
            st.metric("Delta", f"{result['delta']:+.0f}")
        with col4:
            status = "🚨 FLAGGED" if result['flagged'] else "✅ OK"
            st.metric("Status", status)

        # Visual delta display
        st.subheader("Oral-Written Delta Analysis")

        fig = go.Figure()

        # Speaking bar
        fig.add_trace(go.Bar(
            name='Speaking',
            x=['Score'],
            y=[result['speaking_avg']],
            marker_color=NV_GOLD,
            text=[f"{result['speaking_avg']:.0f}"],
            textposition='outside'
        ))

        # Writing bar
        fig.add_trace(go.Bar(
            name='Writing',
            x=['Score'],
            y=[result['writing_avg']],
            marker_color=NV_BLUE,
            text=[f"{result['writing_avg']:.0f}"],
            textposition='outside'
        ))

        fig.update_layout(
            title=f"Speaking vs Writing - {district} - Grade {grade}",
            barmode='group',
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)

        # Interpretation
        if result['flagged']:
            st.error(f"""
            **Type 4 Flag Triggered**

            This grade level shows a significant oral-written gap (delta: {result['delta']:+.0f}).

            - **Estimated students affected:** {result['estimated_flagged']} of {result['total_tested']} tested
            - **Recommended action:** Individual student-level screening for Type 4 dyslexia
            - **Next steps:** Cross-reference with SBAC ELA writing performance
            """)
        else:
            st.success(f"""
            **No Type 4 Flag**

            The oral-written gap for this grade level is within normal range (delta: {result['delta']:+.0f}).

            - **Students tested:** {result['total_tested']}
            - **Continue monitoring:** Regular ACCESS domain analysis recommended
            """)

        # All grades comparison for district
        st.subheader(f"All Grades - {district} ({year})")

        all_grades_data = []
        for g in range(3, 9):
            r = compute_type4_analysis(access_df, district_id, g, year)
            if r:
                all_grades_data.append(r)

        if all_grades_data:
            grades_df = pd.DataFrame(all_grades_data)

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=grades_df['grade'],
                y=grades_df['speaking_avg'],
                name='Speaking',
                mode='lines+markers',
                line=dict(color=NV_GOLD, width=3),
                marker=dict(size=10)
            ))
            fig.add_trace(go.Scatter(
                x=grades_df['grade'],
                y=grades_df['writing_avg'],
                name='Writing',
                mode='lines+markers',
                line=dict(color=NV_BLUE, width=3),
                marker=dict(size=10)
            ))

            fig.update_layout(
                title="Speaking vs Writing Across Grades",
                xaxis_title="Grade",
                yaxis_title="Scale Score",
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)

def render_sbac_analysis(sbac_df, districts_df):
    """Render SBAC assessment analysis."""
    st.header("SBAC Assessment Analysis")

    st.markdown("""
    **Smarter Balanced (SBAC)** assessments measure student achievement in
    English Language Arts and Mathematics aligned to Nevada Academic Content Standards.
    """)

    # Filters
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        district = st.selectbox(
            "Select District",
            options=districts_df['district_name'].tolist(),
            key="sbac_district"
        )

    with col2:
        grade = st.selectbox("Select Grade", options=list(range(3, 9)), key="sbac_grade")

    with col3:
        subject = st.selectbox("Select Subject", options=['ELA', 'Math'], key="sbac_subject")

    with col4:
        year = st.selectbox("Select Year", options=[2025, 2024], key="sbac_year")

    # Get district ID
    district_id = districts_df[districts_df['district_name'] == district]['district_id'].values[0]

    # Filter data
    filtered = sbac_df[
        (sbac_df['district_id'] == district_id) &
        (sbac_df['grade'] == grade) &
        (sbac_df['subject'] == subject) &
        (sbac_df['year'] == year)
    ]

    if not filtered.empty:
        row = filtered.iloc[0]

        st.divider()

        # Proficiency levels
        st.subheader("Proficiency Distribution")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Level 1", f"{row['level_1_pct']:.1f}%", help="Standard Not Met")
        with col2:
            st.metric("Level 2", f"{row['level_2_pct']:.1f}%", help="Standard Nearly Met")
        with col3:
            st.metric("Level 3", f"{row['level_3_pct']:.1f}%", help="Standard Met")
        with col4:
            st.metric("Level 4", f"{row['level_4_pct']:.1f}%", help="Standard Exceeded")

        # Proficiency chart
        levels = ['Level 1\n(Not Met)', 'Level 2\n(Nearly Met)',
                  'Level 3\n(Met)', 'Level 4\n(Exceeded)']
        values = [row['level_1_pct'], row['level_2_pct'], row['level_3_pct'], row['level_4_pct']]
        colors = ['#d32f2f', '#f57c00', NV_GOLD, NV_BLUE]

        fig = go.Figure(data=[
            go.Bar(x=levels, y=values, marker_color=colors, text=[f"{v:.1f}%" for v in values], textposition='outside')
        ])
        fig.update_layout(
            title=f"SBAC {subject} Proficiency - {district} - Grade {grade} ({year})",
            yaxis_title="Percentage",
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)

        # Proficient rate
        proficient_rate = row['level_3_pct'] + row['level_4_pct']
        st.metric(
            "Proficiency Rate (Level 3+4)",
            f"{proficient_rate:.1f}%",
            help="Percentage of students meeting or exceeding standards"
        )

def render_export(access_df, sbac_df, districts_df):
    """Render data export page."""
    st.header("Export Data")

    st.markdown("Download assessment data for further analysis.")

    # District filter
    district = st.selectbox(
        "Select District (or All)",
        options=["All Districts"] + districts_df['district_name'].tolist()
    )

    year = st.selectbox("Select Year", options=[2025, 2024])

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("ACCESS Data")
        if district == "All Districts":
            export_access = access_df[access_df['year'] == year]
        else:
            district_id = districts_df[districts_df['district_name'] == district]['district_id'].values[0]
            export_access = access_df[(access_df['district_id'] == district_id) & (access_df['year'] == year)]

        st.dataframe(export_access, use_container_width=True, hide_index=True)

        csv_access = export_access.to_csv(index=False)
        st.download_button(
            "Download ACCESS CSV",
            csv_access,
            f"vera_nv_access_{year}.csv",
            "text/csv",
            use_container_width=True
        )

    with col2:
        st.subheader("SBAC Data")
        if district == "All Districts":
            export_sbac = sbac_df[sbac_df['year'] == year]
        else:
            district_id = districts_df[districts_df['district_name'] == district]['district_id'].values[0]
            export_sbac = sbac_df[(sbac_df['district_id'] == district_id) & (sbac_df['year'] == year)]

        st.dataframe(export_sbac, use_container_width=True, hide_index=True)

        csv_sbac = export_sbac.to_csv(index=False)
        st.download_button(
            "Download SBAC CSV",
            csv_sbac,
            f"vera_nv_sbac_{year}.csv",
            "text/csv",
            use_container_width=True
        )

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    st.set_page_config(
        page_title="VERA-NV | Nevada Type 4 Detection",
        page_icon="🎰",
        layout="wide"
    )

    # Custom CSS
    st.markdown(f"""
    <style>
        .stApp {{
            background-color: #fafafa;
        }}
        .block-container {{
            padding-top: 2rem;
        }}
        h1, h2, h3 {{
            color: {NV_BLUE};
        }}
        .stButton > button {{
            background-color: {NV_BLUE};
            color: white;
        }}
        .stButton > button:hover {{
            background-color: #001a33;
            color: white;
        }}
    </style>
    """, unsafe_allow_html=True)

    # Authentication
    if not check_password():
        return

    # Load data
    districts_df = load_districts()
    access_df = load_access_data()
    sbac_df = load_sbac_data()

    # Sidebar
    st.sidebar.markdown(f"""
    <div style="text-align: center; padding: 20px 0;">
        <h2 style="color: {NV_BLUE}; margin: 0;">VERA-NV</h2>
        <p style="color: #666; font-size: 0.85rem; margin-top: 5px;">Nevada Implementation</p>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.divider()

    page = st.sidebar.radio(
        "Navigation",
        ["Overview", "ACCESS Analysis", "Type 4 Detection", "SBAC Analysis", "Export Data"]
    )

    st.sidebar.divider()

    st.sidebar.markdown("""
    **Data Sources:**
    - ACCESS for ELLs (WIDA)
    - SBAC (Smarter Balanced)
    - Nevada School Performance Framework

    **Type 4 Detection:**
    - Speaking vs Writing delta
    - Flag threshold: > 8 points

    ---

    [H-EDU.Solutions](https://h-edu.solutions)
    """)

    # Render selected page
    if page == "Overview":
        render_overview(districts_df, access_df, sbac_df)
    elif page == "ACCESS Analysis":
        render_access_analysis(access_df, districts_df)
    elif page == "Type 4 Detection":
        render_type4_detection(access_df, districts_df)
    elif page == "SBAC Analysis":
        render_sbac_analysis(sbac_df, districts_df)
    elif page == "Export Data":
        render_export(access_df, sbac_df, districts_df)

if __name__ == "__main__":
    main()
