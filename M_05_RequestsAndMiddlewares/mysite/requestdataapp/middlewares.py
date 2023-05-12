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
        if not self.request_time:
            print('Fist request')
        else:
            if (round(time.time()) * 1) - self.request_time['time'] < time_limit and \
                    self.request_time['ip'] == request.META.get('REMOTE_ADDR'):
                print('Attention! Service request limit exceeded. Less than 3 seconds have passed')
                return render(request, 'requestdataapp/error-time.html')
        self.request_time = {'time': round(time.time()) * 1, 'ip': request.META.get('REMOTE_ADDR')}

        self.requests_count += 1
        print('requests count', self.requests_count)

        response = self.get_response(request)
        self.responses_count += 1
        print('responses count', self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print('got', self.exceptions_count, 'exceptions so far')
