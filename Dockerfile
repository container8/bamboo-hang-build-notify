FROM --platform=amd64 python:3.9-bullseye

COPY . /src

WORKDIR /src

RUN pip install -r requirements.txt

ENV BAMBOO_TOKEN bamboo_token_replace
ENV BAMBOO_BASE_URL https://ci.example.com
ENV API_ENDPOINT_BASE rest/api/latest
ENV BUILD_TIMEOUT_THRESHOLD_SECONDS 3600
ENV MS_TEAMS_WEB_HOOK_URL web_hook_url_replace
ENV NOTIFICATION_INTERVAL_SECONDS 300
ENV PLAN_KEY_TO_WATCH C8-RUN

CMD ["python", "/src/bamboohbn/main.py"]
