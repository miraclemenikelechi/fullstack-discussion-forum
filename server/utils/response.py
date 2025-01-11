from datetime import datetime
from typing import Any

from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from core.constants import STATUS_CODE


class ResponseDataModel(BaseModel):
    data: Any = None
    message: str
    status_code: int
    timestamp: datetime


class ResponseApiModel(BaseModel):
    response_data: ResponseDataModel
    status_code: int
    success: bool


class ResponseAPI:
    """
    A class to standardize API responses in a FastAPI application.

    This class provides a structured way to create both successful and error responses,
    encapsulating common response attributes such as timestamp, status code, message,
    and data. It leverages FastAPI's `JSONResponse` for successful responses and
    `HTTPException` for error responses.

    Attributes:
        response_data (dict): A dictionary containing the response data.
        status_code (int): The HTTP status code for the response.
        success (bool): Indicates whether the response is successful or an error.
    """

    def __init__(
        self,
        additional_data=None,
        data=None,
        message=None,
        status_code=None,
        success=None,
    ):
        """
        Initializes an instance of the ResponseAPI class.

        Args:
            additional_data (dict, optional): Additional data to include in the response.
            data (any, optional): The main data payload for the response.
            message (str, optional): A message describing the response.
            status_code (int, optional): The HTTP status code for the response.
            success (bool, optional): Indicates if the response is successful. Defaults to None, which will be treated as False.
        """
        self.response_data = {
            "timestamp": datetime.now().isoformat(),
            "status_code": status_code,
            "message": message,
            "data": data,
        }

        if additional_data:
            self.response_data.update(additional_data)

        self.status_code = status_code
        self.success = False if success is None else success

    def is_success(self):
        """
        Creates a JSONResponse for a successful operation.

        Returns:
            JSONResponse: A FastAPI JSONResponse object with the response data.

        Raises:
            Exception: If an error occurs while creating the JSONResponse.
        """
        try:
            return JSONResponse(
                content=self.response_data, status_code=STATUS_CODE[self.status_code]
            )

        except Exception as error:
            raise error

    def is_error(self):
        """
        Creates an HTTPException for an error operation.

        Returns:
            HTTPException: A FastAPI HTTPException object with the error details.

        Raises:
            Exception: If an error occurs while creating the HTTPException.
        """
        try:
            return HTTPException(
                status_code=STATUS_CODE[self.status_code], detail=self.response_data
            )

        except Exception as error:
            raise error

    def response(self):
        """
        Returns the appropriate response based on the success attribute.

        If success is True, it returns a successful JSONResponse.
        If success is False, it raises an HTTPException.

        Returns:
            JSONResponse or raises HTTPException: The appropriate response based on success.

        Raises:
            HTTPException: If success is False and an error occurs.
            Exception: If any other error occurs during processing.
        """
        try:
            match self.success:
                case True:
                    return self.is_success()

                case False:
                    raise self.is_error()

        except HTTPException as error:
            raise error

        except Exception as error:
            raise error
