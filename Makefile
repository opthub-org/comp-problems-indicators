# Makefile

problem: test-problem build-problem push-problem

test-problem:
	echo Testing problem $(NAME)...
	pytest tests/opthub_problems/$(NAME)/

build-problem:
	echo Building problem $(NAME)...
	docker build --build-arg IMAGE_TYPE=problems --build-arg BENCHMARK_NAME=$(NAME) -t opthub/problem-$(NAME) .

push-problem:
	echo Pushing problem $(NAME)...
	docker push opthub/problem-$(NAME)

indicator: test-indicator-$(NAME) build-indicator-$(NAME) push-indicator-$(NAME)

test-indicator:
	echo Testing indicator $(NAME)...
	pytest tests/opthub_indicators/$(NAME)/

build-indicator:
	echo Building indicator $(NAME)...
	docker build --build-arg IMAGE_TYPE=indicators --build-arg BENCHMARK_NAME=$(NAME) -t opthub/indicator-$(NAME) .

push-indicator:
	echo Pushing indicator $(NAME)...
	docker push opthub/indicator-$(NAME)
