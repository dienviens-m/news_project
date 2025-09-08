from dotenv import load_dotenv
from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_tavily import TavilySearch
from langchain_google_genai import ChatGoogleGenerativeAI
from schemas import NewsResponse
from template import template

load_dotenv()
tools = [TavilySearch()]

model = ChatGoogleGenerativeAI(temperature=0, model="gemini-2.5-flash")

output_parser = PydanticOutputParser(pydantic_object=NewsResponse)

react_prompt = PromptTemplate(
    template=template,
    input_variables=["input", "agent_scratchpad", "tool_names","tools"]
).partial(format_instructions=output_parser.get_format_instructions())

agent = create_react_agent(
    llm=model,
    tools=tools,
    prompt=react_prompt
)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

extract_output = RunnableLambda(lambda x: x["output"])
parse_output = RunnableLambda(lambda x: output_parser.parse(x))

chain = agent_executor | extract_output | parse_output

def news_search(topic: str) -> NewsResponse:
    result = chain.invoke({
        "input": topic
    })
    return result
