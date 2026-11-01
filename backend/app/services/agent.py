import uuid
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime

from app.database import get_database
from app.services.llm_provider import get_llm_provider, BaseLLMProvider
from app.services.vector_store import vector_store
from app.services.lab_service import lab_service
from app.services.planner_service import planner_service
from app.models.planner import GeneratePlanRequest
from app.models.chat import Citation, ChatMessage

logger = logging.getLogger("app.services.agent")

# ============================================================================
# Modular Tools Implementation (Requirement 11)
# ============================================================================

class CourseCopilotTools:
    """Modular tools for the AWS Academy Course Copilot Agent."""

    @staticmethod
    async def get_course_outline() -> Dict[str, Any]:
        """Tool 1: Retrieve complete course outline including modules, titles, and IDs."""
        db = get_database()
        modules = []
        async for m in db.modules.find({"course_id": "183194"}, {"_id": 0}).sort("order", 1):
            modules.append({
                "module_id": m.get("module_id"),
                "module_number": m.get("module_number"),
                "title": m.get("title"),
                "is_core_module": m.get("is_core_module"),
                "items_count": len(m.get("items", [])),
                "has_lab": m.get("has_lab", False),
                "lab_id": m.get("lab_id")
            })
        return {
            "course_id": "183194",
            "course_name": "AWS Academy Cloud Foundations",
            "modules": modules
        }

    @staticmethod
    async def get_module_details(module_id: str) -> Optional[Dict[str, Any]]:
        """Tool 2: Get specific module details, items, topics, and services."""
        db = get_database()
        mod = await db.modules.find_one({"module_id": str(module_id)}, {"_id": 0})
        return mod

    @staticmethod
    async def search_course_material(query: str, module_id: Optional[str] = None, top_k: int = 4) -> List[Dict[str, Any]]:
        """Tool 3: Semantic RAG retrieval across indexed course documents and transcripts."""
        return await vector_store.search(
            query=query,
            course_id="183194",
            module_id=module_id,
            top_k=top_k,
            min_score=0.25
        )

    @staticmethod
    async def explain_topic(topic: str, module_id: Optional[str] = None) -> Dict[str, Any]:
        """Tool 4: Beginner-friendly explanation of an AWS concept with practical examples."""
        chunks = await vector_store.search(query=topic, module_id=module_id, top_k=3)
        return {
            "topic": topic,
            "module_id": module_id,
            "grounding_chunks": chunks
        }

    @staticmethod
    async def summarise_lesson(item_id: str) -> Dict[str, Any]:
        """Tool 5: Summarise a specific lesson item or video transcript."""
        db = get_database()
        mod = await db.modules.find_one({"items.item_id": str(item_id)}, {"_id": 0})
        item_title = "Lesson"
        if mod:
            for it in mod.get("items", []):
                if it["item_id"] == str(item_id):
                    item_title = it["title"]
                    break
        
        chunks = await vector_store.search(query=item_title, top_k=3)
        return {
            "item_id": item_id,
            "lesson_title": item_title,
            "summary_content": chunks
        }

    @staticmethod
    async def generate_practice_questions(module_id: Optional[str] = None, difficulty: Optional[str] = None, limit: int = 5) -> List[Dict[str, Any]]:
        """Tool 6: Generate or retrieve practice questions for a module."""
        db = get_database()
        q_filter: Dict[str, Any] = {}
        if module_id and module_id != "all":
            q_filter["module_id"] = str(module_id)
        if difficulty and difficulty != "all":
            q_filter["difficulty"] = difficulty

        questions = []
        async for q in db.practice_questions.find(q_filter, {"_id": 0}).limit(limit):
            questions.append(q)
        return questions

    @staticmethod
    async def evaluate_practice_answer(question_id: str, selected_option_id: str) -> Dict[str, Any]:
        """Tool 7: Check answer against official question rubric and return explanation."""
        db = get_database()
        q = await db.practice_questions.find_one({"question_id": question_id}, {"_id": 0})
        if not q:
            return {"error": "Question not found"}
        
        is_correct = (q.get("correct_option_id") == selected_option_id)
        return {
            "question_id": question_id,
            "selected_option_id": selected_option_id,
            "correct_option_id": q.get("correct_option_id"),
            "is_correct": is_correct,
            "explanation": q.get("explanation"),
            "concept_tags": q.get("concept_tags", []),
            "source_reference": q.get("source_reference")
        }

    @staticmethod
    async def analyse_weak_topics(user_id: str = "default_student") -> Dict[str, Any]:
        """Tool 8: Inspect user test attempts and identify concepts requiring revision."""
        progress = await planner_service.get_overall_progress(user_id=user_id)
        return {
            "weak_topics": progress.get("weak_topics", []),
            "understood_topics": progress.get("understood_topics", [])
        }

    @staticmethod
    async def get_lab_instructions(lab_id: str) -> Optional[Dict[str, Any]]:
        """Tool 9: Retrieve sequential steps and navigation instructions for an AWS lab."""
        return await lab_service.get_lab_by_id(lab_id)

    @staticmethod
    async def guide_lab_step(lab_id: str, step_number: int) -> Dict[str, Any]:
        """Tool 10: Step-by-step guidance and console navigation for a specific lab stage."""
        lab = await lab_service.get_lab_by_id(lab_id)
        if not lab:
            return {"error": f"Lab {lab_id} not found."}
        
        steps = lab.get("steps", [])
        if 1 <= step_number <= len(steps):
            step = steps[step_number - 1]
            return {
                "lab_id": lab_id,
                "lab_title": lab.get("title"),
                "step": step,
                "total_steps": len(steps)
            }
        return {"error": f"Step {step_number} out of range for lab {lab_id}."}

    @staticmethod
    async def record_learning_progress(item_id: str, is_completed: bool, user_id: str = "default_student") -> Dict[str, Any]:
        """Tool 11: Locally record student completion of an item."""
        return await planner_service.record_item_progress(
            user_id=user_id,
            course_id="183194",
            module_id="unknown",
            item_id=item_id,
            completed=is_completed
        )

    @staticmethod
    async def generate_study_plan(available_time_mins: int = 60, user_id: str = "default_student") -> Dict[str, Any]:
        """Tool 12: Generate an adaptive daily study schedule based on user's available study time."""
        req = GeneratePlanRequest(daily_study_mins=available_time_mins)
        plan = await planner_service.generate_study_plan(req, user_id=user_id)
        return plan.model_dump()


# ============================================================================
# Central AI Agent Orchestrator
# ============================================================================

class CourseCopilotAgent:
    """
    Intelligent course-aware learning agent. Decides which tool to invoke,
    retrieves grounded knowledge from indexed course materials, and generates
    educational responses with verified source citations.
    """

    def __init__(self, provider: Optional[BaseLLMProvider] = None):
        # An injected provider is fixed for tests; otherwise resolve the active
        # provider at request time so the Settings page can switch providers.
        self._provider = provider
        self.tools = CourseCopilotTools()

    async def process_chat(
        self,
        user_message: str,
        session_id: Optional[str] = None,
        module_id: Optional[str] = None,
        lesson_id: Optional[str] = None,
        user_id: str = "default_student"
    ) -> Dict[str, Any]:
        db = get_database()
        
        # 1. Manage Chat Session
        if not session_id:
            session_id = f"sess_{uuid.uuid4().hex[:12]}"
            await db.chat_sessions.insert_one({
                "session_id": session_id,
                "user_id": user_id,
                "title": f"Study: {user_message[:30]}...",
                "current_module_id": module_id,
                "current_lesson_id": lesson_id,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow()
            })
        else:
            await db.chat_sessions.update_one(
                {"session_id": session_id},
                {"$set": {"updated_at": datetime.utcnow()}}
            )

        msg_lower = user_message.lower()
        used_tools = []
        citations: List[Citation] = []
        context_chunks: List[Dict[str, Any]] = []

        # 2. Tool routing and intent detection
        if "lab" in msg_lower and any(w in msg_lower for w in ["step", "guide", "how to do", "instructions", "start"]):
            used_tools.append("get_lab_instructions")
            # Detect which lab
            target_lab = "lab_1"
            if "vpc" in msg_lower or "web server" in msg_lower or "2" in msg_lower:
                target_lab = "lab_2"
            elif "ec2" in msg_lower or "3" in msg_lower:
                target_lab = "lab_3"
            elif "ebs" in msg_lower or "4" in msg_lower:
                target_lab = "lab_4"
            elif "database" in msg_lower or "rds" in msg_lower or "5" in msg_lower:
                target_lab = "lab_5"
            elif "scale" in msg_lower or "load balance" in msg_lower or "6" in msg_lower:
                target_lab = "lab_6"

            lab_data = await self.tools.get_lab_instructions(target_lab)
            if lab_data:
                citations.append(Citation(
                    module_id=lab_data.get("module_id"),
                    module_title=lab_data.get("module_title"),
                    document_name=f"AWS Academy Lab Guide - {lab_data.get('title')}",
                    snippet=lab_data.get("objective", ""),
                    confidence=0.95
                ))

        elif any(w in msg_lower for w in ["practice", "quiz", "question", "test me", "knowledge check"]):
            used_tools.append("generate_practice_questions")
            questions = await self.tools.generate_practice_questions(module_id=module_id or "10101", limit=2)
            if questions:
                q = questions[0]
                citations.append(Citation(
                    module_id=q.get("module_id"),
                    module_title=q.get("module_title"),
                    document_name=q.get("source_reference", "Knowledge Check Bank"),
                    snippet=f"Practice assessment item covering: {', '.join(q.get('concept_tags', []))}",
                    confidence=0.9
                ))

        elif any(w in msg_lower for w in ["weak", "struggling", "review topics", "what should i study"]):
            used_tools.append("analyse_weak_topics")

        elif any(w in msg_lower for w in ["plan", "schedule", "calendar", "study time"]):
            used_tools.append("generate_study_plan")

        # 3. Always perform RAG search across course materials to ground the tutor
        used_tools.append("search_course_material")
        context_chunks = await self.tools.search_course_material(
            query=user_message,
            module_id=module_id,
            top_k=4
        )

        for chunk in context_chunks:
            citations.append(Citation(
                module_id=chunk.get("module_id"),
                module_title=chunk.get("module_title"),
                document_name=chunk.get("document_name", "Course Material"),
                page_number=chunk.get("page_number"),
                timestamp=chunk.get("timestamp"),
                source_url=chunk.get("source_url"),
                snippet=chunk.get("content", "")[:180] + "...",
                confidence=chunk.get("score", 0.8)
            ))

        # 4. Generate grounded tutor response
        system_prompt = (
            "You are the AWS Academy Course Copilot, an expert AI tutor for the AWS Academy Cloud Foundations course (ID: 183194).\n"
            "Pedagogical Principles:\n"
            "- Explain concepts clearly, with beginner-friendly metaphors and practical enterprise examples.\n"
            "- Emphasize AWS Cloud best practices, the Shared Responsibility Model, and Well-Architected Framework principles.\n"
            "- Ground answers in official course material and explicitly cite the relevant Module, Document, and Page numbers.\n"
            "- If a specific topic is NOT covered in the indexed AWS Academy course curriculum, clearly inform the student.\n"
            "- Never make up course facts, quiz solutions, or pretend to modify live AWS cloud accounts."
        )

        provider = self._provider or get_llm_provider()
        response_text = await provider.generate_response(
            prompt=user_message,
            system_prompt=system_prompt,
            context_chunks=context_chunks
        )

        # 5. Suggested follow-up questions
        suggested_followups = [
            "Can you explain how this concept appears in the AWS Certified Cloud Practitioner exam?",
            "How do I practice this in the AWS Academy Learner Lab Sandbox?",
            "Can you generate a scenario practice question to test my understanding?"
        ]
        if "s3" in msg_lower:
            suggested_followups = [
                "What is the difference between S3 Standard and S3 Intelligent-Tiering?",
                "How does S3 lifecycle management save operational costs?",
                "Which S3 storage class is best for archival data with retrieval in 12 hours?"
            ]
        elif "vpc" in msg_lower or "network" in msg_lower:
            suggested_followups = [
                "What is the difference between a Security Group and a Network ACL?",
                "Why do we need a NAT Gateway for instances in a private subnet?",
                "Can you guide me through Lab 2: Build your VPC and Launch a Web Server?"
            ]

        # 6. Save message history in database
        msg_id_user = f"msg_{uuid.uuid4().hex[:10]}"
        msg_id_assistant = f"msg_{uuid.uuid4().hex[:10]}"

        user_msg_doc = {
            "message_id": msg_id_user,
            "session_id": session_id,
            "role": "user",
            "content": user_message,
            "module_context": module_id,
            "lesson_context": lesson_id,
            "created_at": datetime.utcnow()
        }
        assistant_msg_doc = {
            "message_id": msg_id_assistant,
            "session_id": session_id,
            "role": "assistant",
            "content": response_text,
            "citations": [c.model_dump() for c in citations],
            "module_context": module_id,
            "lesson_context": lesson_id,
            "created_at": datetime.utcnow()
        }

        await db.chat_messages.insert_many([user_msg_doc, assistant_msg_doc])

        return {
            "session_id": session_id,
            "message": response_text,
            "citations": citations,
            "suggested_followups": suggested_followups,
            "used_tools": list(set(used_tools))
        }

copilot_agent = CourseCopilotAgent()
