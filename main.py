import click
from src.Logs import CloudwatchLogs
from src.Validations import Validations
from src.Utils import Utils


@click.command()
@click.option('--profile', required=False, default='default', type=str)
@click.option('--log-group-name', required=True, type=str)
@click.option('--log-stream-name', required=False, type=str, default='')
@click.option('--event-url', type=str, required=False, default='/de-eec-subscription/oauth2/token')
@click.option('--event-method', type=str, required=False, default='POST', callback=Validations.validate_event_method)
@click.option('--event-status-code', type=int, required=False, default=500)
@click.option('--total-events', type=int, required=False, callback=Validations.validate_total_events, default=10)
def main(profile=None, log_group_name=None, log_stream_name=None, event_url=None, event_method=None,
         event_status_code=None, total_events=None):

    profile = profile.strip()
    log_group_name = log_group_name.strip()
    log_stream_name = log_stream_name.strip()
    event_url = event_url.strip()

    try:

        if not total_events > 0:
            raise Exception('Argument total events cannot less than 0')

        logs = CloudwatchLogs(profile_name=profile)

        events = Utils.create_cloudwatch_events(url=event_url, method=event_method, http_error_code=event_status_code, total=total_events)

        is_empty_argument_log_stream_name = len(log_stream_name) == 0

        if is_empty_argument_log_stream_name:

            log_stream_name = Utils.get_stream_name()

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
