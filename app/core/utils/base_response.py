from email import message
from rest_framework.response import Response as Res
from rest_framework import status


class BaseResponse(Res):
    def __init__(
            self,
            success: bool,
            data: dict = None,
            errors: dict = None,
            status_code: int = 200,
            **kwargs):
        self.success = success
        self.data = data
        self.errors = errors
        self.status_code = status_code

        response_data = self.to_dict()
        super().__init__(data=response_data, status=status_code, **kwargs)

    def to_dict(self):
        response = {
            "success": self.success,
            "data": self.data,
            "errors": self.errors,
        }
        return response


class SuccessResponse(BaseResponse):
    def __init__(self, message: str = None, data: dict = None, **kwargs):
        super().__init__(
            success=True,
            data=data,
            **kwargs,
            status_code=status.HTTP_200_OK)


class ErrorResponse(BaseResponse):
    def __init__(
            self,
            errors: dict = None,
            status_code: int = 400,
            **kwargs):
        super().__init__(
            success=False,
            errors=errors,
            status_code=status_code,
            **kwargs
        )
