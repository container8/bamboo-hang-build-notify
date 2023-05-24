
docker run -d \
    --name bamboo-hanging-builds-notifier-${PLAN_KEY_TO_WATCH} \
    --restart always \
    -e "BAMBOO_TOKEN=${BAMBOO_TOKEN}" \
    -e "BAMBOO_BASE_URL=${BAMBOO_BASE_URL}" \
    -e "MS_TEAMS_WEB_HOOK_URL=${MS_TEAMS_WEB_HOOK_URL}" \
    -e "PLAN_KEY_TO_WATCH=${PLAN_KEY_TO_WATCH}" \
    -e "BUILD_TIMEOUT_THRESHOLD_SECONDS=${BUILD_TIMEOUT_THRESHOLD_SECONDS}" \
    xalt/bamboo-hanging-builds-notifier:latest
