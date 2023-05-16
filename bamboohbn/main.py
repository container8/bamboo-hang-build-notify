# https://docs.atlassian.com/atlassian-bamboo/REST/8.2.5/

import os
import json
import time

import requests

BAMBOO_TOKEN = os.environ.get("BAMBOO_TOKEN", "")
BAMBOO_BASE_URL = os.environ.get("BAMBOO_BASE_URL", "https://ci.example.com")
API_ENDPOINT_BASE = os.environ.get("API_ENDPOINT_BASE", "rest/api/latest")
API_ENDPOINT = f"{BAMBOO_BASE_URL}/{API_ENDPOINT_BASE}"
BUILD_TIMEOUT_THRESHOLD_SECONDS = int(os.environ.get("BUILD_TIMEOUT_THRESHOLD_SECONDS", 3600))
MS_TEAMS_WEB_HOOK_URL = os.environ.get("MS_TEAMS_WEB_HOOK_URL", "")
NOTIFICATION_INTERVAL_SECONDS = int(os.environ.get("NOTIFICATION_INTERVAL_SECONDS", 300))
PLAN_KEY_TO_WATCH = os.environ.get("PLAN_KEY_TO_WATCH", "ALICE-RUN")

######################
# Bamboo API Methods #
######################

def get_running_builds(plan_key: str) -> list:
    method = "GET"
    api_action = f"result/{plan_key}"
    params = {"includeAllStates": "true", "lifeCycleState": "InProgress"}
    api_response = api_request(method, api_action, params)
    if len(api_response["results"]["result"]) > 0:
        return api_response["results"]["result"]
    else:
        return []

def show_build(plan_key: str, build_number: str) -> dict:
    method = "GET"
    api_action = f"result/status/{plan_key}-{build_number}"
    api_response = api_request(method, api_action)
    api_response_status_code = api_response.get('status-code', 200)
    if api_response_status_code != 404:
        return api_response
    else:
        return {}

def get_builds_running_longer_than(plan_key: str, time_threshold_seconds: int) -> list:
    running_builds = get_running_builds(plan_key)
    hanging_builds = []
    for build in running_builds:
        build_details = show_build(plan_key, build['buildNumber'])
        build_time_ms = build_details['progress']['buildTime']
        build_time_seconds = build_time_ms / 1000
        if build_time_seconds > time_threshold_seconds:
            hanging_builds.append(build_details)
    return hanging_builds

def api_request(method: str, api_action: str, params: dict = {}) -> dict:
    request_url = f"{API_ENDPOINT}/{api_action}.json"
    headers = {"Authorization": f"Bearer {BAMBOO_TOKEN}"}
    response = requests.request(method, request_url, headers=headers, params=params)
    return response.json()

##########################
# MS Teams Notifications #
##########################

def notify_ms_teams_about_hanging_builds(plan_key: str, web_hook_url: str = MS_TEAMS_WEB_HOOK_URL):
    hanging_builds = get_builds_running_longer_than(plan_key, BUILD_TIMEOUT_THRESHOLD_SECONDS)
    messages = []
    initial_message = f"""Bamboo plan {plan_key} has {len(hanging_builds)} hanging builds (running over {BUILD_TIMEOUT_THRESHOLD_SECONDS / 60} minutes).
    Navigate to the plan: {BAMBOO_BASE_URL}/browse/{plan_key}.<br><br>"""
    messages.append(initial_message)
    if len(hanging_builds) > 0:
        for hanging_build in hanging_builds:
            message = f"""The build {hanging_build['key']} is hanging since {hanging_build['progress']['startedTime']}.
            To restart the build follow this URL: {BAMBOO_BASE_URL}/browse/{hanging_build['key']}<br>"""
            messages.append(message)
        message_to_send = "\n".join(messages)
        send_ms_teams_notification(web_hook_url, message_to_send)

def send_ms_teams_notification(web_hook_url: str, message: str):
    headers = {"Content-Type": "application/json"}
    data = {"text": message}
    requests.post(web_hook_url, headers=headers, data=json.dumps(data))

if __name__ == "__main__":
    while True:
        print(f"Checking {BAMBOO_BASE_URL} bamboo server, plan key {PLAN_KEY_TO_WATCH} for hanging builds")
        notify_ms_teams_about_hanging_builds(PLAN_KEY_TO_WATCH, MS_TEAMS_WEB_HOOK_URL)
        print(f"Sleeping for {NOTIFICATION_INTERVAL_SECONDS} seconds until next check.")
        time.sleep(NOTIFICATION_INTERVAL_SECONDS)
