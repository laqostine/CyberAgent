import google.generativeai as genai
from enum import Enum
from typing import Dict, List, Optional, Literal
from dataclasses import dataclass
from dotenv import load_dotenv
import logging
import json
import time

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
        
        # Define the module structure
        self.modules = {
            "data_collection": {
                "title": "Data Collection in Cybersecurity",
                "lessons": [
                    {"title": "Introduction to Data Sources", "slides": range(1, 6)},
                    {"title": "SIEM Systems", "slides": range(6, 11)},
                    {"title": "Practical Data Collection", "slides": range(11, 21)}
                ]
            },
            "data_cleaning": {
                "title": "Data Cleaning and Preprocessing",
                "lessons": [
                    {"title": "Importance of Data Cleaning", "slides": range(1, 6)},
                    {"title": "Data Cleaning Techniques", "slides": range(6, 16)},
                    {"title": "Python and Pandas Demo", "slides": range(16, 21)}
                ]
            },
            "data_analysis": {
                "title": "Data Analysis in Cybersecurity",
                "lessons": [
                    {"title": "Analysis Techniques", "slides": range(1, 6)},
                    {"title": "Exploratory Data Analysis", "slides": range(6, 11)},
                    {"title": "Threat Detection Examples", "slides": range(11, 21)}
                ]
            },
            "data_visualization": {
                "title": "Data Visualization for Security",
                "lessons": [
                    {"title": "Visualization Basics", "slides": range(1, 6)},
                    {"title": "Tools and Libraries", "slides": range(6, 16)},
                    {"title": "Security Metrics Visualization", "slides": range(16, 21)}
                ]
            },
            "applications": {
                "title": "Applied Data Analytics in Cybersecurity",
                "lessons": [
                    {"title": "Case Studies", "slides": range(1, 6)},
                    {"title": "SME Anomaly Detection", "slides": range(6, 16)},
                    {"title": "Course Summary", "slides": range(16, 21)}
                ]
            }
        }

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
        """Generate a complete lesson plan with all slides"""
        prompt = f"""
        Create a detailed cybersecurity training lesson plan for SMEs.
        Module: {module}
        Lesson: {lesson_title}

        Generate:
        1. A lesson title (max 8 words)
        2. Brief description (2-3 sentences)
        3. 3-5 specific learning objectives
        4. Practical activity or lab exercise
        5. Assessment questions (2-3 multiple choice)

        Format the response in a clear, structured way.
        Ensure content is practical and relevant for SME environments.
        The response must be valid JSON matching this structure:
        {json.dumps(self.lesson_plan_schema, indent=2)}
        Return only the JSON object, no additional text or formatting.
        """
        
        try:
            for _ in self._handle_api_error():
                response = self.model.generate_content(prompt)
                lesson_data = self._extract_json_from_response(response.text)
                return self._create_lesson_plan(lesson_data)
            
        except Exception as e:
            logger.error(f"Error generating lesson plan: {str(e)}")
            raise

    def generate_slide_content(self, module: str, lesson_title: str, slide_type: SlideType) -> SlideContent:
        """Generate content for a specific slide type"""
        prompt = f"""
        Create content for a {slide_type.value} slide in a cybersecurity training presentation.
        Module: {module}
        Lesson: {lesson_title}

        Requirements:
        1. Title: Clear, concise (max 5 words)
        2. Main Content: {self._get_slide_type_requirements(slide_type)}
        3. Format: Structured, easy to read
        4. Tone: Professional, educational
        5. Level: Suitable for SME staff

        Include practical examples relevant to small and medium enterprises.
        The response must be valid JSON matching this structure:
        {json.dumps(self.slide_content_schema, indent=2)}
        Return only the JSON object, no additional text or formatting.
        """
        
        try:
            for _ in self._handle_api_error():
                response = self.model.generate_content(prompt)
                slide_data = self._extract_json_from_response(response.text)
                return self._create_slide_content(slide_data, slide_type)
            
        except Exception as e:
            logger.error(f"Error generating slide content: {str(e)}")
            # Return a fallback slide content
            return SlideContent(
                title=f"{slide_type.value.title()} Slide",
                main_content="Content generation failed. Please try again.",
                slide_type=slide_type
            )

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
            SlideType.TITLE: "Introduction to the topic and key points to be covered",
            SlideType.CONTENT: "2-3 key points with brief explanations",
            SlideType.INTERACTIVE: "Discussion question or activity with guidance",
            SlideType.LAB: "Step-by-step instructions for practical exercise",
            SlideType.QUIZ: "2-3 multiple choice questions with answers",
            SlideType.SUMMARY: "Key takeaways and next steps"
        }
        return requirements.get(slide_type, "")

    def _generate_lesson_slides(self, title: str, description: str, objectives: List[str], activities: Dict) -> List[SlideContent]:
        """Generate a complete set of 20 slides for the lesson"""
        slides = []
        
        # 1. Title slide
        slides.append(SlideContent(
            title=title,
            main_content=description,
            slide_type=SlideType.TITLE
        ))
        
        # 2. Objectives slide
        slides.append(SlideContent(
            title="Learning Objectives",
            main_content="By the end of this lesson, you will be able to:",
            slide_type=SlideType.CONTENT,
            bullet_points=objectives
        ))
        
        # 3-15. Content slides (12 slides)
        for i in range(12):
            content = self.generate_slide_content(title, f"Content Part {i+1}", SlideType.CONTENT)
            slides.append(content)
        
        # 16-17. Interactive slides (2 slides)
        for i in range(2):
            content = self.generate_slide_content(title, f"Interactive {i+1}", SlideType.INTERACTIVE)
            slides.append(content)
        
        # 18. Lab Exercise slide
        slides.append(SlideContent(
            title="Hands-on Lab Exercise",
            main_content=activities["title"],
            slide_type=SlideType.LAB,
            interactive_elements={
                "objectives": activities["steps"][:3],
                "tools": ["Wireshark", "Zabbix", "Nessus"]
            }
        ))
        
        # 19. Quiz slide
        quiz_content = self.generate_slide_content(title, "Knowledge Check", SlideType.QUIZ)
        slides.append(quiz_content)
        
        # 20. Summary slide
        summary_content = self.generate_slide_content(title, "Summary", SlideType.SUMMARY)
        slides.append(summary_content)
        
        return slides

    def generate_quiz_questions(self, module: str, lesson_title: str) -> List[Dict]:
        """Generate quiz questions for assessment"""
        prompt = f"""
        Create assessment questions for a cybersecurity training module.
        Module: {module}
        Lesson: {lesson_title}

        Generate:
        1. 3 multiple choice questions
        2. 2 short answer questions
        3. 1 practical scenario question

        Questions should test understanding of key concepts and practical application.
        """
        
        response = self.model.generate_content(prompt)
        # TODO: Implement parsing of quiz questions
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