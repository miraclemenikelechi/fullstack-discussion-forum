from typing import Any

from sqlmodel import SQLModel


def serialize_model(
    table_instance: SQLModel = None,
    exclude: set[str] = None,
    include: dict[str, bool] = None,
    depth: int = 1,
):
    if table_instance is None:
        return None

    if exclude is None:
        exclude = set()

    if include is None:
        include = dict()

    model: dict[str, Any] = table_instance.model_dump(exclude=exclude, mode="json")

    if depth <= 0:
        return model

    for relation, should_include in include.items():
        if not should_include:
            continue

        data = getattr(table_instance, relation, None)

        if isinstance(data, list):
            model[relation] = [
                serialize_model(
                    table_instance=table,
                    exclude=exclude,
                    include=include,
                    depth=depth - 1,
                )
                for table in data
            ]

        elif data is not None:
            model[relation] = serialize_model(
                table_instance=data, exclude=exclude, include=include, depth=depth - 1
            )

    return model
