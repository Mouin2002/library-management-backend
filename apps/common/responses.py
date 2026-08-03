from rest_framework.response import Response


def success_response(
    data=None,
    message="Request successful.",
    status_code=200,
):
    response_data = {
        "success": True,
        "message": message,
    }

    if data is not None:
        response_data["data"] = data

    return Response(
        response_data,
        status=status_code,
    )