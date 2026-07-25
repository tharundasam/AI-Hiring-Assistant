import plotly.express as px
import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="AI Hiring Assistant",
    page_icon="🤖",
    layout="wide"
)

tab1, tab2, tab3, tab4 = st.tabs([
    "📄 Upload Resume",
    "💼 Upload Job",
    "🏆 Ranking",
    "💬 Recruiter Chat"
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

            response = requests.post(
                f"{API_URL}/upload/",
                files=files
            )

            st.success(response.json())


# -------------------------
# Job Upload
# -------------------------

with tab2:

    st.header("Upload Job Description")

    job = st.file_uploader(
        "Choose Job Description",
        type=["pdf", "docx"],
        key="job"
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

            response = requests.post(
                f"{API_URL}/job/",
                files=files
            )

            st.success(response.json())


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