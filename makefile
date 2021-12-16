validate:
	rasa data validate

train: validate
	rasa train

run-rasa-server: train
	rasa run \
		--enable-api \
		-vv \
		--cors "*"

run-action-server:
	python -m debugpy \
		--listen 0.0.0.0:5678 \
		-m rasa_sdk \
		--actions actions \
		--auto-reload \
		--debug

run-bot:
	docker-compose up -d

build-kg: run-bot
	docker-compose exec -- knowledge-base ./typedb console --script=/tmp/kb/create_kb.tql

build: build-kg

clean:
	docker-compose down


