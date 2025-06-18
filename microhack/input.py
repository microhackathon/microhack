import time

from microhack.config import get_settings

import pathway as pw


class InfiniteStream(pw.io.python.ConnectorSubject):
    def run(self):
        while True:
            self.next_json({"value": 1})
            time.sleep(0.100)


def input():
    class InputSchema(pw.Schema):
        value: int

    format="json"

    if get_settings().input_connector == "kafka":
        rdkafka_settings = {
            "bootstrap.servers": get_settings().kafka_bootstrap_servers,
            "security.protocol": "plaintext",
            "group.id": get_settings().kafka_group_id,
            "session.timeout.ms": get_settings().kafka_session_timeout_ms,
        }
        return pw.io.kafka.read(
            rdkafka_settings,
            topic=get_settings().kafka_topic,
            schema=InputSchema,
            format=format,
            autocommit_duration_ms=get_settings().autocommit_duration_ms,
        )
    elif get_settings().input_connector == "python":
        return pw.io.python.read(
            InfiniteStream(),
            schema=InputSchema,
            format=format,
            autocommit_duration_ms=get_settings().autocommit_duration_ms,
        )
    elif get_settings().input_connector == "google_drive":
        from microhack.google_drive_connector import google_drive_input
        
        return google_drive_input(
            filename=get_settings().google_drive_filename,
            credentials_file=get_settings().google_drive_credentials_file,
            refresh_interval=get_settings().google_drive_refresh_interval,
            value_column=get_settings().google_drive_value_column
        )
