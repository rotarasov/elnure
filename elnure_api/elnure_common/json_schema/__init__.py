import jsonschema

from elnure_common.json_schema.schemas import *


def validate_schema(instance, schema, exc_cls=None, exc_msg=None) -> str:
    """Validating json schema and raising custom error if given"""
    try:
        jsonschema.validate(instance, schema)
    except jsonschema.ValidationError as init_exc:
        if not exc_cls and not exc_msg:
            raise

        if not exc_cls:
            exc_cls = jsonschema.ValidationError
        if not exc_msg:
            exc_msg = init_exc.message
        raise exc_cls(exc_msg)
