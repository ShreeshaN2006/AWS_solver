from typing import List, Dict, Any
import uuid
from app.database import get_database
from app.services.vector_store import vector_store

COURSE_SEED_MODULES: List[Dict[str, Any]] = [
    {
        "module_id": "10001",
        "course_id": "183194",
        "module_number": 0,
        "title": "Course Introduction & Overview",
        "description": "Introduction to the AWS Academy Cloud Foundations course syllabus, student guide expectations, and cloud career paths.",
        "is_core_module": False,
        "order": 1,
        "has_lab": False,
        "key_aws_services": ["AWS Management Console", "AWS Documentation"],
        "topics": ["Course Syllabus", "AWS Certification Roadmap", "Cloud Career Roles"],
        "items": [
            {"item_id": "20001", "module_id": "10001", "title": "Welcome to AWS Academy Cloud Foundations", "type": "Page", "url": "https://awsacademy.instructure.com/courses/183194/pages/welcome-to-aws-academy-cloud-foundations", "position": 1, "is_completed": True, "time_estimate_mins": 10},
            {"item_id": "20002", "module_id": "10001", "title": "Course Syllabus, Outline and Certification Roadmap", "type": "Page", "url": "https://awsacademy.instructure.com/courses/183194/pages/course-syllabus-and-objectives", "position": 2, "is_completed": True, "time_estimate_mins": 15}
        ]
    },
    {
        "module_id": "10101",
        "course_id": "183194",
        "module_number": 1,
        "title": "Module 1 - Cloud Concepts Overview",
        "description": "Understand cloud computing fundamentals, the six advantages of cloud computing, deployment models (Public, Private, Hybrid), and the AWS Cloud Adoption Framework (AWS CAF).",
        "is_core_module": True,
        "order": 2,
        "has_lab": False,
        "key_aws_services": ["AWS Cloud", "AWS CAF"],
        "topics": ["Cloud Computing Definition", "Six Advantages of Cloud Computing", "IaaS vs PaaS vs SaaS", "Public vs Private vs Hybrid", "AWS Cloud Adoption Framework (AWS CAF)"],
        "items": [
            {"item_id": "20101", "module_id": "10101", "title": "Video: Introduction to Cloud Computing and AWS", "type": "ExternalTool", "url": "https://awsacademy.instructure.com/courses/183194/pages/m1-video-introduction-to-cloud-computing", "position": 1, "is_completed": True, "time_estimate_mins": 15},
            {"item_id": "20102", "module_id": "10101", "title": "Student Guide: Cloud Concepts & Six Advantages of Cloud", "type": "File", "url": "https://awsacademy.instructure.com/courses/183194/files/m1-student-guide-cloud-concepts.pdf", "position": 2, "is_completed": True, "time_estimate_mins": 25},
            {"item_id": "20103", "module_id": "10101", "title": "Module 1 Knowledge Check", "type": "Quiz", "url": "https://awsacademy.instructure.com/courses/183194/quizzes/m1-knowledge-check", "position": 3, "is_completed": True, "time_estimate_mins": 15}
        ]
    },
    {
        "module_id": "10201",
        "course_id": "183194",
        "module_number": 2,
        "title": "Module 2 - Cloud Economics and Billing",
        "description": "Master AWS pricing principles (pay-as-you-go, save when you commit, pay less by using more), Total Cost of Ownership (TCO), AWS Pricing Calculator, AWS Billing Dashboard, AWS Budgets, and AWS Cost Explorer.",
        "is_core_module": True,
        "order": 3,
        "has_lab": False,
        "key_aws_services": ["AWS Cost Explorer", "AWS Budgets", "AWS Pricing Calculator", "AWS Organizations", "AWS Cost and Usage Report"],
        "topics": ["Pay-as-you-go Pricing", "Capital Expense (CapEx) vs Operational Expense (OpEx)", "AWS Pricing Calculator", "AWS Organizations Consolidated Billing", "AWS Budgets & Cost Explorer", "AWS Support Plans"],
        "items": [
            {"item_id": "20201", "module_id": "10201", "title": "Video: Fundamentals of AWS Pricing & Total Cost of Ownership", "type": "ExternalTool", "url": "https://awsacademy.instructure.com/courses/183194/pages/m2-video-cloud-economics-pricing-models", "position": 1, "is_completed": True, "time_estimate_mins": 20},
            {"item_id": "20202", "module_id": "10201", "title": "Student Guide: AWS Organizations, AWS Budgets and Cost Explorer", "type": "File", "url": "https://awsacademy.instructure.com/courses/183194/files/m2-student-guide-billing-budgets.pdf", "position": 2, "is_completed": True, "time_estimate_mins": 25},
            {"item_id": "20203", "module_id": "10201", "title": "Module 2 Knowledge Check", "type": "Quiz", "url": "https://awsacademy.instructure.com/courses/183194/quizzes/m2-knowledge-check", "position": 3, "is_completed": True, "time_estimate_mins": 15}
        ]
    },
    {
        "module_id": "10301",
        "course_id": "183194",
        "module_number": 3,
        "title": "Module 3 - AWS Global Infrastructure Overview",
        "description": "Explore the worldwide AWS Global Infrastructure: AWS Regions, Availability Zones (AZs), Edge Locations, Points of Presence, and AWS Outposts for high availability and low-latency delivery.",
        "is_core_module": True,
        "order": 4,
        "has_lab": False,
        "key_aws_services": ["AWS Global Infrastructure", "AWS Regions", "Availability Zones", "Edge Locations", "AWS Outposts"],
        "topics": ["AWS Regions Selection Criteria (Latency, Compliance, Cost, Services)", "Availability Zone Isolation & Redundancy", "Edge Locations & CloudFront PoPs", "AWS Local Zones & Wavelength"],
        "items": [
            {"item_id": "20301", "module_id": "10301", "title": "Video: AWS Global Infrastructure - Regions, Availability Zones & Edge Locations", "type": "ExternalTool", "url": "https://awsacademy.instructure.com/courses/183194/pages/m3-video-regions-azs-edge-locations", "position": 1, "is_completed": True, "time_estimate_mins": 20},
            {"item_id": "20302", "module_id": "10301", "title": "Student Guide: Selecting AWS Regions and Fault Tolerance", "type": "File", "url": "https://awsacademy.instructure.com/courses/183194/files/m3-student-guide-global-infrastructure.pdf", "position": 2, "is_completed": False, "time_estimate_mins": 25},
            {"item_id": "20303", "module_id": "10301", "title": "Module 3 Knowledge Check", "type": "Quiz", "url": "https://awsacademy.instructure.com/courses/183194/quizzes/m3-knowledge-check", "position": 3, "is_completed": False, "time_estimate_mins": 15}
        ]
    },
    {
        "module_id": "10401",
        "course_id": "183194",
        "module_number": 4,
        "title": "Module 4 - AWS Cloud Security",
        "description": "Dive deep into the AWS Shared Responsibility Model, AWS IAM (users, groups, roles, policies, MFA), AWS Organizations Service Control Policies (SCPs), AWS Shield, AWS WAF, AWS KMS, and AWS Artifact.",
        "is_core_module": True,
        "order": 5,
        "has_lab": True,
        "lab_id": "lab_1",
        "key_aws_services": ["AWS IAM", "AWS Shield", "AWS WAF", "AWS KMS", "AWS Artifact", "AWS Secrets Manager", "Amazon Inspector"],
        "topics": ["Shared Responsibility Model (Security OF vs IN the Cloud)", "IAM Users, Groups, Roles & Policies", "Multi-Factor Authentication (MFA)", "AWS Shield DDoS Protection", "AWS WAF Web Application Firewall", "Encryption At Rest & In Transit (AWS KMS)", "Compliance Reports via AWS Artifact"],
        "items": [
            {"item_id": "20401", "module_id": "10401", "title": "Video: AWS Shared Responsibility Model & IAM", "type": "ExternalTool", "url": "https://awsacademy.instructure.com/courses/183194/pages/m4-video-shared-responsibility-model", "position": 1, "is_completed": True, "time_estimate_mins": 25},
            {"item_id": "20402", "module_id": "10401", "title": "Student Guide: IAM Policies, MFA, KMS, AWS Shield & WAF", "type": "File", "url": "https://awsacademy.instructure.com/courses/183194/files/m4-student-guide-cloud-security.pdf", "position": 2, "is_completed": True, "time_estimate_mins": 30},
            {"item_id": "20403", "module_id": "10401", "title": "Lab 1 - Introduction to AWS IAM", "type": "ExternalTool", "url": "https://awsacademy.instructure.com/courses/183194/assignments/lab-1-introduction-to-aws-iam", "position": 3, "is_completed": True, "time_estimate_mins": 45},
            {"item_id": "20404", "module_id": "10401", "title": "Module 4 Knowledge Check", "type": "Quiz", "url": "https://awsacademy.instructure.com/courses/183194/quizzes/m4-knowledge-check", "position": 4, "is_completed": True, "time_estimate_mins": 15}
        ]
    },
    {
        "module_id": "10501",
        "course_id": "183194",
        "module_number": 5,
        "title": "Module 5 - Networking and Content Delivery",
        "description": "Master virtual private clouds (Amazon VPC), public and private subnets, Internet Gateways (IGW), NAT Gateways, Route Tables, Security Groups (stateful), Network ACLs (stateless), Amazon Route 53 (DNS), and Amazon CloudFront (CDN).",
        "is_core_module": True,
        "order": 6,
        "has_lab": True,
        "lab_id": "lab_2",
        "key_aws_services": ["Amazon VPC", "Internet Gateway", "NAT Gateway", "Route Tables", "Security Groups", "Network ACLs", "Amazon Route 53", "Amazon CloudFront"],
        "topics": ["VPC CIDR Blocks and Subnets", "Public Subnets vs Private Subnets", "Internet Gateways & NAT Gateways", "Stateful Security Groups vs Stateless Network ACLs", "Amazon Route 53 DNS Routing", "Amazon CloudFront Content Delivery Network"],
        "items": [
            {"item_id": "20501", "module_id": "10501", "title": "Video: Amazon VPC, Subnets, Gateways & Route Tables", "type": "ExternalTool", "url": "https://awsacademy.instructure.com/courses/183194/pages/m5-video-vpc-subnets-routing", "position": 1, "is_completed": True, "time_estimate_mins": 25},
            {"item_id": "20502", "module_id": "10501", "title": "Student Guide: VPC Security Groups, Network ACLs, Route 53, CloudFront", "type": "File", "url": "https://awsacademy.instructure.com/courses/183194/files/m5-student-guide-networking.pdf", "position": 2, "is_completed": False, "time_estimate_mins": 35},
            {"item_id": "20503", "module_id": "10501", "title": "Lab 2 - Build your VPC and Launch a Web Server", "type": "ExternalTool", "url": "https://awsacademy.instructure.com/courses/183194/assignments/lab-2-build-your-vpc-and-launch-a-web-server", "position": 3, "is_completed": False, "time_estimate_mins": 60},
            {"item_id": "20504", "module_id": "10501", "title": "Module 5 Knowledge Check", "type": "Quiz", "url": "https://awsacademy.instructure.com/courses/183194/quizzes/m5-knowledge-check", "position": 4, "is_completed": False, "time_estimate_mins": 15}
        ]
    },
    {
        "module_id": "10601",
        "course_id": "183194",
        "module_number": 6,
        "title": "Module 6 - Compute",
        "description": "Analyze AWS compute options: Amazon EC2 instance families, purchasing models (On-Demand, Savings Plans, Reserved, Spot, Dedicated Hosts), AWS Lambda serverless execution, containers with ECS, EKS, and AWS Fargate, and AWS Elastic Beanstalk PaaS.",
        "is_core_module": True,
        "order": 7,
        "has_lab": True,
        "lab_id": "lab_3",
        "key_aws_services": ["Amazon EC2", "AWS Lambda", "Amazon ECS", "Amazon EKS", "AWS Fargate", "AWS Elastic Beanstalk"],
        "topics": ["Amazon EC2 Instance Types (Compute, Memory, Storage, General)", "EC2 Pricing Models (On-Demand, Spot, Reserved, Dedicated)", "Serverless Compute with AWS Lambda", "Container Orchestration (ECS, EKS, Fargate)", "AWS Elastic Beanstalk Application Deployment"],
        "items": [
            {"item_id": "20601", "module_id": "10601", "title": "Video: Amazon EC2 Instances, AWS Lambda & Containers", "type": "ExternalTool", "url": "https://awsacademy.instructure.com/courses/183194/pages/m6-video-ec2-lambda-containers", "position": 1, "is_completed": False, "time_estimate_mins": 25},
            {"item_id": "20602", "module_id": "10601", "title": "Student Guide: EC2 Pricing Options (On-Demand, Reserved, Spot), ECS, EKS, Fargate, Elastic Beanstalk", "type": "File", "url": "https://awsacademy.instructure.com/courses/183194/files/m6-student-guide-compute.pdf", "position": 2, "is_completed": False, "time_estimate_mins": 35},
            {"item_id": "20603", "module_id": "10601", "title": "Lab 3 - Introduction to Amazon EC2", "type": "ExternalTool", "url": "https://awsacademy.instructure.com/courses/183194/assignments/lab-3-introduction-to-amazon-ec2", "position": 3, "is_completed": False, "time_estimate_mins": 45},
            {"item_id": "20604", "module_id": "10601", "title": "Module 6 Knowledge Check", "type": "Quiz", "url": "https://awsacademy.instructure.com/courses/183194/quizzes/m6-knowledge-check", "position": 4, "is_completed": False, "time_estimate_mins": 15}
        ]
    },
    {
        "module_id": "10701",
        "course_id": "183194",
        "module_number": 7,
        "title": "Module 7 - Storage",
        "description": "Differentiate Amazon S3 object storage (Standard, Intelligent-Tiering, Standard-IA, One Zone-IA, Glacier Instant/Flexible/Deep Archive), Amazon EBS block storage (gp3, io2, st1, sc1), Amazon EFS network file systems, and AWS Storage Gateway hybrid solutions.",
        "is_core_module": True,
        "order": 8,
        "has_lab": True,
        "lab_id": "lab_4",
        "key_aws_services": ["Amazon S3", "Amazon EBS", "Amazon EFS", "Amazon S3 Glacier", "AWS Storage Gateway"],
        "topics": ["Object Storage vs Block Storage vs File Storage", "Amazon S3 Storage Classes & Lifecycle Rules", "Amazon EBS Volume Types & Snapshots", "Amazon EFS Shared File Storage", "AWS Snowball, Snowmobile & Storage Gateway"],
        "items": [
            {"item_id": "20701", "module_id": "10701", "title": "Video: Amazon S3, EBS, and EFS Storage Options", "type": "ExternalTool", "url": "https://awsacademy.instructure.com/courses/183194/pages/m7-video-ebs-s3-efs", "position": 1, "is_completed": False, "time_estimate_mins": 25},
            {"item_id": "20702", "module_id": "10701", "title": "Student Guide: S3 Storage Classes, Lifecycle Policies, EBS Snapshots, AWS Storage Gateway", "type": "File", "url": "https://awsacademy.instructure.com/courses/183194/files/m7-student-guide-storage.pdf", "position": 2, "is_completed": False, "time_estimate_mins": 35},
            {"item_id": "20703", "module_id": "10701", "title": "Lab 4 - Working with EBS", "type": "ExternalTool", "url": "https://awsacademy.instructure.com/courses/183194/assignments/lab-4-working-with-ebs", "position": 3, "is_completed": False, "time_estimate_mins": 45},
            {"item_id": "20704", "module_id": "10701", "title": "Module 7 Knowledge Check", "type": "Quiz", "url": "https://awsacademy.instructure.com/courses/183194/quizzes/m7-knowledge-check", "position": 4, "is_completed": False, "time_estimate_mins": 15}
        ]
    },
    {
        "module_id": "10801",
        "course_id": "183194",
        "module_number": 8,
        "title": "Module 8 - Databases",
        "description": "Explore managed databases: relational databases via Amazon RDS and Amazon Aurora, key-value and document databases with Amazon DynamoDB, data warehousing with Amazon Redshift, in-memory caching with Amazon ElastiCache, and database migration via AWS DMS.",
        "is_core_module": True,
        "order": 9,
        "has_lab": True,
        "lab_id": "lab_5",
        "key_aws_services": ["Amazon RDS", "Amazon Aurora", "Amazon DynamoDB", "Amazon Redshift", "Amazon ElastiCache", "AWS DMS"],
        "topics": ["Relational (SQL) vs Non-Relational (NoSQL)", "Amazon RDS Multi-AZ Failover & Read Replicas", "Amazon Aurora High-Performance Engine", "Amazon DynamoDB Serverless NoSQL Tables", "Amazon Redshift Columnar Data Warehouse", "Amazon ElastiCache (Redis / Memcached)", "AWS Database Migration Service (AWS DMS)"],
        "items": [
            {"item_id": "20801", "module_id": "10801", "title": "Video: Managed Databases - RDS, Aurora & DynamoDB", "type": "ExternalTool", "url": "https://awsacademy.instructure.com/courses/183194/pages/m8-video-relational-vs-nosql", "position": 1, "is_completed": False, "time_estimate_mins": 25},
            {"item_id": "20802", "module_id": "10801", "title": "Student Guide: Amazon RDS Multi-AZ, Read Replicas, DynamoDB, Redshift & ElastiCache", "type": "File", "url": "https://awsacademy.instructure.com/courses/183194/files/m8-student-guide-databases.pdf", "position": 2, "is_completed": False, "time_estimate_mins": 35},
            {"item_id": "20803", "module_id": "10801", "title": "Lab 5 - Build a Database Server", "type": "ExternalTool", "url": "https://awsacademy.instructure.com/courses/183194/assignments/lab-5-build-a-database-server", "position": 3, "is_completed": False, "time_estimate_mins": 50},
            {"item_id": "20804", "module_id": "10801", "title": "Module 8 Knowledge Check", "type": "Quiz", "url": "https://awsacademy.instructure.com/courses/183194/quizzes/m8-knowledge-check", "position": 4, "is_completed": False, "time_estimate_mins": 15}
        ]
    },
    {
        "module_id": "10901",
        "course_id": "183194",
        "module_number": 9,
        "title": "Module 9 - Cloud Architecture",
        "description": "Adopt the AWS Well-Architected Framework: the six pillars (Operational Excellence, Security, Reliability, Performance Efficiency, Cost Optimization, Sustainability), design principles, and automated architecture reviews.",
        "is_core_module": True,
        "order": 10,
        "has_lab": False,
        "key_aws_services": ["AWS Well-Architected Tool", "AWS Trusted Advisor", "AWS CloudFormation"],
        "topics": ["Six Pillars of AWS Well-Architected Framework", "Design Principles (Design for Failure, Loose Coupling)", "Reliability & Disaster Recovery Strategies", "AWS Trusted Advisor Best Practice Checks", "Infrastructure as Code with AWS CloudFormation"],
        "items": [
            {"item_id": "20901", "module_id": "10901", "title": "Video: AWS Well-Architected Framework 6 Pillars", "type": "ExternalTool", "url": "https://awsacademy.instructure.com/courses/183194/pages/m9-video-well-architected-framework", "position": 1, "is_completed": False, "time_estimate_mins": 25},
            {"item_id": "20902", "module_id": "10901", "title": "Student Guide: Operational Excellence, Security, Reliability, Performance, Cost & Sustainability", "type": "File", "url": "https://awsacademy.instructure.com/courses/183194/files/m9-student-guide-architecture.pdf", "position": 2, "is_completed": False, "time_estimate_mins": 35},
            {"item_id": "20903", "module_id": "10901", "title": "Module 9 Knowledge Check", "type": "Quiz", "url": "https://awsacademy.instructure.com/courses/183194/quizzes/m9-knowledge-check", "position": 3, "is_completed": False, "time_estimate_mins": 15}
        ]
    },
    {
        "module_id": "11001",
        "course_id": "183194",
        "module_number": 10,
        "title": "Module 10 - Auto Scaling and Monitoring",
        "description": "Implement elastic, resilient architectures using Amazon CloudWatch metrics, alarms, and dashboards, AWS CloudTrail API auditing, Elastic Load Balancing (ALB, NLB, GLB), and EC2 Auto Scaling groups.",
        "is_core_module": True,
        "order": 11,
        "has_lab": True,
        "lab_id": "lab_6",
        "key_aws_services": ["Amazon CloudWatch", "AWS CloudTrail", "Elastic Load Balancing", "Amazon EC2 Auto Scaling"],
        "topics": ["Amazon CloudWatch Metrics, Alarms & Logs", "AWS CloudTrail API Governance & Governance Auditing", "Application Load Balancer (ALB) vs Network Load Balancer (NLB)", "Auto Scaling Groups (Min, Desired, Max Capacity)", "Dynamic, Target Tracking & Scheduled Scaling Policies"],
        "items": [
            {"item_id": "21001", "module_id": "11001", "title": "Video: Amazon CloudWatch, Elastic Load Balancing, EC2 Auto Scaling", "type": "ExternalTool", "url": "https://awsacademy.instructure.com/courses/183194/pages/m10-video-cloudwatch-autoscaling-elb", "position": 1, "is_completed": False, "time_estimate_mins": 25},
            {"item_id": "21002", "module_id": "11001", "title": "Student Guide: Metrics, Alarms, Scaling Policies, Target Groups, Health Checks", "type": "File", "url": "https://awsacademy.instructure.com/courses/183194/files/m10-student-guide-scaling-monitoring.pdf", "position": 2, "is_completed": False, "time_estimate_mins": 35},
            {"item_id": "21003", "module_id": "11001", "title": "Lab 6 - Scale and Load Balance your Architecture", "type": "ExternalTool", "url": "https://awsacademy.instructure.com/courses/183194/assignments/lab-6-scale-and-load-balance-your-architecture", "position": 3, "is_completed": False, "time_estimate_mins": 60},
            {"item_id": "21004", "module_id": "11001", "title": "Module 10 Knowledge Check", "type": "Quiz", "url": "https://awsacademy.instructure.com/courses/183194/quizzes/m10-knowledge-check", "position": 4, "is_completed": False, "time_estimate_mins": 15}
        ]
    },
    {
        "module_id": "11101",
        "course_id": "183194",
        "module_number": 11,
        "title": "Course Assessment & Practice Exams",
        "description": "Preparation resources and practice questions for the official AWS Academy Cloud Foundations end-of-course assessment.",
        "is_core_module": False,
        "order": 12,
        "has_lab": False,
        "key_aws_services": ["AWS Certified Cloud Practitioner"],
        "topics": ["End of Course Assessment", "Certification Readiness"],
        "items": [
            {"item_id": "21101", "module_id": "11101", "title": "AWS Academy Cloud Foundations - Final Course Assessment", "type": "Quiz", "url": "https://awsacademy.instructure.com/courses/183194/quizzes/course-assessment", "position": 1, "is_completed": False, "time_estimate_mins": 90}
        ]
    },
    {
        "module_id": "11201",
        "course_id": "183194",
        "module_number": 12,
        "title": "Sandbox Environment",
        "description": "AWS Academy Learner Lab Sandbox environment instructions, budget monitoring, and safety rules.",
        "is_core_module": False,
        "order": 13,
        "has_lab": False,
        "key_aws_services": ["AWS Learner Lab"],
        "topics": ["Learner Lab Sandbox", "Budget Constraints", "Allowed AWS Services"],
        "items": [
            {"item_id": "21201", "module_id": "11201", "title": "AWS Academy Learner Lab Sandbox", "type": "ExternalTool", "url": "https://awsacademy.instructure.com/courses/183194/assignments/aws-academy-learner-lab", "position": 1, "is_completed": True, "time_estimate_mins": 15}
        ]
    },
    {
        "module_id": "11301",
        "course_id": "183194",
        "module_number": 13,
        "title": "Certification Resources",
        "description": "Exam guide, official practice questions, and voucher guidance for the AWS Certified Cloud Practitioner (CLF-C02) examination.",
        "is_core_module": False,
        "order": 14,
        "has_lab": False,
        "key_aws_services": ["AWS Training and Certification"],
        "topics": ["CLF-C02 Exam Guide", "Domain Weightings", "Pearson VUE Registration"],
        "items": [
            {"item_id": "21301", "module_id": "11301", "title": "AWS Certified Cloud Practitioner (CLF-C02) Exam Guide & Discount Voucher Information", "type": "Page", "url": "https://awsacademy.instructure.com/courses/183194/pages/aws-certified-cloud-practitioner-exam-guide", "position": 1, "is_completed": False, "time_estimate_mins": 20}
        ]
    },
    {
        "module_id": "11401",
        "course_id": "183194",
        "module_number": 14,
        "title": "Feedback, Badges and Completion Certificates",
        "description": "Steps to claim your digital Credly badge and downloadable course completion certificate.",
        "is_core_module": False,
        "order": 15,
        "has_lab": False,
        "key_aws_services": ["Credly Digital Badges"],
        "topics": ["Credly Badges", "Course Completion Certificate", "Course Feedback Survey"],
        "items": [
            {"item_id": "21401", "module_id": "11401", "title": "Claiming your Credly Digital Badge & Course Certificate", "type": "Page", "url": "https://awsacademy.instructure.com/courses/183194/pages/claiming-your-credly-digital-badge-and-certificate", "position": 1, "is_completed": False, "time_estimate_mins": 10},
            {"item_id": "21402", "module_id": "11401", "title": "End of Course Student Feedback Survey", "type": "Quiz", "url": "https://awsacademy.instructure.com/courses/183194/quizzes/course-feedback-survey", "position": 2, "is_completed": False, "time_estimate_mins": 10}
        ]
    },
    {
        "module_id": "11501",
        "course_id": "183194",
        "module_number": 15,
        "title": "AWS Terms and Conditions Resources",
        "description": "AWS Customer Agreement, Service Terms, and Acceptable Use Policy compliance.",
        "is_core_module": False,
        "order": 16,
        "has_lab": False,
        "key_aws_services": ["AWS Terms"],
        "topics": ["AWS Customer Agreement", "Acceptable Use Policy"],
        "items": [
            {"item_id": "21501", "module_id": "11501", "title": "AWS Customer Agreement & Acceptable Use Policy", "type": "ExternalUrl", "url": "https://aws.amazon.com/terms/", "position": 1, "is_completed": True, "time_estimate_mins": 10}
        ]
    }
]

# Rich textbook learning material chunks for verified RAG citations
COURSE_TEXTBOOK_CHUNKS: List[Dict[str, Any]] = [
    {
        "chunk_id": "txt_chunk_101_1",
        "doc_id": "doc_m1_guide",
        "course_id": "183194",
        "module_id": "10101",
        "module_title": "Module 1 - Cloud Concepts Overview",
        "document_name": "m1-student-guide-cloud-concepts.pdf",
        "page_number": 4,
        "content": "Cloud computing is the on-demand delivery of IT resources over the internet with pay-as-you-go pricing. Instead of buying, owning, and maintaining physical data centers and servers, organizations can access technology services, such as computing power, storage, and databases, on an as-needed basis from a cloud provider like Amazon Web Services (AWS).",
        "source_url": "https://awsacademy.instructure.com/courses/183194/files/m1-student-guide-cloud-concepts.pdf"
    },
    {
        "chunk_id": "txt_chunk_101_2",
        "doc_id": "doc_m1_guide",
        "course_id": "183194",
        "module_id": "10101",
        "module_title": "Module 1 - Cloud Concepts Overview",
        "document_name": "m1-student-guide-cloud-concepts.pdf",
        "page_number": 8,
        "content": "Six Advantages of Cloud Computing: 1. Trade capital expense (CapEx) for variable expense (OpEx). 2. Benefit from massive economies of scale. 3. Stop guessing capacity. 4. Increase speed and agility. 5. Stop spending money running and maintaining data centers. 6. Go global in minutes using AWS Global Infrastructure.",
        "source_url": "https://awsacademy.instructure.com/courses/183194/files/m1-student-guide-cloud-concepts.pdf"
    },
    {
        "chunk_id": "txt_chunk_102_1",
        "doc_id": "doc_m2_guide",
        "course_id": "183194",
        "module_id": "10201",
        "module_title": "Module 2 - Cloud Economics and Billing",
        "document_name": "m2-student-guide-billing-budgets.pdf",
        "page_number": 12,
        "content": "AWS Fundamental Pricing Principles: 1. Pay as you go: pay only for the individual services you need, for as long as you use them. 2. Save when you commit: commit to 1- or 3-year terms for EC2 Savings Plans or Reserved Instances to save up to 72% compared to On-Demand. 3. Pay less by using more: tiered pricing discounts for Amazon S3 storage and data transfer.",
        "source_url": "https://awsacademy.instructure.com/courses/183194/files/m2-student-guide-billing-budgets.pdf"
    },
    {
        "chunk_id": "txt_chunk_102_2",
        "doc_id": "doc_m2_guide",
        "course_id": "183194",
        "module_id": "10201",
        "module_title": "Module 2 - Cloud Economics and Billing",
        "document_name": "m2-student-guide-billing-budgets.pdf",
        "page_number": 18,
        "content": "AWS Organizations enables consolidated billing across multiple AWS accounts. Consolidated billing aggregates usage across accounts to share volume pricing discounts, provides a single invoice, and allows centralized management of security policies using Service Control Policies (SCPs).",
        "source_url": "https://awsacademy.instructure.com/courses/183194/files/m2-student-guide-billing-budgets.pdf"
    },
    {
        "chunk_id": "txt_chunk_103_1",
        "doc_id": "doc_m3_guide",
        "course_id": "183194",
        "module_id": "10301",
        "module_title": "Module 3 - AWS Global Infrastructure Overview",
        "document_name": "m3-student-guide-global-infrastructure.pdf",
        "page_number": 6,
        "content": "An AWS Region is a physical geographical location in the world where AWS clusters data centers. Each AWS Region consists of multiple, isolated, and physically separate Availability Zones (AZs) connected with low-latency, high-throughput, and redundant private networking. Criteria for choosing a Region include: compliance with legal requirements, proximity to customers (latency), available services, and cost differences.",
        "source_url": "https://awsacademy.instructure.com/courses/183194/files/m3-student-guide-global-infrastructure.pdf"
    },
    {
        "chunk_id": "txt_chunk_104_1",
        "doc_id": "doc_m4_guide",
        "course_id": "183194",
        "module_id": "10401",
        "module_title": "Module 4 - AWS Cloud Security",
        "document_name": "m4-student-guide-cloud-security.pdf",
        "page_number": 5,
        "content": "AWS Shared Responsibility Model: AWS is responsible for 'Security OF the Cloud' - protecting the infrastructure that runs all of the services offered in the AWS Cloud (hardware, software, networking, and facilities). The customer is responsible for 'Security IN the Cloud' - customer data, identity and access management (IAM), operating system configuration, firewall and network configuration (Security Groups), and client-side and server-side data encryption.",
        "source_url": "https://awsacademy.instructure.com/courses/183194/files/m4-student-guide-cloud-security.pdf"
    },
    {
        "chunk_id": "txt_chunk_104_2",
        "doc_id": "doc_m4_guide",
        "course_id": "183194",
        "module_id": "10401",
        "module_title": "Module 4 - AWS Cloud Security",
        "document_name": "m4-student-guide-cloud-security.pdf",
        "page_number": 14,
        "content": "AWS Identity and Access Management (IAM): Best practices include locking away AWS account root user credentials, creating individual IAM users with least privilege, using user groups to assign permissions, granting temporary permissions with IAM roles, and enabling Multi-Factor Authentication (MFA) for privileged users.",
        "source_url": "https://awsacademy.instructure.com/courses/183194/files/m4-student-guide-cloud-security.pdf"
    },
    {
        "chunk_id": "txt_chunk_105_1",
        "doc_id": "doc_m5_guide",
        "course_id": "183194",
        "module_id": "10501",
        "module_title": "Module 5 - Networking and Content Delivery",
        "document_name": "m5-student-guide-networking.pdf",
        "page_number": 11,
        "content": "Amazon VPC allows you to provision a logically isolated section of the AWS Cloud. Subnets reside inside a single Availability Zone. A Public Subnet has a route table directing 0.0.0.0/0 to an Internet Gateway (IGW). A Private Subnet routes outbound internet traffic through a NAT Gateway located in a Public Subnet.",
        "source_url": "https://awsacademy.instructure.com/courses/183194/files/m5-student-guide-networking.pdf"
    },
    {
        "chunk_id": "txt_chunk_105_2",
        "doc_id": "doc_m5_guide",
        "course_id": "183194",
        "module_id": "10501",
        "module_title": "Module 5 - Networking and Content Delivery",
        "document_name": "m5-student-guide-networking.pdf",
        "page_number": 22,
        "content": "Security Groups vs Network Access Control Lists (NACLs): Security Groups operate at the instance level, support allow rules only, and are stateful (inbound return traffic is allowed automatically). NACLs operate at the subnet level, support both allow and deny rules, evaluate rules in numerical order, and are stateless (return traffic must be explicitly allowed).",
        "source_url": "https://awsacademy.instructure.com/courses/183194/files/m5-student-guide-networking.pdf"
    },
    {
        "chunk_id": "txt_chunk_106_1",
        "doc_id": "doc_m6_guide",
        "course_id": "183194",
        "module_id": "10601",
        "module_title": "Module 6 - Compute",
        "document_name": "m6-student-guide-compute.pdf",
        "page_number": 9,
        "content": "Amazon EC2 Instance Purchasing Options: 1. On-Demand Instances: pay by the second with no long-term commitment (unpredictable, short-term workloads). 2. Reserved Instances & Savings Plans: commit to a 1-year or 3-year term for up to 72% discount (steady-state workloads). 3. Spot Instances: request unused EC2 capacity for up to 90% discount (fault-tolerant, flexible workloads that can tolerate interruption). 4. Dedicated Hosts: physical servers dedicated for your use to satisfy compliance and licensing.",
        "source_url": "https://awsacademy.instructure.com/courses/183194/files/m6-student-guide-compute.pdf"
    },
    {
        "chunk_id": "txt_chunk_107_1",
        "doc_id": "doc_m7_guide",
        "course_id": "183194",
        "module_id": "10701",
        "module_title": "Module 7 - Storage",
        "document_name": "m7-student-guide-storage.pdf",
        "page_number": 15,
        "content": "Amazon S3 Storage Classes: S3 Standard (frequently accessed data, 99.999999999% 11 9s durability across >=3 AZs), S3 Intelligent-Tiering (automatically moves objects between frequent and infrequent tiers without retrieval fees), S3 Standard-IA (infrequently accessed, rapid retrieval), S3 One Zone-IA (lower cost, single AZ, reproducible data), S3 Glacier Instant Retrieval, S3 Glacier Flexible Retrieval (minutes to hours), and S3 Glacier Deep Archive (lowest cost, retrieval in 12 hours).",
        "source_url": "https://awsacademy.instructure.com/courses/183194/files/m7-student-guide-storage.pdf"
    },
    {
        "chunk_id": "txt_chunk_108_1",
        "doc_id": "doc_m8_guide",
        "course_id": "183194",
        "module_id": "10801",
        "module_title": "Module 8 - Databases",
        "document_name": "m8-student-guide-databases.pdf",
        "page_number": 8,
        "content": "Amazon RDS Multi-AZ Deployments: Amazon RDS automatically creates a primary DB instance and synchronously replicates data to a standby instance in a different Availability Zone. In event of planned maintenance or unplanned failure, Amazon RDS automatically fails over to the standby instance without manual administrative intervention, preserving DNS endpoint connectivity.",
        "source_url": "https://awsacademy.instructure.com/courses/183194/files/m8-student-guide-databases.pdf"
    },
    {
        "chunk_id": "txt_chunk_109_1",
        "doc_id": "doc_m9_guide",
        "course_id": "183194",
        "module_id": "10901",
        "module_title": "Module 9 - Cloud Architecture",
        "document_name": "m9-student-guide-architecture.pdf",
        "page_number": 4,
        "content": "The AWS Well-Architected Framework helps cloud architects build secure, high-performing, resilient, and efficient infrastructure. The six pillars are: 1. Operational Excellence: run and monitor systems to deliver business value. 2. Security: protect information, systems, and assets. 3. Reliability: recover from disruptions and meet demand. 4. Performance Efficiency: use compute resources efficiently. 5. Cost Optimization: avoid unnecessary spending. 6. Sustainability: minimize environmental impact.",
        "source_url": "https://awsacademy.instructure.com/courses/183194/files/m9-student-guide-architecture.pdf"
    },
    {
        "chunk_id": "txt_chunk_110_1",
        "doc_id": "doc_m10_guide",
        "course_id": "183194",
        "module_id": "11001",
        "module_title": "Module 10 - Auto Scaling and Monitoring",
        "document_name": "m10-student-guide-scaling-monitoring.pdf",
        "page_number": 12,
        "content": "Amazon CloudWatch monitors AWS resources and applications in real-time. CloudWatch collects metrics, logs, and events, and allows you to configure alarms that trigger notifications (via SNS) or automated actions (such as EC2 Auto Scaling policy execution) when metrics breach defined thresholds.",
        "source_url": "https://awsacademy.instructure.com/courses/183194/files/m10-student-guide-scaling-monitoring.pdf"
    }
]

async def seed_course_data():
    """Initializes the MongoDB collections with course modules, items, and vector knowledge chunks."""
    db = get_database()
    
    # Check if modules already exist
    existing_count = await db.modules.count_documents({"course_id": "183194"})
    if existing_count == 0:
        for mod in COURSE_SEED_MODULES:
            await db.modules.update_one(
                {"course_id": "183194", "module_id": mod["module_id"]},
                {"$set": mod},
                upsert=True
            )

        # Upsert Course
        course_record = {
            "course_id": "183194",
            "name": "AWS Academy Cloud Foundations",
            "code": "ACF-183194",
            "canvas_url": "https://awsacademy.instructure.com/courses/183194/modules",
            "total_modules": 10,
            "modules": COURSE_SEED_MODULES
        }
        await db.courses.update_one({"course_id": "183194"}, {"$set": course_record}, upsert=True)

    # Seed textbook chunks into vector store
    chunk_count = await db.document_chunks.count_documents({"course_id": "183194"})
    if chunk_count == 0:
        await vector_store.add_chunks(COURSE_TEXTBOOK_CHUNKS)
