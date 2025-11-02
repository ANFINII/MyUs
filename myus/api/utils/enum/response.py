from enum import Enum


class ApiResponse(Enum):
    UNAUTHORIZED = (True, "Un Authorized", 401)
    NOT_FOUND = (True, "Not Found", 404)

    def run(self) -> dict[str, str | bool | int]:
        is_error, content, status_code = self.value
        return {"error": is_error, "message": content, "status_code": status_code}
