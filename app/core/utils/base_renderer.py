from rest_framework.renderers import JSONRenderer

from core.utils.base_response import (
  ErrorResponse,
  SuccessResponse,
)


class BaseRenderer(JSONRenderer):
    """
    Custom JSON renderer that wraps the response data in a consistent format.
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get('response')

        if isinstance(data, dict) and 'status' in data and 'data' in data:
            payload = data
        elif response and response.status_code >= 400:
            payload = ErrorResponse(
                errors=data,
                status=response.status_code
            ).to_dict()
        else:
            payload = SuccessResponse(data=data).to_dict()

        return super().render(payload, accepted_media_type, renderer_context)
