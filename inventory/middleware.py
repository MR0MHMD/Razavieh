from django.http import Http404


class InventorySuperuserOnlyMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        # بررسی اینکه آدرس مربوط به اپ اینونتوری هست یا نه
        if path.startswith('/inventory/'):
            if not request.user.is_authenticated or not request.user.is_superuser:
                raise Http404("Page not found")

        response = self.get_response(request)
        return response
