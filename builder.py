
import os
import json
import re
from langchain_groq import ChatGroq
from langchain import LLMChain
from langchain.prompts import ChatPromptTemplate
from typing import Dict, Any
from dotenv import load_dotenv

# Load environment
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
llm = ChatGroq(api_key=GROQ_API_KEY, model_name="qwen/qwen3-32b")

# Load JSON schema content to include in prompts
schema_path = os.path.join(os.path.dirname(__file__), 'models', 'resume_schema.json')
with open(schema_path) as f:
    raw_schema = f.read()
# Escape braces to avoid template interpolation
escaped_schema = raw_schema.replace('{', '{{').replace('}', '}}')

# Prompt templates
SUMMARY_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "act as an professional resume writer. Generate a concise 2-3 sentence summary from the user’s free-form description. ONLY GENERATE THE SUMMARY NO ADDITIONAL TEXT OR HEADING SO I CAN JUST COPY PASTE IT"),
    ("human", "{raw_text}")
])

STRUCT_PROMPT = ChatPromptTemplate.from_messages([
    ("system", (
        "You are a professional resume writer. Produce a JSON matching the following JSON schema exactly (no extra keys):\n"
        + escaped_schema
    )),
    ("human", (
        "Name: {name}\n"
        "Email: {email}\n"
        "Phone: {phone}\n\n"
        "Summary: {summary}\n\n"
        "Free-form description:\n{raw_text}"
    ))
])

# Chains
summary_chain = LLMChain(llm=llm, prompt=SUMMARY_PROMPT)
struct_chain = LLMChain(llm=llm, prompt=STRUCT_PROMPT)


def generate_summary(raw_text: str) -> str:
    result = summary_chain.predict(raw_text=raw_text)
    only_text = re.sub(r'<think>.*?</think>', '', result.strip(), flags=re.DOTALL).strip()
    return only_text


def generate_structured_resume(profile: Dict[str, Any], summary: str, raw_text: str) -> str:
    result = struct_chain.predict(
        name=profile['personal_info']['name'],
        email=profile['personal_info']['email'],
        phone=profile['personal_info'].get('phone', ''),
        summary=summary,
        raw_text=raw_text
    )
    return result.strip()