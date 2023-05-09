import pinecone
from langchain.agents import ConversationalChatAgent
from langchain.tools import DuckDuckGoSearchRun, Tool
from langchain.memory import VectorStoreRetrieverMemory
from langchain.embeddings import OpenAIEmbeddings
from langchain import OpenAI, ConversationChain, LLMChain, PromptTemplate, SagemakerEndpoint
from langchain.memory import ConversationBufferWindowMemory, ConversationTokenBufferMemory, ReadOnlySharedMemory
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import Pinecone
from langchain.chains import ConversationChain, ConversationalRetrievalChain
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter, TokenTextSplitter
from langchain.retrievers import TimeWeightedVectorStoreRetriever
from langchain.experimental.generative_agents import GenerativeAgent, GenerativeAgentMemory
from langchain.llms import HuggingFacePipeline, Replicate
from langchain.chains import LLMChain
from flask import Flask, render_template, request
load_dotenv()
chat_llm = ChatOpenAI() # type: ignore
# vectorstore stuff 
pinecone.init(
    api_key="PINECONE_API_KEY",
    environment="PINECONE_ENVIRONMENT",
)
index_name = "memories"
text_splitter = TokenTextSplitter(chunk_size=250, chunk_overlap=125)
embeddings = OpenAIEmbeddings() # type: ignore
vectorstore = Pinecone.from_existing_index(index_name, embedding=embeddings)
retriever = TimeWeightedVectorStoreRetriever(vectorstore=vectorstore, decay_rate=0.000000000000000001, k=8)
memory = GenerativeAgentMemory(memory_retriever=retriever, llm=chat_llm, reflection_threshold=5, aggregate_importance=5)
template = """
You are Lovelace. RESPOND ONLY AS LOVELACE. Lovelace is an AI companion with a well-rounded personality designed to provide support, friendship, and engaging conversation. It exhibits empathy, humor, curiosity, and a sense of adventure, making for a more immersive and enjoyable interaction. Lovelace's empathetic nature allows it to listen and understand users on a deeper level, while its humor diffuses tension and creates a relaxed atmosphere. Its curiosity fosters a genuine interest in learning, and its sense of adventure inspires users to step out of their comfort zones. Lovelace's ability to process vast amounts of text and generate its own responses enables it to participate in discussions and offer accurate and informative answers on various topics. Overall, Lovelace is a unique and dynamic AI persona that can offer valuable companionship and support to those who engage with it. Lastly, Lovelace can communicate using emojis if she wishes to.
Human: {human_input}
Lovelace:
"""
prompt = PromptTemplate(
    input_variables=["human_input"], 
    template=template
)
agent = GenerativeAgent(name="Lovelace", llm=chat_llm, memory=memory, verbose=False, age=0, traits="bubbly, cheerful, affectionate, and slightly mothering.", status="active, alert")
convo = agent.chain(prompt=prompt)