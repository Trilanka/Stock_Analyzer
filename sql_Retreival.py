from langchain.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
from langchain_community.tools import QuerySQLDatabaseTool

from langchain_openai import ChatOpenAI

db = SQLDatabase.from_uri("sqlite:////content/market_data.db")

query_execute = QuerySQLDatabaseTool(db = db)

llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
chain = create_sql_query_chain(llm, db)

template = chain.invoke({"question": "How LIOC doing?"})
print(template)
data_retreive = query_execute.invoke(template)

print(data_retreive)