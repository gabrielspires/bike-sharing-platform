import logging
from datetime import datetime
from zoneinfo import ZoneInfo

from decouple import config
from opensearchpy import OpenSearch

from .base import TIME_ZONE

OPENSEARCH_HOST = config("OPENSEARCH_HOST", default="localhost")
OPENSEARCH_PORT = int(config("OPENSEARCH_PORT", default=9200))
OPENSEARCH_PASSWORD = config("OPENSEARCH_INITIAL_ADMIN_PASSWORD", default="admin")


opensearch_client = OpenSearch(
    hosts=[{"host": OPENSEARCH_HOST, "port": OPENSEARCH_PORT}],
    use_ssl=False,
    verify_certs=False,
)


class OpenSearchLogHandler(logging.Handler):
    def emit(self, record):
        try:
            if record.name.startswith("opensearch"):
                print(f"[OpenSearch-Client-Internal] {record.getMessage()}\n")
                return

            log_data = {
                "timestamp": datetime.now(tz=ZoneInfo(TIME_ZONE)).isoformat(),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
                "module": record.module,
                "funcName": record.funcName,
                "lineNo": record.lineno,
            }
            # Append extra properties if needed (via extra={})
            if hasattr(record, "extra_data"):
                log_data.update(record.extra_data)

            index_name = f"bike-sharing-{datetime.now(tz=ZoneInfo(TIME_ZONE)).strftime('%Y-%m-%d')}"

            opensearch_client.index(index=index_name, body=log_data)
        except Exception as e:  # noqa: BLE001
            print(f"CRITICAL: Failed to ship log to OpenSearch. Error: {e}\n")
