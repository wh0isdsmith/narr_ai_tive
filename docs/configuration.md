# Configuration Guide

## Configuration File

The main configuration file is `config.yaml`. Here is an example configuration:

```yaml
api:
  batch_size: 10
  rate_limit: 10
embedding:
  chunk_size: 5000
  model: models/embedding-001
generation:
  temperature: 0.7
  model: models/gemini-exp-1206
```

## Secrets File

The `secrets.yaml` file contains sensitive information such as API keys. Make sure to add your Google API key for Gemini access.

```yaml
google_api_key: "YOUR_GOOGLE_API_KEY"
```

## Customizing Configuration

You can customize various parameters in the `config.yaml` file to suit your needs. For example, you can change the `temperature` parameter to control the creativity of the generated content.

Refer to the documentation for each parameter to understand its impact on the generation process.
