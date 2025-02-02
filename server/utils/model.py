from typing import Any

from sqlmodel import SQLModel


def serialize_model(
    table_instance: SQLModel = None,
    exclude: dict[str, bool | dict] | set[str] = None,
    include: dict[str, bool | dict] = None,
    depth: int = 1,
):
    if table_instance is None or depth < 0:
        return None

    if exclude is None:
        exclude = set()

    if include is None:
        include = dict()

    _exclude_as_dict = dict() if isinstance(exclude, dict) else exclude

    _model: dict[str, Any] = table_instance.model_dump(
        exclude=(set(exclude) if isinstance(exclude, set) else set()),
        mode="json",
    )

    if isinstance(_exclude_as_dict, dict):
        for _field, _should_exclude in _exclude_as_dict.items():
            if _should_exclude:
                _model.pop(_field, None)

    for _relation, _should_include in include.items():
        _data = getattr(table_instance, _relation, None)

        if _should_include and _data:
            _nested_include = (
                _should_include if isinstance(_should_include, dict) else dict()
            )

            _nested_exclude = (
                exclude.get(_relation, dict()) if isinstance(exclude, dict) else dict()
            )

            if isinstance(_data, list):
                _model[_relation] = [
                    serialize_model(
                        table_instance=table,
                        exclude=_nested_exclude,
                        include=_nested_include,
                        depth=depth - 1,
                    )
                    for table in _data
                ]

            elif _data is not None:
                _model[_relation] = serialize_model(
                    table_instance=_data,
                    exclude=_nested_exclude,
                    include=_nested_include,
                    depth=depth - 1,
                )

    return dict(sorted(_model.items()))
