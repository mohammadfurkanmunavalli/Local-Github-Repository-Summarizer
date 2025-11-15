# GitHub Repository Summarizer

A **local AI-powered tool** that analyzes and summarizes GitHub repositories (or any local folder) using **Ollama** models — all running **100% offline**.

This tool helps developers quickly understand the purpose and structure of unfamiliar repositories by generating:
-  **File-by-file summaries** (explaining what each file does)
-  **Overall repository summary** (purpose, architecture, and functionality)
-  **Markdown report** (downloadable summary file)

---

##  Features

 Summarizes **any GitHub repo or local project folder**  
 Works **completely offline** using **Ollama** (no API key required)  
 File-level + project-level summaries  
 Simple UI built with **Streamlit**  
 Supports multiple local models (`llama3`, `mistral`, `codellama`)  
 Downloadable `.md` summary report  

---

##  Tech Stack

- **Python 3.8+**
- **Streamlit** – for UI  
- **Ollama** – local LLM engine  
- **GitPython** – for cloning repositories  
- **Subprocess** – for executing LLM commands  
- **OS & JSON** – for handling files and formatting output  

---

##  Prerequisites

Before running this project, ensure you have the following installed:

1. **Python 3.8+**  
    [Download Python](https://www.python.org/downloads/)

2. **Git**  
    [Download Git](https://git-scm.com/downloads)

3. **Ollama (Local LLM Engine)**  
    [Download Ollama](https://ollama.com/download)

4. **Pull your preferred local model(s):**
   ```bash
   ollama pull llama3
   ollama pull mistral
   ollama pull codellama


## Installation

Clone this repository

git clone https://github.com/saqeeb05n/GitHub_Repository_Summarizer.git
cd GitHub_Repository_Summarizer


Create a virtual environment (optional but recommended)

python -m venv venv
venv\Scripts\activate      # On Windows

source venv/bin/activate   # On macOS/Linux


Install dependencies

> pip install -r requirements.txt

 Running the App (Streamlit UI)

Start the local Streamlit interface:

> streamlit run app.py


Then open your browser and go to:
 http://localhost:8501
