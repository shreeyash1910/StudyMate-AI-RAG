from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.conversation import Conversation
from app.models.message import Message
from app.services.retrieval_service import search_document
from app.services.llm_service import generate_answer


router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


class ChatRequest(BaseModel):
    question: str
    document_id: int
    user_id: int
    conversation_id: int | None = None
    top_k: int = 5


@router.post("/")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db)
):

    try:

        # ------------------------------------------------
        # 1. CREATE OR USE CONVERSATION
        # ------------------------------------------------

        if request.conversation_id is None:

            conversation = Conversation(
                user_id=request.user_id,
                title=request.question[:255]
            )

            db.add(conversation)
            db.commit()
            db.refresh(conversation)

            conversation_id = conversation.id

        else:

            conversation = db.query(Conversation).filter(
                Conversation.id == request.conversation_id
            ).first()

            if not conversation:
                raise HTTPException(
                    status_code=404,
                    detail="Conversation not found"
                )

            conversation_id = conversation.id


        # ------------------------------------------------
        # 2. SAVE USER MESSAGE
        # ------------------------------------------------

        user_message = Message(
            conversation_id=conversation_id,
            role="user",
            content=request.question
        )

        db.add(user_message)
        db.commit()
        db.refresh(user_message)


        # ------------------------------------------------
        # 3. SEARCH RELEVANT DOCUMENT CHUNKS
        # ------------------------------------------------

        results = search_document(
            query=request.question,
            document_id=request.document_id,
            top_k=request.top_k
        )


        # ------------------------------------------------
        # 4. IF NOTHING FOUND
        # ------------------------------------------------

        if not results:

            answer = (
                "I could not find relevant information "
                "in your uploaded study material."
            )

            assistant_message = Message(
                conversation_id=conversation_id,
                role="assistant",
                content=answer
            )

            db.add(assistant_message)
            db.commit()
            db.refresh(assistant_message)

            return {
                "conversation_id": conversation_id,
                "question": request.question,
                "answer": answer,
                "sources": []
            }


        # ------------------------------------------------
        # 5. BUILD CONTEXT
        # ------------------------------------------------

        context_parts = []

        for result in results:

            context_parts.append(
                f"""
Page {result['page_number']}:

{result['text']}
"""
            )

        context = "\n".join(context_parts)


        # ------------------------------------------------
        # 6. GENERATE AI ANSWER
        # ------------------------------------------------

        answer = generate_answer(
            question=request.question,
            context=context
        )


        # ------------------------------------------------
        # 7. SAVE AI MESSAGE
        # ------------------------------------------------

        assistant_message = Message(
            conversation_id=conversation_id,
            role="assistant",
            content=answer
        )

        db.add(assistant_message)
        db.commit()
        db.refresh(assistant_message)


        # ------------------------------------------------
        # 8. PREPARE SOURCES
        # ------------------------------------------------

        sources = []

        for result in results:

            sources.append({
                "page_number": result["page_number"],
                "chunk_number": result["chunk_number"],
                "distance": result["distance"]
            })


        # ------------------------------------------------
        # 9. RETURN RESPONSE
        # ------------------------------------------------

        return {

            "conversation_id": conversation_id,

            "question": request.question,

            "answer": answer,

            "sources": sources

        }


    except FileNotFoundError as e:

        db.rollback()

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


    except HTTPException:

        db.rollback()

        raise


    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )