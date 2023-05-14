import time
from django.http import HttpRequest
from django.shortcuts import render


def set_useragent_onrequest_middleware(get_response):
    print('initial call')

    def middleware(request: HttpRequest):
        print('before get response')
        request.user_agent = request.META['HTTP_USER_AGENT']
        response = get_response(request)
        return response
    return middleware


class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.request_time = {}
        self.responses_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        time_limit = 3
        user_key = request.META.get('REMOTE_ADDR')

        if user_key not in self.request_time:
            print('New IP!')
            self.request_time = ({user_key: (round(time.time()) * 1)})
            print('test:', self.request_time)

        try:
            print('Now in first-part try', 'ip:', user_key, 'last-time:', self.request_time[user_key])
            if (round(time.time()) * 1) - self.request_time[user_key] >= time_limit:
                self.request_time = ({user_key: (round(time.time()) * 1)})
                print('add new last-time for user:', user_key, self.request_time[user_key])
            else:
                return render(request, 'requestdataapp/error-time.html')

        except PermissionError:
            print('Now in second-part block-try')
            raise PermissionError('Time-limit!')

        self.requests_count += 1
        print('requests count', self.requests_count)

        response = self.get_response(request)
        self.responses_count += 1
        print('responses count', self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print('got', self.exceptions_count, 'exceptions so far')
