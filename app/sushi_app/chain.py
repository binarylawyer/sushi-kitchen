from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_template("Answer: {question}")
llm = ChatOpenAI(model="gpt-3.5-turbo")
chain = LLMChain(llm=llm, prompt=prompt)
