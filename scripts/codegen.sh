#!/usr/bin/env bash
./scripts/bundle.sh

docker run --user $(id -u):$(id -g) --rm -v \
    $PWD:/local openapitools/openapi-generator-cli generate \
    -i /local/API/PH2-API.oas3.json \
    -g python-aiohttp \
    -o /local/out/python-aiohttp

