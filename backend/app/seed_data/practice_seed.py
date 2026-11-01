from typing import List, Dict, Any
from app.database import get_database

SEED_PRACTICE_QUESTIONS: List[Dict[str, Any]] = [
    # Module 1 Questions
    {
        "question_id": "q_m1_mcq_1",
        "module_id": "10101",
        "module_title": "Module 1 - Cloud Concepts Overview",
        "question_type": "multiple_choice",
        "difficulty": "easy",
        "prompt": "Which of the following represents one of the six advantages of cloud computing?",
        "options": [
            {"id": "A", "text": "Trade variable expense for capital expense"},
            {"id": "B", "text": "Trade capital expense for variable expense"},
            {"id": "C", "text": "Maintain physical data center security personally"},
            {"id": "D", "text": "Guess maximum infrastructure capacity in advance"}
        ],
        "correct_option_id": "B",
        "explanation": "One of the core six advantages is trading upfront capital expenses (CapEx) for low variable expenses (OpEx), allowing companies to pay only when computing resources are consumed.",
        "concept_tags": ["Six Advantages of Cloud", "CapEx vs OpEx"],
        "aws_services": ["AWS Cloud"],
        "source_reference": "Module 1 Student Guide, Page 8"
    },
    {
        "question_id": "q_m1_tf_1",
        "module_id": "10101",
        "module_title": "Module 1 - Cloud Concepts Overview",
        "question_type": "true_false",
        "difficulty": "easy",
        "prompt": "True or False: In an Infrastructure as a Service (IaaS) model, the cloud provider manages the operating system, database software, and application deployment.",
        "options": [
            {"id": "A", "text": "True"},
            {"id": "B", "text": "False"}
        ],
        "correct_option_id": "B",
        "explanation": "False. In IaaS (e.g. Amazon EC2), AWS manages the virtualization, hardware, and physical data center, while the customer is responsible for installing, configuring, and patching the operating system and applications.",
        "concept_tags": ["IaaS vs PaaS vs SaaS", "Cloud Service Models"],
        "aws_services": ["Amazon EC2"],
        "source_reference": "Module 1 Student Guide, Page 12"
    },
    {
        "question_id": "q_m1_scenario_1",
        "module_id": "10101",
        "module_title": "Module 1 - Cloud Concepts Overview",
        "question_type": "scenario",
        "difficulty": "medium",
        "prompt": "A startup company wants to test an e-commerce prototype for two weeks without investing in physical servers or long-term lease agreements. Which cloud advantage best describes this benefit?",
        "scenario": "The startup needs to iterate rapidly, spin up temporary development environments, and terminate them when testing concludes without stranded hardware costs.",
        "options": [
            {"id": "A", "text": "Massive economies of scale"},
            {"id": "B", "text": "Increase speed and agility"},
            {"id": "C", "text": "Fixed monthly capacity forecasting"},
            {"id": "D", "text": "Dedicated physical hosting"}
        ],
        "correct_option_id": "B",
        "explanation": "Increasing speed and agility allows organizations to dramatically reduce the time it takes to make resources available to developers from weeks to just minutes.",
        "concept_tags": ["Agility", "Six Advantages of Cloud"],
        "aws_services": ["AWS Cloud"],
        "source_reference": "Module 1 Student Guide, Page 9"
    },
    {
        "question_id": "q_m1_hard_1",
        "module_id": "10101",
        "module_title": "Module 1 - Cloud Concepts Overview",
        "question_type": "difficult",
        "difficulty": "hard",
        "prompt": "An enterprise is planning its cloud migration using the AWS Cloud Adoption Framework (AWS CAF). Which perspective focuses on ensuring that cloud investments accelerate business outcomes and align with strategic goals?",
        "options": [
            {"id": "A", "text": "People Perspective"},
            {"id": "B", "text": "Governance Perspective"},
            {"id": "C", "text": "Business Perspective"},
            {"id": "D", "text": "Platform Perspective"}
        ],
        "correct_option_id": "C",
        "explanation": "The Business Perspective of the AWS CAF ensures that IT strategies align with business goals, assessing finance, strategy, and organizational value realization.",
        "concept_tags": ["AWS CAF", "Cloud Governance"],
        "aws_services": ["AWS CAF"],
        "source_reference": "Module 1 Student Guide, Page 22"
    },

    # Module 2 Questions
    {
        "question_id": "q_m2_mcq_1",
        "module_id": "10201",
        "module_title": "Module 2 - Cloud Economics and Billing",
        "question_type": "multiple_choice",
        "difficulty": "easy",
        "prompt": "Which AWS billing tool provides forecasts of estimated future spending for the next up to 12 months based on historical usage?",
        "options": [
            {"id": "A", "text": "AWS Pricing Calculator"},
            {"id": "B", "text": "AWS Cost Explorer"},
            {"id": "C", "text": "AWS Marketplace"},
            {"id": "D", "text": "AWS Artifact"}
        ],
        "correct_option_id": "B",
        "explanation": "AWS Cost Explorer has an easy-to-use interface that lets you visualize, understand, and manage your AWS costs and usage over time, including predictive forecasting for future spend.",
        "concept_tags": ["AWS Cost Explorer", "Cost Forecasting"],
        "aws_services": ["AWS Cost Explorer"],
        "source_reference": "Module 2 Student Guide, Page 15"
    },
    {
        "question_id": "q_m2_scenario_1",
        "module_id": "10201",
        "module_title": "Module 2 - Cloud Economics and Billing",
        "question_type": "scenario",
        "difficulty": "medium",
        "prompt": "A finance director wants an alert when the monthly AWS spend exceeds $5,000, and an automated notification if forecasted spend will exceed that threshold by mid-month. Which service should they configure?",
        "scenario": "Proactive financial guardrails with automated email notifications when spending thresholds are breached.",
        "options": [
            {"id": "A", "text": "AWS Budgets"},
            {"id": "B", "text": "AWS Organizations"},
            {"id": "C", "text": "AWS CloudFormation"},
            {"id": "D", "text": "AWS Trusted Advisor"}
        ],
        "correct_option_id": "A",
        "explanation": "AWS Budgets allows customers to set custom cost and usage budgets with email or SNS alerts when actual or forecasted spend crosses defined limits.",
        "concept_tags": ["AWS Budgets", "Billing Alarms"],
        "aws_services": ["AWS Budgets"],
        "source_reference": "Module 2 Student Guide, Page 18"
    },

    # Module 3 Questions
    {
        "question_id": "q_m3_conceptual_1",
        "module_id": "10301",
        "module_title": "Module 3 - AWS Global Infrastructure Overview",
        "question_type": "conceptual",
        "difficulty": "medium",
        "prompt": "Which statement correctly describes the relationship between AWS Regions and Availability Zones?",
        "options": [
            {"id": "A", "text": "Each Availability Zone contains multiple AWS Regions"},
            {"id": "B", "text": "Each AWS Region consists of a minimum of three isolated Availability Zones"},
            {"id": "C", "text": "Availability Zones in different Regions share physical power grids"},
            {"id": "D", "text": "An Availability Zone is identical to an Edge Location"}
        ],
        "correct_option_id": "B",
        "explanation": "An AWS Region is a physical geographic area containing multiple (typically three or more) physically separate and isolated Availability Zones interconnected with high-bandwidth, low-latency private links.",
        "concept_tags": ["AWS Global Infrastructure", "Regions vs AZs"],
        "aws_services": ["AWS Global Infrastructure"],
        "source_reference": "Module 3 Student Guide, Page 6"
    },

    # Module 4 Questions
    {
        "question_id": "q_m4_scenario_1",
        "module_id": "10401",
        "module_title": "Module 4 - AWS Cloud Security",
        "question_type": "scenario",
        "difficulty": "medium",
        "prompt": "Under the AWS Shared Responsibility Model, which security task is the customer exclusively responsible for when running an Amazon EC2 Linux instance?",
        "scenario": "A company hosts a database on an EC2 instance and needs to ensure compliance with data protection laws.",
        "options": [
            {"id": "A", "text": "Physical security of the data center facility"},
            {"id": "B", "text": "Decommissioning defective physical hard drives"},
            {"id": "C", "text": "Patching the guest operating system and installing security updates"},
            {"id": "D", "text": "Maintaining the hypervisor virtualization software"}
        ],
        "correct_option_id": "C",
        "explanation": "For infrastructure services like EC2, the customer is responsible for security 'IN' the cloud, which includes installing guest OS security patches, configuring firewall rules (Security Groups), and managing user passwords.",
        "concept_tags": ["Shared Responsibility Model", "Security IN the Cloud"],
        "aws_services": ["AWS IAM", "Amazon EC2"],
        "source_reference": "Module 4 Student Guide, Page 5"
    },
    {
        "question_id": "q_m4_hard_1",
        "module_id": "10401",
        "module_title": "Module 4 - AWS Cloud Security",
        "question_type": "difficult",
        "difficulty": "hard",
        "prompt": "An administrator needs to restrict access across multiple member accounts in an AWS Organization so that nobody—including the root user of member accounts—can disable AWS CloudTrail. What should be used?",
        "options": [
            {"id": "A", "text": "IAM User Permission Boundary"},
            {"id": "B", "text": "Service Control Policy (SCP)"},
            {"id": "C", "text": "Amazon Inspector assessment rule"},
            {"id": "D", "text": "AWS KMS key policy"}
        ],
        "correct_option_id": "B",
        "explanation": "Service Control Policies (SCPs) in AWS Organizations specify the maximum available permissions for an organization or organizational unit (OU). Even the account root user in a member account cannot override an SCP deny policy.",
        "concept_tags": ["AWS Organizations", "Service Control Policies (SCPs)"],
        "aws_services": ["AWS Organizations", "AWS CloudTrail"],
        "source_reference": "Module 4 Student Guide, Page 20"
    },

    # Module 5 Questions
    {
        "question_id": "q_m5_mcq_1",
        "module_id": "10501",
        "module_title": "Module 5 - Networking and Content Delivery",
        "question_type": "multiple_choice",
        "difficulty": "medium",
        "prompt": "What is the primary difference between a Security Group and a Network Access Control List (NACL)?",
        "options": [
            {"id": "A", "text": "Security Groups are stateless; NACLs are stateful"},
            {"id": "B", "text": "Security Groups are stateful; NACLs are stateless"},
            {"id": "C", "text": "Security Groups operate at the VPC level; NACLs operate at the instance level"},
            {"id": "D", "text": "Security Groups support explicit Deny rules; NACLs do not"}
        ],
        "correct_option_id": "B",
        "explanation": "Security Groups are stateful (return traffic is automatically allowed regardless of inbound rules) and operate at instance ENI level. NACLs are stateless (both inbound and outbound rules must be defined explicitly) and operate at subnet boundary.",
        "concept_tags": ["Security Groups vs NACLs", "VPC Security"],
        "aws_services": ["Amazon VPC"],
        "source_reference": "Module 5 Student Guide, Page 22"
    },
    {
        "question_id": "q_m5_scenario_1",
        "module_id": "10501",
        "module_title": "Module 5 - Networking and Content Delivery",
        "question_type": "scenario",
        "difficulty": "medium",
        "prompt": "An application in a private subnet needs to download operating system patches from the internet, but must not accept inbound connections from external internet users. What VPC component should be deployed in the public subnet?",
        "scenario": "Outbound-only internet egress for private subnet EC2 instances.",
        "options": [
            {"id": "A", "text": "Internet Gateway (IGW)"},
            {"id": "B", "text": "NAT Gateway"},
            {"id": "C", "text": "Virtual Private Gateway (VGW)"},
            {"id": "D", "text": "VPC Endpoint"}
        ],
        "correct_option_id": "B",
        "explanation": "A Network Address Translation (NAT) Gateway allows instances in a private subnet to connect to services outside the VPC while preventing external services from initiating direct inbound connections.",
        "concept_tags": ["NAT Gateway", "Private Subnet Egress"],
        "aws_services": ["Amazon VPC"],
        "source_reference": "Module 5 Student Guide, Page 14"
    },

    # Module 6 Questions
    {
        "question_id": "q_m6_scenario_1",
        "module_id": "10601",
        "module_title": "Module 6 - Compute",
        "question_type": "scenario",
        "difficulty": "medium",
        "prompt": "A media processing pipeline performs batch video rendering that can be paused and resumed at any time. Which EC2 purchasing option provides the steepest cost savings (up to 90%) for this fault-tolerant workload?",
        "scenario": "Fault-tolerant batch rendering with flexible start and stop times.",
        "options": [
            {"id": "A", "text": "On-Demand Instances"},
            {"id": "B", "text": "Spot Instances"},
            {"id": "C", "text": "Dedicated Hosts"},
            {"id": "D", "text": "Standard Reserved Instances"}
        ],
        "correct_option_id": "B",
        "explanation": "EC2 Spot Instances allow customers to take advantage of unused EC2 capacity at steep discounts of up to 90% off On-Demand rates, ideal for workloads that can tolerate interruptions.",
        "concept_tags": ["Spot Instances", "EC2 Pricing"],
        "aws_services": ["Amazon EC2"],
        "source_reference": "Module 6 Student Guide, Page 11"
    },

    # Module 7 Questions
    {
        "question_id": "q_m7_conceptual_1",
        "module_id": "10701",
        "module_title": "Module 7 - Storage",
        "question_type": "conceptual",
        "difficulty": "easy",
        "prompt": "Which AWS storage service provides object storage with 99.999999999% (11 9's) durability designed for unlimited capacity accessible via HTTP/REST APIs?",
        "options": [
            {"id": "A", "text": "Amazon Elastic Block Store (EBS)"},
            {"id": "B", "text": "Amazon Simple Storage Service (S3)"},
            {"id": "C", "text": "Amazon Elastic File System (EFS)"},
            {"id": "D", "text": "AWS Storage Gateway"}
        ],
        "correct_option_id": "B",
        "explanation": "Amazon S3 is an object storage service offering industry-leading scalability, data availability, security, and performance with 11 9's durability.",
        "concept_tags": ["Amazon S3", "Object Storage"],
        "aws_services": ["Amazon S3"],
        "source_reference": "Module 7 Student Guide, Page 15"
    },

    # Module 8 Questions
    {
        "question_id": "q_m8_scenario_1",
        "module_id": "10801",
        "module_title": "Module 8 - Databases",
        "question_type": "scenario",
        "difficulty": "medium",
        "prompt": "A gaming application requires a fully managed, serverless NoSQL database capable of single-digit millisecond latency at any scale to track live player sessions. Which service should be chosen?",
        "scenario": "Ultra-low latency key-value data retrieval with unpredictable spiky player logins.",
        "options": [
            {"id": "A", "text": "Amazon RDS for MySQL"},
            {"id": "B", "text": "Amazon DynamoDB"},
            {"id": "C", "text": "Amazon Redshift"},
            {"id": "D", "text": "Amazon Aurora Multi-Master"}
        ],
        "correct_option_id": "B",
        "explanation": "Amazon DynamoDB is a serverless, key-value and document NoSQL database that delivers consistent, single-digit millisecond response times with automatic horizontal scaling.",
        "concept_tags": ["Amazon DynamoDB", "NoSQL Databases"],
        "aws_services": ["Amazon DynamoDB"],
        "source_reference": "Module 8 Student Guide, Page 18"
    },

    # Module 9 Questions
    {
        "question_id": "q_m9_mcq_1",
        "module_id": "10901",
        "module_title": "Module 9 - Cloud Architecture",
        "question_type": "multiple_choice",
        "difficulty": "medium",
        "prompt": "Which pillar of the AWS Well-Architected Framework focuses on designing workloads to recover automatically from failures and meet dynamic capacity demands?",
        "options": [
            {"id": "A", "text": "Operational Excellence"},
            {"id": "B", "text": "Reliability"},
            {"id": "C", "text": "Cost Optimization"},
            {"id": "D", "text": "Performance Efficiency"}
        ],
        "correct_option_id": "B",
        "explanation": "The Reliability pillar encompasses the ability of a workload to perform its intended function correctly and consistently, recover from infrastructure failures, and automatically acquire compute capacity to satisfy demand.",
        "concept_tags": ["Well-Architected Framework", "Reliability Pillar"],
        "aws_services": ["AWS Well-Architected Tool"],
        "source_reference": "Module 9 Student Guide, Page 7"
    },

    # Module 10 Questions
    {
        "question_id": "q_m10_scenario_1",
        "module_id": "11001",
        "module_title": "Module 10 - Auto Scaling and Monitoring",
        "question_type": "scenario",
        "difficulty": "hard",
        "prompt": "A web application experiences high morning traffic spikes. The architect wants to automatically increase the number of EC2 instances when average CPU utilization exceeds 75% for 3 consecutive minutes, and reduce instances when traffic calms down. Which combination of services enables this?",
        "scenario": "Automated elasticity driven by system utilization metrics.",
        "options": [
            {"id": "A", "text": "Amazon CloudWatch Alarms and EC2 Auto Scaling"},
            {"id": "B", "text": "AWS CloudTrail and AWS Config"},
            {"id": "C", "text": "Amazon Route 53 and AWS Artifact"},
            {"id": "D", "text": "AWS Shield and Amazon Inspector"}
        ],
        "correct_option_id": "A",
        "explanation": "Amazon CloudWatch monitors EC2 CPU utilization and triggers an alarm when the 75% threshold is crossed, which instructs the Auto Scaling Group policy to launch or terminate EC2 instances.",
        "concept_tags": ["Auto Scaling", "Amazon CloudWatch Alarms"],
        "aws_services": ["Amazon CloudWatch", "Amazon EC2 Auto Scaling"],
        "source_reference": "Module 10 Student Guide, Page 16"
    }
]

async def seed_practice_questions():
    """Seed practice question bank in MongoDB."""
    db = get_database()
    for q in SEED_PRACTICE_QUESTIONS:
        await db.practice_questions.update_one(
            {"question_id": q["question_id"]},
            {"$set": q},
            upsert=True
        )
