from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image

from src.config import DEFAULT_WEIGHTS, EXAMPLE_IMAGE, resolve_weights_path
from src.predictor import SafetyPredictor


st.set_page_config(page_title="Construction Safety Monitor", page_icon="⛑", layout="wide")


@st.cache_resource(show_spinner=False)
def load_predictor(weights_path: str) -> SafetyPredictor:
    return SafetyPredictor(weights_path)


def load_selected_image(uploaded_file, use_example: bool) -> Image.Image | None:
    if uploaded_file is not None:
        return Image.open(uploaded_file).convert("RGB")
    if use_example and EXAMPLE_IMAGE.exists():
        return Image.open(EXAMPLE_IMAGE).convert("RGB")
    return None


st.title("Construction Safety Detection")
st.caption(
    "Deteksi pekerja konstruksi dan analisis kepatuhan alat pelindung diri berdasarkan model object detection."
)

with st.sidebar:
    st.header("Inference Settings")
    resolved_weights_path, weights_note = resolve_weights_path()
    weights_path = st.text_input("Path model weights (.pt)", value=str(resolved_weights_path))
    if weights_note:
        st.caption(weights_note)
    conf_threshold = st.slider("Confidence threshold", min_value=0.05, max_value=0.95, value=0.25, step=0.05)
    iou_threshold = st.slider("IoU threshold", min_value=0.05, max_value=0.95, value=0.45, step=0.05)
    use_example = st.checkbox("Use sample image", value=True)

uploaded_file = st.file_uploader("Upload gambar pekerja konstruksi", type=["jpg", "jpeg", "png"])
image = load_selected_image(uploaded_file, use_example)

if image is None:
    st.info("Upload gambar atau aktifkan sample image untuk mencoba aplikasi.")
    st.stop()

try:
    predictor = load_predictor(weights_path)
except FileNotFoundError as error:
    st.error(str(error))
    st.info(
        "Untuk deploy Streamlit Cloud: set environment variable MODEL_WEIGHTS_URL (link direct .pt) "
        "atau WEIGHTS_PATH ke lokasi model yang valid."
    )
    st.code(
        "MODEL_WEIGHTS_URL=https://.../best.pt\nWEIGHTS_PATH=artifacts/best.pt",
        language="bash",
    )
    st.info(
        f"Default project path yang dicoba: {DEFAULT_WEIGHTS}. "
        "Jika model tidak dipush ke repo (misalnya karena .gitignore), aplikasi tidak bisa load model saat deploy."
    )
    st.stop()

prediction = predictor.predict(np.array(image), conf_threshold=conf_threshold, iou_threshold=iou_threshold)
analysis = prediction["analysis"]

left_col, right_col = st.columns([1.25, 1])

with left_col:
    st.image(prediction["annotated_image"], caption="Detection result", use_container_width=True)

with right_col:
    metric_cols = st.columns(3)
    metric_cols[0].metric("Total Workers", analysis["total_workers"])
    metric_cols[1].metric("Compliant", analysis["compliant_workers"])
    metric_cols[2].metric("Non-Compliant", analysis["non_compliant_workers"])

    class_counts = analysis["class_counts"]
    counts_df = pd.DataFrame(
        [{"label": label, "count": count} for label, count in sorted(class_counts.items())]
    )
    st.subheader("Object Count")
    if counts_df.empty:
        st.warning("Tidak ada objek yang terdeteksi.")
    else:
        st.dataframe(counts_df, use_container_width=True, hide_index=True)

worker_rows = []
for worker in analysis["worker_assessments"]:
    worker_rows.append(
        {
            "worker_id": worker.worker_id,
            "helmet": "Yes" if worker.has_helmet else "No",
            "vest": "Yes" if worker.has_vest else "No",
            "missing_items": ", ".join(worker.missing_items) if worker.missing_items else "-",
            "violations": ", ".join(worker.violations) if worker.violations else "-",
        }
    )

st.subheader("Per Worker PPE Assessment")
if worker_rows:
    st.dataframe(pd.DataFrame(worker_rows), use_container_width=True, hide_index=True)
else:
    st.info("Tidak ada person yang terdeteksi pada gambar.")

with st.expander("How this app makes the decision"):
    st.markdown(
        """
        - Model mendeteksi lima class: helmet, no-helmet, no-vest, person, dan vest.
        - Setiap item APD dipasangkan ke bounding box person terdekat.
        - Seorang worker dianggap compliant jika terdeteksi memakai helmet dan vest, tanpa label pelanggaran.
        - Ringkasan akhir menampilkan total pekerja, jumlah pekerja patuh, dan jumlah pekerja tidak patuh.
        """
    )