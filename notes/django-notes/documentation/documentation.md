### Docs in DRF

- DRF Spectacular: tool that creates OpenAPI schema (yaml file) which is accepted by Swagger UI

## Installation

In requirements.txt specify drf-spectacular>=0.20.0,<0.21 and build docker image

# Changes in Settings.py

- Under installed Apps add below
  'rest_framework',
  'drf_spectacular',

- Then below also:
  REST_FRAMEWORK = {
  'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
  }

# Changes in Urls.py

- import from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
- Add below in urlpatterns list
  - path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
  - path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),

## To see api doc:

visit localhost:8080/api/docs

#### File format of schema is also added in this folder
