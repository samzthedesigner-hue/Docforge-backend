# DocForge Backend 🛠️

> **"From DOCFORGE, JESUS LOVES YOU ❤️"**

DocForge is a server-side document processing engine. It receives any file (PDF, DOCX, TXT, JSON), extracts and edits the content based on user instructions, repackages it into a requested format, and returns a secure download link. 

It is specifically designed to handle **large files (>50MB)** without timeouts by streaming processed files to disk and serving them via downloadable links.

---

## ✨ Features

- **Read & Extract:** Parses PDF, DOCX, TXT, and JSON files.
- **Smart Editing:** Applies text replacements based on user commands.
- **Repackage:** Converts extracted text to PDF, DOCX, JSON, or TXT.
- **Large File Support:** Processes huge files efficiently (saves to disk, not RAM).
- **Download Links:** Returns a URL for the processed file instead of raw data.
- **Custom Watermark:** Automatically stamps "From DOCFORGE, JESUS LOVES YOU ❤️" with custom colors (Silver, Blue, White) on every exported file.
- **History Logging:** Saves every process to a local SQLite database for future re-downloads.
- **Cloud Backup Ready:** Includes an API endpoint to mark records as "Backed up to Google Drive".

---

## 🚀 Live Deployment (Render.com)

This backend is designed to run flawlessly on **Render.com** (Free Tier).

### Deployment Steps:
1. Push this folder to a **GitHub repository**.
2. Go to [Render.com](https://render.com) → **New Web Service**.
3. Connect your GitHub repo. Select the `docforge-backend` folder.
4. **Runtime:** `Python 3`
5. **Build Command:** `pip install -r requirements.txt`
6. **Start Command:** `mkdir -p temp && uvicorn main:app --host 0.0.0.0 --port 8000`

### Environment Variables (Required):
Add this in your Render dashboard under **Environment Variables**:
- `RENDER_EXTERNAL_URL`: `https://your-app-name.onrender.com` (This ensures download links work correctly).

---

## 📡 API Endpoints

### 1. Health Check (Auto-Ping)
- **GET** `/health`
- **Response:** `{ "status": "alive" }`
- *Use this to keep your Render instance awake via cron-job.org (ping every 10 mins).*

### 2. Process Document
- **POST** `/process`
- **Form Data:**
  - `file`: The uploaded document (PDF, DOCX, TXT, JSON).
  - `instructions`: Edit command (e.g., "replace 'John' with 'Jane'").
  - `output_format`: "pdf", "docx", "json", or "txt".
  - `new_name`: Desired filename (without extension).
- **Response:**
```json
{
  "status": "success",
  "download_url": "https://.../download/xyz123.pdf",
  "filename": "myfile.pdf"
}
