from typing import Any, List
from functools import reduce


def get_nested_value(doc: dict, dotted_key: str) -> Any:
    """
    Extrait une valeur depuis un document avec la notation pointee
    """
    keys = dotted_key.split(".")
    try:
        return reduce(lambda d, k: d[k] if isinstance(d, dict) else None, keys, doc)
    except (KeyError, TypeError):
        return None


def set_nested_value(result: dict, dotted_key: str, value: Any) -> None:
    """
    Insere une valeur dans un dict en reconstruisant la hierarchie
    """
    keys = dotted_key.split(".")
    current = result
    for key in keys[:-1]:
        if key not in current:
            current[key] = {}
        current = current[key]
    current[keys[-1]] = value


def apply_template(deal: dict, template: dict) -> dict:
    """
    Applique un template sur un deal complet
    """
    visible_fields: List[str] = template.get("visibleFields", [])
    labels: dict = template.get("labels", {})
    sections: list = template.get("sections", [])

    # Extraction uniquement des champs autorises
    projected_data = {}
    for field in visible_fields:
        value = get_nested_value(deal, field)
        if value is not None:
            set_nested_value(projected_data, field, value)

    # Construction des labels
    rendered_sections = []
    for section in sections:
        section_fields = []
        for field in section.get("fields", []):
            if field in visible_fields:
                section_fields.append({
                    "key": field,
                    "label": labels.get(field, field),
                    "value": get_nested_value(deal, field),
                })
        rendered_sections.append({
            "name": section.get("name"),
            "fields": section_fields,
        })

    return {
        "dealId": deal.get("_id", ""),
        "templateName": template.get("name"),
        "templateCode": template.get("code"),
        "sections": rendered_sections,
    }