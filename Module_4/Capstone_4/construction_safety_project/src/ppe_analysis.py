from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple


PERSON_LABEL = "person"
HELMET_LABEL = "helmet"
NO_HELMET_LABEL = "no-helmet"
VEST_LABEL = "vest"
NO_VEST_LABEL = "no-vest"
MIN_NEGATIVE_CONFIDENCE = 0.45


@dataclass
class Detection:
    label: str
    confidence: float
    x1: float
    y1: float
    x2: float
    y2: float

    @property
    def width(self) -> float:
        return max(self.x2 - self.x1, 0.0)

    @property
    def height(self) -> float:
        return max(self.y2 - self.y1, 0.0)

    @property
    def center(self) -> Tuple[float, float]:
        return ((self.x1 + self.x2) / 2.0, (self.y1 + self.y2) / 2.0)

    def contains_center(self, other: "Detection") -> bool:
        other_x, other_y = other.center
        return self.x1 <= other_x <= self.x2 and self.y1 <= other_y <= self.y2


@dataclass
class WorkerAssessment:
    worker_id: int
    person_box: Detection
    has_helmet: bool
    has_vest: bool
    missing_items: List[str]
    violations: List[str]
    related_detections: List[Detection]


def _max_label_confidence(items: List[Detection], label: str) -> float:
    confidences = [item.confidence for item in items if item.label == label]
    return max(confidences, default=0.0)


def _nearest_person_for_item(item: Detection, persons: List[Detection]) -> Optional[Detection]:
    containing = [person for person in persons if person.contains_center(item)]
    candidates = containing or persons
    if not candidates:
        return None

    item_x, item_y = item.center

    def distance(person: Detection) -> float:
        person_x, person_y = person.center
        return (item_x - person_x) ** 2 + (item_y - person_y) ** 2

    return min(candidates, key=distance)


def analyze_ppe_compliance(detections: Iterable[Detection]) -> Dict[str, object]:
    detections = list(detections)
    persons = [detection for detection in detections if detection.label == PERSON_LABEL]
    gear = [detection for detection in detections if detection.label != PERSON_LABEL]
    vest_detection_count = sum(1 for detection in detections if detection.label == VEST_LABEL)
    no_vest_detection_count = sum(1 for detection in detections if detection.label == NO_VEST_LABEL)

    assignments: Dict[int, List[Detection]] = {index: [] for index in range(len(persons))}

    for item in gear:
        matched_person = _nearest_person_for_item(item, persons)
        if matched_person is None:
            continue
        person_index = persons.index(matched_person)
        assignments[person_index].append(item)

    worker_features = []

    for index, person in enumerate(persons):
        related = assignments[index]
        helmet_conf = _max_label_confidence(related, HELMET_LABEL)
        no_helmet_conf = _max_label_confidence(related, NO_HELMET_LABEL)
        vest_conf = _max_label_confidence(related, VEST_LABEL)
        no_vest_conf = _max_label_confidence(related, NO_VEST_LABEL)

        negative_helmet_active = no_helmet_conf >= MIN_NEGATIVE_CONFIDENCE
        negative_vest_active = no_vest_conf >= MIN_NEGATIVE_CONFIDENCE

        # Resolve conflicting labels by confidence: higher-confidence signal wins.
        has_helmet = helmet_conf > 0 and helmet_conf >= no_helmet_conf
        has_vest = vest_conf > 0 and vest_conf >= no_vest_conf

        worker_features.append(
            {
                "worker_id": index + 1,
                "person": person,
                "related": related,
                "helmet_conf": helmet_conf,
                "no_helmet_conf": no_helmet_conf,
                "vest_conf": vest_conf,
                "no_vest_conf": no_vest_conf,
                "negative_helmet_active": negative_helmet_active,
                "negative_vest_active": negative_vest_active,
                "has_helmet": has_helmet,
                "has_vest": has_vest,
            }
        )

    # Adaptive fallback: if scene has no-vest evidence, allow one no-evidence worker to be vest=Yes.
    # This helps when a vest box is missed for one worker in mixed-compliance scenes.
    if no_vest_detection_count > 0:
        no_evidence_workers = [
            idx
            for idx, info in enumerate(worker_features)
            if info["vest_conf"] == 0
            and info["no_vest_conf"] == 0
            and info["has_helmet"]
            and not info["has_vest"]
        ]
        if no_evidence_workers:
            chosen = max(no_evidence_workers, key=lambda idx: worker_features[idx]["helmet_conf"])
            worker_features[chosen]["has_vest"] = True

    max_allowed_vest_yes = vest_detection_count + (1 if no_vest_detection_count > 0 else 0)

    # Guardrail: workers marked as vest=Yes should not exceed the allowed positive vest evidence.
    workers_with_vest = [
        idx for idx, info in enumerate(worker_features) if info["has_vest"]
    ]
    if len(workers_with_vest) > max_allowed_vest_yes:
        ranked_workers = sorted(
            workers_with_vest,
            key=lambda idx: worker_features[idx]["vest_conf"],
            reverse=True,
        )
        allowed_workers = set(ranked_workers[:max_allowed_vest_yes])
        for idx in workers_with_vest:
            if idx not in allowed_workers:
                worker_features[idx]["has_vest"] = False

    worker_assessments: List[WorkerAssessment] = []
    compliant_workers = 0

    for info in worker_features:
        has_helmet = bool(info["has_helmet"])
        has_vest = bool(info["has_vest"])
        no_helmet_conf = float(info["no_helmet_conf"])
        helmet_conf = float(info["helmet_conf"])
        no_vest_conf = float(info["no_vest_conf"])
        vest_conf = float(info["vest_conf"])
        negative_helmet_active = bool(info["negative_helmet_active"])
        negative_vest_active = bool(info["negative_vest_active"])
        related = info["related"]

        missing_items: List[str] = []
        violations: List[str] = []

        if not has_helmet:
            missing_items.append(HELMET_LABEL)
        if not has_vest:
            missing_items.append(VEST_LABEL)
        if negative_helmet_active and no_helmet_conf > helmet_conf:
            violations.append(NO_HELMET_LABEL)
        if negative_vest_active and no_vest_conf > vest_conf:
            violations.append(NO_VEST_LABEL)

        if has_helmet and has_vest:
            compliant_workers += 1

        worker_assessments.append(
            WorkerAssessment(
                worker_id=int(info["worker_id"]),
                person_box=info["person"],
                has_helmet=has_helmet,
                has_vest=has_vest,
                missing_items=missing_items,
                violations=violations,
                related_detections=related,
            )
        )

    class_counts: Dict[str, int] = {}
    for detection in detections:
        class_counts[detection.label] = class_counts.get(detection.label, 0) + 1

    total_workers = len(persons)
    non_compliant_workers = total_workers - compliant_workers

    return {
        "class_counts": class_counts,
        "total_workers": total_workers,
        "compliant_workers": compliant_workers,
        "non_compliant_workers": non_compliant_workers,
        "worker_assessments": worker_assessments,
    }