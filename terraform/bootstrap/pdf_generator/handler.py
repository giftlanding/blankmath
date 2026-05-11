import json


def handler(event, context):
    return {
        "statusCode": 503,
        "headers": {
            "content-type": "application/json",
        },
        "body": json.dumps({
            "error": "backend_not_deployed",
            "message": "The Blankmath PDF generator has not been deployed yet.",
        }),
    }
