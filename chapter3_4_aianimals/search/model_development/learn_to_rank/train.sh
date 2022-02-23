#!/bin/sh

set -eu

docker run \
    -it \
    --rm \
    --name test \
    --network aianimals \
    -v $(pwd)/outputs:/opt/outputs/ \
    -e LEARN_TO_RANK_CONFIG=learn_to_rank_lightgbm_regression \
    -e POSTGRES_USER=postgres \
    -e POSTGRES_PASSWORD=password \
    -e POSTGRES_PORT=5432 \
    -e POSTGRES_DB=aianimals \
    -e POSTGRES_HOST=postgres \
    shibui/building-ml-system:ai_animals_search_learn_to_rank_train_0.0.0 \
    python -m src.main
