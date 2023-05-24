ifeq ($(USE_DOT_ENV),true) 
	include .env
endif

publish_prefix := xalt
image_name := bamboo-hanging-builds-notifier
# In a normal scenario using the "latest" tag to build and publish image with a production application deployment
# (not a crutch for CI tooling) is not the best practice
# As we are deploying on the latest version of an application on a single VM, this is sufficient
image_tag := latest

test:
	pytest -s ./tests

docker-test:
	docker build -t bamboohbn:${image_tag} .
	docker run -it \
	-e "BAMBOO_TOKEN=${BAMBOO_TOKEN}" \
	-e "BAMBOO_BASE_URL=${BAMBOO_BASE_URL}" \
	-e "MS_TEAMS_WEB_HOOK_URL=${MS_TEAMS_WEB_HOOK_URL}"
	bamboohbn:${image_tag}

publish-image:
	docker build -t $(publish_prefix)/$(image_name):$(image_tag) .
	docker push $(publish_prefix)/$(image_name):$(image_tag)

TF_DIR := deployment/terraform
TF_RUN=terraform -chdir=${TF_DIR}
TF_PLAN_FILE=apply.tfplan

COUNT := $(words $(PLAN_KEYS_TO_WATCH))
SEQUENCE := $(shell seq 1 $(COUNT))
render-user-data:
	rm -f ${TF_DIR}/.user_data.sh
	cat ${TF_DIR}/user_data_init.sh >> ${TF_DIR}/.user_data.sh
	$(foreach var,$(SEQUENCE),\
	export PLAN_KEY_TO_WATCH=$(word $(var), $(PLAN_KEYS_TO_WATCH)) && \
	export BUILD_TIMEOUT_THRESHOLD_SECONDS=$(word $(var), $(BUILD_TIMEOUT_THRESHOLD_SECONDS_LIST)) && \
	cat ${TF_DIR}/user_data_docker_run.sh | envsubst >> ${TF_DIR}/.user_data.sh;)

tf-init:
	$(TF_RUN) init -reconfigure \
		-backend-config="bucket=${BUCKET_NAME}" \
		-backend-config="region=${AWS_DEFAULT_REGION}" \
		-backend-config="key=${BUCKET_KEY}"	

tf-plan: tf-init render-user-data
	$(TF_RUN) plan \
		-var-file=../environment/main.tfvars \
		-out=${TF_PLAN_FILE}

deploy: tf-plan
	$(TF_RUN) apply ${TF_PLAN_FILE}

tf-destroy:
	$(TF_RUN) plan -destroy -var-file=../environment/main.tfvars -out=${TF_PLAN_FILE}
	$(TF_RUN) apply ${TF_PLAN_FILE}
