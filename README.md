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

### Environment setup

1. Ensure pyenv is installed: `curl https://pyenv.run | bash`
2. Create Python Development Environment:
    - `pyenv update`
    - `pyenv install 3.8.6`
    - `pyenv virutalenv 3.8.6 ph2-apidocs`
    - `pyenv activate ph2-apidocs`
3. Install Development tools for python.
    - `pyenv activate ph2-apidocs`
    - `pip install --upgrade pip wheel poetry`
4. Install all requirements (dev and runtime):
    - `cd API-WS`
    - `poetry install`

#### VSCode Integration.

If using VSCode, the settings.json should be minimally set for python development as follows:

```json
{
    "python.pythonPath": "/home/<you>/.pyenv/versions/ph2-apidocs/bin/python",
    "python.formatting.provider": "black",
    "editor.formatOnSave": true,
    "python.linting.pylintEnabled": true,
    "[python]": {
        "editor.codeActionsOnSave": {
            "source.fixAll": true,
            "source.organizeImports": true
        }
    }
}
```

This points VSCode to the correct python environment, uses black and isort for code formatting and pylint for linting.