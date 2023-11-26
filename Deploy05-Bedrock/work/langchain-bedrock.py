from langchain.llms import Bedrock
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

llm = Bedrock(model_id="anthropic.claude-v2")

conversation = ConversationChain(
    llm=llm,
    verbose=True,
    memory=ConversationBufferMemory()
)

response = conversation.predict(input="日本語で自己紹介してください")

print(response)
