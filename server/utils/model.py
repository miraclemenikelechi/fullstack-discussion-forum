from typing import Any

from sqlmodel import Relationship, SQLModel


def serialize_model(
    table_instance: SQLModel = None,
    exclude: dict[str, bool | dict] | set[str] = None,
    include: dict[str, bool | dict] = None,
    depth: int = 1,
):
    """
    Serialize a SQLModel instance into a dictionary, allowing for nested relationships and field exclusion.

    Args:
        table_instance: The SQLModel instance to serialize.
        exclude: A set of field names to exclude from the serialized output, or a dictionary of field
            names to boolean values indicating whether to exclude the field. If a dictionary is provided,
            the boolean value can also be a dictionary of nested field names to exclude.
        include: A dictionary of field names to boolean values indicating whether to include the field
            in the serialized output. If a boolean value is `True`, the field will be included, and if
            it is a dictionary, the dictionary will be used to recursively serialize the field.
        depth: The maximum depth of nested relationships to serialize. Defaults to 1.

    Returns:
        A dictionary containing the serialized data.
    """

    if table_instance is None or depth < 0:
        return None

    if exclude is None:
        exclude = set()

    if include is None:
        include = dict()

    _exclude_as_dict: dict | set[str] = dict() if isinstance(exclude, dict) else exclude

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

        if _should_include:
            _nested_include = (
                _should_include if isinstance(_should_include, dict) else dict()
            )

            _nested_exclude = (
                exclude.get(_relation, dict()) if isinstance(exclude, dict) else dict()
            )

            if isinstance(_data, list):
                _model[_relation] = (
                    [
                        serialize_model(
                            table_instance=table,
                            exclude=_nested_exclude,
                            include=_nested_include,
                            depth=depth - 1,
                        )
                        for table in _data
                    ]
                    if _data
                    else list()
                )

            elif _data is not None:
                _model[_relation] = serialize_model(
                    table_instance=_data,
                    exclude=_nested_exclude,
                    include=_nested_include,
                    depth=depth - 1,
                )

            else:
                _relation_attr_type = getattr(type(table_instance), _relation, None)

                _model[_relation] = (
                    list()
                    if isinstance(_relation_attr_type, Relationship)
                    and _relation_attr_type.is_list
                    else None
                )

    return dict(sorted(_model.items()))
