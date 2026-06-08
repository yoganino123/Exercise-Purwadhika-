import os
from pathlib import Path
from urllib.request import urlretrieve


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


def resolve_weights_path() -> tuple[Path, str | None]:
    ensure_project_dirs()

    # Allow explicit path override from deployment environment.
    env_weights_path = os.getenv("WEIGHTS_PATH") or os.getenv("MODEL_WEIGHTS_PATH")
    if env_weights_path:
        path = Path(env_weights_path)
        return path, "Using WEIGHTS_PATH/MODEL_WEIGHTS_PATH from environment."

    if DEFAULT_WEIGHTS.exists():
        return DEFAULT_WEIGHTS, None

    fallback_candidates = [
        ARTIFACTS_DIR / "last.pt",
        PROJECT_ROOT / "best.pt",
        PROJECT_ROOT / "last.pt",
    ]

    for candidate in fallback_candidates:
        if candidate.exists():
            return candidate, f"Using fallback weights: {candidate.name}."

    # Optional: download weights on first run in hosted environments.
    weights_url = os.getenv("MODEL_WEIGHTS_URL")
    if weights_url:
        target_path = DEFAULT_WEIGHTS
        try:
            urlretrieve(weights_url, target_path)
            return target_path, "Downloaded weights from MODEL_WEIGHTS_URL."
        except Exception as error:  # pragma: no cover - network/path errors vary by runtime
            return target_path, f"Failed to download MODEL_WEIGHTS_URL: {error}"

    return DEFAULT_WEIGHTS, None