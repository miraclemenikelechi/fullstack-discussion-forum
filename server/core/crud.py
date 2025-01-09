from sqlmodel import select


def create(
    data,
    db,
    table,
):
    """
    Creates a new object in the database based on the provided data.

    Args:
        data (Any): The data used to create the new object.
        db (Session): The database session used for the operation.
        table (SQLModel): The SQLModel class representing the database table.

    Returns:
        Any: The created object, or None if an error occurred.
    """
    try:
        match data:
            case list() as data:
                created = [
                    item.dict() for item in data
                ]  # create a list of dictionaries
                db.bulk_insert_mappings(
                    table, created
                )  # bulk insert the list of dictionaries

            case _:
                created = table(
                    **data
                )  # create a new instance of the table class using the provided data

                db.add(created)  # add the new instance to the session

        db.commit()  # commit the transaction to save the new object in the database

        if not isinstance(data, list):
            db.refresh(created)  # refresh the created object to ensure it's up-to-date

    except Exception as error:
        db.rollback()  # roll back the transaction in case of an error
        raise error

    finally:  # ensure the database session is closed
        db.close()


def transact_by_param(
    db,
    table,
    arg=None,
    op=None,
    param=None,
    single=False,
):
    """
    Transact with the database based on the provided parameters.

    Args:
        db (Session): The database session used for executing the query.
        table (SQLModel): The SQLModel class representing the database table to query.
        arg (str, optional): The name of the attribute (column) in the database table used for filtering.
        op (str, optional): The comparison operation to use for filtering. Can be one of: "==", "!=", ">", "<", ">=", "<=".
        param (Any, optional): The value to filter by. If None, all records will be returned. Defaults to None.
        single (bool, optional): If True, returns a single object; otherwise, returns a list of objects. Defaults to True.

    Returns:
        Any or List[Any]: The read object(s), or None if an error occurred.
    """
    try:
        # If no filtering parameters are provided, return all records from the table
        if arg is None or op is None or param is None:
            statement = select(table)

        else:
            # mapping of filtering operations to SQLModel expressions
            FILTER_OPERATIONS: dict[str, any] = {
                "==": getattr(table, arg) == param,
                "!=": getattr(table, arg) != param,
                ">": getattr(table, arg) > param,
                "<": getattr(table, arg) < param,
                ">=": getattr(table, arg) >= param,
                "<=": getattr(table, arg) <= param,
            }

            # validate the provided operation
            if op not in FILTER_OPERATIONS.keys():
                raise Exception(f"invalid filter operation: {op}")

            # construct the SQL statement with the specified filter
            statement = select(table).where(FILTER_OPERATIONS[op])

        match single:  # execute the query based on the 'single' parameter
            case True:
                return db.exec(statement).first()
            case False:
                return db.exec(statement).all()

    except Exception as error:
        raise error

    finally:  # close the database session
        db.close()
