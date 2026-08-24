"""Backend de inferência YOLO via ONNX Runtime (CPU), sem dependência de torch.

Implementa o fluxo padrão: letterbox -> blob -> sessão ORT -> decode+ NMS ->
mapeamento de volta para as coordenadas originais do frame.

Compatível com saídas YOLOv8/YOLO11 exportadas em ONNX (shape [1, 4+C, N]).
"""
import logging
from pathlib import Path

import cv2
import numpy as np

logger = logging.getLogger(__name__)

DEFAULT_INPUT_SIZE = 640
_PAD_VALUE = 114


class OnnxYoloDetector:
    """Detector YOLO genérico rodando em ONNX Runtime (CPUExecutionProvider)."""

    def __init__(
        self,
        model_path: str,
        conf: float = 0.25,
        iou: float = 0.45,
        input_size: int = DEFAULT_INPUT_SIZE,
        class_names: list[str] | None = None,
    ):
        self.model_path = str(model_path)
        self.conf_threshold = conf
        self.iou_threshold = iou
        self.input_size = input_size
        self.class_names = class_names or []
        self._session = None
        self._input_name = ""

    @property
    def is_available(self) -> bool:
        return Path(self.model_path).exists()

    def _ensure_session(self) -> bool:
        if self._session is not None:
            return True
        if not self.is_available:
            logger.warning("Modelo ONNX nao encontrado: %s", self.model_path)
            return False
        try:
            import onnxruntime as ort

            self._session = ort.InferenceSession(
                self.model_path,
                providers=["CPUExecutionProvider"],
            )
            self._input_name = self._session.get_inputs()[0].name
            logger.info("ONNX backend carregado: %s", self.model_path)
            return True
        except Exception as e:
            logger.error("Falha ao carregar modelo ONNX %s: %s", self.model_path, e)
            self._session = None
            return False

    def detect(
        self,
        frame: np.ndarray,
        class_filter: set[int] | None = None,
    ) -> list[dict]:
        """Roda inferência e retorna dicts {bbox_xywh, confidence, class_id, class_name}."""
        if not self._ensure_session():
            return []

        h_orig, w_orig = frame.shape[:2]
        letterboxed, ratio, pad_x, pad_y = _letterbox(frame, self.input_size)
        blob = _to_blob(letterboxed)

        try:
            raw = self._session.run(None, {self._input_name: blob})[0]
        except Exception as e:
            logger.error("Inferencia ONNX falhou (%s): %s", self.model_path, e)
            return []

        preds = _decode_output(raw)
        boxes = _nms(preds, self.conf_threshold, self.iou_threshold, class_filter)

        detections = []
        for cx, cy, bw, bh, score, class_id in boxes:
            x1 = (cx - bw / 2 - pad_x) / ratio
            y1 = (cy - bh / 2 - pad_y) / ratio
            w = bw / ratio
            h = bh / ratio
            x1 = max(0.0, min(x1, w_orig))
            y1 = max(0.0, min(y1, h_orig))
            w = min(w, w_orig - x1)
            h = min(h, h_orig - y1)
            detections.append({
                "bbox": [float(x1), float(y1), float(w), float(h)],
                "confidence": float(score),
                "class_id": int(class_id),
                "class_name": (
                    self.class_names[class_id]
                    if 0 <= class_id < len(self.class_names)
                    else f"class_{class_id}"
                ),
            })
        return detections


def _letterbox(img: np.ndarray, size: int) -> tuple[np.ndarray, float, int, int]:
    """Redimensiona preservando aspecto e centraliza em canvas cinza size×size."""
    h, w = img.shape[:2]
    ratio = min(size / w, size / h)
    new_w, new_h = int(round(w * ratio)), int(round(h * ratio))
    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)
    canvas = np.full((size, size, 3), _PAD_VALUE, dtype=np.uint8)
    pad_x = (size - new_w) // 2
    pad_y = (size - new_h) // 2
    canvas[pad_y : pad_y + new_h, pad_x : pad_x + new_w] = resized
    return canvas, ratio, pad_x, pad_y

def _to_blob(letterboxed: np.ndarray) -> np.ndarray:
    """BGR uint8 HWC -> RGB float32 CHW normalizado, batch de 1."""
    rgb = cv2.cvtColor(letterboxed, cv2.COLOR_BGR2RGB)
    chw = rgb.transpose(2, 0, 1)
    return (chw[None].astype(np.float32) / 255.0).astype(np.float32)


def _decode_output(raw: np.ndarray) -> np.ndarray:
    """Normaliza saída para shape [N, 4+C] (cx, cy, w, h, scores...)."""
    preds = np.asarray(raw)
    if preds.ndim == 3:
        preds = preds[0]
    # YOLOv8/11 exporta [1, 4+C, N]; transposto fica [N, 4+C].
    if preds.shape[0] < preds.shape[1]:
        preds = preds.T
    return preds


def _nms(
    preds: np.ndarray,
    conf_threshold: float,
    iou_threshold: float,
    class_filter: set[int] | None,
) -> list[tuple[float, float, float, float, float, int]]:
    """Filtra por confiança/classe, aplica NMS e devolve caixas em cxcywh."""
    if preds.shape[1] < 5:
        return []
    class_scores = preds[:, 4:]
    best_ids = class_scores.argmax(axis=1)
    best_scores = class_scores.max(axis=1)

    candidates = []
    for i in range(preds.shape[0]):
        score = float(best_scores[i])
        if score < conf_threshold:
            continue
        class_id = int(best_ids[i])
        if class_filter is not None and class_id not in class_filter:
            continue
        cx, cy, bw, bh = preds[i, :4]
        candidates.append([float(cx - bw / 2), float(cy - bh / 2), float(bw), float(bh), score, class_id])

    if not candidates:
        return []

    indices = cv2.dnn.NMSBoxes(
        [c[:4] for c in candidates],
        [c[4] for c in candidates],
        conf_threshold,
        iou_threshold,
    )
    indices = np.asarray(indices).flatten()
    return [tuple(candidates[int(i)]) for i in indices]
