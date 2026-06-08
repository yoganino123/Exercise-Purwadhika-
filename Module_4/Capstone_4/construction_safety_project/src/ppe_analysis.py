from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Tuple


PERSON_LABEL = "person"
HELMET_LABEL = "helmet"
NO_HELMET_LABEL = "no-helmet"
VEST_LABEL = "vest"
NO_VEST_LABEL = "no-vest"


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

    assignments: Dict[int, List[Detection]] = {index: [] for index in range(len(persons))}

    for item in gear:
        matched_person = _nearest_person_for_item(item, persons)
        if matched_person is None:
            continue
        person_index = persons.index(matched_person)
        assignments[person_index].append(item)

    worker_assessments: List[WorkerAssessment] = []
    compliant_workers = 0

    for index, person in enumerate(persons):
        related = assignments[index]
        labels = [item.label for item in related]
        has_helmet = HELMET_LABEL in labels and NO_HELMET_LABEL not in labels
        has_vest = VEST_LABEL in labels and NO_VEST_LABEL not in labels

        missing_items: List[str] = []
        violations: List[str] = []

        if not has_helmet:
            missing_items.append(HELMET_LABEL)
        if not has_vest:
            missing_items.append(VEST_LABEL)
        if NO_HELMET_LABEL in labels:
            violations.append(NO_HELMET_LABEL)
        if NO_VEST_LABEL in labels:
            violations.append(NO_VEST_LABEL)

        if has_helmet and has_vest:
            compliant_workers += 1

        worker_assessments.append(
            WorkerAssessment(
                worker_id=index + 1,
                person_box=person,
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