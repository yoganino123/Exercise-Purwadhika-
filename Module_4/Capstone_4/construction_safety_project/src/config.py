from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CAPSTONE_ROOT = PROJECT_ROOT.parent
DATASET_DIR = CAPSTONE_ROOT / "construction safety.v1i.yolov12"
DATASET_YAML = DATASET_DIR / "data.yaml"
EXAMPLE_IMAGE = CAPSTONE_ROOT / "Contoh Data Test" / "construction-workers.jpg"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"
RUNS_DIR = PROJECT_ROOT / "runs"
DEFAULT_WEIGHTS = ARTIFACTS_DIR / "best.pt"


def ensure_project_dirs() -> None:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    RUNS_DIR.mkdir(parents=True, exist_ok=True)