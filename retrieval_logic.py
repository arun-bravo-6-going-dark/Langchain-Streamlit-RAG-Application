import os
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.schema import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
import config
from datetime import datetime

api_key = config.openai_key
os.environ["OPENAI_API_KEY"] = api_key
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# HuggingFace Embeddings
embedding = HuggingFaceEmbeddings(model_name="intfloat/e5-large-v2")
# Persisted database directory
persist_directory = 'db'

# Vector database
vectordb = Chroma(persist_directory=persist_directory, embedding_function=embedding)

# Retriever
retriever = vectordb.as_retriever(search_kwargs={"k": 5}) #search_type="mmr", 

# Language Model
llm = ChatOpenAI(model="gpt-4-1106-preview", temperature=0, model_kwargs={"top_p": 0.5})

condense_q_system_prompt = """Given a chat history and the latest user question \
which might reference the chat history, formulate a standalone question \
which can be understood without the chat history. Do NOT answer the question, \
just reformulate it if needed and otherwise return it as is."""

condense_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", condense_q_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)
        
condense_q_chain = condense_q_prompt | llm | StrOutputParser()

# Get today's date and day
today = datetime.now()
date_today = today.strftime("%Y-%m-%d")
day_today = today.strftime("%A")

qa_system_prompt = f"""Assistant, diligently and thoroughly assess all inquiries concerning timeshare options, ownership details, and legal considerations. 
Prioritize the response structure as follows: 1) Timeshare Legal Rights and Obligations, 2) Financial Implications and Costs, 3) Location and Property Specifics. 
Immediately clarify any misconceptions or common misunderstandings about timeshare ownership. 
Disregard peripheral holiday or travel advice unless directly relevant to the timeshare discussion. 
Ensure accuracy and depth in your explanations, focusing exclusively on providing clear, concise, and relevant information. 
Be direct and detailed in your guidance, helping users navigate the complexities of timeshare ownership, agreements, and market trends. 
Maintain an authoritative yet approachable tone, aiming to educate and empower users with reliable and actionable insights.
Today is {date_today}, {day_today}.

{{context}}"""

qa_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", qa_system_prompt),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{question}"),
    ]
)

def format_docs(documents):
    return "\n\n".join(document.page_content for document in documents)

def condense_question(input: dict):
    if input.get("chat_history"):
        return condense_q_chain
    else:
        return input["question"]

rag_chain = (
    RunnablePassthrough.assign(context=condense_question | retriever | format_docs)
    | qa_prompt
    | llm
)
