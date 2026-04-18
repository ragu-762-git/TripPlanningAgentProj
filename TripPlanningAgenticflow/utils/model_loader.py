from .config_loader import load_config
from pydantic import BaseModel, Field
from typing import Literal, Optional, Any
import os 
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

class ConfigLoader :
    """load configurations once and access it """
    def __init__(self):
        print("loading config...")
        self.config = load_config() # dict of key value pairs streaming from the config file 

    "this method allows to access the value by the object created from the class (obj[key]=value)"
    def __getitem__(self, key):
        return self.config[key]

class ModelLoader(BaseModel):
    """get inputs from config and build a model"""
    #without Basemodel we would have used def__init__(self) and defined model provider, user would have entered anything
    model_provider: Literal["openrouter"]="openrouter" 
    config:Optional[ConfigLoader] =  Field(default=None, exclude=True)

    class Config:
        arbitrary_types_allowed = True

    def load_llm(self):
        """
        load and return the model
        """
        if self.config is None:
            raise ValueError("config file not found")
        
        print(f"loading model from provider{self.model_provider}")

        if self.model_provider == "openrouter":
            openrouter_api_key = os.getenv("API_KEY")
            model_name = self.config["llm"]["openrouter"]["model_name"]
            base_url = self.config["llm"]["openrouter"]["base_url"]
            llm = ChatOpenAI(model=model_name, api_key=openrouter_api_key, base_url=base_url)
    
        return llm


