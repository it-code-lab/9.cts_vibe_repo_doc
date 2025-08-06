README Boost is a modern web application that automatically generates professional-quality README.md files from GitHub repositories or uploaded source code archives. It's built with React and FastAPI and focuses on enhancing developer productivity and documentation quality.

🚀 Features

✅ Implemented:

🔍 Analyze GitHub Repos or ZIP Uploads

🧠 Function Docstring Extraction

🎯 FastAPI/Flask Route Detection

🧪 Dynamic .env.sample Generator

⏳ Loading Spinner UI Feedback

📜 Markdown Preview with Syntax Highlighting

🧱 File Tree Visualization

📦 Download All Docs (README + .env + API_DOC) as ZIP

🧹 Project Overview Generator

🧪 In Queue:

🌐 Multi-language Parsing (JS, Java, PHP, etc.)

🧾 Export OpenAPI (Swagger)

🧠 AI-Powered Summaries

🔄 Editable README before Export

📦 VS Code Extension

☁️ GitHub Actions (CI/CD Auto README)

📦 Tech Stack

Frontend: React + Tailwind CSS

Backend: FastAPI (Python)

Parsing: ast, inspect, os, pathlib

Optional AI: OpenAI (Pluggable)

📁 Example Output



⚙️ Installation

# Backend
venv\Scripts\activate
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
npm install
npm start


📜 License

MIT