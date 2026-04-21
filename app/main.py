from pathlib import Path
import shutil
import uuid

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.model_service import ModelService
from app.text_service import TextService
from app.schemas import PredictResponse

APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"
UPLOAD_DIR = STATIC_DIR / "uploads"
RESULT_DIR = STATIC_DIR / "results"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
RESULT_DIR.mkdir(parents=True, exist_ok=True)

MODEL_PATH = "models/best.pt"

app = FastAPI(title="Grape Leaf Recognition System")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

model_service = ModelService(MODEL_PATH)
text_service = TextService()


@app.get("/")
def home():
    return FileResponse(str(STATIC_DIR / "index.html"))


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictResponse)
async def predict(
    file: UploadFile = File(...),
    detail: str = Form("medium"),
):
    suffix = Path(file.filename).suffix.lower() or ".jpg"
    file_id = f"{uuid.uuid4().hex}{suffix}"
    save_path = UPLOAD_DIR / file_id

    with save_path.open("wb") as f:
        shutil.copyfileobj(file.file, f)

    labels, top_label, image_url = model_service.predict(str(save_path))
    description = text_service.generate_description(labels, detail=detail)

    return PredictResponse(
        labels=labels,
        top_label=top_label,
        description=description,
        image_url=image_url,
    )