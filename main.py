from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from pathlib import Path
from typing import List

app = FastAPI(title="File Download Service")

# Папка где хранятся файлы для скачивания
FILES_DIRECTORY = "download_files"

# Создаем папку если она не существует
os.makedirs(FILES_DIRECTORY, exist_ok=True)

# Монтируем статическую папку для доступа к файлам
app.mount("/files", StaticFiles(directory=FILES_DIRECTORY), name="files")


@app.get("/")
async def root():
    """Главная страница со списком файлов"""
    return {
        "message": "File Download Service",
        "endpoints": {
            "list_files": "/files",
            "download_file": "/download/{filename}",
            "preview_file": "/files/{filename}"
        }
    }


@app.get("/files", response_model=List[str])
async def list_files():
    """Получить список всех доступных файлов"""
    try:
        files = []
        for file_path in Path(FILES_DIRECTORY).iterdir():
            if file_path.is_file():
                files.append(file_path.name)
        return files
    except Exception as e:
        raise HTTPException(status_code=500,
                            detail=f"Error reading directory: {str(e)}")


@app.get("/download/{filename}")
async def download_file(filename: str):
    """Скачать файл (с заголовком для скачивания)"""
    file_path = Path(FILES_DIRECTORY) / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    if not file_path.is_file():
        raise HTTPException(status_code=400, detail="Not a file")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )


@app.get("/file-info/{filename}")
async def get_file_info(filename: str):
    """Получить информацию о файле"""
    file_path = Path(FILES_DIRECTORY) / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    if not file_path.is_file():
        raise HTTPException(status_code=400, detail="Not a file")

    stat = file_path.stat()
    return {
        "filename": filename,
        "size_bytes": stat.st_size,
        "size_mb": round(stat.st_size / (1024 * 1024), 2),
        "modified": stat.st_mtime
    }


from fastapi.responses import HTMLResponse


@app.get("/browser", response_class=HTMLResponse)
async def file_browser():
    """Веб-интерфейс для просмотра и скачивания файлов"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>File Download Browser</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .file-list { list-style: none; padding: 0; }
            .file-item { 
                padding: 10px; 
                margin: 5px 0; 
                background: #f5f5f5; 
                border-radius: 5px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .btn { 
                padding: 5px 15px; 
                background: #007bff; 
                color: white; 
                text-decoration: none; 
                border-radius: 3px;
                margin-left: 10px;
            }
            .btn:hover { background: #0056b3; }
            .btn-download { background: #28a745; }
            .btn-download:hover { background: #1e7e34; }
        </style>
    </head>
    <body>
        <h1>File Download Browser</h1>
        <div id="fileList">Loading...</div>

        <script>
            async function loadFiles() {
                try {
                    const response = await fetch('/files');
                    const files = await response.json();

                    const fileList = document.getElementById('fileList');
                    if (files.length === 0) {
                        fileList.innerHTML = '<p>No files available</p>';
                        return;
                    }

                    fileList.innerHTML = '<ul class="file-list">' + 
                        files.map(file => `
                            <li class="file-item">
                                <span>${file}</span>
                                <div>
                                    <a href="/files/${file}" class="btn" target="_blank">Preview</a>
                                    <a href="/download/${file}" class="btn btn-download">Download</a>
                                </div>
                            </li>
                        `).join('') + 
                        '</ul>';
                } catch (error) {
                    document.getElementById('fileList').innerHTML = '<p>Error loading files</p>';
                }
            }

            loadFiles();
            // Auto-refresh every 30 seconds
            setInterval(loadFiles, 30000);
        </script>
    </body>
    </html>
    """


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app,)