from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from services.llm_service import ask_llm_about_profession

router = APIRouter(prefix="/llm", tags=["LLM"])


class LLMRequest(BaseModel):
    profession: str
    question: str


@router.post("/ask")
async def ask_llm(request: LLMRequest):
    try:
        answer = ask_llm_about_profession(request.profession, request.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
