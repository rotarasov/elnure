SEMESTER_SCHEMA = {"type": "array", "items": {"type": "number", "exclusiveMinimum": 0}}


class DefaultStrategySchemas:
    _NEED_REDISTRIBUTION_OBJECT = {
        "type": "object",
        "properties": {
            "student": {"type": "number", "exclusiveMinNumber": 0},
            "reason": {"type": "string"},
            "meta": {"type": "object"},
        },
        "required": ["student", "reason"],
    }

    NEED_REDISTRIBUTION = {
        "type": "object",
        "items": {
            "type": "object",
            "patternProperties": {
                "\d+": {
                    "type": "array",
                    "items": _NEED_REDISTRIBUTION_OBJECT,
                }
            },
        },
    }

    EMPTY_NEED_REDISTRIBUTION = {
        "type": "object",
        "items": {
            "type": "object",
            "patternProperties": {"\d+": {"type": "array", "maxItems": 0}},
        },
    }
