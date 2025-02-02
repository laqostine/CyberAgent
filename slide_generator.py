from pptx import Presentation
from pptx.util import Pt, Inches
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE_TYPE
from gemini_content_generator import GeminiContentGenerator, SlideContent, SlideType, LessonPlan
from template_config import get_layout_info, get_placeholder_info, get_formatting
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
logger = logging.getLogger(__name__)

class EnhancedSlideGenerator:
    def __init__(self, template_path: str):
        """Initialize the slide generator with a template"""
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template file not found: {template_path}")
        
        self.presentation = Presentation(template_path)
        self.template_path = template_path
        logger.info(f"Initialized slide generator with template: {template_path}")

    def _get_slide_layout(self, slide_type: str) -> int:
        """Get the appropriate slide layout index"""
        layout_info = get_layout_info(slide_type)
        if not layout_info:
            logger.warning(f"Layout not found for type {slide_type}, using default")
            return 0
        return layout_info['index']

    def _apply_formatting(self, text_frame, element_type: str) -> None:
        """Apply formatting settings to a text frame"""
        formatting = get_formatting(element_type)
        
        for paragraph in text_frame.paragraphs:
            for run in paragraph.runs:
                if formatting.get('font_size'):
                    run.font.size = Pt(formatting['font_size'])
                if formatting.get('font_bold') is not None:
                    run.font.bold = formatting['font_bold']
                if formatting.get('font_name'):
                    run.font.name = formatting['font_name']

    def _set_placeholder_text(self, slide, placeholder_name: str, text: str, 
                            layout_type: str, element_type: str = None) -> None:
        """Set text in a placeholder with proper formatting"""
        ph_info = get_placeholder_info(layout_type, placeholder_name)
        if not ph_info:
            logger.warning(f"Placeholder {placeholder_name} not found in layout {layout_type}")
            return
        
        try:
            shape = slide.placeholders[ph_info['idx']]
            shape.text = text
            
            # Apply formatting
            if element_type:
                self._apply_formatting(shape.text_frame, element_type)
                
        except KeyError as e:
            logger.error(f"Error setting placeholder text: {str(e)}")
            raise

    def create_title_slide(self, content: SlideContent) -> None:
        """Create a title slide with the given content"""
        layout_idx = self._get_slide_layout('title')
        slide = self.presentation.slides[0]
        
        # Set title
        self._set_placeholder_text(slide, 'title', content.title, 'title', 'title')
        
        # Set subtitle/description
        self._set_placeholder_text(slide, 'subtitle', content.main_content, 'title', 'subtitle')
        
        logger.info(f"Created title slide: {content.title}")

    def create_content_slide(self, content: SlideContent) -> None:
        """Create a content slide based on the slide type"""
        layout_idx = self._get_slide_layout(content.slide_type.value)
        slide = self.presentation.slides.add_slide(self.presentation.slide_layouts[layout_idx])
        
        # Set title
        self._set_placeholder_text(slide, 'title', content.title, content.slide_type.value, 'title')
        
        # Add content based on slide type
        try:
            if content.slide_type == SlideType.CONTENT:
                self._add_content_body(slide, content)
            elif content.slide_type == SlideType.INTERACTIVE:
                self._add_interactive_content(slide, content)
            elif content.slide_type == SlideType.LAB:
                self._add_lab_content(slide, content)
            elif content.slide_type == SlideType.QUIZ:
                self._add_quiz_content(slide, content)
            elif content.slide_type == SlideType.SUMMARY:
                self._add_summary_content(slide, content)
        except Exception as e:
            logger.error(f"Error adding content to slide: {str(e)}")
            self._add_fallback_content(slide, content)

    def _add_content_body(self, slide, content: SlideContent) -> None:
        """Add regular content with bullet points"""
        self._set_placeholder_text(slide, 'content', content.main_content, 'content', 'body')
        
        if content.bullet_points:
            shape = slide.placeholders[get_placeholder_info('content', 'content')['idx']]
            tf = shape.text_frame
            tf.text = content.main_content
            
            for point in content.bullet_points:
                p = tf.add_paragraph()
                p.text = point
                p.level = 0
                self._apply_formatting(p, 'bullet')

    def _add_interactive_content(self, slide, content: SlideContent) -> None:
        """Add interactive content with discussion points"""
        shape = slide.placeholders[get_placeholder_info('content', 'content')['idx']]
        tf = shape.text_frame
        tf.text = "Discussion Points:"
        self._apply_formatting(tf, 'body')
        
        if content.interactive_elements:
            for point in content.interactive_elements.get("points", []):
                p = tf.add_paragraph()
                p.text = f"👉 {point}"
                p.level = 0
                self._apply_formatting(p, 'bullet')

    def _add_lab_content(self, slide, content: SlideContent) -> None:
        """Add lab exercise content"""
        shape = slide.placeholders[get_placeholder_info('content', 'content')['idx']]
        tf = shape.text_frame
        tf.text = "Lab Exercise"
        self._apply_formatting(tf, 'body')
        
        if content.interactive_elements:
            # Add objectives
            p = tf.add_paragraph()
            p.text = "Objectives:"
            self._apply_formatting(p, 'body')
            
            for obj in content.interactive_elements.get("objectives", []):
                p = tf.add_paragraph()
                p.text = f"• {obj}"
                p.level = 1
                self._apply_formatting(p, 'bullet')

    def _add_quiz_content(self, slide, content: SlideContent) -> None:
        """Add quiz questions"""
        shape = slide.placeholders[get_placeholder_info('content', 'content')['idx']]
        tf = shape.text_frame
        tf.text = "Knowledge Check"
        self._apply_formatting(tf, 'body')
        
        if content.interactive_elements:
            for i, question in enumerate(content.interactive_elements.get("questions", []), 1):
                p = tf.add_paragraph()
                p.text = f"\nQ{i}: {question['question']}"
                self._apply_formatting(p, 'body')
                
                for option in question.get("options", []):
                    p = tf.add_paragraph()
                    p.text = f"   □ {option}"
                    p.level = 1
                    self._apply_formatting(p, 'bullet')

    def _add_summary_content(self, slide, content: SlideContent) -> None:
        """Add summary content"""
        shape = slide.placeholders[get_placeholder_info('content', 'content')['idx']]
        tf = shape.text_frame
        tf.text = "Key Takeaways:"
        self._apply_formatting(tf, 'body')
        
        if content.bullet_points:
            for point in content.bullet_points:
                p = tf.add_paragraph()
                p.text = f"✓ {point}"
                p.level = 0
                self._apply_formatting(p, 'bullet')

    def generate_lesson_slides(self, lesson_plan: LessonPlan) -> None:
        """Generate all slides for a lesson"""
        try:
            # Create title slide
            logger.info("Creating title slide...")
            title_content = SlideContent(
                title=lesson_plan.title,
                main_content=lesson_plan.description,
                slide_type=SlideType.TITLE
            )
            self.create_title_slide(title_content)
            
            # Create content slides
            for i, slide in enumerate(lesson_plan.slides, 1):
                logger.info(f"Creating slide {i} of {len(lesson_plan.slides)}...")
                self.create_content_slide(slide)
                
        except Exception as e:
            logger.error(f"Error in generate_lesson_slides: {str(e)}", exc_info=True)
            raise

    def save_presentation(self, output_path: str) -> None:
        """Save the presentation to the specified path"""
        try:
            self.presentation.save(output_path)
            logger.info(f"Presentation saved successfully to {output_path}")
        except Exception as e:
            logger.error(f"Error saving presentation: {str(e)}")
            raise

def main():
    # Initialize Gemini content generator
    api_key = os.getenv("Gemini_API_KEY")
    if not api_key:
        raise ValueError("Please set Gemini_API_KEY in your .env file")
    
    content_generator = GeminiContentGenerator(api_key)
    slide_generator = EnhancedSlideGenerator("template.pptx")
    
    # Generate a complete lesson plan
    lesson_plan = content_generator.generate_lesson_plan(
        "data_collection",
        "Introduction to Data Sources"
    )
    
    # Generate all slides for the lesson
    slide_generator.generate_lesson_slides(lesson_plan)
    
    # Save the presentation
    output_path = "Updated_CyberAgent_Slide.pptx"
    slide_generator.save_presentation(output_path)
    print(f"Presentation saved as {output_path}")

if __name__ == "__main__":
    main() 