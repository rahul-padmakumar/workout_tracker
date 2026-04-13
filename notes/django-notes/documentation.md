### Docs in DRF

- DRF Spectacular: tool that creates OpenAPI schema (yaml file) which is accepted by Swagger UI

# Installation

In requirements.txt specify drf-spectacular>=0.20.0,<0.21 and build docker image

# Changes in Settings.py

- Under installed Apps add below
  'rest_framework',
  'drf_spectacular',

- Then below also:
  REST_FRAMEWORK = {
  'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
  }
