import { useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [readme, setReadme] = useState("");
  const [repoUrl, setRepoUrl] = useState("");
  const [envSample, setEnvSample] = useState("");
  const [loading, setLoading] = useState(false);

  // const handleSubmit = async () => {
  //   const formData = new FormData();
  //   formData.append("file", file);

  //   try {
  //     const res = await axios.post("http://localhost:8000/analyze/", formData, {
  //       headers: { "Content-Type": "multipart/form-data" },
  //     });
  //     setReadme(res.data.readme);
  //   } catch (err) {
  //     console.error("Error uploading file:", err);
  //     alert("Failed to generate documentation.");
  //   }
  // };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const formData = new FormData();

      if (file) {
        formData.append("file", file);
      } else if (repoUrl) {
        formData.append("repo_url", repoUrl);
      } else {
        alert("Please select a file or enter a GitHub repo URL.");
        return;
      }

      const res = await axios.post("http://localhost:8000/analyze/", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setReadme(res.data.readme);
      setEnvSample(res.data.env_sample);
    } catch (err) {
      console.error(err);
      alert("Error: " + (err.response?.data?.detail || err.message));
    } finally {
      setLoading(false);
    }
  };

  const downloadReadme = () => {
    const blob = new Blob([readme], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "README.md";
    a.click();
    URL.revokeObjectURL(url);
  };

  const downloadFile = (content, filename) => {
    const blob = new Blob([content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    a.click();
    URL.revokeObjectURL(url);
  };

  const downloadZip = async () => {
    const formData = new FormData();
    if (file) {
      formData.append("file", file);
    } else if (repoUrl) {
      formData.append("repo_url", repoUrl);
    } else {
      alert("Please upload a file or enter a repo URL first.");
      return;
    }

    try {
      const res = await fetch("http://localhost:8000/download-docs/", {
        method: "POST",
        body: formData,
      });

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "project_docs.zip";
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      alert("Error downloading ZIP: " + err.message);
    }
  };

  return (
    <div className="App">
      <h1>ReadmeBoost</h1>

      <input
        type="file"
        disabled={loading}
        onChange={(e) => setFile(e.target.files[0])}
      />

      <input
        type="text"
        disabled={loading}
        placeholder="Paste GitHub repo URL"
        value={repoUrl}
        onChange={(e) => setRepoUrl(e.target.value)}
        style={{
          width: "100%",
          margin: "12px 0",
          padding: "8px",
          fontSize: "1rem",
        }}
      />

      <button onClick={handleSubmit} disabled={loading}>
        Generate Docs
      </button>

      {readme && (
        <>
          <div className="readme-preview">
            <ReactMarkdown>{readme}</ReactMarkdown>
          </div>

          <button onClick={downloadZip} disabled={loading}>
            Download All Docs (.zip)
          </button>

          <button onClick={downloadReadme}>Download README</button>
        </>
      )}



      {envSample && (
        <button onClick={() => downloadFile(envSample, ".env.sample")}>
          Download .env.sample
        </button>
      )}

      {loading && (
        <div>
          <div className="spinner"></div>
          <p>Analyzing your code…</p>
        </div>
      )}
    </div>

    // <div className="App">
    //   <h1>📘 ReadmeBoost</h1>
    //   <input type="file" onChange={(e) => setFile(e.target.files[0])} />
    //   <button onClick={handleSubmit}>Generate Docs</button>
    //   <div className="readme-preview">
    //     <ReactMarkdown>{readme}</ReactMarkdown>
    //   </div>
    //   <button onClick={downloadReadme}>Download README</button>
    // </div>
  );
}

export default App;
