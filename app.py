import streamlit as st
from summarizer import analyze_repo

st.set_page_config(page_title="Local GitHub Repo Summarizer", layout="wide")

st.title("🧠 Local GitHub Repository Summarizer")
st.caption("Runs entirely offline using Ollama + Streamlit")

# Input fields
repo_url = st.text_input("🔗 Enter GitHub Repository URL or local folder path:")
model_name = st.selectbox("🧩 Choose Local Model", ["phi", "llama3", "mistral", "codellama"])
run_btn = st.button("🚀 Analyze Repository")

# Run analysis
if run_btn and repo_url:
    with st.spinner("🔍 Analyzing repository locally... Please wait."):
        result = analyze_repo(repo_url, model_name)

    # ✅ Handle errors gracefully
    if "error" in result:
        st.error(f"❌ {result['error']}")
    else:
        st.success("✅ Analysis complete!")

        # ✅ File summaries
        st.subheader("📁 File Summaries")
        for file, summary in result["files"].items():
            with st.expander(file):
                st.markdown(summary)

        # ✅ Overall summary
        st.subheader("🧩 Overall Summary")
        st.markdown(result["overall_summary"])

        # ✅ Download button
        st.download_button(
            label="📥 Download Summary (Markdown)",
            data=result["markdown"],
            file_name="repo_summary.md",
            mime="text/markdown"
        )

elif run_btn and not repo_url:
    st.warning("⚠️ Please enter a valid GitHub URL or local folder path before analyzing.")
