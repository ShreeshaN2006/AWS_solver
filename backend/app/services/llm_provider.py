import abc
import os
import logging
import hashlib
import numpy as np
from typing import List, Dict, Any, Optional
from app.config import settings

logger = logging.getLogger("app.services.llm_provider")

class BaseLLMProvider(abc.ABC):
    @abc.abstractmethod
    async def generate_response(
        self,
        prompt: str,
        system_prompt: str = "You are the AWS Academy Course Copilot.",
        temperature: float = 0.2,
        context_chunks: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """Generate response given a user prompt and optional context chunks."""
        pass

    @abc.abstractmethod
    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Generate vector embeddings for a list of strings."""
        pass

class OpenAIProvider(BaseLLMProvider):
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None, embedding_model: Optional[str] = None):
        from openai import AsyncOpenAI
        self.api_key = api_key or settings.OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is required when LLM_PROVIDER=openai.")
        self.model = model or settings.OPENAI_MODEL
        self.embedding_model = embedding_model or settings.OPENAI_EMBEDDING_MODEL
        self.client = AsyncOpenAI(api_key=self.api_key)

    async def generate_response(
        self,
        prompt: str,
        system_prompt: str = "You are the AWS Academy Course Copilot.",
        temperature: float = 0.2,
        context_chunks: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        messages = [{"role": "system", "content": system_prompt}]
        if context_chunks:
            context_text = "\n\n---\n\n".join([
                f"[Source: {c.get('document_name', 'Doc')} | Module: {c.get('module_title', 'General')} | Page/Time: {c.get('page_number') or c.get('timestamp') or 'N/A'}]\n{c.get('content', '')}"
                for c in context_chunks
            ])
            messages.append({
                "role": "system",
                "content": f"Verified AWS Academy Course Materials for Grounding:\n{context_text}\n\nStrict rule: Prioritise official course material. If information is not in the course documents, clearly inform the student."
            })
        messages.append({"role": "user", "content": prompt})

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature
        )
        return response.choices[0].message.content or ""

    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        if not texts:
            return []
        response = await self.client.embeddings.create(
            model=self.embedding_model,
            input=texts
        )
        return [item.embedding for item in response.data]

class BedrockProvider(BaseLLMProvider):
    def __init__(self):
        import boto3
        import json
        self.json = json
        self.region = settings.AWS_REGION
        self.model_id = settings.BEDROCK_MODEL_ID
        self.embedding_model_id = settings.BEDROCK_EMBEDDING_MODEL_ID
        # Use explicit credentials only when a complete key pair is configured.
        # Otherwise let boto3 use its standard chain (profile, SSO, web identity,
        # container credentials, or an EC2 instance role).
        access_key = settings.AWS_ACCESS_KEY_ID or os.getenv("AWS_ACCESS_KEY_ID")
        secret_key = settings.AWS_SECRET_ACCESS_KEY or os.getenv("AWS_SECRET_ACCESS_KEY")
        session_token = settings.AWS_SESSION_TOKEN or os.getenv("AWS_SESSION_TOKEN")
        if bool(access_key) != bool(secret_key):
            raise ValueError(
                "Configure both AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY, "
                "or use the AWS SDK default credential chain."
            )
        client_options = {"service_name": "bedrock-runtime", "region_name": self.region}
        if access_key and secret_key:
            client_options.update(
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                aws_session_token=session_token,
            )
        self.client = boto3.client(**client_options)

    async def generate_response(
        self,
        prompt: str,
        system_prompt: str = "You are the AWS Academy Course Copilot.",
        temperature: float = 0.2,
        context_chunks: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        import asyncio
        loop = asyncio.get_event_loop()
        
        full_system = system_prompt
        if context_chunks:
            context_text = "\n\n---\n\n".join([
                f"[Source: {c.get('document_name')} | Module: {c.get('module_title')} | Ref: {c.get('page_number') or c.get('timestamp') or 'Course'}]\n{c.get('content', '')}"
                for c in context_chunks
            ])
            full_system += f"\n\nOfficial AWS Course Materials:\n{context_text}"

        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 2048,
            "temperature": temperature,
            "system": full_system,
            "messages": [{"role": "user", "content": prompt}]
        }

        def _invoke():
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=self.json.dumps(body)
            )
            response_body = self.json.loads(response.get("body").read())
            return response_body.get("content", [{}])[0].get("text", "")

        return await loop.run_in_executor(None, _invoke)

    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        import asyncio
        loop = asyncio.get_event_loop()
        embeddings = []

        def _embed_single(text: str):
            body = self.json.dumps({"inputText": text})
            response = self.client.invoke_model(
                modelId=self.embedding_model_id,
                body=body
            )
            result = self.json.loads(response.get("body").read())
            return result.get("embedding", [])

        for text in texts:
            emb = await loop.run_in_executor(None, _embed_single, text)
            embeddings.append(emb)
        return embeddings

class LocalMockProvider(BaseLLMProvider):
    """
    Offline demonstration provider with deterministic, hashed lexical vectors.
    It can demonstrate the chat and retrieval workflow without paid credentials, but its
    vectors are not semantic embeddings and it should not be used to judge paraphrase retrieval.
    """
    def __init__(self, vector_dim: int = 128):
        self.vector_dim = vector_dim

    async def generate_response(
        self,
        prompt: str,
        system_prompt: str = "You are the AWS Academy Course Copilot.",
        temperature: float = 0.2,
        context_chunks: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        prompt_lower = prompt.lower()

        # Build citations header if context chunks are available
        sources_text = ""
        top_source = None
        if context_chunks and len(context_chunks) > 0:
            top_source = context_chunks[0]
            sources_text = f"\n\n**Verified Course Reference:**\n- **Module:** {top_source.get('module_title', 'General')}\n- **Document:** {top_source.get('document_name', 'Course Guide')}\n- **Page / Section:** {top_source.get('page_number', '1')}"

        # Topic detection for course-aware responses:
        if "compare" in prompt_lower or "versus" in prompt_lower or "vs" in prompt_lower:
            if "s3" in prompt_lower and ("ebs" in prompt_lower or "efs" in prompt_lower):
                return (
                    "### AWS Storage Comparison: S3 vs. EBS vs. EFS\n\n"
                    "| Feature | Amazon S3 (Simple Storage Service) | Amazon EBS (Elastic Block Store) | Amazon EFS (Elastic File System) |\n"
                    "| :--- | :--- | :--- | :--- |\n"
                    "| **Storage Type** | Object Storage | Block Storage | Network File System (NFS) |\n"
                    "| **Attachment** | Internet-accessible via REST/HTTP API | Attached to a single EC2 instance (same AZ) | Mounted concurrently across thousands of EC2 instances |\n"
                    "| **Use Cases** | Backups, static web hosting, media assets, data lakes | OS boot volumes, databases (MySQL, MongoDB) | Shared file storage, web server content pools, home directories |\n"
                    "| **Scalability** | Unlimited capacity; up to 5 TB per single object | Scale by volume resizing; IOPS provisionable (gp3, io2) | Elastic automatic scale-up and scale-down |\n"
                    "| **Durability** | 99.999999999% (11 9's) across multiple AZs | Replicated within a single AZ (99.8%–99.9% availability) | Multi-AZ durability across regional AZs |\n\n"
                    "**AWS Academy Rule of Thumb:**\n"
                    "- Choose **EBS** when your EC2 operating system or database engine requires high-speed block storage.\n"
                    "- Choose **S3** for durable internet-accessible object storage with life cycle policies.\n"
                    "- Choose **EFS** when Linux workloads need POSIX file sharing across multiple instances."
                    + sources_text
                )
            elif "rds" in prompt_lower and "dynamodb" in prompt_lower:
                return (
                    "### AWS Database Comparison: Amazon RDS vs. Amazon DynamoDB\n\n"
                    "- **Amazon RDS (Relational Database Service):**\n"
                    "  - *Type:* Managed Relational (SQL) database service.\n"
                    "  - *Engines Supported:* Amazon Aurora, PostgreSQL, MySQL, MariaDB, Oracle, and Microsoft SQL Server.\n"
                    "  - *Characteristics:* Fixed schemas, complex joins, ACID compliance, Multi-AZ automated failover, and Read Replicas.\n\n"
                    "- **Amazon DynamoDB:**\n"
                    "  - *Type:* Fully managed NoSQL key-value and document database.\n"
                    "  - *Characteristics:* Schema-less, single-digit millisecond latency at any scale, serverless with auto-scaling, Multi-Region Global Tables.\n\n"
                    "**Exam Tip (Cloud Foundations):** Use RDS when relational integrity and complex SQL queries are necessary. Use DynamoDB when predictable sub-10ms response times and massive horizontal scale are required."
                    + sources_text
                )

        if "security" in prompt_lower or "shared responsibility" in prompt_lower:
            return (
                "### AWS Shared Responsibility Model (Module 4)\n\n"
                "The Shared Responsibility Model separates security obligations into two clear tiers:\n\n"
                "1. **Security OF the Cloud (AWS Responsibility):**\n"
                "   - Physical security of data centers, biometric access controls.\n"
                "   - Core hardware, networking infrastructure (cables, routers, switches).\n"
                "   - Virtualization layer (hypervisor) and managed service software (e.g. patching the OS in Amazon RDS).\n\n"
                "2. **Security IN the Cloud (Customer Responsibility):**\n"
                "   - Customer data encryption (in-transit using TLS and at-rest using AWS KMS).\n"
                "   - Identity and Access Management (IAM) user configuration, policies, and MFA enforcement.\n"
                "   - Operating System patching and firewall configuration (Security Groups, Network ACLs) on Amazon EC2.\n\n"
                "> **Key Takeaway:** AWS protects the global infrastructure that runs all of the services; you control how you configure, access, and encrypt your assets."
                + sources_text
            )

        if "well-architected" in prompt_lower or "pillar" in prompt_lower or "architecture" in prompt_lower:
            return (
                "### The Six Pillars of the AWS Well-Architected Framework (Module 9)\n\n"
                "1. **Operational Excellence:** Focuses on running and monitoring systems, and continually improving processes (e.g., Infrastructure as Code via AWS CloudFormation).\n"
                "2. **Security:** Focuses on protecting information and systems through identity management, data protection (KMS), and automated detection (GuardDuty).\n"
                "3. **Reliability:** Ability of a system to recover from infrastructure disruptions, dynamically acquire computing resources, and mitigate disruptions (Multi-AZ, Auto Scaling).\n"
                "4. **Performance Efficiency:** Using computing resources efficiently to meet system requirements and maintain that efficiency as demand changes (Serverless, Graviton, CloudFront).\n"
                "5. **Cost Optimization:** Avoiding unnecessary costs by understanding spending over time, selecting appropriate resource types, and scaling according to demand.\n"
                "6. **Sustainability:** Minimizing the environmental impacts of running cloud workloads (optimizing compute utilization, reducing idle resources)."
                + sources_text
            )

        if "lab" in prompt_lower:
            return (
                "### AWS Academy Lab Assistance\n\n"
                "I am equipped to guide you step-by-step through all six AWS Academy Cloud Foundations labs:\n"
                "1. **Lab 1:** Introduction to AWS IAM (Users, Groups, Policies, MFA)\n"
                "2. **Lab 2:** Build your VPC and Launch a Web Server (VPC, Subnets, IGW, Route Tables, Apache EC2)\n"
                "3. **Lab 3:** Introduction to Amazon EC2 (AMI, Instance types, Key pairs, User Data)\n"
                "4. **Lab 4:** Working with EBS (Volumes, Snapshots, IOPS performance)\n"
                "5. **Lab 5:** Build a Database Server (Amazon RDS Multi-AZ MySQL)\n"
                "6. **Lab 6:** Scale and Load Balance your Architecture (Application Load Balancer, Auto Scaling Group)\n\n"
                "Navigate to the **AWS Lab Assistant** tab to select your lab, inspect sequential steps, and troubleshoot console errors with safety reminders."
                + sources_text
            )

        # Grounding with retrieved context
        if context_chunks and len(context_chunks) > 0:
            top_chunk = context_chunks[0]
            summary = top_chunk.get("content", "")[:350]
            return (
                f"### Course Explanation: {top_source.get('module_title', 'AWS Concept')}\n\n"
                f"Based on the official AWS Academy Cloud Foundations curriculum:\n\n"
                f"{summary}...\n\n"
                f"**Key Concepts to Remember:**\n"
                f"- This topic aligns with learning objectives in **{top_source.get('module_title', 'Module')}**.\n"
                f"- In real-world enterprise deployments, AWS recommends automating this configuration and applying least-privilege permissions.\n\n"
                f"Would you like me to generate a practice question or explain how this applies in the practical hands-on labs?"
                + sources_text
            )

        return (
            f"### AWS Academy Cloud Foundations - Study Guide\n\n"
            f"Here is an explanation regarding your inquiry about **{prompt.strip()}**:\n\n"
            f"1. **Core Definition:** In AWS Cloud computing, services are categorized across Compute, Storage, Database, Networking, and Security.\n"
            f"2. **Architectural Best Practice:** Always design for failure, decouple components using messaging (SQS, SNS), and encrypt sensitive data using AWS KMS.\n"
            f"3. **Certification Tip:** For the AWS Certified Cloud Practitioner exam, understand the business value, pricing model, and high-level use case for each AWS service.\n\n"
            f"*(Note: You can ask me to explain any module topic, compare services, generate practice quiz questions, or walk through a lab step.)*"
        )

    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Creates deterministic lexical-hash vectors for offline demonstrations only.
        These vectors are reproducible but are not semantic embeddings. Use OpenAI or
        Bedrock for semantic retrieval across paraphrased questions.
        """
        embeddings = []
        for text in texts:
            vec = np.zeros(self.vector_dim, dtype=np.float32)
            words = text.lower().split()
            for i, word in enumerate(words):
                h = int(hashlib.md5(word.encode("utf-8")).hexdigest(), 16)
                idx = h % self.vector_dim
                vec[idx] += 1.0 + (i % 3) * 0.1
            # Normalize vector
            norm = np.linalg.norm(vec)
            if norm > 0:
                vec = vec / norm
            embeddings.append(vec.tolist())
        return embeddings

def get_llm_provider(provider_type: Optional[str] = None) -> BaseLLMProvider:
    """Return exactly the requested provider; never silently downgrade to the offline mock."""
    provider = (provider_type or settings.LLM_PROVIDER).strip().lower()
    if provider == "local_mock":
        return LocalMockProvider()
    if provider == "openai":
        try:
            return OpenAIProvider()
        except Exception as exc:
            raise RuntimeError(f"OpenAI provider is not configured correctly: {exc}") from exc
    if provider == "bedrock":
        try:
            return BedrockProvider()
        except Exception as exc:
            raise RuntimeError(f"Amazon Bedrock provider is not configured correctly: {exc}") from exc
    raise ValueError(
        f"Unsupported LLM_PROVIDER '{provider}'. Choose local_mock, openai, or bedrock."
    )
