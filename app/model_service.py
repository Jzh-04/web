from pathlib import Path
from typing import List, Tuple
import uuid
import cv2
from ultralytics import YOLO


class ModelService:
    def __init__(self, model_path: str):
        self.model = YOLO(model_path)

    def predict(self, image_path: str) -> Tuple[List[str], str | None, str | None]:
        results = self.model.predict(image_path, verbose=False)

        labels: List[str] = []
        plotted_image_path = None

        for result in results:
            if result.boxes is not None and len(result.boxes.cls) > 0:
                labels = [self.model.names[int(cls)] for cls in result.boxes.cls]

            plotted = result.plot()
            out_dir = Path("app/static/results")
            out_dir.mkdir(parents=True, exist_ok=True)
            filename = f"{uuid.uuid4().hex}.jpg"
            save_path = out_dir / filename
            cv2.imwrite(str(save_path), plotted)
            plotted_image_path = f"/static/results/{filename}"

        top_label = labels[0] if labels else None
        return labels, top_label, plotted_image_path