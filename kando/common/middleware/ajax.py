class AjaxRequestFragmentMiddleware:
    """Checks for the X-Request-Fragment header passed in AJAX query,
    and sets boolean attribute request.is_ajax_fragment
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.is_ajax_fragment = (
            request.is_ajax() and "X-Request-Fragment" in request.headers
        )
        return self.get_response(request)
