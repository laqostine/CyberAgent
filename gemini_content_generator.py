import google.generativeai as genai
from enum import Enum
from typing import Dict, List, Optional, Literal, TypedDict, Tuple
from dataclasses import dataclass
from dotenv import load_dotenv
import logging
import json
import time
from visualization_tools import VisualizationTools

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class SlideType(Enum):
    TITLE = "title"
    CONTENT = "content"
    INTERACTIVE = "interactive"
    LAB = "lab"
    QUIZ = "quiz"
    SUMMARY = "summary"

class SlideSchema(TypedDict):
    title: str
    main_content: str
    bullet_points: Optional[List[str]]
    sub_points: Optional[List[List[str]]]  # For nested bullet points
    references: Optional[List[str]]
    examples: Optional[List[str]]

class LessonPlanSchema(TypedDict):
    title: str
    description: str
    learning_objectives: List[str]
    practical_activities: Optional[Dict]
    assessment: Optional[Dict]

@dataclass
class SlideContent:
    title: str
    main_content: str
    slide_type: SlideType
    bullet_points: Optional[List[str]] = None
    notes: Optional[str] = None
    interactive_elements: Optional[Dict] = None

@dataclass
class LessonPlan:
    title: str
    description: str
    learning_objectives: List[str]
    slides: List[SlideContent]
    practical_activities: Optional[Dict] = None
    assessment: Optional[Dict] = None

class GeminiContentGenerator:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.viz_tools = VisualizationTools()
        
        # Update content validation settings
        self.content_settings = {
            "max_chars_per_line": 90,
            "max_lines_per_slide": 8,
            "max_bullet_points": 6,
            "min_bullet_points": 3,
            "min_font_size": 18,
            "max_chars_per_bullet": 120,
            "graph_size": (8, 6),
            "icon_size": (1, 1)
        }
        
        self.presentation_structure_expanded = {
    "title": "Data Analytics in Cybersecurity",
    "duration": "4-8 hours",
    "lab_time": "1-2 hours",
    "instructors": ["Ismail Molla", "Ensar Bera"],
    "sections": [
        {
            "title": "Data Collection",
            "slides": range(1, 21), # Increased slide range
            "topics": [
                "Cybersecurity Data Sources: Overview of diverse data origins in cybersecurity.",
                "  * Internal Sources: System Logs (Windows Event Logs, Syslog), Application Logs (Web Server Logs, Database Logs), Security Logs (Firewall Logs, IDS/IPS Logs), Endpoint Logs (EDR Agents).",
                "  * External Sources: Network Traffic (PCAP, NetFlow, Zeek/Bro), Threat Intelligence Feeds (Commercial APIs, Open-Source Feeds - e.g., MISP, AlienVault OTX), Vulnerability Databases (NVD, CVE), OSINT (Shodan, Censys).",
                "  * Cloud Data Sources: Cloud Provider Logs (AWS CloudTrail, Azure Activity Log, GCP Audit Logs), SaaS Application Logs.",

                "Cybersecurity Data Collection Methods and Tools: Techniques and technologies for gathering security data.",
                "  * Log Management Systems (LMS) and SIEM: Centralized log collection, aggregation, and indexing. Examples: Elasticsearch, Splunk, ELK Stack (Elasticsearch, Logstash, Kibana).",
                "  * Network Packet Capture (PCAP): Deep packet inspection for network analysis. Tools: Wireshark, tcpdump, TShark (command-line Wireshark). Libraries: Scapy (Python library for packet manipulation).",
                "  * Network Flow Data Collection: Summarized network traffic information (NetFlow, IPFIX). Tools:  `flow-tools`, `ntopng`.",
                "  * Endpoint Detection and Response (EDR) Agents: Real-time endpoint monitoring and data collection. Examples: CrowdStrike Falcon, SentinelOne.",
                "  * API Integrations for Data Ingestion: Automating data retrieval from threat intelligence platforms, cloud services. Example: Python `requests` library for API calls.",
                "  * Scripting for Custom Data Collection: Using Python (libraries: `psutil` for system info, `subprocess` for command execution), PowerShell for tailored data gathering.",

                "Cybersecurity Data Types and Formats: Understanding the structure and organization of security data.",
                "  * Structured Data: Databases (SQL, NoSQL), CSV files, JSON logs, configuration files. Example: Vulnerability scan reports in CSV.",
                "  * Semi-structured Data: Logs (Syslog, Web Server Logs, Firewall Logs), key-value pairs, XML. Example: Apache access logs.",
                "  * Unstructured Data: Textual Security Reports, Threat Intelligence Articles, emails, incident descriptions. Example: CVE descriptions.",
                "  * Common Cybersecurity Data Formats and Standards: CEF (Common Event Format), LEEF (Log Event Extended Format), STIX/TAXII (for threat intelligence sharing).",

                "Best Practices for Secure and Efficient Cybersecurity Data Collection: Ensuring data quality, security, and scalability.",
                "  * Data Integrity and Validation: Hashing, checksums to verify data authenticity. Data validation rules to ensure data accuracy.",
                "  * Secure Data Pipelines and Storage: Encryption in transit (TLS/SSL) and at rest (AES encryption). Access control mechanisms (RBAC).",
                "  * Data Retention Policies and Compliance: Defining data storage duration based on legal and organizational requirements (GDPR, HIPAA, PCI DSS).",
                "  * Scalability and Performance Considerations: Handling high-volume, high-velocity security data streams. Distributed data collection and processing.",
                "  * Ethical Considerations in Cybersecurity Data Collection: Privacy implications, data minimization principles, anonymization techniques.",
                "  * Automated Data Collection Pipelines: Orchestration of data collection processes using tools like Apache Kafka, Apache NiFi, message queues."
            ]
        },
        {
            "title": "Data Cleaning and Preprocessing",
            "slides": range(21, 31), # Slightly increased slide range
            "topics": [
                "Cybersecurity Data Quality Challenges & Assessment: Identifying and evaluating data quality issues.",
                "  * Noise and Irrelevant Data: Filtering out verbose logs, debugging messages, benign events. Example: Identifying false positive security alerts.",
                "  * Incomplete or Missing Data: Handling missing log fields, gaps in network traffic data. Imputation techniques.",
                "  * Inconsistent Data Formats: Standardizing log formats from different systems and vendors using parsing libraries (e.g., Python `regex`, `pyparsing`).",
                "  * Time Zone Issues and Normalization: Handling timestamps from different geographical locations. Time zone conversion using libraries like `pytz` (Python).",
                "  * Data Redundancy and Duplication: Deduplication techniques for logs and security alerts to reduce noise and storage.",
                "  * Data Quality Assessment Metrics: Completeness, Accuracy, Consistency, Validity, Timeliness. Using statistical methods to measure data quality.",

                "Cybersecurity Data Cleaning Techniques: Methods for improving data quality and resolving data issues.",
                "  * Log Parsing and Standardization: Using regular expressions, parsing libraries (like `regex`, `antlr`) to extract structured data from logs.",
                "  * Data Deduplication and Noise Reduction: Algorithms for identifying and removing duplicate entries and irrelevant data.",
                "  * Handling Missing Values: Imputation methods (mean, median, mode imputation), deletion of incomplete records when appropriate.",
                "  * Error Correction and Data Transformation: Data type conversion (string to integer, timestamp parsing), IP address validation (using libraries like `ipaddress` in Python), URL parsing and normalization.",
                "  * Geolocation Enrichment: Mapping IP addresses to geographic locations using GeoIP databases (e.g., MaxMind GeoLite2, Python `geoip2` library).",

                "Cybersecurity Data Preprocessing Steps for Analysis: Transforming data into a suitable format for analysis and modeling.",
                "  * Feature Engineering for Security Analysis: Creating relevant features from raw data. Examples: Feature extraction from URLs (domain, path, query parameters), IP addresses (network class, ASN), User Agents, timestamps (time of day, day of week), log messages (keywords, n-grams). Libraries: pandas, scikit-learn.",
                "  * Text Preprocessing for Security Logs and Reports: Tokenization (splitting text into words), stemming/lemmatization (reducing words to root form using NLTK, spaCy in Python), stop word removal, TF-IDF for feature representation from text.",
                "  * Data Aggregation and Grouping: Summarizing data by time intervals, IP addresses, user accounts, etc. using pandas `groupby()` function.",
                "  * Data Transformation and Scaling for Machine Learning: Normalization, standardization (using scikit-learn `StandardScaler`, `MinMaxScaler`) to prepare data for machine learning algorithms.",
                "  * Anonymization and Pseudonymization Techniques: Protecting sensitive data by removing or masking identifying information for privacy compliance."
            ]
        },
        {
            "title": "Data Analysis",
            "slides": range(31, 46), # Slightly increased slide range
            "topics": [
                "Statistical Analysis Methods for Cybersecurity: Applying statistical techniques to understand security data.",
                "  * Descriptive Statistics for Security Event Summarization: Mean, median, mode, standard deviation, percentiles to summarize security events. Example: Average number of daily intrusion attempts.",
                "  * Hypothesis Testing for Security Incident Investigation: T-tests, chi-squared tests to compare groups of security events. Example: Testing if a new security rule reduces false positive alerts.",
                "  * Correlation Analysis for Security Event Relationships: Pearson, Spearman correlation to identify relationships between security metrics. Example: Correlation between vulnerability severity and exploit attempts.",
                "  * Regression Analysis for Risk Scoring and Prediction: Linear regression, logistic regression to predict security risks and vulnerabilities. Example: Predicting the likelihood of a system being compromised based on vulnerability scores.",
                "  * Time Series Analysis for Trend Detection in Security Metrics: ARIMA, Exponential Smoothing to analyze security trends over time. Example: Identifying seasonal patterns in DDoS attacks.",

                "Cybersecurity Pattern Recognition & Machine Learning: Using machine learning for advanced threat detection and pattern identification.",
                "  * Anomaly Detection Techniques for Network and System Behavior: Isolation Forest, One-Class SVM, Autoencoders, Local Outlier Factor for detecting unusual activities. Libraries: scikit-learn `sklearn.ensemble.IsolationForest`, `sklearn.svm.OneClassSVM`, TensorFlow/Keras for Autoencoders.",
                "  * Signature-based and Anomaly-based Intrusion Detection Systems (IDS): Rule-based IDS (Snort, Suricata), Machine learning-based IDS (using anomaly detection techniques).",
                "  * Behavioral Analysis for User and Entity Behavior Analytics (UEBA): Profiling normal user and entity behavior and detecting deviations. Machine learning models for behavior profiling.",
                "  * Machine Learning for Malware Detection and Classification: Supervised learning algorithms (Random Forest, Gradient Boosting, Support Vector Machines) for classifying malware. Datasets: VirusShare, VirusTotal Dataset. Libraries: scikit-learn.",
                "  * Supervised and Unsupervised Learning for Security Event Classification and Clustering: Clustering algorithms (K-Means, DBSCAN) for grouping similar security events, classification for predicting event types. Libraries: scikit-learn.",
                "  * Deep Learning for Cybersecurity: Convolutional Neural Networks (CNNs) for image-based malware analysis, Recurrent Neural Networks (RNNs) for sequential data like network traffic. Libraries: TensorFlow, Keras, PyTorch.",

                "Cybersecurity Trend & Time Series Analysis: Analyzing security data over time to identify patterns and predict future events.",
                "  * Baseline Creation and Deviation Analysis: Establishing normal behavior baselines and detecting deviations. Example: Setting a baseline for normal network traffic volume.",
                "  * Forecasting Security Incidents and Trends: Time series forecasting models (ARIMA, Prophet) to predict future security events. Example: Predicting future phishing attacks based on historical data.",
                "  * Seasonal and Periodic Pattern Analysis: Identifying recurring patterns in security data (daily, weekly, monthly). Example: Analyzing weekly patterns in login failures.",
                "  * Change Point Detection: Algorithms for detecting sudden shifts in security time series (e.g., rupture in attack frequency). Example: Detecting the start of a new attack campaign.",

                "Cybersecurity Anomaly Detection Techniques: Deep dive into methods for finding unusual security events.",
                "  * Statistical Anomaly Detection: Z-score, Grubbs' test, Box Plot method for identifying statistical outliers in security data.",
                "  * Machine Learning-based Anomaly Detection: Detailed exploration of Isolation Forest, One-Class SVM, Autoencoders, their parameters and applications in security.",
                "  * Rule-based Anomaly Detection: Defining rules based on domain expertise to identify anomalies. Example: Rules for detecting suspicious login attempts (multiple failed logins from different locations).",
                "  * Behavioral Anomaly Detection in Network Traffic and User Activities: Techniques for profiling and detecting deviations in network flow data, user access patterns, and application behavior."
            ]
        },
        {
            "title": "Data Visualization",
            "slides": range(46, 61), # Slightly increased slide range
            "topics": [
                "Cybersecurity Data Visualization Techniques & Tools: Overview of visualization methods and software for security data.",
                "  * Choosing Effective Visualizations for Security Data: Selecting appropriate chart types (line charts, bar charts, scatter plots, heatmaps, geographic maps, network graphs) based on data type and analytical goals.",
                "  * Security Dashboarding Principles and Best Practices: Design principles for effective dashboards (information hierarchy, visual clarity, actionability). Examples: Kibana dashboards for ELK stack, Grafana dashboards for time-series data.",
                "  * Geospatial Visualization for Attack Origin and Distribution: Mapping attack sources, malware outbreaks, and threat actor locations on geographic maps. Libraries: Folium (Python for leaflet maps), GeoPandas.",
                "  * Network Graph Visualization for Security Connectivity: Visualizing network traffic, attack paths, and relationships between network entities using network graphs. Libraries: NetworkX (Python for graph analysis and visualization), Gephi.",
                "  * Time Series Visualization for Security Trends and Events: Line charts, area charts for displaying security metrics and events over time. Tools: Grafana, Kibana time series visualizations.",
                "  * Tools for Security Data Visualization: Open-source and commercial visualization tools. Examples: Grafana, Kibana, Power BI, Tableau, Qlik Sense, Apache Superset.",

                "Effective Chart Types for Cybersecurity Data: Specific chart types and their best uses in cybersecurity.",
                "  * Time Series Charts for Incident Timelines and Trends: Visualizing security events and metrics over time. Example: Number of phishing emails detected per day.",
                "  * Bar Charts and Histograms for Security Event Counts and Distributions: Showing frequency of different security event categories, attack types, vulnerability severities. Example: Distribution of malware families.",
                "  * Pie Charts and Donut Charts for Categorical Security Data: Representing proportions of different categories. Example: Percentage breakdown of attack vectors.",
                "  * Heatmaps for Vulnerability Density and Security Alert Concentrations: Displaying density of vulnerabilities or alerts across systems or time. Example: Vulnerability heatmap of servers.",
                "  * Geographic Maps for Attack Source Visualization: Pin maps, choropleth maps to visualize attack origins geographically.",
                "  * Network Graphs for Connectivity and Attack Paths: Visualizing relationships between network nodes and potential attack propagation paths.",

                "Interactive Cybersecurity Visualizations for Investigation: Enhancing data exploration and incident response through interactivity.",
                "  * Drill-down Capabilities in Security Dashboards: Allowing users to explore data at different levels of detail.",
                "  * Filtering and Slicing Security Data in Visualizations: Interactive filters to focus on specific data subsets.",
                "  * Interactive Exploration of Security Event Data: Tools for dynamically exploring and querying security data visualizations.",
                "  * Linking Visualizations to Underlying Data for Investigation: Connecting visualizations to raw data logs for deeper analysis.",
                "  * Real-time vs. Historical Interactive Security Dashboards: Designing dashboards for real-time monitoring and historical analysis.",

                "Designing Actionable Cybersecurity Dashboards & Reports: Creating visualizations that drive security actions and decisions.",
                "  * Key Performance Indicators (KPIs) for Security Dashboards: Defining relevant security metrics (MTTR, detection rate, vulnerability remediation time).",
                "  * Customizing Dashboards for Different Security Roles: Tailoring dashboards for SOC analysts (detailed event views), managers (summary views, KPIs), executives (high-level risk posture).",
                "  * Alerting and Notification Integration with Dashboards: Integrating alerts and notifications directly into dashboards for real-time awareness.",
                "  * Report Generation from Security Visualizations: Automating report creation from dashboard data and visualizations.",
                "  * Storytelling with Security Data Visualizations: Structuring visualizations to communicate security insights effectively to different audiences."
            ]
        },
    ]
}
        # Define the presentation structure

        # Define JSON schema for lesson plan
        self.lesson_plan_schema = {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "The title of the lesson (max 8 words)"
                },
                "description": {
                    "type": "string",
                    "description": "Brief description of the lesson (2-3 sentences)"
                },
                "learning_objectives": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "A specific learning objective"
                    },
                    "description": "3-5 specific learning objectives"
                },
                "practical_activities": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "steps": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    }
                },
                "assessment": {
                    "type": "object",
                    "properties": {
                        "questions": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "question": {"type": "string"},
                                    "options": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "required": ["title", "description", "learning_objectives"]
        }

        # Define JSON schema for slide content
        self.slide_content_schema = {
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Clear, concise title (max 5 words)"
                },
                "main_content": {
                    "type": "string",
                    "description": "Main content of the slide"
                },
                "bullet_points": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of bullet points"
                },
                "interactive_elements": {
                    "type": "object",
                    "properties": {
                        "points": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "objectives": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "tools": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "questions": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "question": {"type": "string"},
                                    "options": {
                                        "type": "array",
                                        "items": {"type": "string"}
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "required": ["title", "main_content"]
        }

    def _extract_json_from_response(self, response_text: str) -> Dict:
        """Extract JSON from response text, handling potential formatting issues"""
        try:
            # Try direct JSON parsing first
            return json.loads(response_text)
        except json.JSONDecodeError:
            logger.warning("Failed to parse direct JSON, attempting to extract JSON content")
            try:
                # Look for JSON-like content between curly braces
                start_idx = response_text.find('{')
                end_idx = response_text.rfind('}') + 1
                if start_idx != -1 and end_idx != 0:
                    json_content = response_text[start_idx:end_idx]
                    return json.loads(json_content)
                raise ValueError("No JSON content found in response")
            except Exception as e:
                logger.error(f"Failed to extract JSON: {str(e)}")
                # Return a minimal valid structure
                return {
                    "title": "Error in Content Generation",
                    "main_content": "Failed to generate content. Please try again.",
                    "description": "An error occurred during content generation.",
                    "learning_objectives": ["Review and retry content generation"]
                }

    def _handle_api_error(self, retries: int = 3, delay: int = 5) -> None:
        """Handle API errors with retries and exponential backoff"""
        for attempt in range(retries):
            try:
                yield
                break
            except Exception as e:
                if "429" in str(e) and attempt < retries - 1:
                    wait_time = delay * (2 ** attempt)  # Exponential backoff
                    logger.warning(f"API quota exceeded. Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                else:
                    raise

    def generate_lesson_plan(self, module: str, lesson_title: str) -> LessonPlan:
        """Generate a lesson plan using the predefined presentation structure"""
        try:
            # Find the relevant section from presentation structure
            section = None
            if module.lower() == "comprehensive":
                # Use the entire structure for comprehensive module
                plan_data = {
                    "title": self.presentation_structure_expanded["title"],
                    "description": "Comprehensive course covering data analytics in cybersecurity",
                    "learning_objectives": [
                        s["title"].split(" - ")[0] for s in self.presentation_structure_expanded["sections"]
                    ],
                    "practical_activities": {
                        "title": "Comprehensive Implementation",
                        "steps": [
                            # Get first practical step from each section
                            next((topic for topic in s["topics"] if topic.startswith("  *")), "")
                            for s in self.presentation_structure_expanded["sections"]
                        ]
                    }
                }
            else:
                # Find specific section
                for s in self.presentation_structure_expanded["sections"]:
                    if module.lower() in s["title"].lower():
                        section = s
                        break
                
                if not section:
                    raise ValueError(f"No content found for module: {module}")
                
                # Create structured lesson plan from the section
                plan_data = {
                    "title": section["title"],
                    "description": section["topics"][0],  # First topic usually contains overview
                    "learning_objectives": [
                        topic.split(":")[0]  # Use main topic headers as objectives
                        for topic in section["topics"]
                        if ":" in topic and not topic.startswith("  *")
                    ],
                    "practical_activities": {
                        "title": "Practical Implementation",
                        "steps": [
                            topic.strip("* ")  # Use detailed points as practical steps
                            for topic in section["topics"]
                            if topic.startswith("  *")
                        ][:5]  # Limit to 5 steps
                    }
                }
            
            return self._create_lesson_plan(plan_data)
            
        except Exception as e:
            logger.error(f"Error generating lesson plan from structure: {str(e)}")
            raise

    def generate_slide_content(self, module: str, topic: str, slide_type: SlideType) -> SlideContent:
        """Generate content for a specific slide type using structured output"""
        prompt = f"""
        Create detailed content for a cybersecurity training slide.
        Module: {module}
        Topic: {topic}

        Requirements:
        1. Title must be clear and concise (max 8 words, 60 characters)
        2. Main content should be thorough but concise (max 500 characters)
        3. Use 3-6 bullet points, each max 80 characters
        4. Include specific examples or practical applications
        5. Reference relevant standards or frameworks
        6. Use proper technical terminology
        7. Ensure content fits slide format:
           - Title at top
           - Main content below
           - Bullet points for key information
           - Examples or references at bottom
        8. Content should be educational and actionable for SME staff
        9. Use proper line breaks for readability

        Return ONLY a JSON object in the following format (no other text):
        {{
            "title": "clear topic title",
            "main_content": "detailed explanation",
            "bullet_points": ["point 1", "point 2", "point 3"],
            "examples": ["example 1", "example 2"],
            "references": ["reference 1", "reference 2"]
        }}
        """
        
        try:
            # Use retry mechanism for content generation
            content = self.retry_content_generation(self.model.generate_content, prompt)
            
            if not content:
                logger.warning(f"Failed to generate content for {topic}, using fallback")
                return self._create_fallback_content(module, topic)
            
            # Validate and format content
            content = self._validate_and_format_content(content)
            
            # Create slide content
            slide_content = SlideContent(
                title=content["title"],
                main_content=self._format_main_content(content),
                slide_type=slide_type,
                bullet_points=content.get("bullet_points", []),
                notes=self._format_notes(content),
                interactive_elements=self._create_interactive_elements(content)
            )
            
            return slide_content
            
        except Exception as e:
            logger.error(f"Error generating slide content: {str(e)}")
            return self._create_fallback_content(module, topic)

    def _validate_and_format_content(self, content: Dict) -> Dict:
        """Validate and format the generated content"""
        try:
            # Validate title
            if len(content["title"]) > 60:
                content["title"] = content["title"][:57] + "..."
            
            # Format main content
            if "main_content" in content:
                content["main_content"] = self._format_text_content(
                    content["main_content"],
                    max_chars=500
                )
            
            # Validate and format bullet points
            if "bullet_points" in content:
                formatted_points = []
                for point in content["bullet_points"][:6]:  # Limit to 6 points
                    if len(point) > 80:
                        point = point[:77] + "..."
                    formatted_points.append(point)
                content["bullet_points"] = formatted_points
            
            # Format examples and references
            if "examples" in content:
                content["examples"] = [
                    ex[:100] + "..." if len(ex) > 100 else ex
                    for ex in content["examples"][:2]  # Limit to 2 examples
                ]
            
            if "references" in content:
                content["references"] = [
                    ref[:100] + "..." if len(ref) > 100 else ref
                    for ref in content["references"][:2]  # Limit to 2 references
                ]
            
            return content
            
        except Exception as e:
            logger.error(f"Content validation failed: {str(e)}")
            return self._create_fallback_content("", "")

    def _format_main_content(self, content: Dict) -> str:
        """Format the main content with examples and references"""
        parts = []
        
        if "main_content" in content:
            parts.append(content["main_content"])
        
        if "examples" in content and content["examples"]:
            parts.append("\nExamples:")
            parts.extend(f"• {ex}" for ex in content["examples"])
        
        if "references" in content and content["references"]:
            parts.append("\nReferences:")
            parts.extend(f"• {ref}" for ref in content["references"])
        
        return "\n".join(parts)

    def _format_notes(self, content: Dict) -> str:
        """Format speaker notes from content"""
        notes = []
        
        if "main_content" in content:
            notes.append("Key Points:")
            notes.append(content["main_content"])
        
        if "examples" in content and content["examples"]:
            notes.append("\nExample Details:")
            notes.extend(f"- {ex}" for ex in content["examples"])
        
        if "references" in content and content["references"]:
            notes.append("\nAdditional References:")
            notes.extend(f"- {ref}" for ref in content["references"])
        
        return "\n".join(notes)

    def _create_interactive_elements(self, content: Dict) -> Dict:
        """Create interactive elements from content"""
        return {
            "examples": content.get("examples", []),
            "references": content.get("references", []),
            "discussion_points": [
                f"Discuss: {point}"
                for point in content.get("bullet_points", [])[:2]
            ]
        }

    def _create_lesson_plan(self, lesson_data: Dict) -> LessonPlan:
        """Create a LessonPlan object from structured data with validation"""
        try:
            # Validate required fields
            required_fields = ["title", "description", "learning_objectives"]
            for field in required_fields:
                if field not in lesson_data:
                    raise ValueError(f"Missing required field: {field}")

            return LessonPlan(
                title=lesson_data["title"],
                description=lesson_data["description"],
                learning_objectives=lesson_data["learning_objectives"],
                slides=self._generate_lesson_slides(
                    lesson_data["title"],
                    lesson_data["description"],
                    lesson_data["learning_objectives"],
                    lesson_data.get("practical_activities", {})
                ),
                practical_activities=lesson_data.get("practical_activities"),
                assessment=lesson_data.get("assessment")
            )
        except Exception as e:
            logger.error(f"Error creating lesson plan: {str(e)}")
            raise

    def _create_slide_content(self, slide_data: Dict, slide_type: SlideType) -> SlideContent:
        """Create a SlideContent object from structured data with validation"""
        try:
            # Validate required fields
            if "title" not in slide_data or "main_content" not in slide_data:
                raise ValueError("Missing required fields: title and/or main_content")

            return SlideContent(
                title=slide_data["title"],
                main_content=slide_data["main_content"],
                slide_type=slide_type,
                bullet_points=slide_data.get("bullet_points"),
                interactive_elements=slide_data.get("interactive_elements")
            )
        except Exception as e:
            logger.error(f"Error creating slide content: {str(e)}")
            # Return a fallback slide content
            return SlideContent(
                title=f"{slide_type.value.title()} Slide",
                main_content="Content generation failed. Please try again.",
                slide_type=slide_type
            )

    def _get_slide_type_requirements(self, slide_type: SlideType) -> str:
        """Get specific requirements based on slide type"""
        requirements = {
            SlideType.TITLE: "Comprehensive overview of the topic with key objectives",
            SlideType.CONTENT: "Detailed explanation with examples and references",
            SlideType.INTERACTIVE: "Practical scenarios and discussion points",
            SlideType.LAB: "Step-by-step implementation guide with real-world examples",
            SlideType.QUIZ: "Assessment questions with detailed explanations",
            SlideType.SUMMARY: "Key takeaways and practical next steps"
        }
        return requirements.get(slide_type, "")

    def _generate_lesson_slides(self, title: str, description: str, objectives: List[str], activities: Dict) -> List[SlideContent]:
        """Generate a complete set of 60 slides for the comprehensive presentation"""
        slides = []
        
        # Title and introduction
        title_prompt = f"""
        Create a compelling title slide introduction for a cybersecurity course titled "{self.presentation_structure_expanded['title']}"
        Keep it concise and impactful (max 3-4 sentences).
        Focus on the importance of data analytics in cybersecurity.
        """
        title_content = self.model.generate_content(title_prompt)
        
        slides.append(SlideContent(
            title=self.presentation_structure_expanded["title"],
            main_content=title_content.text,
            slide_type=SlideType.TITLE,
            bullet_points=objectives
        ))
        
        # Generate content for each section
        for section in self.presentation_structure_expanded["sections"]:
            # Generate section overview slide
            overview_prompt = f"""
            Create an overview for the section "{section['title']}" in cybersecurity data analytics.
            Provide a brief introduction (2-3 sentences) explaining why this topic is important.
            Focus on practical applications and key learning outcomes.
            """
            overview_content = self.model.generate_content(overview_prompt)
            
            slides.append(SlideContent(
                title=section["title"],
                main_content=overview_content.text,
                slide_type=SlideType.TITLE
            ))
            
            # Generate slides for each main topic
            for topic in section["topics"]:
                if not topic.startswith("  *"):  # Main topics only
                    topic_title = topic.split(":")[0]
                    
                    # Get bullet points for this topic
                    bullet_points = [
                        t.strip("* ") for t in section["topics"]
                        if t.startswith("  *") and topic_title in t
                    ]
                    
                    # Generate detailed content for the topic
                    content_prompt = f"""
                    Create detailed slide content for the topic "{topic_title}" in cybersecurity data analytics.
                    Context: {topic}
                    
                    Requirements:
                    1. Provide a clear, concise explanation (2-3 sentences)
                    2. Focus on practical applications and real-world examples
                    3. Use technical but understandable language
                    4. Make it relevant for cybersecurity professionals
                    
                    The content should complement these bullet points:
                    {bullet_points}
                    """
                    
                    content_response = self.model.generate_content(content_prompt)
                    
                    slides.append(SlideContent(
                        title=topic_title,
                        main_content=content_response.text,
                        slide_type=SlideType.CONTENT,
                        bullet_points=bullet_points
                    ))
                    
                    # Generate practical example slide if needed
                    if len(bullet_points) > 2:  # Only for substantial topics
                        example_prompt = f"""
                        Create a practical example slide for "{topic_title}" in cybersecurity.
                        Include:
                        1. A real-world scenario
                        2. Specific tools or techniques used
                        3. Step-by-step approach
                        4. Expected outcomes or results
                        Keep it concise and actionable.
                        """
                        
                        example_response = self.model.generate_content(example_prompt)
                        
                        slides.append(SlideContent(
                            title=f"Practical Example: {topic_title}",
                            main_content=example_response.text,
                            slide_type=SlideType.LAB,
                            bullet_points=[
                                "Scenario Overview",
                                "Tools Used",
                                "Implementation Steps",
                                "Expected Outcomes"
                            ]
                        ))
        
        # If we need more slides to reach 60
        while len(slides) < 60:
            # Generate additional case study slides
            case_study_prompt = """
            Create a cybersecurity case study slide focusing on data analytics.
            Include:
            1. Brief scenario description
            2. Challenge faced
            3. Analytics approach used
            4. Results and lessons learned
            """
            
            case_study_response = self.model.generate_content(case_study_prompt)
            
            slides.append(SlideContent(
                title="Case Study: Data Analytics in Action",
                main_content=case_study_response.text,
                slide_type=SlideType.CONTENT,
                bullet_points=[
                    "Scenario Background",
                    "Analytical Approach",
                    "Implementation",
                    "Key Findings"
                ]
            ))
        
        return slides[:60]  # Ensure exactly 60 slides

    def generate_quiz_questions(self, module: str, lesson_title: str) -> List[Dict]:
        """Generate quiz questions with structured output"""
        prompt = f"""
        Create assessment questions for a cybersecurity training module.
        Module: {module}
        Lesson: {lesson_title}

        Generate 3 multiple choice questions with 4 options each.
        Return the response in the following JSON structure:
        [
            {{
                "question": "question text",
                "options": ["option1", "option2", "option3", "option4"],
                "correct_answer": "correct option"
            }}
        ]
        """
        
        try:
            response = self.model.generate_content(prompt)
            
            # Parse the response text as JSON
            try:
                return json.loads(response.text)
            except json.JSONDecodeError:
                # If JSON parsing fails, try to extract JSON from the text
                start_idx = response.text.find('[')
                end_idx = response.text.rfind(']') + 1
                if start_idx != -1 and end_idx != 0:
                    json_str = response.text[start_idx:end_idx]
                    return json.loads(json_str)
                else:
                    return []
            
        except Exception as e:
            logger.error(f"Error generating quiz questions: {str(e)}")
            return []

    def generate_lab_exercise(self, module: str, lesson_title: str) -> Dict:
        """Generate hands-on lab exercise instructions"""
        prompt = f"""
        Create a practical lab exercise for cybersecurity training.
        Module: {module}
        Lesson: {lesson_title}

        Include:
        1. Exercise objectives
        2. Required tools (Wireshark, Zabbix, or Nessus)
        3. Step-by-step instructions
        4. Expected outcomes
        5. Discussion questions

        Make it practical and relevant for SME environments.
        """
        
        response = self.model.generate_content(prompt)
        # TODO: Implement parsing of lab exercise
        return {}

    def retry_content_generation(self, func, *args, max_retries=3):
        """Retry content generation with exponential backoff"""
        last_error = None
        for attempt in range(max_retries):
            try:
                response = func(*args)
                
                # Extract text from Gemini response properly
                try:
                    if hasattr(response, 'parts'):
                        content = response.parts[0].text
                    elif hasattr(response, 'candidates'):
                        content = response.candidates[0].content.parts[0].text
                    else:
                        content = str(response)  # Fallback to string representation
                        
                    # Clean the content string
                    content = content.strip()
                    content = content.replace('\n', ' ')
                    content = content.replace('\r', ' ')
                    content = content.replace('\t', ' ')
                    
                    # Try to find and extract JSON content
                    start_idx = content.find('{')
                    end_idx = content.rfind('}') + 1
                    
                    if start_idx != -1 and end_idx > start_idx:
                        json_str = content[start_idx:end_idx]
                        # Clean any potential control characters
                        json_str = ''.join(char for char in json_str if ord(char) >= 32 or char in '\n\r\t')
                        content_json = json.loads(json_str)
                        
                        if self.validate_slide_content(content_json):
                            return content_json
                    else:
                        logger.warning(f"Attempt {attempt + 1}: No JSON content found in response")
                        
                except json.JSONDecodeError as je:
                    logger.warning(f"Attempt {attempt + 1}: JSON parsing failed: {str(je)}")
                    last_error = je
                except Exception as e:
                    logger.warning(f"Attempt {attempt + 1}: Error processing response: {str(e)}")
                    last_error = e
                
                # If we get here, either JSON parsing failed or validation failed
                # Wait before retry
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    logger.info(f"Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                    
            except Exception as e:
                logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
                last_error = e
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                continue
                
        logger.error(f"All retry attempts failed. Last error: {str(last_error)}")
        return self._create_fallback_content(*args)

    def validate_slide_content(self, content: Dict) -> bool:
        """Validate slide content structure and length"""
        try:
            # Check required fields
            required_fields = ["title", "main_content"]
            if not all(k in content for k in required_fields):
                logger.warning(f"Missing required fields. Found: {list(content.keys())}")
                return False
            
            # Format main content for proper wrapping
            content["main_content"] = self._format_text_content(content["main_content"])
            
            # Format bullet points
            if "bullet_points" in content and content["bullet_points"]:
                formatted_bullets = []
                for bullet in content["bullet_points"]:
                    if len(bullet) > self.content_settings["max_chars_per_bullet"]:
                        # Split long bullet points into multiple lines
                        formatted_bullet = self._wrap_text(bullet, self.content_settings["max_chars_per_bullet"])
                        formatted_bullets.append(formatted_bullet)
                    else:
                        formatted_bullets.append(bullet)
                content["bullet_points"] = formatted_bullets[:self.content_settings["max_bullet_points"]]
            
            return True
            
        except Exception as e:
            logger.error(f"Content validation failed: {str(e)}")
            return False

    def _format_text_content(self, text: str, max_chars: int = None) -> str:
        """Format text content to fit within slide boundaries"""
        # Split into sentences
        sentences = text.split('. ')
        formatted_lines = []
        current_line = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence.endswith('.'):
                sentence += '.'
                
            # If adding this sentence exceeds line length, start a new line
            if max_chars and len(current_line) + len(sentence) + 1 > max_chars:
                if current_line:
                    formatted_lines.append(current_line.strip())
                current_line = sentence + ' '
            else:
                current_line += sentence + ' '
        
        if current_line:
            formatted_lines.append(current_line.strip())
        
        # Limit number of lines
        if max_chars and len(formatted_lines) > max_chars:
            # Split content into two columns if too long
            mid_point = len(formatted_lines) // 2
            left_column = formatted_lines[:mid_point]
            right_column = formatted_lines[mid_point:]
            
            # Format columns
            return {
                "left_column": "\n".join(left_column),
                "right_column": "\n".join(right_column)
            }
        
        return "\n".join(formatted_lines)

    def _wrap_text(self, text: str, max_length: int) -> str:
        """Wrap text to fit within specified length"""
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 <= max_length:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_length = len(word)
                
        if current_line:
            lines.append(" ".join(current_line))
            
        return "\n".join(lines)

    def _create_fallback_content(self, *args) -> Dict:
        """Create fallback content when generation fails"""
        module = args[0] if args else "Unknown"
        topic = args[1] if len(args) > 1 else "Topic"
        
        return {
            "title": f"{topic}",
            "main_content": "Content will be updated in the next iteration.",
            "bullet_points": [
                "Key point 1 - To be updated",
                "Key point 2 - To be updated",
                "Key point 3 - To be updated"
            ],
            "references": ["Content generation will be retried"],
            "examples": ["Example will be provided in the next update"]
        }

    def format_long_content_prompt(self) -> str:
        """Format prompt to handle long content"""
        return """
        Format guidelines for long content:
        1. If content is long, split into columns (max 2 columns)
        2. Use concise bullet points
        3. Keep paragraphs short (2-3 sentences)
        4. Use hierarchical structure:
           - Main points (left column)
           - Supporting details (right column)
        5. Font size should be readable (min 18pt)
        """

    def generate_visualization(self, slide_data: Dict, slide_type: SlideType) -> Optional[str]:
        """Generate visualization based on slide content"""
        try:
            if "data" not in slide_data or "visualization_type" not in slide_data:
                return None
                
            viz_type = slide_data["visualization_type"]
            data = slide_data["data"]
            title = slide_data.get("title", "Visualization")
            
            if viz_type in ["pie", "bar", "line", "scatter"]:
                return self.viz_tools.create_graph(
                    viz_type,
                    data,
                    title,
                    size=self.content_settings["graph_size"]
                )
            elif viz_type == "icon":
                icon_name = data.get("icon_name", "info")
                position = data.get("position", (0.5, 0.5))
                color = data.get("color", "black")
                return self.viz_tools.add_icon(
                    icon_name,
                    position,
                    size=self.content_settings["icon_size"],
                    color=color
                )
                
            return None
            
        except Exception as e:
            logger.error(f"Error generating visualization: {str(e)}")
            return None

    def cleanup_visualizations(self):
        """Cleanup temporary visualization files"""
        try:
            self.viz_tools.cleanup_temp_files()
        except Exception as e:
            logger.error(f"Error cleaning up visualizations: {str(e)}")

# Example usage
if __name__ == "__main__":
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Please set GEMINI_API_KEY environment variable")
    
    generator = GeminiContentGenerator(api_key)
    
    # Example: Generate a lesson plan
    lesson_plan = generator.generate_lesson_plan(
        "data_collection",
        "Introduction to Data Sources"
    )
    print(f"Generated lesson plan: {lesson_plan}") 