import os


class RequestValidator:
    ALLOWED_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"}
    ALLOWED_CONTENT_TYPES = {
        "application/json",
        "application/x-www-form-urlencoded",
        "multipart/form-data",
        "text/plain",
        "text/html",
    }
    ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.csv', '.zip'}

    def validate_method(self, method):
        return method.upper() in self.ALLOWED_METHODS

    def validate_content_type(self, request):
        content_type = request.META.get("CONTENT_TYPE", "").split(";")[0].strip()
        if content_type and content_type not in self.ALLOWED_CONTENT_TYPES:
            return False
        return True

    def validate_file_upload(self, request):
        if request.method.upper() != "POST" and request.method.upper() != "PUT" and request.method.upper() != "PATCH":
            return True

        if not request.FILES:
            return True

        for field_name, file in request.FILES.items():
            ext = os.path.splitext(file.name)[1].lower()
            if ext not in self.ALLOWED_EXTENSIONS:
                return False
            if file.size > 10 * 1024 * 1024:
                return False

        return True
