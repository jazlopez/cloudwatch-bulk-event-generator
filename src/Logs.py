
from typing import Any
from boto3.session import Session


class CloudwatchLogs:

    """
    Note: per boto3 spec you should be aware of the following limitations:
        - The maximum batch size is 1,048,576 bytes. This size is calculated as the sum of all event messages in UTF-8,
        - plus 26 bytes for each log event.
        - None of the log events in the batch can be more than 2 hours in the future.
        - None of the log events in the batch can be older than 14 days or older than the retention period of the log group.
        - A batch of log events in a single request cannot span more than 24 hours. Otherwise, the operation fails.
        - The maximum number of log events in a batch is 10,000.
    """

    _client: Any = None

    def __init__(self, profile_name=None):

        self._client = Session(profile_name=profile_name).client('logs')

    def create_log_stream(self, log_group_name=None, log_stream_name=None):

        self._client.createe_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)

    def get_upload_token(self, log_group_name=None, log_stream_name=None):

        props = self._client.describe_log_streams(logGroupName=log_group_name, logStreamNamePrefix=log_stream_name)

        return props['logStreams'][0]['uploadSequenceToken']

    def put_log_events(self, log_group_name=None, log_stream_name=None, events=None):

        return self._client.put_log_events(logGroupName=log_group_name, logStreamName=log_stream_name,logEvents=events)

    def put_log_events_with_token(self, log_group_name=None, log_stream_name=None, events=None, sequence_token=None):

        return self._client.put_log_events(logGroupName=log_group_name, logStreamName=log_stream_name,
                                           logEvents=events,sequenceToken=sequence_token)
