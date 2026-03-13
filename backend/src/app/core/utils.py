from bson import ObjectId 

def serialize_doc(doc: dict) -> dict:
    """Convertit les ObjectId en string pour la serialisation vers JSON"""
    if doc is None:
        return None

    result = {}
    for key, value in doc.items():
        if isinstance(value, ObjectId):
            result[key] = str(value)
        elif isinstance(value, dict):
            result[key] = serialize_doc(value)
        elif isinstance(value, list):
            serialized_list = []
            for item in value:
                if isinstance(item, dict):
                    serialized_list.append(serialize_doc(item))
                elif isinstance(item, ObjectId):
                    serialized_list.append(str(item))
                else:
                    serialized_list.append(item)
            result[key] = serialized_list
        else:
            result[key] = value
    return result

def to_object_id(id_str: str) -> ObjectId:
    """Convertit un string en ObjectId et renvoie ValueError si invalide"""
    try:
        return ObjectId(id_str)
    except Exception:
        raise ValueError(f"Invalid ID : '{id_str}'")