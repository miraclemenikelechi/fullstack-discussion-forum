# from typing import Any

# from sqlmodel import SQLModel


# def serialize_model(
#     table_instance: SQLModel = None,
#     # exclude: set[str] = None,
#     # include: dict[str, bool] = None,
#     exclude: dict[str, bool | dict] | set[str] = None,
#     include: dict[str, bool | dict] = None,
#     depth: int = 1,
# ):
#     if table_instance is None or depth < 0:
#         return None

#     if exclude is None:
#         # exclude = set()
#         exclude = dict()

#     if include is None:
#         include = dict()

#     # model: dict[str, Any] = table_instance.model_dump(exclude=exclude, mode="json")
#     _model: dict[str, Any] = table_instance.model_dump(
#         # exclude=set(k for k, v in exclude.items() if isinstance(v, bool) and v),
#         exclude=set(exclude) if isinstance(exclude, set) else set(),
#         mode="json",
#     )

#     if depth <= 0:
#         return _model

#     for _relation, _should_include in include.items():
#         # if not should_include:
#         #     continue

#         _data = getattr(table_instance, _relation, None)

#         if _should_include and _data:
#             _nested_include = (
#                 _should_include if isinstance(_should_include, dict) else dict()
#             )

#             _nested_exclude = exclude.get(_relation, dict())

#             if isinstance(_data, list):
#                 _model[_relation] = [
#                     serialize_model(
#                         table_instance=table,
#                         exclude=_nested_exclude,
#                         include=_nested_include,
#                         depth=depth - 1,
#                     )
#                     for table in _data
#                 ]

#             elif _data is not None:
#                 _model[_relation] = serialize_model(
#                     table_instance=_data,
#                     exclude=_nested_exclude,
#                     include=_nested_include,
#                     depth=depth - 1,
#                 )

#     return _model

from typing import Any, Union
from sqlmodel import SQLModel


def serialize_model(
    table_instance: SQLModel = None,
    exclude: Union[set[str], dict[str, bool | dict]] = None,
    include: dict[str, bool | dict] = None,
    depth: int = 1,
):
    if table_instance is None or depth < 0:
        return None

    if exclude is None:
        exclude = set()

    if include is None:
        include = dict()

    # Handle set-based exclusion (this will directly exclude fields at the top level)
    _exclude_set = set(exclude) if isinstance(exclude, set) else set()
    _exclude_dict = {} if isinstance(exclude, dict) else exclude

    # Initialize the model, using the exclude set to exclude top-level fields
    _model: dict[str, Any] = table_instance.model_dump(
        exclude=_exclude_set, mode="json"
    )

    # Exclude fields based on the dict exclusion logic
    if isinstance(_exclude_dict, dict):
        for field, should_exclude in _exclude_dict.items():
            if should_exclude:
                _model.pop(field, None)  # Remove excluded fields

    # Process nested relationships based on include/exclude logic
    for _relation, _should_include in include.items():
        _data = getattr(table_instance, _relation, None)

        if _should_include and _data:
            _nested_include = (
                _should_include if isinstance(_should_include, dict) else dict()
            )

            _nested_exclude = (
                exclude.get(_relation, dict()) if isinstance(exclude, dict) else {}
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

            else:
                _model[_relation] = serialize_model(
                    table_instance=_data,
                    exclude=_nested_exclude,
                    include=_nested_include,
                    depth=depth - 1,
                )

    return _model
