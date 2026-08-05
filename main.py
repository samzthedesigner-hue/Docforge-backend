from fastapi import FastAPI, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from database import init_db, save_history, get_history, mark_backed_up
from processor import extract_text, apply_edit, repackage_and_save

app = FastAPI(title="DocForge API")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
init_db()

@app.get("/health")
async def health():
    return {"status": "alive"}

@app.post("/process")
async def process_document(
    file: UploadFile,
    instructions: str = Form(...),
    output_format: str = Form(...),
    new_name: str = Form("output")
):
    try:
        raw_bytes = await file.read()
        mime_type = file.content_type or "text/plain"

        text = extract_text(raw_bytes, mime_type)
        edited_text = apply_edit(text, instructions)

        file_path = repackage_and_save(edited_text, output_format, new_name)

        base_url = os.getenv('RENDER_EXTERNAL_URL', 'http://localhost:8000')
        download_url = f"{base_url}/download/{os.path.basename(file_path)}"

        save_history(file.filename, new_name, output_format, download_url, {"instructions": instructions})

        return JSONResponse({
            "status": "success",
            "download_url": download_url,
            "filename": f"{new_name}.{output_format}"
        })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/download/{file_id}")
async def download_file(file_id: str, background_tasks: BackgroundTasks):
    file_path = f"temp/{file_id}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found or expired")
    
    background_tasks.add_task(os.remove, file_path)
    return FileResponse(file_path, media_type="application/octet-stream", filename=file_id)

@app.get("/history")
async def history():
    rows = get_history()
    return JSONResponse([
        {
            "id": r[0], "original": r[1], "new": r[2], "format": r[3], 
            "date": r[4], "download": r[5], "meta": r[6], "backed_up": r[7]
        }
        for r in rows
    ])

@app.post("/mark_backed_up/{record_id}")
async def backend_mark_backed_up(record_id: int):
    mark_backed_up(record_id)
    return {"status": "marked"}
