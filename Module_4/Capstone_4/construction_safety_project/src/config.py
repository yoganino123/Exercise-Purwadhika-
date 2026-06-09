import os
import importlib
import re
from urllib.parse import parse_qs, urlparse
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

# Load local secrets from .env for local development.
try:
    dotenv_module = importlib.import_module("dotenv")
    dotenv_module.load_dotenv(dotenv_path=PROJECT_ROOT / ".env")
except ImportError:  # pragma: no cover - optional for environments without python-dotenv
    pass


def ensure_project_dirs() -> None:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)
    RUNS_DIR.mkdir(parents=True, exist_ok=True)


def _extract_google_drive_file_id(url: str) -> str | None:
    parsed = urlparse(url)
    host = parsed.netloc.lower()

    if "drive.google.com" not in host and "docs.google.com" not in host:
        return None

    query_id = parse_qs(parsed.query).get("id")
    if query_id and query_id[0]:
        return query_id[0]

    parts = [part for part in parsed.path.split("/") if part]
    if "d" in parts:
        index = parts.index("d")
        if index + 1 < len(parts):
            return parts[index + 1]

    return None


def _download_google_drive_without_gdown(file_id: str, target_path: Path) -> None:
    try:
        requests = importlib.import_module("requests")
    except ImportError as error:  # pragma: no cover - runtime dependency varies
        raise RuntimeError("Install gdown or requests to download Google Drive model weights.") from error

    base_url = "https://drive.google.com/uc"
    session = requests.Session()

    response = session.get(base_url, params={"export": "download", "id": file_id}, stream=True, timeout=60)
    response.raise_for_status()

    if "text/html" in response.headers.get("Content-Type", ""):
        html = response.text
        token_match = re.search(r"confirm=([0-9A-Za-z_]+)", html)
        if token_match:
            confirm_token = token_match.group(1)
            response = session.get(
                base_url,
                params={"export": "download", "id": file_id, "confirm": confirm_token},
                stream=True,
                timeout=60,
            )
            response.raise_for_status()

    with target_path.open("wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                file.write(chunk)


def _validate_weights_file(path: Path) -> None:
    if not path.exists() or path.stat().st_size < 1024:
        raise RuntimeError("Downloaded weights file is missing or too small.")

    with path.open("rb") as file:
        head = file.read(512).lstrip().lower()

    if head.startswith(b"<!doctype html") or head.startswith(b"<html"):
        raise RuntimeError("Downloaded file is HTML, not a .pt model file.")


def _download_weights(weights_url: str, target_path: Path) -> None:
    target_path.parent.mkdir(parents=True, exist_ok=True)

    file_id = _extract_google_drive_file_id(weights_url)
    if file_id:
        try:
            gdown = importlib.import_module("gdown")
            output = gdown.download(id=file_id, output=str(target_path), quiet=True)
            if not output:
                raise RuntimeError("Google Drive download failed.")
        except ImportError:
            _download_google_drive_without_gdown(file_id, target_path)
    else:
        urlretrieve(weights_url, target_path)

    _validate_weights_file(target_path)


def resolve_weights_path() -> tuple[Path, str | None]:
    ensure_project_dirs()

    # Allow explicit path override from deployment environment.
    env_weights_path = os.getenv("WEIGHTS_PATH") or os.getenv("MODEL_WEIGHTS_PATH")
    if env_weights_path:
        path = Path(env_weights_path)
        return path, "Using WEIGHTS_PATH/MODEL_WEIGHTS_PATH from environment."

    force_refresh = os.getenv("MODEL_FORCE_REFRESH", "0").strip().lower() in {"1", "true", "yes"}
    weights_url = os.getenv("MODEL_WEIGHTS_URL", "").strip()

    if not force_refresh and DEFAULT_WEIGHTS.exists():
        return DEFAULT_WEIGHTS, "Using cached model at artifacts/best.pt."

    fallback_candidates = [
        ARTIFACTS_DIR / "last.pt",
        PROJECT_ROOT / "best.pt",
        PROJECT_ROOT / "last.pt",
    ]

    for candidate in fallback_candidates:
        if candidate.exists():
            return candidate, f"Using fallback weights: {candidate.name}."

    if not weights_url:
        return DEFAULT_WEIGHTS, "MODEL_WEIGHTS_URL is not set. Add it in .env (local) or Streamlit Secrets (deploy)."

    if weights_url:
        target_path = DEFAULT_WEIGHTS
        try:
            _download_weights(weights_url, target_path)
            return target_path, "Downloaded weights from MODEL_WEIGHTS_URL."
        except Exception as error:  # pragma: no cover - network/path errors vary by runtime
            if target_path.exists():
                return target_path, f"Failed to refresh MODEL_WEIGHTS_URL, using cached model: {error}"
            return target_path, f"Failed to download MODEL_WEIGHTS_URL: {error}"

    return DEFAULT_WEIGHTS, None