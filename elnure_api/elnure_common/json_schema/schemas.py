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
        "additionalProperties": False,
    }

    NEED_REDISTRIBUTION = {
        "type": "object",
        "patternProperties": {
            r"\d+": {
                "type": "array",
                "items": _NEED_REDISTRIBUTION_OBJECT,
            }
        },
        "additionalProperties": False,
    }

    EMPTY_NEED_REDISTRIBUTION = {
        "type": "object",
        "patternProperties": {r"\d+": {"type": "array", "maxItems": 0}},
        "additionalProperties": False,
    }

    RESULT = {
        "type": "object",
        "patternProperties": {
            r"\d+": {
                "type": "object",
                "patternProperties": {
                    r"\d+": {
                        "type": "object",
                        "patternProperties": {
                            r"ПЗПІ\[[а-яА-ЯіІїЇєЄa-zA-Z]+\]-\d+-\d+": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "email": {"type": "string"},
                                        "academic_group": {"type": "string"},
                                    },
                                    "required": ["email", "academic_group"],
                                    "additionalProperties": False,
                                },
                            }
                        },
                        "additionalProperties": False,
                    }
                },
                "additionalProperties": False,
            }
        },
        "additionalProperties": False,
    }
