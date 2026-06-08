from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from ultralytics import YOLO

from src.config import ARTIFACTS_DIR, DATASET_YAML, RUNS_DIR, ensure_project_dirs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a construction safety detector")
    parser.add_argument("--model", default="yolo11n.pt", help="Base YOLO weights to fine-tune")
    parser.add_argument("--epochs", type=int, default=30, help="Number of training epochs")
    parser.add_argument("--imgsz", type=int, default=640, help="Image size")
    parser.add_argument("--batch", type=int, default=16, help="Batch size")
    parser.add_argument("--device", default="cpu", help="Training device, for example cpu or 0")
    parser.add_argument("--patience", type=int, default=10, help="Early stopping patience")
    parser.add_argument("--run-name", default="construction_safety_yolo11n", help="Run directory name")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ensure_project_dirs()

    if not DATASET_YAML.exists():
        raise FileNotFoundError(f"Dataset config not found: {DATASET_YAML}")

    model = YOLO(args.model)
    results = model.train(
        data=str(DATASET_YAML),
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=args.batch,
        device=args.device,
        patience=args.patience,
        project=str(RUNS_DIR),
        name=args.run_name,
        exist_ok=True,
        pretrained=True,
        optimizer="auto",
        plots=True,
    )

    best_weights = Path(results.save_dir) / "weights" / "best.pt"
    if best_weights.exists():
        target_path = ARTIFACTS_DIR / "best.pt"
        shutil.copy2(best_weights, target_path)
        print(f"Best weights copied to: {target_path}")
    else:
        print("Training completed, but best.pt was not found.")

    metrics = model.val(data=str(DATASET_YAML), split="test")
    print("Validation summary:")
    print(metrics.results_dict)


if __name__ == "__main__":
    main()