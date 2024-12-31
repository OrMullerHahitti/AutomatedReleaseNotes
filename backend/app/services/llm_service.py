from azure_authentication_client import authenticate_openai
from fastapi import FastAPI, HTTPException
from langchain.chat_models import AzureChatOpenAI
from pydantic import BaseModel, Field
from langchain.llms import OpenAI, HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Initialize FastAPI app
app = FastAPI()

# Define the configuration model
class LLMConfig(BaseModel):
    provider: str = Field(..., description="LLM provider, e.g., 'openai' or 'huggingface'")
    model_name: str = Field(default=None, description="Model name for the selected provider")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0, description="Randomness of the output")
    max_tokens: int = Field(default=256, ge=1, description="Maximum number of tokens in output")
    api_key: str = Field(..., description="API key for the selected LLM provider")

class QueryRequest(BaseModel):
    prompt: str
    config: LLMConfig

# Function to initialize the LLM dynamically
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

