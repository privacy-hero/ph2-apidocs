# ph2-apidocs

PrivacyHero2 API Documentation

The REST API is Documented using
**[OpenAPI3 (OAS3)](https://spec.openapis.org/oas/v3.0.3)**.

The Websocket API is Documented using **[AsyncAPI2](https://www.asyncapi.com)**

Flow diagrams are written using **[mermaid](https://mermaid-js.github.io/mermaid/)**

Tools Needed:

* [REDOCLY OpenAPI3 CLI](https://github.com/Redocly/openapi-cli)
* [Python Poetry](https://python-poetry.org/)
* [pyenv](https://github.com/pyenv/pyenv)
* [jsonlint](https://github.com/zaach/jsonlint)
* [AsyncAPI Generator](https://github.com/asyncapi/generator)
* [AsyncAPI Parser](https://github.com/asyncapi/parser-js)
* [Docker](https://www.docker.com)

## Websocket API

In order to simplify the creation of the AsyncAPI document, it is created using
a self executing python template.
