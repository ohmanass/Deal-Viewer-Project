from bson import ObjectId

def serialize_doc(doc: dict) -> dict:
    """Convertit les ObjectId en string pour la serialisation JSON."""
    if doc is None:
        return None
    result = {}
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            result[key] = str(value)
        elif isinstance(value, dict):
            result[key] = serialize_doc(value)
        elif isinstance(value, list):
            result[key] = [
                serialize_doc(item) if isinstance(item, dict) else
                str(item) if isinstance(item, ObjectId) else item
                for item in value
            ]
        else:
            result[key] = value
    return result


def to_object_id(id_str: str) -> ObjectId:
    """Convertit un string en ObjectId, leve ValueError si invalide."""
    try:
        return ObjectId(id_str)
    except Exception:
        raise ValueError(f"Invalid ID : '{id_str}'")





