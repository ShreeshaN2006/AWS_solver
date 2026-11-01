from collections import Counter

from app.models.schemas import (
    DashboardStats,
    PracticeEvaluation,
    PracticeQuestion,
    PracticeQuestionType,
    ProgressState,
    StudyPlan,
)
from app.services.data_store import store
from app.services.retrieval import retrieval_service


LABS = {
    "iam": {
        "title": "Introduction to AWS IAM",
        "services": ["IAM"],
        "steps": [
            "Open IAM in AWS console and review users and groups.",
            "Create an IAM group with least-privilege policy.",
            "Create user and attach to the group.",
            "Validate sign-in and policy behavior.",
        ],
    },
    "vpc-web": {
        "title": "Build your VPC and Launch a Web Server",
        "services": ["VPC", "EC2", "Security Groups"],
        "steps": [
            "Create custom VPC and subnets.",
            "Configure route tables and internet gateway.",
            "Launch EC2 web instance into public subnet.",
            "Validate HTTP access using instance public DNS.",
        ],
    },
}


class AgentTools:
    def __init__(self) -> None:
        self.practice_questions: dict[str, PracticeQuestion] = {}

    def get_course_outline(self) -> dict:
        return store.course()

    def get_module_details(self, module_id: str) -> dict | None:
        return next((m for m in store.modules() if m["module_id"] == module_id), None)

    def dashboard(self) -> DashboardStats:
        modules = store.modules()
        completed = 0
        in_progress = 0
        for module in modules:
            progress = store.module_progress(module["module_id"])
            if progress and all(s == ProgressState.completed.value for s in progress.values()):
                completed += 1
            elif progress:
                in_progress += 1
        total = len(modules)
        return DashboardStats(
            course_title=store.course()["course_title"],
            total_modules=total,
            completed_modules=completed,
            modules_in_progress=in_progress,
            remaining_modules=max(0, total - completed - in_progress),
            overall_study_progress=(completed / total) * 100 if total else 0,
            recent_learning_activity=["Reviewed Cloud Security notes", "Completed VPC lab step 2"],
            upcoming_tasks=["Module 6 knowledge check", "Review S3 storage classes"],
            weak_topics=self.analyse_weak_topics(),
            recommended_next_activity="Complete Module 5 networking practice set",
        )

    def search_course_material(self, query: str, module_id: str | None = None) -> list[dict]:
        return [chunk.model_dump() for chunk in retrieval_service.search(query, module_id=module_id)]

    def explain_topic(self, topic: str, module_id: str | None = None) -> dict:
        results = retrieval_service.search(topic, module_id=module_id)
        if not results:
            return {
                "answer": "I could not find this topic in indexed course material. Please upload the related module guide or transcript.",
                "sources": [],
            }
        lead = results[0]
        return {
            "answer": f"From {lead.module_title}: {lead.extracted_content[:450]}",
            "sources": [
                {
                    "module": c.module_title,
                    "document": c.document_name,
                    "page_number": c.page_number,
                    "timestamp": c.timestamp,
                    "source_url": c.source_url,
                }
                for c in results
            ],
        }

    def summarise_lesson(self, item_id: str) -> dict:
        for module in store.modules():
            for item in module["items"]:
                if item["item_id"] == item_id:
                    return {
                        "summary": f"{item['title']} focuses on the key concepts in {module['title']}.",
                        "module": module["title"],
                    }
        return {"summary": "Lesson item not found.", "module": "Unknown"}

    def generate_practice_questions(self, module_id: str, difficulty: str) -> list[PracticeQuestion]:
        module = self.get_module_details(module_id)
        module_title = module["title"] if module else "Unknown Module"
        questions = [
            PracticeQuestion(
                question_id=f"{module_id}-mcq-1",
                module_id=module_id,
                difficulty=difficulty,
                qtype=PracticeQuestionType.mcq,
                prompt=f"Which statement best explains the core concept of {module_title}?",
                options=["Shared responsibility", "Physical server ownership", "On-prem capex", "Offline scaling"],
                answer="Shared responsibility",
                explanation="AWS services follow a shared responsibility model between AWS and customer.",
            ),
            PracticeQuestion(
                question_id=f"{module_id}-tf-1",
                module_id=module_id,
                difficulty=difficulty,
                qtype=PracticeQuestionType.true_false,
                prompt="AWS availability zones in a region are designed for fault isolation.",
                options=["True", "False"],
                answer="True",
                explanation="Availability zones are physically separate locations within a region.",
            ),
        ]
        for question in questions:
            self.practice_questions[question.question_id] = question
        return questions

    def evaluate_practice_answer(self, question_id: str, answer: str) -> PracticeEvaluation:
        question = self.practice_questions[question_id]
        result = PracticeEvaluation(
            is_correct=question.answer.lower() == answer.lower(),
            correct_answer=question.answer,
            explanation=question.explanation,
        )
        store.add_attempt({"question_id": question_id, "answer": answer, "correct": result.is_correct})
        return result

    def analyse_weak_topics(self) -> list[str]:
        attempts = store.practice_attempts
        if not attempts:
            return ["No weak topics yet"]
        failures = [a["question_id"].split("-")[0] for a in attempts if not a["correct"]]
        if not failures:
            return ["Strong performance across attempted modules"]
        counts = Counter(failures).most_common(3)
        return [f"Module {m}" for m, _ in counts]

    def get_lab_instructions(self, lab_id: str) -> dict:
        return LABS.get(lab_id, {"title": "Unknown lab", "steps": [], "services": []})

    def guide_lab_step(self, lab_id: str, step: int) -> dict:
        lab = self.get_lab_instructions(lab_id)
        steps = lab.get("steps", [])
        if step < 1 or step > len(steps):
            return {"message": "Invalid step", "expected_result": "Select a valid step number."}
        current = steps[step - 1]
        return {
            "message": current,
            "expected_result": "Confirm completion before moving ahead.",
            "troubleshooting": "Check IAM permissions and region selection if errors occur.",
        }

    def record_learning_progress(self, item_id: str, module_id: str, status: ProgressState) -> dict:
        store.update_progress(module_id=module_id, item_id=item_id, status=status)
        return {"item_id": item_id, "module_id": module_id, "status": status.value}

    def generate_study_plan(self, available_time: str) -> StudyPlan:
        weak = self.analyse_weak_topics()
        return StudyPlan(
            schedule=[
                {"day": "Day 1", "activity": "Review Module 5 notes", "duration": available_time},
                {"day": "Day 2", "activity": "Attempt practice quiz and revise weak topics", "duration": available_time},
                {"day": "Day 3", "activity": f"Lab practice and recap: {weak[0]}", "duration": available_time},
            ]
        )


agent_tools = AgentTools()
