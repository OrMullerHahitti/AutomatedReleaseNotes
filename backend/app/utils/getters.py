
from typing import List

from azure_authentication_client import authenticate_openai
from langchain.chat_models import AzureChatOpenAI
from langchain.llms import OpenAI, HuggingFaceHub
from backend.app.models.models import LLMConfig

#TODO: re-write LLMConfig in models.py

def get_llm(config: LLMConfig):
    '''Initialize the LLM dynamically based on the configuration
    Args:
        config (LLMConfig): LLM configuration
        make sure the provider is openai if you want to use openai  '''
    if config.provider == "openai":
        api_key = authenticate_openai().api_key

        # OpenAI initialization
        return AzureChatOpenAI(deployment_name=config.model_name or "gpt-4o-deployment",
                               temperature=config.temperature,
                               api_key=api_key,
                               azure_endpoint='https://function-app-open-ai-prod-apim.azure-api.net/proxy-api/')

    elif config.provider == "huggingface":
        # HuggingFace initialization
        return HuggingFaceHub(
            repo_id=config.model_name or "google/flan-t5-large",
            model_kwargs={"temperature": config.temperature, "max_length": config.max_tokens},
            huggingfacehub_api_token=config.api_key
        )
    else:
        raise ValueError(f"Unsupported provider: {config.provider}")