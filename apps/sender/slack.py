class SlackHandler(object):

    @classmethod
    def send_api_error_alarm(cls, request=None, response=None, traceback=None, message=None):
        slack_message = '> *MoveDot API ERROR* \n\n'

        try:
            if request:
                slack_message += '*url* : {}\n\n'.format(request.get_full_path())
                slack_message += '*request* \n'
                slack_message += '- method : {}\n'.format(str(request.method))
                slack_message += '- headers : {}\n'.format(request.META.get('HTTP_AUTHORIZATION'))
                slack_message += '- content type : {}\n'.format(request.content_type)

            if response:
                slack_message += '*response* \n'
                slack_message += '- status : {}\n'.format(response.status_code)
                slack_message += '- data : ```\n{}```\n'.format(str(response.data))

            if message:
                slack_message += '*message* \n'
                slack_message += '```\n{}```'.format(str(message))

            if traceback:
                slack_message += '*traceback* \n'
                slack_message += '```\n{}```'.format(str(traceback))

        except Exception as error:
            slack_message = '```\n{}```'.format(repr(error))

        # async_send_slack_error_channel.delay(slack_message)