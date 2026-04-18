from utils.model_loader import ModelLoader, ConfigLoader


config = ConfigLoader()
model = ModelLoader(config=config)
llm = model.load_llm()

response = llm.invoke("hi")
print(response.content)

