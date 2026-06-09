from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Simple LLM API", version="1.0.0")


class ChatRequest(BaseModel):
    question: str
    history: str = ""


class ChatResponse(BaseModel):
    answer: str
    token_input: int
    token_output: int


def build_chain():
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        api_key=os.getenv("OPENAI_API_KEY"),
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                (
                    "You are a helpful assistant. "
                    "Use the conversation history below to provide context-aware responses.\n\n"
                    "Conversation History:\n{history}"
                ),
            ),
            ("human", "{question}"),
        ]
    )

    return prompt | llm


chain = build_chain()


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = chain.invoke(
            {
                "question": request.question,
                "history": request.history,
            }
        )

        usage = response.usage_metadata
        return ChatResponse(
            answer=response.content,
            token_input=usage["input_tokens"],
            token_output=usage["output_tokens"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health():
    return {"status": "ok"}
