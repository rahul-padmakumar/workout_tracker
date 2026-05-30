from rest_framework.exceptions import ErrorDetail


def ui_error(message: str, ui_msg_code: str = None):
    error_response = {'message': message}
    if ui_msg_code is not None:
        error_response['ui_msg_code'] = ui_msg_code
    return error_response


def flatten_errors(errors):
    if isinstance(errors, dict):
        flat = {}
        for key, value in errors.items():
            if isinstance(value, (dict, list)):
                flat[key] = flatten_errors(value)
            else:
                flat[key] = str(value)
        return flat
    elif isinstance(errors, list):
        if len(errors) == 1:
            return flatten_errors(errors[0])
        else:
            return [flatten_errors(item) for item in errors]
    elif isinstance(errors, ErrorDetail):
        print(f"ErrorDetail found: {errors}")
        return str(errors)
    else:
        return errors


def get_custom_error(errors):
    custom_error = errors.get('ui_msg_code', None)
    if custom_error and len(custom_error) > 0:
        return custom_error[0]
    return None
