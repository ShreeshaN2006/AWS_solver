from typing import List, Dict, Any, Optional
from datetime import datetime
from app.database import get_database
from app.models.lab import LabDetail, LabStep, UserLabProgress, LabTroubleshootResponse

# Detailed definitions for the six AWS Academy Cloud Foundations Labs
COURSE_LABS: List[Dict[str, Any]] = [
    {
        "lab_id": "lab_1",
        "lab_number": 1,
        "title": "Introduction to AWS IAM",
        "duration_mins": 45,
        "module_id": "10401",
        "module_title": "Module 4 - AWS Cloud Security",
        "objective": "Learn how to manage AWS Identity and Access Management (IAM) users, groups, and policies to control access to AWS services, apply least-privilege permissions, and inspect sign-in activity.",
        "aws_services": ["AWS IAM", "AWS CloudTrail", "AWS Organizations"],
        "architecture_summary": "Simulated multi-role IAM hierarchy with Admin and Developer groups, managed policies for Amazon S3 read-only access, and security enforcement via Multi-Factor Authentication (MFA).",
        "final_summary": "You successfully configured IAM user accounts, assigned users to dedicated administrative and developer groups, attached managed policies with least-privilege S3 permissions, and tested credential-based console sign-in.",
        "steps": [
            {
                "step_number": 1,
                "title": "Explore Existing IAM Users and Groups",
                "objective": "Inspect pre-created test users in the AWS Management Console.",
                "console_navigation": "AWS Management Console -> Search 'IAM' -> Navigation pane -> Users & User Groups.",
                "instructions": [
                    "In the AWS Console search bar, type 'IAM' and select IAM.",
                    "In the left-hand navigation pane, select 'Users'.",
                    "Observe existing users (e.g. user-1, user-2, user-3).",
                    "Click on user-1 and select the 'Permissions' tab to verify that no direct policies are attached."
                ],
                "expected_result": "Three distinct user identities are displayed in the Users table with Status: Active and MFA: Not enabled.",
                "common_pitfalls": [
                    "Attaching policies directly to individual users instead of user groups (violating AWS least privilege best practice).",
                    "Using the AWS Account root user for routine administrative tasks."
                ],
                "verification_check": "Verify that user-1, user-2, and user-3 are present in the IAM Users table."
            },
            {
                "step_number": 2,
                "title": "Create User Groups and Assign Managed Policies",
                "objective": "Create 'S3-Support' and 'EC2-Support' groups with appropriate AWS managed policies.",
                "console_navigation": "IAM -> User groups -> Create group.",
                "instructions": [
                    "In the IAM navigation pane, click 'User groups' -> 'Create group'.",
                    "Name the group 'S3-Support'.",
                    "In the 'Attach permissions policies' search bar, type 'AmazonS3ReadOnlyAccess' and select its checkbox.",
                    "Click 'Create group'.",
                    "Repeat the procedure to create an 'EC2-Support' group with 'AmazonEC2ReadOnlyAccess'."
                ],
                "expected_result": "Two user groups appear in the User Groups list with policy counts = 1.",
                "common_pitfalls": [
                    "Accidentally selecting 'AmazonS3FullAccess' instead of 'AmazonS3ReadOnlyAccess'.",
                    "Typing the group name with spaces or incorrect capitalization."
                ],
                "verification_check": "Confirm that 'S3-Support' has 'AmazonS3ReadOnlyAccess' policy attached."
            },
            {
                "step_number": 3,
                "title": "Add Users to Groups",
                "objective": "Assign user-1 to S3-Support and user-2 to EC2-Support.",
                "console_navigation": "IAM -> User groups -> S3-Support -> Users tab -> Add users.",
                "instructions": [
                    "Select the 'S3-Support' group.",
                    "Click 'Add users' button.",
                    "Select the checkbox next to 'user-1' and click 'Add users'.",
                    "Navigate back to User groups, select 'EC2-Support', and add 'user-2'."
                ],
                "expected_result": "user-1 is a member of S3-Support and inherits S3 read permissions; user-2 inherits EC2 read permissions.",
                "common_pitfalls": [
                    "Adding the wrong user to the group.",
                    "Forgetting to click the final confirmation 'Add users' button."
                ],
                "verification_check": "Inspect 'S3-Support' group and confirm 'user-1' is listed under the Users tab."
            },
            {
                "step_number": 4,
                "title": "Test IAM Permissions via Sign-in URL",
                "objective": "Sign in as user-1 to verify authorized S3 access and unauthorized EC2 access.",
                "console_navigation": "IAM Dashboard -> Copy IAM users sign-in URL -> Open Incognito/Private browser window.",
                "instructions": [
                    "Copy the 12-digit Account ID or custom sign-in alias URL from the IAM Dashboard.",
                    "In a private browser window, navigate to the sign-in URL.",
                    "Sign in as user-1 with provided lab credentials.",
                    "Navigate to Amazon S3: observe you can view buckets.",
                    "Navigate to Amazon EC2: observe 'API Error / UnauthorizedOperation' warning message."
                ],
                "expected_result": "user-1 can view S3 buckets, but receives an Explicit Deny / Authorization Failure when viewing EC2 instances.",
                "common_pitfalls": [
                    "Signing in with the root email instead of the 12-digit account ID sign-in portal.",
                    "Confusing default deny behavior with an account outage."
                ],
                "verification_check": "Confirm receipt of Access Denied error when user-1 attempts to list EC2 instances."
            },
            {
                "step_number": 5,
                "title": "Enable Password Policy & Clean Up",
                "objective": "Configure account password policy requirements and complete the lab verification.",
                "console_navigation": "IAM -> Account settings -> Password policy -> Edit.",
                "instructions": [
                    "In the primary administrator console, open IAM -> Account settings.",
                    "Click 'Edit' under Password policy.",
                    "Set minimum password length to 8 characters and require uppercase, lowercase, and numbers.",
                    "Save changes."
                ],
                "expected_result": "Password policy is updated account-wide.",
                "common_pitfalls": [
                    "Locking existing users out with overly restrictive immediate expiration."
                ],
                "verification_check": "Password policy shows minimum 8 characters with symbol/number enforcement."
            }
        ]
    },
    {
        "lab_id": "lab_2",
        "lab_number": 2,
        "title": "Build your VPC and Launch a Web Server",
        "duration_mins": 60,
        "module_id": "10501",
        "module_title": "Module 5 - Networking and Content Delivery",
        "objective": "Create a custom Virtual Private Cloud (VPC), configure public and private subnets, attach an Internet Gateway, configure route tables, and launch an Apache HTTP server.",
        "aws_services": ["Amazon VPC", "Internet Gateway", "Route Tables", "Security Groups", "Amazon EC2"],
        "architecture_summary": "10.0.0.0/16 VPC with Public Subnet (10.0.0.0/24) connected to the internet via Internet Gateway (IGW), Protected Private Subnet (10.0.1.0/24), and Security Group allowing HTTP (port 80) and SSH (port 22).",
        "final_summary": "You successfully created a custom Amazon VPC network topology, attached an Internet Gateway, configured the public route table (0.0.0.0/0 -> IGW), created a web security group, and launched an EC2 instance that served an active web page.",
        "steps": [
            {
                "step_number": 1,
                "title": "Create a Custom Amazon VPC",
                "objective": "Create a VPC with IPv4 CIDR block 10.0.0.0/16.",
                "console_navigation": "AWS Console -> VPC -> Your VPCs -> Create VPC.",
                "instructions": [
                    "Select 'VPC only'.",
                    "Name tag: 'Lab VPC'.",
                    "IPv4 CIDR: '10.0.0.0/16'.",
                    "Leave Tenancy as Default and click 'Create VPC'."
                ],
                "expected_result": "VPC state transitions to 'Available' with CIDR 10.0.0.0/16.",
                "common_pitfalls": ["Selecting 'VPC and more' when manual step-by-step creation is required."],
                "verification_check": "Lab VPC is listed as Available with ID vpc-xxxx and CIDR 10.0.0.0/16."
            },
            {
                "step_number": 2,
                "title": "Create Public and Private Subnets",
                "objective": "Provision a Public Subnet (10.0.0.0/24) in AZ 1 and Private Subnet (10.0.1.0/24) in AZ 1.",
                "console_navigation": "VPC -> Subnets -> Create subnet.",
                "instructions": [
                    "Choose VPC ID: 'Lab VPC'.",
                    "Subnet 1 Name: 'Public Subnet', AZ: Choose us-east-1a, CIDR: '10.0.0.0/24'.",
                    "Click 'Add new subnet'.",
                    "Subnet 2 Name: 'Private Subnet', AZ: Choose us-east-1a, CIDR: '10.0.1.0/24'.",
                    "Click 'Create subnet'.",
                    "Select 'Public Subnet' -> Actions -> Edit subnet settings -> Enable auto-assign public IPv4 address."
                ],
                "expected_result": "Two subnets are created within Lab VPC with auto-assign public IPv4 enabled on Public Subnet.",
                "common_pitfalls": ["Forgetting to enable auto-assign public IPv4 on the public subnet."],
                "verification_check": "Public Subnet shows 'Auto-assign public IPv4: Yes'."
            },
            {
                "step_number": 3,
                "title": "Create & Attach Internet Gateway",
                "objective": "Attach an Internet Gateway to Lab VPC to enable two-way internet routing.",
                "console_navigation": "VPC -> Internet gateways -> Create internet gateway -> Attach to VPC.",
                "instructions": [
                    "Click 'Create internet gateway'.",
                    "Name tag: 'Lab IGW'.",
                    "Click 'Create internet gateway'.",
                    "Select Actions -> 'Attach to VPC' -> Select 'Lab VPC' -> Click 'Attach internet gateway'."
                ],
                "expected_result": "Lab IGW shows State: 'Attached' to Lab VPC.",
                "common_pitfalls": ["Creating the IGW but forgetting to attach it to the VPC."],
                "verification_check": "Internet Gateway state is 'attached' to Lab VPC."
            },
            {
                "step_number": 4,
                "title": "Configure Public Route Table",
                "objective": "Add a default route (0.0.0.0/0 -> IGW) to the public route table.",
                "console_navigation": "VPC -> Route tables -> Create route table / Edit routes.",
                "instructions": [
                    "Create Route Table: Name 'Public Route Table', VPC 'Lab VPC'.",
                    "Select the 'Routes' tab -> 'Edit routes'.",
                    "Click 'Add route': Destination '0.0.0.0/0', Target 'Internet Gateway' (choose Lab IGW).",
                    "Click 'Save changes'.",
                    "Select 'Subnet associations' tab -> 'Edit subnet associations' -> Select 'Public Subnet' -> Save."
                ],
                "expected_result": "Public Subnet is associated with a route table directing internet traffic to Lab IGW.",
                "common_pitfalls": ["Attaching the default route to the Private Subnet instead."],
                "verification_check": "Public Route Table lists 0.0.0.0/0 pointing to igw-xxxx."
            },
            {
                "step_number": 5,
                "title": "Launch Web Server EC2 Instance & Verify",
                "objective": "Launch an Amazon Linux 2 EC2 instance into Public Subnet with Apache user data script.",
                "console_navigation": "EC2 -> Instances -> Launch instance.",
                "instructions": [
                    "Name: 'Web Server 1', AMI: Amazon Linux 2023 or Amazon Linux 2.",
                    "Instance type: t2.micro or t3.micro.",
                    "Network settings: Select 'Lab VPC', Subnet 'Public Subnet'.",
                    "Firewall (Security Groups): Create Security Group 'Web-SG' allowing HTTP (Port 80) from Anywhere (0.0.0.0/0).",
                    "Expand 'Advanced Details' -> In 'User data' paste:\n#!/bin/bash\nyum update -y\nyum install -y httpd\nsystemctl start httpd\nsystemctl enable httpd\necho '<h1>Hello from AWS Academy Cloud Foundations Lab!</h1>' > /var/www/html/index.html",
                    "Click 'Launch instance'."
                ],
                "expected_result": "Instance launches and reaches 'Running' state. Browsing its Public IPv4 address in a browser displays the Hello page.",
                "common_pitfalls": [
                    "Launching into the default VPC instead of 'Lab VPC'.",
                    "Forgetting HTTP port 80 inbound rule in the security group."
                ],
                "verification_check": "Browser loads http://<Public-IP> and renders the Hello page."
            }
        ]
    },
    {
        "lab_id": "lab_3",
        "lab_number": 3,
        "title": "Introduction to Amazon EC2",
        "duration_mins": 45,
        "module_id": "10601",
        "module_title": "Module 6 - Compute",
        "objective": "Launch an Amazon EC2 Linux instance, configure security groups, attach an Elastic IP address, inspect instance metadata, and examine CloudWatch basic metrics.",
        "aws_services": ["Amazon EC2", "Amazon CloudWatch", "Elastic IP", "Security Groups"],
        "architecture_summary": "Amazon EC2 t2/t3.micro compute instance with attached EBS root volume, protected by a customized security group, and monitored with Amazon CloudWatch.",
        "final_summary": "You launched and configured an Amazon EC2 instance, managed security group firewall rules, attached an Elastic IP address, connected securely, and queried instance metadata.",
        "steps": [
            {
                "step_number": 1,
                "title": "Configure EC2 Instance Launch Options",
                "objective": "Select AMI, instance architecture, and instance type.",
                "console_navigation": "EC2 -> Launch instances.",
                "instructions": [
                    "Name: 'App-Server'.",
                    "Select Amazon Linux AMI.",
                    "Select instance type 't2.micro' (or 't3.micro' based on lab region).",
                    "Key pair: Select 'vockey' or 'Proceed without key pair' as instructed."
                ],
                "expected_result": "Instance configuration prepared with free-tier eligible specs.",
                "common_pitfalls": ["Selecting a large paid instance type not allowed in the learner lab sandbox."],
                "verification_check": "t2.micro / t3.micro selected with Amazon Linux AMI."
            },
            {
                "step_number": 2,
                "title": "Configure Security Group Rules",
                "objective": "Allow inbound SSH (22) and HTTP (80) traffic.",
                "console_navigation": "EC2 -> Launch instances -> Network settings -> Edit.",
                "instructions": [
                    "Create Security Group named 'App-Server-SG'.",
                    "Rule 1: SSH, Port 22, Source: My IP (or Anywhere for sandbox).",
                    "Rule 2: HTTP, Port 80, Source: Anywhere (0.0.0.0/0)."
                ],
                "expected_result": "Firewall configured for web and management access.",
                "common_pitfalls": ["Restricting SSH to a dynamic IP that changes, locking out access."],
                "verification_check": "Security group has inbound rules for ports 22 and 80."
            },
            {
                "step_number": 3,
                "title": "Launch and Monitor Instance Status",
                "objective": "Launch the instance and monitor the 2/2 status checks.",
                "console_navigation": "EC2 -> Instances -> Select App-Server -> Status checks.",
                "instructions": [
                    "Click 'Launch instance'.",
                    "Navigate to the EC2 Instances dashboard.",
                    "Wait for Instance State to change from 'Pending' to 'Running'.",
                    "Confirm 'Status check' displays '2/2 checks passed' (System reachability and Instance reachability)."
                ],
                "expected_result": "Status check column confirms '2/2 checks passed'.",
                "common_pitfalls": ["Attempting to connect before the initialization checks finish."],
                "verification_check": "Status checks show 2/2 checks passed."
            },
            {
                "step_number": 4,
                "title": "Allocate and Associate an Elastic IP",
                "objective": "Assign a static public IPv4 address to the instance.",
                "console_navigation": "EC2 -> Network & Security -> Elastic IPs -> Allocate Elastic IP address.",
                "instructions": [
                    "Click 'Allocate Elastic IP address' -> 'Allocate'.",
                    "Select the newly allocated Elastic IP.",
                    "Click Actions -> 'Associate Elastic IP address'.",
                    "Resource type: Instance -> Select 'App-Server' -> Click 'Associate'."
                ],
                "expected_result": "The Elastic IP is attached to App-Server, replacing its initial dynamic public IP.",
                "common_pitfalls": ["Leaving unassociated Elastic IPs running (which incurs an hourly AWS charge)."],
                "verification_check": "App-Server public IP reflects the allocated Elastic IP address."
            },
            {
                "step_number": 5,
                "title": "Inspect Instance Metadata",
                "objective": "Query the EC2 Instance Metadata Service (IMDSv2).",
                "console_navigation": "EC2 -> Connect -> EC2 Instance Connect.",
                "instructions": [
                    "Connect via EC2 Instance Connect.",
                    "In the browser shell run:\nTOKEN=`curl -X PUT \"http://169.254.169.254/latest/api/token\" -H \"X-aws-ec2-metadata-token-ttl-seconds: 21600\"`\ncurl -H \"X-aws-ec2-metadata-token: $TOKEN\" -v http://169.254.169.254/latest/meta-data/instance-id\ncurl -H \"X-aws-ec2-metadata-token: $TOKEN\" -v http://169.254.169.254/latest/meta-data/placement/availability-zone",
                    "Observe the returned instance-id and availability-zone."
                ],
                "expected_result": "Terminal outputs instance metadata details directly from 169.254.169.254.",
                "common_pitfalls": ["Using legacy IMDSv1 GET queries without token when IMDSv2 is enforced."],
                "verification_check": "Terminal prints instance ID and AZ from metadata curl."
            }
        ]
    },
    {
        "lab_id": "lab_4",
        "lab_number": 4,
        "title": "Working with EBS",
        "duration_mins": 45,
        "module_id": "10701",
        "module_title": "Module 7 - Storage",
        "objective": "Create an Amazon Elastic Block Store (EBS) volume, attach it to a running EC2 instance, format a filesystem, mount it, create an EBS snapshot, and restore the snapshot into a new volume.",
        "aws_services": ["Amazon EBS", "Amazon EC2", "EBS Snapshots"],
        "architecture_summary": "Amazon EC2 instance with primary root volume (/dev/xvda) and secondary attached EBS General Purpose SSD gp3 volume formatted with ext4/xfs and backed up to S3 via Snapshots.",
        "final_summary": "You provisioned an independent Amazon EBS gp3 volume in the same AZ as your EC2 instance, attached it, formatted and mounted the storage in Linux, created a point-in-time EBS snapshot, and restored the volume from the snapshot.",
        "steps": [
            {
                "step_number": 1,
                "title": "Create an Amazon EBS Volume",
                "objective": "Create a 5 GiB gp3 volume in the same Availability Zone as your EC2 instance.",
                "console_navigation": "EC2 -> Elastic Block Store -> Volumes -> Create volume.",
                "instructions": [
                    "Check the Availability Zone of your running EC2 Lab instance (e.g. us-east-1a).",
                    "Navigate to Volumes -> 'Create volume'.",
                    "Volume type: General Purpose SSD (gp3).",
                    "Size: 5 GiB.",
                    "Availability Zone: MUST match your EC2 instance AZ exactly.",
                    "Tag: Key 'Name', Value 'Lab-Volume'.",
                    "Click 'Create volume'."
                ],
                "expected_result": "Volume state is 'Available' (green) in the target AZ.",
                "common_pitfalls": [
                    "Creating the volume in a different Availability Zone (EBS cannot be attached across AZs)."
                ],
                "verification_check": "Volume Lab-Volume is in 'Available' state in the matching instance AZ."
            },
            {
                "step_number": 2,
                "title": "Attach EBS Volume to EC2 Instance",
                "objective": "Attach Lab-Volume to the running EC2 instance.",
                "console_navigation": "EC2 -> Volumes -> Select Lab-Volume -> Actions -> Attach volume.",
                "instructions": [
                    "Select 'Lab-Volume'.",
                    "Actions -> 'Attach volume'.",
                    "Select your running EC2 instance from the dropdown.",
                    "Device name: accept default /dev/sdf (or /dev/xvdf).",
                    "Click 'Attach volume'."
                ],
                "expected_result": "Volume state changes from 'Available' to 'In-use'.",
                "common_pitfalls": ["Attempting to attach before volume creation completes."],
                "verification_check": "Volume status shows 'In-use' attached to instance-id."
            },
            {
                "step_number": 3,
                "title": "Format and Mount the Volume in Linux",
                "objective": "Initialize the file system and mount to /data directory.",
                "console_navigation": "EC2 -> Connect -> Terminal.",
                "instructions": [
                    "Run `lsblk` to identify the new unpartitioned device (e.g. nvme1n1 or xvdf).",
                    "Create an ext4 filesystem: `sudo mkfs -t ext4 /dev/xvdf` (or matching nvme name).",
                    "Create a mount directory: `sudo mkdir /data`.",
                    "Mount the volume: `sudo mount /dev/xvdf /data`.",
                    "Verify with `df -h` that /data shows ~5.0G available.",
                    "Create a test file: `sudo echo 'EBS persistent data' > /data/test.txt`."
                ],
                "expected_result": "Storage is mounted to /data and test file is written.",
                "common_pitfalls": ["Running mkfs on the root volume /dev/xvda by mistake."],
                "verification_check": "df -h lists /data mounted with ~5GB capacity."
            },
            {
                "step_number": 4,
                "title": "Create an EBS Snapshot",
                "objective": "Capture a point-in-time incremental snapshot of Lab-Volume.",
                "console_navigation": "EC2 -> Volumes -> Select Lab-Volume -> Actions -> Create snapshot.",
                "instructions": [
                    "Select 'Lab-Volume'.",
                    "Click Actions -> 'Create snapshot'.",
                    "Description: 'Lab-Volume backup snapshot'.",
                    "Click 'Create snapshot'.",
                    "Navigate to EC2 -> Elastic Block Store -> Snapshots to monitor progress until status is 'Completed'."
                ],
                "expected_result": "Snapshot status transitions from 'Pending' to 'Completed' (100%).",
                "common_pitfalls": ["Assuming snapshots are stored on the same drive (snapshots are durably stored in Amazon S3)."],
                "verification_check": "Snapshot status displays 'Completed'."
            },
            {
                "step_number": 5,
                "title": "Restore Volume from Snapshot",
                "objective": "Restore the snapshot into a new volume in another AZ for disaster recovery.",
                "console_navigation": "EC2 -> Snapshots -> Actions -> Create volume from snapshot.",
                "instructions": [
                    "Select the completed snapshot.",
                    "Actions -> 'Create volume from snapshot'.",
                    "Select Availability Zone (e.g. us-east-1b).",
                    "Name Tag: 'Restored-Volume'.",
                    "Click 'Create volume'."
                ],
                "expected_result": "A new independent volume is created from the snapshot backup.",
                "common_pitfalls": ["Trying to overwrite the existing volume rather than creating a new restored volume."],
                "verification_check": "Restored-Volume is created in Available state."
            }
        ]
    },
    {
        "lab_id": "lab_5",
        "lab_number": 5,
        "title": "Build a Database Server",
        "duration_mins": 50,
        "module_id": "10801",
        "module_title": "Module 8 - Databases",
        "objective": "Provision a VPC DB Subnet Group, launch an Amazon Relational Database Service (RDS) MySQL instance with Multi-AZ automated failover, and connect an EC2 web application.",
        "aws_services": ["Amazon RDS", "Amazon VPC", "AWS Secrets Manager", "Amazon EC2"],
        "architecture_summary": "Amazon RDS Multi-AZ MySQL DB instance deployed across two private subnets with synchronous replication, protected by a dedicated database security group allowing inbound port 3306 only from the web security group.",
        "final_summary": "You created a VPC DB subnet group across multiple availability zones, provisioned a managed Amazon RDS MySQL database with Multi-AZ redundancy, configured database security groups with least-privilege port 3306 rules, and verified database connectivity from an application instance.",
        "steps": [
            {
                "step_number": 1,
                "title": "Create a DB Subnet Group",
                "objective": "Define subnets in at least two Availability Zones for RDS deployment.",
                "console_navigation": "AWS Console -> RDS -> Subnet groups -> Create DB subnet group.",
                "instructions": [
                    "Name: 'lab-db-subnet-group'.",
                    "VPC: Select 'Lab VPC'.",
                    "Availability Zones: Select two distinct AZs (e.g. us-east-1a and us-east-1b).",
                    "Subnets: Select the corresponding private subnets in both AZs.",
                    "Click 'Create'."
                ],
                "expected_result": "DB Subnet group created with subnets across 2 AZs.",
                "common_pitfalls": ["Selecting only 1 AZ (RDS Multi-AZ requires at least two AZs in the subnet group)."],
                "verification_check": "lab-db-subnet-group is created with subnets in 2 AZs."
            },
            {
                "step_number": 2,
                "title": "Configure Database Security Group",
                "objective": "Allow MySQL (Port 3306) traffic originating only from the web server security group.",
                "console_navigation": "VPC -> Security groups -> Create security group.",
                "instructions": [
                    "Security group name: 'DB-SG'.",
                    "VPC: 'Lab VPC'.",
                    "Inbound rule: Type 'MySQL/Aurora', Port '3306', Source: Select 'Custom' and choose 'Web-SG' ID.",
                    "Click 'Create security group'."
                ],
                "expected_result": "Inbound port 3306 is secured to only accept traffic from Web-SG.",
                "common_pitfalls": ["Setting source to 0.0.0.0/0 (exposing database port to the public internet)."],
                "verification_check": "DB-SG inbound rule specifies Web-SG as the source for port 3306."
            },
            {
                "step_number": 3,
                "title": "Create an Amazon RDS MySQL Database",
                "objective": "Launch a MySQL DB instance with Multi-AZ standby replica.",
                "console_navigation": "RDS -> Databases -> Create database.",
                "instructions": [
                    "Choose database creation method: 'Standard create'.",
                    "Engine options: 'MySQL' -> Community Edition.",
                    "Templates: 'Dev/Test' (or Free tier if non-multi-AZ lab instructions).",
                    "Availability and durability: 'Multi-AZ DB instance' (creates a standby in another AZ).",
                    "DB instance identifier: 'lab-db'.",
                    "Master username: 'admin', Master password: enter lab password.",
                    "DB instance class: 'db.t3.micro'.",
                    "Connectivity: VPC 'Lab VPC', Subnet group 'lab-db-subnet-group', Public access: 'No', Security group: 'DB-SG'.",
                    "Click 'Create database'."
                ],
                "expected_result": "Database creation begins and status transitions from 'Creating' to 'Available'.",
                "common_pitfalls": ["Setting Public access to 'Yes'.", "Forgetting the DB password."],
                "verification_check": "lab-db status is 'Available' with Multi-AZ enabled."
            },
            {
                "step_number": 4,
                "title": "Retrieve RDS Endpoint & Verify Connectivity",
                "objective": "Obtain the DNS endpoint and test connectivity from Web Server.",
                "console_navigation": "RDS -> Databases -> lab-db -> Connectivity & security -> Copy Endpoint.",
                "instructions": [
                    "Copy the RDS Endpoint (e.g. lab-db.xxxx.us-east-1.rds.amazonaws.com).",
                    "Connect to your EC2 Web Server via EC2 Instance Connect.",
                    "Run:\nmysql -h <RDS-ENDPOINT> -u admin -p",
                    "Enter your master password.",
                    "Verify connection by typing `SHOW DATABASES;`."
                ],
                "expected_result": "MySQL prompt `mysql>` appears and displays default database schemas.",
                "common_pitfalls": ["Using the DB identifier instead of the full DNS endpoint string."],
                "verification_check": "MySQL CLI connects successfully and displays databases."
            },
            {
                "step_number": 5,
                "title": "Simulate Multi-AZ Failover",
                "objective": "Observe automated failover to the standby replica.",
                "console_navigation": "RDS -> Databases -> lab-db -> Actions -> Reboot.",
                "instructions": [
                    "Select 'lab-db'.",
                    "Actions -> 'Reboot'.",
                    "Check the checkbox 'Reboot with Failover?'.",
                    "Click 'Reboot'.",
                    "Observe the primary AZ switch to the secondary AZ while the DNS endpoint remains unchanged."
                ],
                "expected_result": "Instance reboots and switches primary AZ with zero configuration change on the client.",
                "common_pitfalls": ["Failing to check 'Reboot with Failover'."],
                "verification_check": "lab-db primary availability zone switches to the standby AZ."
            }
        ]
    },
    {
        "lab_id": "lab_6",
        "lab_number": 6,
        "title": "Scale and Load Balance your Architecture",
        "duration_mins": 60,
        "module_id": "11001",
        "module_title": "Module 10 - Auto Scaling and Monitoring",
        "objective": "Build a fault-tolerant, scalable architecture using an Amazon EC2 Launch Template, an Application Load Balancer (ALB), Target Groups with health checks, and an Auto Scaling Group.",
        "aws_services": ["Elastic Load Balancing (ALB)", "Amazon EC2 Auto Scaling", "Amazon CloudWatch", "Amazon VPC"],
        "architecture_summary": "Internet-facing Application Load Balancer distributing HTTP traffic across a dynamic Auto Scaling Group of EC2 instances spanning multiple Availability Zones with automated scale-out CloudWatch alarms.",
        "final_summary": "You created a reusable EC2 Launch Template, established a Target Group with HTTP health checking, deployed an internet-facing Application Load Balancer, and configured an Auto Scaling Group with dynamic scaling policies that maintained high availability during simulated traffic load.",
        "steps": [
            {
                "step_number": 1,
                "title": "Create an Amazon Machine Image (AMI) & Launch Template",
                "objective": "Package the web server into an AMI and create an EC2 Launch Template.",
                "console_navigation": "EC2 -> Launch Templates -> Create launch template.",
                "instructions": [
                    "Create an AMI from an existing configured web server or specify Amazon Linux AMI.",
                    "Navigate to EC2 -> 'Launch Templates' -> 'Create launch template'.",
                    "Template name: 'Web-Server-Template'.",
                    "AMI: Select Amazon Linux AMI.",
                    "Instance type: t2.micro or t3.micro.",
                    "Security groups: Select 'Web-SG'.",
                    "User data: Insert web server bootstrapping script.",
                    "Click 'Create launch template'."
                ],
                "expected_result": "Launch template Web-Server-Template created successfully.",
                "common_pitfalls": ["Forgetting to include the bootstrap user data in the template."],
                "verification_check": "Launch template is saved with Version 1 as default."
            },
            {
                "step_number": 2,
                "title": "Create Target Group for Load Balancer",
                "objective": "Define health check path and target type for HTTP traffic.",
                "console_navigation": "EC2 -> Target Groups -> Create target group.",
                "instructions": [
                    "Target type: 'Instances'.",
                    "Target group name: 'Web-Target-Group'.",
                    "Protocol: HTTP, Port: 80.",
                    "VPC: 'Lab VPC'.",
                    "Health checks: Protocol HTTP, Path '/index.html' (or '/').",
                    "Click 'Next' -> Do not manually register instances now (Auto Scaling will register them) -> Click 'Create target group'."
                ],
                "expected_result": "Web-Target-Group is created with health checks configured.",
                "common_pitfalls": ["Registering static instances instead of letting Auto Scaling register targets dynamically."],
                "verification_check": "Target group Web-Target-Group is active with HTTP 80 health checks."
            },
            {
                "step_number": 3,
                "title": "Deploy Application Load Balancer",
                "objective": "Create an internet-facing ALB across multiple public subnets.",
                "console_navigation": "EC2 -> Load Balancers -> Create Load Balancer -> Application Load Balancer.",
                "instructions": [
                    "Name: 'Lab-ALB'.",
                    "Scheme: 'Internet-facing', IP address type: IPv4.",
                    "Network mapping: VPC 'Lab VPC' -> Select at least two Availability Zones and their Public Subnets.",
                    "Security groups: Select 'Web-SG'.",
                    "Listeners and routing: Protocol HTTP, Port 80 -> Forward to 'Web-Target-Group'.",
                    "Click 'Create load balancer'."
                ],
                "expected_result": "ALB state transitions to 'Active' with a DNS name provided.",
                "common_pitfalls": ["Selecting private subnets for an internet-facing load balancer."],
                "verification_check": "Load balancer Lab-ALB state is Active."
            },
            {
                "step_number": 4,
                "title": "Configure Auto Scaling Group (ASG)",
                "objective": "Configure ASG with Min=2, Desired=2, Max=4 instances attached to the Target Group.",
                "console_navigation": "EC2 -> Auto Scaling Groups -> Create Auto Scaling group.",
                "instructions": [
                    "Name: 'Web-ASG'.",
                    "Launch template: Select 'Web-Server-Template'.",
                    "Network: 'Lab VPC', Subnets: Select Public Subnet 1 and Public Subnet 2.",
                    "Load balancing: Select 'Attach to an existing load balancer' -> Choose 'Web-Target-Group'.",
                    "Health checks: Check 'Turn on Elastic Load Balancing health checks'.",
                    "Group size: Desired capacity: 2, Minimum capacity: 2, Maximum capacity: 4.",
                    "Click 'Skip to review' -> 'Create Auto Scaling group'."
                ],
                "expected_result": "ASG automatically launches 2 EC2 instances and registers them as Healthy in Web-Target-Group.",
                "common_pitfalls": [
                    "Not checking the ELB health check option.",
                    "Setting desired capacity to 0."
                ],
                "verification_check": "Target group shows 2 instances with health status: Healthy."
            },
            {
                "step_number": 5,
                "title": "Test Load Balancing and Simulated High Availability",
                "objective": "Verify traffic distribution across instances and auto-healing on instance termination.",
                "console_navigation": "EC2 -> Load Balancers -> Copy DNS Name -> Test in browser.",
                "instructions": [
                    "Copy the DNS name of 'Lab-ALB' into a browser and refresh multiple times.",
                    "Notice the instance ID or IP displayed on the web page alternates between instances.",
                    "Simulate failure: In EC2 Instances, manually terminate one of the ASG instances.",
                    "Observe: Target group detects unhealthy status, deregisters the terminated instance, and ASG immediately launches a replacement instance to restore Desired capacity = 2."
                ],
                "expected_result": "The web application stays reachable continuously through the ALB URL, and the terminated instance is replaced automatically.",
                "common_pitfalls": ["Testing using instance public IPs rather than the ALB DNS name."],
                "verification_check": "Terminated instance is replaced automatically by the ASG."
            }
        ]
    }
]

class LabAssistantService:
    @classmethod
    async def init_seed_labs(cls):
        db = get_database()
        for lab in COURSE_LABS:
            await db.labs.update_one(
                {"lab_id": lab["lab_id"]},
                {"$set": lab},
                upsert=True
            )

    @classmethod
    async def get_all_labs(cls) -> List[Dict[str, Any]]:
        db = get_database()
        labs = []
        async for doc in db.labs.find({}, {"_id": 0}).sort("lab_number", 1):
            labs.append(doc)
        if not labs:
            return COURSE_LABS
        return labs

    @classmethod
    async def get_lab_by_id(cls, lab_id: str) -> Optional[Dict[str, Any]]:
        db = get_database()
        doc = await db.labs.find_one({"lab_id": lab_id}, {"_id": 0})
        if not doc:
            for l in COURSE_LABS:
                if l["lab_id"] == lab_id:
                    return l
        return doc

    @classmethod
    async def get_user_progress(cls, user_id: str, lab_id: str) -> Dict[str, Any]:
        db = get_database()
        progress = await db.lab_progress.find_one({"user_id": user_id, "lab_id": lab_id}, {"_id": 0})
        if not progress:
            return {
                "user_id": user_id,
                "lab_id": lab_id,
                "current_step": 1,
                "total_steps": 5,
                "completed_steps": [],
                "is_completed": False,
                "started_at": datetime.utcnow().isoformat()
            }
        return progress

    @classmethod
    async def update_step_progress(cls, user_id: str, lab_id: str, step_number: int, confirmed: bool) -> Dict[str, Any]:
        db = get_database()
        current = await cls.get_user_progress(user_id, lab_id)
        completed_steps = set(current.get("completed_steps", []))
        
        if confirmed:
            completed_steps.add(step_number)
        else:
            completed_steps.discard(step_number)

        completed_list = sorted(list(completed_steps))
        total_steps = current.get("total_steps", 5)
        is_completed = len(completed_list) >= total_steps
        next_step = step_number + 1 if (confirmed and step_number < total_steps) else step_number

        updated_record = {
            "user_id": user_id,
            "lab_id": lab_id,
            "current_step": next_step,
            "total_steps": total_steps,
            "completed_steps": completed_list,
            "is_completed": is_completed,
            "updated_at": datetime.utcnow().isoformat()
        }

        await db.lab_progress.update_one(
            {"user_id": user_id, "lab_id": lab_id},
            {"$set": updated_record},
            upsert=True
        )
        return updated_record

    @classmethod
    async def troubleshoot(
        cls,
        lab_id: str,
        step_number: int,
        error_message: Optional[str],
        screenshot_base64: Optional[str],
        user_description: str
    ) -> LabTroubleshootResponse:
        """
        Diagnoses lab obstacles based on console error messages and AWS best practices.
        Adheres strictly to the safety rule:
        Never independently create, modify or terminate AWS resources in a student's account or sandbox.
        """
        err_lower = (error_message or "").lower()
        desc_lower = user_description.lower()

        lab = await cls.get_lab_by_id(lab_id)
        step_title = f"Step {step_number}"
        if lab and step_number <= len(lab.get("steps", [])):
            step_title = lab["steps"][step_number - 1].get("title", step_title)

        diagnosis = "General configuration or parameter mismatch."
        fixes = []
        checks = []

        if "unauthorizedoperation" in err_lower or "accessdenied" in err_lower or "permission" in err_lower:
            diagnosis = "AWS IAM Authorization Denied: The active IAM credentials lack permission to perform this API action."
            fixes = [
                "Verify that you signed into the AWS Academy Learner Lab Sandbox with the provided lab role credentials rather than a personal AWS account.",
                "In IAM, inspect your user group permissions: verify the required AWS managed policy (e.g. AmazonS3ReadOnlyAccess or AmazonEC2ReadOnlyAccess) is properly attached.",
                "Ensure you are not attempting an action outside the approved scope of the AWS Academy learner policy."
            ]
            checks = [
                "Check IAM -> Users -> Permissions tab -> Effective Permissions.",
                "Inspect the top-right corner of the AWS Management Console to confirm the correct Account ID is active."
            ]
        elif "security group" in err_lower or "timed out" in err_lower or "connection refused" in err_lower or "port 80" in desc_lower:
            diagnosis = "Network Reachability / Firewall Obstacle: Inbound traffic is blocked by Security Group or Network ACL rules."
            fixes = [
                "Open EC2 -> Security Groups -> Locate your Web Server Security Group.",
                "Inspect Inbound Rules: Verify HTTP (Port 80) is open to Source '0.0.0.0/0' (Anywhere IPv4).",
                "If connecting via SSH, verify SSH (Port 22) rule exists and matches your current IP address.",
                "Verify the instance is deployed in a Public Subnet with an attached Internet Gateway and route 0.0.0.0/0 -> IGW."
            ]
            checks = [
                "VPC Console -> Route Tables -> Verify 0.0.0.0/0 route exists with Target 'igw-xxxx'.",
                "EC2 Console -> Select instance -> 'Security' tab -> Review effective inbound rules."
            ]
        elif "az" in err_lower or "availability zone" in err_lower or "volume" in err_lower:
            diagnosis = "Availability Zone Mismatch: Amazon EBS volumes cannot be attached across different Availability Zones."
            fixes = [
                "Check the exact Availability Zone of your EC2 instance (e.g., us-east-1a).",
                "Create a new EBS volume specifying the exact same Availability Zone.",
                "Attach the volume to the instance using default device naming (/dev/sdf or /dev/xvdf)."
            ]
            checks = [
                "EC2 Console -> Instances -> Check 'Availability Zone' column.",
                "EC2 Console -> Volumes -> Check 'Availability Zone' column."
            ]
        elif "db subnet group" in err_lower or "multi-az" in err_lower or "rds" in err_lower:
            diagnosis = "RDS Subnet Group Requirements: Multi-AZ DB deployments require subnets in at least two distinct Availability Zones."
            fixes = [
                "Navigate to RDS -> Subnet groups -> Edit your DB Subnet Group.",
                "Ensure at least two Availability Zones are selected, each with at least one corresponding private subnet.",
                "Re-attempt the RDS instance creation."
            ]
            checks = [
                "RDS Console -> Subnet Groups -> Verify coverage across 2 AZs."
            ]
        else:
            diagnosis = f"Assistance for {lab.get('title', 'Lab')} - {step_title}: Potential parameter or sequence discrepancy."
            fixes = [
                f"Carefully re-read the navigation and instruction steps for {step_title}.",
                "Double-check that resource names, VPC selection, and CIDR blocks match the lab instructions exactly.",
                "If using AWS CLI or scripts, ensure all placeholder values (e.g. <RDS-ENDPOINT> or <Public-IP>) are substituted."
            ]
            checks = [
                "Check the AWS Management Console resource tables to verify the resource state is 'Available' or 'Running'.",
                "Review the troubleshooting guide and expected results in the Lab Assistant panel."
            ]

        return LabTroubleshootResponse(
            lab_id=lab_id,
            step_number=step_number,
            diagnosis=diagnosis,
            suggested_fix=fixes,
            console_steps_to_verify=checks,
            safety_reminder="Safety Rule Enforced: The AWS Lab Assistant provides guided instructions. It will never create, modify, or terminate AWS cloud resources in your account."
        )

lab_service = LabAssistantService()
