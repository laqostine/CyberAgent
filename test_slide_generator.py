import os
import sys
from dotenv import load_dotenv
from gemini_content_generator import GeminiContentGenerator
from slide_generator import EnhancedSlideGenerator
import time

def test_slide_generation():
    # Load environment variables
    load_dotenv()
    
    # Get API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not found in .env file")
        print("Please make sure your .env file contains: GEMINI_API_KEY=your_api_key_here")
        return False
    
    try:
        # Initialize generators
        print("Initializing content generator...")
        content_generator = GeminiContentGenerator(api_key)
        
        print("Checking for template file...")
        template_path = "Template-for-training-material.pptx"
        if not os.path.exists(template_path):
            template_path = "template.pptx"
            if not os.path.exists(template_path):
                print("Error: No template file found. Please ensure either 'template.pptx' or 'Template-for-training-material.pptx' exists")
                return False
        
        print(f"Initializing slide generator with template: {template_path}")
        slide_generator = EnhancedSlideGenerator(template_path)
        
        # Generate a test lesson plan
        print("\nGenerating test lesson plan...")
        lesson_plan = content_generator.generate_lesson_plan(
            "test",
            "Test Presentation"
        )
        
        if not lesson_plan:
            print("Error: Failed to generate lesson plan")
            return False
            
        print(f"\nGenerated lesson plan: {lesson_plan.title}")
        
        # Generate slides
        print("\nGenerating slides...")
        slide_generator.generate_lesson_slides(lesson_plan)
        
        # Save presentation
        output_path = "test_presentation.pptx"
        print(f"\nSaving presentation to {output_path}...")
        slide_generator.save_presentation(output_path)
        
        if os.path.exists(output_path):
            print(f"\nTest successful! Presentation saved as {output_path}")
            return True
        else:
            print(f"\nError: Failed to save presentation to {output_path}")
            return False
        
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
        return False
    except Exception as e:
        print(f"\nTest failed with error: {str(e)}")
        return False

if __name__ == "__main__":
    print("Starting slide generator test...\n")
    success = test_slide_generation()
    if not success:
        sys.exit(1) 