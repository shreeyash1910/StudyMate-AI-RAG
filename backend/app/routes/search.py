from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.retrieval_service import search_document


router = APIRouter(
    prefix="/search",
    tags=["Search"]
)


class SearchRequest(BaseModel):

    query: str

    document_id: int

    top_k: int = 5


@router.post("/")
def search(request: SearchRequest):

    try:

        results = search_document(
            query=request.query,
            document_id=request.document_id,
            top_k=request.top_k
        )

        return {
            "query": request.query,
            "results": results
        }

    except FileNotFoundError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )