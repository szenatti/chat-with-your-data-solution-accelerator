import base64
import json
import logging
import os
from backend.batch.utilities.helpers.config.conversation_flow import ConversationFlow

logger = logging.getLogger(__name__)
encoded_account_key = str(base64.b64encode(b"some-blob-account-key"), "utf-8")


class AppConfig:
    before_config: dict[str, str] = {}
    config: dict[str, str | None] = {
        "APPLICATIONINSIGHTS_ENABLED": "False",
        "AZURE_AUTH_TYPE": "keys",
        "AZURE_BLOB_STORAGE_INFO": '{"accountName": "some-blob-account-name", "containerName": "some-blob-container-name", "accountKey": "'
        + encoded_account_key
        + '"}',
        "AZURE_COMPUTER_VISION_KEY": "some-computer-vision-key",
        "AZURE_CONTENT_SAFETY_ENDPOINT": "some-content-safety-endpoint",
        "AZURE_CONTENT_SAFETY_KEY": "some-content-safety-key",
        "AZURE_FORM_RECOGNIZER_ENDPOINT": "some-form-recognizer-endpoint",
        "AZURE_FORM_RECOGNIZER_INFO": '{"endpoint":"some-key-vault-endpoint","key":"some-key-vault-endpoint"}',
        "AZURE_OPENAI_API_KEY": "some-azure-openai-api-key",
        "AZURE_OPENAI_API_VERSION": "2024-02-01",
        "AZURE_OPENAI_EMBEDDING_MODEL_INFO": '{"model":"some-embedding-model","modelName":"some-embedding-model-name","modelVersion":"some-embedding-model-version"}',
        "AZURE_OPENAI_ENDPOINT": "some-openai-endpoint",
        "AZURE_OPENAI_MAX_TOKENS": "1000",
        "AZURE_OPENAI_MODEL_INFO": '{"model":"some-openai-model","modelName":"some-openai-model-name","modelVersion":"some-openai-model-version"}',
        "AZURE_OPENAI_VISION_MODEL": "some-openai-vision-model",
        "AZURE_OPENAI_RESOURCE": "some-openai-resource",
        "AZURE_OPENAI_STREAM": "True",
        "AZURE_OPENAI_STOP_SEQUENCE": "",
        "AZURE_OPENAI_SYSTEM_MESSAGE": "You are an AI assistant that helps people find information.",
        "AZURE_OPENAI_TEMPERATURE": "0",
        "AZURE_OPENAI_TOP_P": "1.0",
        "AZURE_RESOURCE_GROUP": "some-resource-group",
        "AZURE_SEARCH_CONVERSATIONS_LOG_INDEX": "some-log-index",
        "AZURE_SEARCH_CONTENT_COLUMN": "content",
        "AZURE_SEARCH_CONTENT_VECTOR_COLUMN": "some-search-content-vector-columns",
        "AZURE_SEARCH_DIMENSIONS": "some-search-dimensions",
        "AZURE_SEARCH_ENABLE_IN_DOMAIN": "True",
        "AZURE_SEARCH_FIELDS_ID": "some-search-fields-id",
        "AZURE_SEARCH_FIELDS_METADATA": "some-search-fields-metadata",
        "AZURE_SEARCH_FIELDS_TAG": "some-search-fields-tag",
        "AZURE_SEARCH_FILENAME_COLUMN": "filepath",
        "AZURE_SEARCH_FILTER": "some-search-filter",
        "AZURE_SEARCH_INDEX": "some-azure-search-index",
        "AZURE_SEARCH_INDEX_IS_PRECHUNKED": "some-azure-search-index-is-prechunked",
        "AZURE_SEARCH_KEY": "some-azure-search-key",
        "AZURE_SEARCH_SERVICE": "some-azure-search-service",
        "AZURE_SEARCH_SEMANTIC_SEARCH_CONFIG": "some-search-semantic-search-config",
        "AZURE_SEARCH_TITLE_COLUMN": "title",
        "AZURE_SEARCH_CHUNK_COLUMN": "chunk",
        "AZURE_SEARCH_SOURCE_COLUMN": "source",
        "AZURE_SEARCH_OFFSET_COLUMN": "offset",
        "AZURE_SEARCH_TOP_K": "5",
        "AZURE_SEARCH_URL_COLUMN": "url",
        "AZURE_SEARCH_USE_INTEGRATED_VECTORIZATION": "False",
        "AZURE_SEARCH_INDEXER_NAME": "some-azure-search-indexer-name",
        "AZURE_SEARCH_DATASOURCE_NAME": "some-azure-search-datasource-name",
        "AZURE_SEARCH_USE_SEMANTIC_SEARCH": "False",
        "AZURE_SPEECH_REGION_ENDPOINT": "some-speech-region-endpoint",
        "AZURE_SPEECH_SERVICE_KEY": "some-azure-speech-service-key",
        "AZURE_SPEECH_SERVICE_NAME": "some-speech-service-name",
        "AZURE_SPEECH_SERVICE_REGION": "some-azure-speech-service-region",
        "AZURE_SUBSCRIPTION_ID": "some-subscription-id",
        "BACKEND_URL": "some-backend-url",
        "DOCUMENT_PROCESSING_QUEUE_NAME": "some-document-processing-queue-name",
        "FUNCTION_KEY": "some-function-key",
        "LOAD_CONFIG_FROM_BLOB_STORAGE": "True",
        "LOGLEVEL": "DEBUG",
        "ORCHESTRATION_STRATEGY": "openai_function",
        "CONVERSATION_FLOW": ConversationFlow.CUSTOM.value,
        "AZURE_SPEECH_RECOGNIZER_LANGUAGES": "en-US,es-ES",
        "TIKTOKEN_CACHE_DIR": f"{os.path.dirname(os.path.realpath(__file__))}/resources",
        "USE_ADVANCED_IMAGE_PROCESSING": "False",
        "ADVANCED_IMAGE_PROCESSING_MAX_IMAGES": "1",
        "USE_KEY_VAULT": "False",
        # These values are set directly within EnvHelper, adding them here ensures
        # that they are removed from the environment when remove_from_environment() runs
        "OPENAI_API_TYPE": None,
        "OPENAI_API_KEY": None,
        "OPENAI_API_VERSION": None,
        "DATABASE_TYPE": "CosmosDB",
    }

    def __init__(self, config_overrides: dict[str, str | None] = {}) -> None:
        self.config = self.config | config_overrides

    def set(self, key: str, value: str | None) -> None:
        self.config[key] = value

    def get(self, key: str) -> str | None:
        return self.config[key]

    def get_from_json(self, config_key: str, field: str) -> str | None:
        config_json = json.loads(self.config[config_key])
        return config_json.get(field)

    def get_all(self) -> dict[str, str | None]:
        return self.config

    def apply_to_environment(self) -> None:
        for key, value in self.config.items():
            current_config = os.environ.get(key)
            if current_config is not None:
                self.before_config[key] = current_config

            if value is not None:
                logger.info(f"Applying env var: {key}={value}")
                os.environ[key] = value
            else:
                logger.info(f"Removing env var: {key}")
                os.environ.pop(key, None)

    def remove_from_environment(self) -> None:
        for key in self.config.keys():
            if key in self.before_config:
                logger.info(f"Resetting env var: {key}")
                os.environ[key] = self.before_config[key]
            else:
                logger.info(f"Removing env var: {key}")
                os.environ.pop(key, None)
