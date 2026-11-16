import json
import logging
import os
from datetime import datetime, timedelta, timezone

logger = logging.getLogger()
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))


def handler(event, context):
    """Minimal AWS Lambda entry point. Real pipeline logic is added later."""
    logger.info("Lambda invoked with event: %s", event)

    now_utc = datetime.now(timezone.utc)
    now_wib = now_utc.astimezone(timezone(timedelta(hours=7)))

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "Hello from AWS Lambda Docker!",
                "event": event,
                "utc_time": now_utc.isoformat(),
                "wib_time": now_wib.isoformat(),
            }
        ),
    }
