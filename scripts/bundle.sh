#!/usr/bin/env bash

cd API
openapi bundle PH2-API.oas3.yml -o PH2-API.oas3.json
openapi bundle PH2-API-BrowserExtension.oas3.yml -o PH2-API-BrowserExtension.oas3.json
cd ..
