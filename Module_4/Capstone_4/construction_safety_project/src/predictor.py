from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import cv2
import numpy as np
from ultralytics import YOLO

from src.ppe_analysis import Detection, analyze_ppe_compliance


class SafetyPredictor:
    def __init__(self, weights_path: str | Path) -> None:
        self.weights_path = Path(weights_path)
        if not self.weights_path.exists():
            raise FileNotFoundError(f"Model weights not found: {self.weights_path}")
        self.model = YOLO(str(self.weights_path))

    def predict(
        self,
        image: np.ndarray,
        conf_threshold: float = 0.25,
        iou_threshold: float = 0.45,
    ) -> Dict[str, Any]:
        results = self.model.predict(
            source=image,
            conf=conf_threshold,
            iou=iou_threshold,
            verbose=False,
        )
        result = results[0]
        detections: List[Detection] = []
        names = result.names

        if result.boxes is not None:
            xyxy = result.boxes.xyxy.cpu().numpy()
            confidences = result.boxes.conf.cpu().numpy()
            classes = result.boxes.cls.cpu().numpy().astype(int)

            for box, confidence, class_index in zip(xyxy, confidences, classes):
                detections.append(
                    Detection(
                        label=names[class_index],
                        confidence=float(confidence),
                        x1=float(box[0]),
                        y1=float(box[1]),
                        x2=float(box[2]),
                        y2=float(box[3]),
                    )
                )

        analysis = analyze_ppe_compliance(detections)
        annotated_bgr = result.plot()
        annotated_rgb = cv2.cvtColor(annotated_bgr, cv2.COLOR_BGR2RGB)

        return {
            "detections": detections,
            "analysis": analysis,
            "annotated_image": annotated_rgb,
        }