import time
import json
import datetime


class Utils:

    REJECTED_LOG_EVENTS = 'rejectedLogEventsInfo'

    TOO_OLD_REJECTED_REASON = 'tooOld'

    TOO_NEW_REJECTED_REASON = 'tooNew'

    @staticmethod
    def get_stream_name() -> str:
        """
        :return:
        """
        return str(int(time.time())) + "_test_stream"

    @staticmethod
    def create_cloudwatch_events(url: str = None, method='POST', http_error_code: int = 200, total: int = 10) -> list:
        """
        :param url:
        :param method:
        :param http_error_code:
        :param total:
        :return:
        """
        events = list()
        event = {'timestamp': None, 'message': None}
        message = f"{method} {url} HTTP/1.1 {http_error_code} - -"
        from_now = int(datetime.datetime.now().timestamp() * 1000)
        entry = {'log': message}
        for i in range(total):
            event['timestamp'] = from_now
            event["message"] = json.dumps(entry)
            from_now += 1
            events.append(event)

        return events