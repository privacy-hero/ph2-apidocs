#!/usr/bin/env bash
./scripts/bundle.sh

#docker run --user $(id -u):$(id -g) --rm -v ${PWD}:/local swaggerapi/swagger-codegen-cli-v3 generate \
#    -i /local/API/PH2-API.oas3.json \
#    -l python \
#    -o /local/out/python-swagger

docker pull openapitools/openapi-generator-cli

rm -rf out/python-openapi

docker run --user $(id -u):$(id -g) --rm -v \
    $PWD:/local openapitools/openapi-generator-cli generate \
    -i /local/API/PH2-API.oas3.json \
    -g python \
    -o /local/out/python-openapi

