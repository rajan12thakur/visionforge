from typing import Any


def validate_yolo_annotation(
    content: str,
    num_classes: int,
) -> dict[str, Any]:
    """
    Validate YOLO-format annotation text.

    Expected format per non-empty line:
    class_id x_center y_center width height
    """
    errors: list[dict[str, Any]] = []
    valid_annotations = 0
    total_lines = 0

    if num_classes <= 0:
        return {
            "is_valid": False,
            "total_lines": 0,
            "valid_annotations": 0,
            "errors": [
                {
                    "line": None,
                    "code": "invalid_num_classes",
                    "message": "num_classes must be greater than zero.",
                }
            ],
        }

    for line_number, raw_line in enumerate(content.splitlines(), start=1):
        line = raw_line.strip()

        if not line:
            continue

        total_lines += 1
        parts = line.split()

        if len(parts) != 5:
            errors.append(
                {
                    "line": line_number,
                    "code": "invalid_column_count",
                    "message": "Expected exactly five values per annotation.",
                }
            )
            continue

        try:
            class_id = int(parts[0])
            x_center, y_center, width, height = map(float, parts[1:])
        except ValueError:
            errors.append(
                {
                    "line": line_number,
                    "code": "invalid_numeric_value",
                    "message": "Class ID must be an integer and coordinates must be numeric.",
                }
            )
            continue

        if not 0 <= class_id < num_classes:
            errors.append(
                {
                    "line": line_number,
                    "code": "invalid_class_id",
                    "message": (
                        f"Class ID must be between 0 and {num_classes - 1}."
                    ),
                }
            )
            continue

        coordinates = {
            "x_center": x_center,
            "y_center": y_center,
            "width": width,
            "height": height,
        }

        invalid_coordinate = False

        for name, value in coordinates.items():
            if not 0 <= value <= 1:
                errors.append(
                    {
                        "line": line_number,
                        "code": "coordinate_out_of_range",
                        "message": f"{name} must be between 0 and 1.",
                    }
                )
                invalid_coordinate = True

        if invalid_coordinate:
            continue

        if width == 0 or height == 0:
            errors.append(
                {
                    "line": line_number,
                    "code": "zero_area_box",
                    "message": "Bounding-box width and height must be greater than zero.",
                }
            )
            continue

        if x_center - width / 2 < 0 or x_center + width / 2 > 1:
            errors.append(
                {
                    "line": line_number,
                    "code": "bounding_box_out_of_bounds",
                    "message": "Bounding box extends beyond the image horizontally.",
                }
            )
            continue

        if y_center - height / 2 < 0 or y_center + height / 2 > 1:
            errors.append(
                {
                    "line": line_number,
                    "code": "bounding_box_out_of_bounds",
                    "message": "Bounding box extends beyond the image vertically.",
                }
            )
            continue

        valid_annotations += 1

    return {
        "is_valid": len(errors) == 0,
        "total_lines": total_lines,
        "valid_annotations": valid_annotations,
        "invalid_annotations": total_lines - valid_annotations,
        "errors": errors,
    }