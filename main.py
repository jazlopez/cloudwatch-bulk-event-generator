#
#
#
import json
import time
import click
import datetime
from src.Logs import CloudwatchLogs


def get_stream_name() -> str:

    """
    :return:
    """
    return str(int(time.time())) + "_test_stream"


def create_cloudwatch_events(url: str = None, http_error_code: int = None, total: int = None) -> list:

    """
    :param url:
    :param http_error_code:
    :param total:
    :return:
    """
    events = list()
    event = {'timestamp': None, 'message': None}
    message = f"POST {url} HTTP/1.1 {http_error_code} - -"
    from_now = int(datetime.datetime.now().timestamp() * 1000)
    entry = {'log': message}
    for i in range(total):
        event['timestamp'] = from_now
        event["message"] = json.dumps(entry)
        from_now += 1
        events.append(event)

    return events


@click.command()
@click.option('--profile', required=False, default='default', type=str)
@click.option('--log-group-name', required=True, type=str)
@click.option('--log-stream-name', required=False, type=str, default='')
@click.option('--event-url', type=str, required=False, default='/de-eec-subscription/oauth2/token')
@click.option('--event-status-code', type=int, required=False, default=500)
@click.option('--total-events', type=int, required=False, default=10)
def main(profile=None, log_group_name=None, log_stream_name=None, event_url=None, event_status_code=None, total_events=None):

    profile = profile.strip()
    log_group_name = log_group_name.strip()
    log_stream_name = log_stream_name.strip()
    event_url = event_url.strip()

    try:

        if not total_events > 0:
            raise Exception('Argument total events cannot less than 0')

        logs = CloudwatchLogs(profile_name=profile)

        events = create_cloudwatch_events(url=event_url, http_error_code=event_status_code, total=total_events)

        is_empty_argument_log_stream_name = len(log_stream_name) == 0

        if is_empty_argument_log_stream_name:

            log_stream_name = get_stream_name()

            logs.create_log_stream(log_group_name=log_group_name, log_stream_name=log_stream_name)

            response = logs.put_log_events(log_group_name=log_group_name,
                                           log_stream_name=log_stream_name,
                                           events=events)
        else:

            sequence_token = logs.get_upload_token(log_group_name=log_group_name, log_stream_name=log_stream_name)

            response = logs.put_log_events_with_token(log_group_name=log_group_name,
                                                      log_stream_name=log_stream_name,
                                                      events=events,
                                                      sequence_token=sequence_token)

        if 'rejectedLogEventsInfo' in response:

            output = "Unable to write logs: payload contains events that could not be created in stream logs "
            errors = [errors for errors in response['rejectedLogEventsInfo']]

            for error in errors:

                if 'tooOld' in error:
                    output += '(Too old events found in payload)'

                if 'tooNew' in error:
                    output += '(Events in future found in payload)'

            raise Exception(output)

        click.secho(f"[OK] Written {total_events} events into specified log: {log_group_name}/{log_stream_name}")
        click.secho("[OK] Bye now....")
        print(events)

    except Exception as e:
        click.secho("[ERROR] {e}".format(e=e))


if __name__ == '__main__':
    main()
