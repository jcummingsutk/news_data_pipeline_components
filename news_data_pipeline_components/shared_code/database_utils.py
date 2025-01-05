from datetime import datetime

from mongoengine import Document
from mongoengine.queryset.queryset import QuerySet


def get_max_date_by_source_name(doc_class: Document, source_name: str) -> datetime:
    result = doc_class.objects(source_name=source_name).aggregate(
        [{"$group": {"_id": None, "max_date": {"$max": "$date"}}}]
    )
    max_date = next(result, {}).get("max_date")
    if max_date is not None:
        return max_date
    return datetime(year=1900, month=1, day=1)


def get_entries_above_date(
    doc_class: Document,
    source_name: str,
    date_dt: datetime,
) -> QuerySet:
    return doc_class.objects(source_name=source_name, date__gt=date_dt)
