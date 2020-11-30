# Standard Library
import json

# Local
from .http import Http400


def get_draggable_items(request, json_field="items"):
    """Used with drag AJAX views, returns list of PKs"""
    try:
        return [int(item) for item in json.loads(request.body)[json_field]]
    except (json.JSONDecodeError, KeyError):
        raise Http400(f"Invalid JSON payload, must contain {json_field}")


def sort_draggable_items(request, queryset, fields=None, start=1, json_field="items"):
    """Handles bulk sorting of draggable items."""
    items = queryset.in_bulk()
    for_update = []
    for position, item_id in enumerate(get_draggable_items(request, json_field), start):
        item = items.get(item_id)
        if item:
            yield position, item
            for_update.append(item)

    queryset.bulk_update(for_update, fields or [])
