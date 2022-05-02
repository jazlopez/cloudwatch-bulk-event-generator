
from typing import Any
from boto3.session import Session


class CloudwatchLogs:

    """
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
