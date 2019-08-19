from django.conf import settings

from rest_framework import status

from apps.sender.slack import SlackHandler


class LoggingMixin(object):

    allowed_logging_methods = ('post', 'put', 'patch', 'delete')

    def finalize_response(self, request, response, *args, **kwargs):

        print('[Request]')
        print('- url : {}'.format(request.get_full_path()))
        print('- method : {}'.format(request.method.upper()))
        print('- headers : {}'.format(request.META.get('HTTP_AUTHORIZATION')))
        print('- data : {}'.format(str(request.data)))

        response = super().finalize_response(request, response, *args, **kwargs)
        status_code = response.status_code

        print('[Response]')
        print('- status code : {}'.format(status_code))

        if request.method.lower() not in self.allowed_logging_methods:
            return response

        print('- data : {}'.format(str(response.data)))

        try:
            if status.is_server_error(status_code):
                SlackHandler.send_api_error_alarm(request=request, response=response, message='Error From Server')
            # if status.is_client_error(status_code):
            #     SlackHandler.send_api_error_alarm(request=request, response=response, message='Error From Client')
        except Exception as e:
            print('[Slack Message ERROR]')
            print(e)
        return response