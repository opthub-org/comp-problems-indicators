# Makefile

.PHONY: sphere


sphere: build-sphere deploy-sphere

build-sphere:
	docker build --build-arg BENCHMARK_NAME=sphere -t opthub/problem-sphere .

deploy-sphere:
	docker push opthub/problem-sphere

