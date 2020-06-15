#!/usr/bin/env bash

# Generate the Websocket API from source

cd API-WS
poetry run ws_api make-docs
cd ..
