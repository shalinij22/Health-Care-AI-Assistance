from langchain.chat_models import ChatOpenAI
from langchain_community.llms import Ollama
from langchain.prompts import ChatPromptTemplate
from langchain.embeddings import OllamaEmbeddings

llm = Ollama(model="llama2")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "you are a teacher for AI and ML"),
        ("human", "What is the difference between AI and ML?")
    ]
)

response = prompt | llm
print(response)
