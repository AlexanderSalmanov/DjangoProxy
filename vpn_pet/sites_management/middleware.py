import sys


class DataSentMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if hasattr(response, "content"):
            # NOTE: we keep track of the data sent within a single interaction;
            # so that we don't incrementally update it with each request
            sent_data_size = sys.getsizeof(response.content)
            request.session.setdefault("site_data_sent", {"sent_data": 0})
            request.session["site_data_sent"]["sent_data"] = sent_data_size

        return response
