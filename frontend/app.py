import plotly.express as px
import streamlit as st
import requests
import pandas as pd

API_URL = "https://ai-hiring-assistant-6o5j.onrender.com"

st.set_page_config(
    page_title="AI Hiring Assistant",
    page_icon="🤖",
    layout="wide"
)

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📄 Upload Resume",
    "💼 Upload Job",
    "🏆 Ranking",
    "💬 Recruiter Chat",
    "📊 Dashboard"
])
# -------------------------
# Resume Upload
# -------------------------

with tab1:

    st.header("Upload Resume")

    resume = st.file_uploader(
        "Choose Resume",
        type=["pdf", "docx"]
    )

    if st.button("Upload Resume"):

        if resume:

            files = {
                "file": (
                    resume.name,
                    resume,
                    resume.type
                )
            }

            try:

                response = requests.post(
                    f"{API_URL}/upload/",
                    files=files
                )

                if response.status_code == 200:
                    st.success("✅ Resume Uploaded Successfully")
                    st.json(response.json())

                else:
                    st.error(f"❌ Upload Failed ({response.status_code})")
                    st.code(response.text)

            except Exception as e:
                st.error(f"Connection Error:\n{str(e)}")

        else:
            st.warning("Please choose a Resume.")


# -------------------------
# Job Upload
# -------------------------

with tab2:

    st.header("Upload Job Description")

    job = st.file_uploader(
        "Choose Job Description",
        type=["txt", "pdf", "docx"]
    )

    if st.button("Upload Job"):

        if job:

            files = {
                "file": (
                    job.name,
                    job,
                    job.type
                )
            }

            try:

                response = requests.post(
                    f"{API_URL}/job/",
                    files=files
                )

                if response.status_code == 200:
                    st.success("✅ Job Description Uploaded Successfully")
                    st.json(response.json())

                else:
                    st.error(f"❌ Upload Failed ({response.status_code})")
                    st.code(response.text)

            except Exception as e:
                st.error(f"Connection Error:\n{str(e)}")

        else:
            st.warning("Please choose a Job Description.")


# -------------------------
# Ranking
# -------------------------

with tab3:

    st.header("Candidate Ranking")

    if st.button("Generate Ranking"):

        response = requests.get(
            f"{API_URL}/ranking/"
        )

        data = response.json()

        if "ranking" in data:

            df = pd.DataFrame(data["ranking"])

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "Candidates",
                len(df)
            )

            col2.metric(
                "Highest Score",
                f"{df['overall_score'].max():.1f}%"
            )

            col3.metric(
                "Average Score",
                f"{df['overall_score'].mean():.1f}%"
            )

            st.divider()

            st.dataframe(df, width="stretch")

            fig = px.bar(
                df,
                x="candidate",
                y="overall_score",
                title="Candidate Scores"
            )

            st.plotly_chart(fig, width="stretch")



            candidate = st.selectbox(
                "Select Candidate",
                df["candidate"]
            )

            selected = df[
                df["candidate"] == candidate
            ].iloc[0]

            st.subheader("👤 Candidate Details")

            st.write(f"**Candidate:** {selected['candidate']}")

            st.metric(
                "Overall Score",
                f"{selected['overall_score']:.2f}%"
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Semantic",
                    f"{selected['semantic_score']:.2f}%"
                )

            with col2:
                st.metric(
                    "Skills",
                    f"{selected['skills_score']:.2f}%"
                )

            with col3:
                st.metric(
                    "Education",
                    f"{selected['education_score']:.2f}%"
                )

            col1, col2 = st.columns(2)

            with col1:

                st.success("✅ Matched Skills")

                SPECIAL = {
                    "aws": "AWS",
                    "sql": "SQL",
                    "azure": "Azure",
                    "typescript": "TypeScript"
                }

                for skill in selected["matched_skills"]:
                    st.write(f"✔ {SPECIAL.get(skill.lower(), skill.title())}")
            with col2:

                st.error("❌ Missing Skills")

                for skill in selected["missing_skills"]:
                    st.write(f"✘ {SPECIAL.get(skill.lower(), skill.title())}")

            if "strengths" in selected:

                st.subheader("💪 Strengths")

                for item in selected["strengths"]:
                    st.success(item)

            if "weaknesses" in selected:

                st.subheader("⚠ Weaknesses")

                for item in selected["weaknesses"]:
                    st.warning(item)

            if "recommendations" in selected:

                st.subheader("💡 Recommendations")

                for item in selected["recommendations"]:
                    st.info(item) 
            st.subheader("📊 Additional Scores")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Experience",
                    f"{selected['experience_score']:.0f}%"
                )

            with col2:
                st.metric(
                    "Projects",
                    f"{selected['projects_score']:.0f}%"
                )

            with col3:
                st.metric(
                    "Certifications",
                    f"{selected['certification_score']:.0f}%"
                )  

            st.divider()

            st.subheader("🎯 AI Interview Questions")

            questions = selected["interview_questions"]

            for topic, question_list in questions.items():

                with st.expander(f"📌 {topic}"):

                    for i, question in enumerate(question_list, start=1):

                        st.write(f"{i}. {question}")

            csv = df.to_csv(index=False)

            st.download_button(
                "📥 Download Ranking CSV",
                csv,
                "candidate_ranking.csv",
                "text/csv"
            )                

        else:

            st.error(data)

with tab4:

    st.header("💬 AI Recruiter Chat")

    context = st.text_area(
        "Resume Context",
        height=250,
        placeholder="Paste resume text or AI summary here..."
    )

    question = st.text_input(
        "Ask a Question",
        placeholder="Example: Does this candidate know Python?"
    )

    if st.button("Ask AI"):

        if context and question:

            response = requests.post(
                f"{API_URL}/chat/",
                json={
                    "context": context,
                    "question": question
                }
            )

            if response.status_code == 200:

                answer = response.json()["answer"]

                st.success(answer)

            else:

                st.error("Unable to generate answer.")

with tab5:

    st.header("📊 Recruiter Dashboard")

    try:
        response = requests.get(f"{API_URL}/dashboard/")

        if response.status_code == 200:

            candidates = response.json()

            if candidates:

                df = pd.DataFrame(candidates)

                top_candidate = df.sort_values(
                    by="overall_score",
                    ascending=False
                ).iloc[0]

                st.success(
                    f"🏆 Top Candidate: {top_candidate['name']} "
                    f"(ATS Score: {top_candidate['overall_score']})"
                )

                st.divider()

                # ---------------- Dashboard Metrics ----------------

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Total Candidates",
                    len(df)
                )

                col2.metric(
                    "Highest ATS",
                    int(df["overall_score"].max())
                )

                col3.metric(
                    "Average ATS",
                    round(df["overall_score"].mean(), 1)
                )

                st.subheader("📊 Recruitment Statistics")

                st.write(f"Total Candidates : {len(df)}")

                st.write(
                    f"Average ATS : {round(df['overall_score'].mean(),2)}"
                )

                st.write(
                    f"Highest ATS : {df['overall_score'].max()}"
                )

                st.write(
                    f"Lowest ATS : {df['overall_score'].min()}"
                )

                st.divider()

                # ---------------- Search ----------------

                search = st.text_input("🔍 Search Candidate")

                skill = st.text_input("🛠 Filter by Skill")

                if skill:
                    df = df[
                        df["skills"].str.contains(
                            skill,
                            case=False,
                            na=False
                        )
                    ]

                if search:
                    df = df[df["name"].str.contains(search, case=False, na=False)]

                # ---------------- Table ----------------

                styled_df = df.style.background_gradient(
                    subset=["overall_score"],
                    cmap="Greens"
                )

                st.dataframe(
                    styled_df,
                    use_container_width=True
                )

                st.divider()

                candidate = st.selectbox(
                    "👤 Select Candidate",
                    df["name"].tolist()
                )

                selected = df[df["name"] == candidate].iloc[0]

                st.subheader("📄 Candidate Details")

                st.write("### 👤 Personal Information")

                st.write(f"**Name:** {selected['name']}")
                st.write(f"**Email:** {selected['email']}")
                st.write(f"**Phone:** {selected['phone']}")

                st.write("### 🛠 Skills")

                st.write(selected["skills"])

                col1, col2 = st.columns(2)

                col1.metric(
                    "ATS Score",
                    selected["overall_score"]
                )

                col2.metric(
                    "Semantic Score",
                    selected["semantic_score"]
                )

                st.write("### 🤖 AI Summary")

                st.info(selected["summary"])

                st.write("### 🎓 Education")

                st.write(selected["education"])

                st.write("### 💼 Experience")

                st.write(selected["experience"])

                st.write("### 📂 Projects")

                st.write(selected["projects"])

                st.write("### 🏅 Certifications")

                st.write(selected["certifications"])

                st.write("### ❓ AI Interview Questions")

                st.text(selected["interview_questions"])

                st.divider()

                st.subheader("📈 Candidate Score Comparison")

                chart_df = pd.DataFrame({
                    "Score Type": ["ATS Score", "Semantic Score"],
                    "Score": [
                        selected["overall_score"],
                        selected["semantic_score"]
                    ]
                })

                st.bar_chart(
                    chart_df.set_index("Score Type")
                )

                st.divider()

                st.subheader("🛠 Candidate Skills")

                skills = str(selected["skills"]).split(",")

                for skill in skills:
                    st.success(skill.strip())

                st.subheader("📊 ATS Progress")

                st.progress(
                    int(selected["overall_score"]) / 100
                )

                st.write(f"Overall ATS Score : {selected['overall_score']}")

            else:
                st.info("No resumes found.")

        else:
            st.error("Failed to load dashboard.")

    except Exception as e:
        st.error(f"Error: {e}")