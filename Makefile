KAFKA_CONTAINER_NAME := $(shell docker ps --filter name=kafka --format "{{.Names}}" | head -n1)
TOPIC := currencies

kafka_check_topic:
	@if [ -z "$$(docker exec $(KAFKA_CONTAINER_NAME) kafka-topics --bootstrap-server kafka:9092 --list | grep -w $(TOPIC))" ]; then \
		echo "ERROR: Topic '$(TOPIC)' does not exist!"; \
		exit 1; \
	fi

kafka_create_topic:
	docker exec $(KAFKA_CONTAINER_NAME) kafka-topics \
	--create --topic $(TOPIC) --bootstrap-server kafka:9092 --partitions 3 --replication-factor 1

kafka_write_topic:kafka_check_topic
	docker exec -i $(KAFKA_CONTAINER_NAME) kafka-console-producer \
	--broker-list kafka:9092 --topic $(TOPIC) \
	--property "parse.key=true" --property "key.separator=:"

kafka_read_topic:kafka_check_topic
	docker exec -it $(KAFKA_CONTAINER_NAME) kafka-console-consumer \
	--bootstrap-server kafka:9092 --topic $(TOPIC) --from-beginning \
	--property print.key=true --property key.separator=: