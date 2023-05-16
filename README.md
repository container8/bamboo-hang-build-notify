# Bamboo Hanging Build Notifier

This app checks a build plan for hanging builds and sends a notification to webhook.
Hanging build is a build, which runs more than specified amount of time.

## Testing

Tested Bamboo version: 8.2.5, see API docs [here](https://docs.atlassian.com/atlassian-bamboo/REST/8.2.5/).

```
export BAMBOO_TOKEN=foo
BAMBOO_BASE_URL=https://ci.example.com
API_ENDPOINT_BASE=rest/api/latest

# Get all projects (pagination)

API_ENDPOINT=project
METHOD=GET

curl -H "Authorization: Bearer ${BAMBOO_TOKEN}" -X ${METHOD} ${BAMBOO_BASE_URL}/${API_ENDPOINT_BASE}/${API_ENDPOINT}.json | python -m json.tool

# Get single project

API_ENDPOINT=project/C8
METHOD=GET

curl -H "Authorization: Bearer ${BAMBOO_TOKEN}" -X ${METHOD} ${BAMBOO_BASE_URL}/${API_ENDPOINT_BASE}/${API_ENDPOINT}.json | python -m json.tool

# Get plan

API_ENDPOINT=plan/C8-RUN
METHOD=GET

curl -H "Authorization: Bearer ${BAMBOO_TOKEN}" -X ${METHOD} ${BAMBOO_BASE_URL}/${API_ENDPOINT_BASE}/${API_ENDPOINT}.json\&actions | python -m json.tool

# Get results

API_ENDPOINT=result/C8-RUN
METHOD=GET

curl -H "Authorization: Bearer ${BAMBOO_TOKEN}" -X ${METHOD} ${BAMBOO_BASE_URL}/${API_ENDPOINT_BASE}/${API_ENDPOINT}.json | python -m json.tool

# Get currently running jobs

API_ENDPOINT=result/C8-RUN
METHOD=GET

curl -H "Authorization: Bearer ${BAMBOO_TOKEN}" -X ${METHOD} ${BAMBOO_BASE_URL}/${API_ENDPOINT_BASE}/${API_ENDPOINT}.json\?includeAllStates=true\&lifeCycleState=InProgress | python -m json.tool

# Get details about a job

API_ENDPOINT=result/status/C8-RUN-2
METHOD=GET

curl -H "Authorization: Bearer ${BAMBOO_TOKEN}" -X ${METHOD} ${BAMBOO_BASE_URL}/${API_ENDPOINT_BASE}/${API_ENDPOINT}.json | python -m json.tool

# Get logs for a build

API_ENDPOINT=result/C8-RUN-2
METHOD=GET

curl -H "Authorization: Bearer ${BAMBOO_TOKEN}" -X ${METHOD} ${BAMBOO_BASE_URL}/${API_ENDPOINT_BASE}/${API_ENDPOINT}.json\?os_authType=basic\&expand=logEntries | python -m json.tool
```

## MS Teams Notifications

To send message to the MS Teams web hook use the following request:

```
export MS_TEAMS_WEB_HOOK_URL=https://webhook_url
curl -H 'Content-Type: application/json' -d '{"text": "Hello World"}' ${WEBHOOK_URL}
```

## Running Automated Tests

```
export BAMBOO_TOKEN=bamboo_token
export MS_TEAMS_WEB_HOOK_URL=https://webhook_url
make test
```

## Deployment

```
export BAMBOO_TOKEN=bamboo_token
export MS_TEAMS_WEB_HOOK_URL=https://webhook_url
export BAMBOO_BASE_URL=https://ci.example.com
export TF_VAR_hcloud_token=hcloud_token
export PLAN_KEYS_TO_WATCH=C8-ABC C8-DFG
export BUILD_TIMEOUT_THRESHOLD_SECONDS=60 120

make render-user-data
make deploy
```
