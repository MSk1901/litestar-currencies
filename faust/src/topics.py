from src.app import faust_app

request_topic = faust_app.topic("request.audit")
warning_topic = faust_app.topic("request.audit.warning")
