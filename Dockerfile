FROM python:3.12.1-slim

ARG BENCHMARK_NAME

RUN echo "BENCHMARK_NAME is set to ${BENCHMARK_NAME}"

# 必要なパッケージのインストールとキャッシュのクリア
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Poetryのインストール
RUN pip install poetry

# Poetryのパス設定
ENV PATH="/root/.local/bin:${PATH}"

# 作業ディレクトリの設定
WORKDIR /usr/src/app

# 依存関係ファイルを先にコピー
COPY pyproject.toml poetry.lock* ./


# アプリケーションコードをコピー
COPY . /usr/src/app

ENV BENCHMARK_NAME=${BENCHMARK_NAME}

# 依存関係のインストール
RUN poetry install

# エントリーポイントの設定
CMD ["sh", "-c", "poetry run python ./problem_opt_benchmarks/$BENCHMARK_NAME/main.py"]
