from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_community.tools import QuerySQLDatabaseTool
from dotenv import load_dotenv
import os
load_dotenv()
from langchain_openai import ChatOpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
db = SQLDatabase.from_uri("postgresql://postgres:abc@localhost:5432/market")

query_execute = QuerySQLDatabaseTool(db = db)

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
chain = create_sql_query_chain(llm, db)

template = chain.invoke({"question": "How LIOC doing in last few days?"})
print(template)
data_retreive = query_execute.invoke(template)
print("")
print(data_retreive)

