import os
import logging
import shutil
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv
from gemini_content_generator import GeminiContentGenerator
from slide_generator import EnhancedSlideGenerator
import time
from tqdm import tqdm
import re

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('slide_generator.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class PresentationManager:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("Gemini_API_KEY")
        if not self.api_key:
            raise ValueError("Please set Gemini_API_KEY in your .env file")
        
        self.content_generator = GeminiContentGenerator(self.api_key)
        self.template_path = self._find_template()
        self._create_output_directory()
        
    def _find_template(self) -> str:
        """Find the template file and validate it exists"""
        template_paths = [
            "template.pptx",
            "Template-for-training-material.pptx",
            "templates/template.pptx"
        ]
        
        for path in template_paths:
            if os.path.exists(path):
                logger.info(f"Found template file: {path}")
                return path
                
        # If no template found, copy the default template
        default_template = "Template-for-training-material.pptx"
        if os.path.exists(default_template):
            template_path = "template.pptx"
            shutil.copy2(default_template, template_path)
            logger.info(f"Copied default template to: {template_path}")
            return template_path
            
        raise FileNotFoundError("No template file found. Please ensure 'template.pptx' or 'Template-for-training-material.pptx' exists in the current directory.")

    def _create_output_directory(self):
        """Create output directories if they don't exist"""
        self.output_dir = "presentations"
        self.backup_dir = os.path.join(self.output_dir, "backups")
        os.makedirs(self.output_dir, exist_ok=True)
        os.makedirs(self.backup_dir, exist_ok=True)
        
    def _generate_filename(self, module: str, lesson_title: str) -> str:
        """Generate a filename based on module and lesson title"""
        # Clean the module and lesson title to create a valid filename
        clean_name = lambda s: re.sub(r'[^\w\s-]', '', s).strip().replace(' ', '_')
        module_name = clean_name(module)
        lesson_name = clean_name(lesson_title)
        
        # Get the next version number
        base_name = f"{module_name}_{lesson_name}"
        pattern = f"{base_name}_v(\\d+).pptx"
        
        version = 1
        existing_files = os.listdir(self.output_dir)
        for file in existing_files:
            match = re.match(pattern, file)
            if match:
                version = max(version, int(match.group(1)) + 1)
        
        return f"{base_name}_v{version}.pptx"
        
    def create_backup(self, original_file: str) -> str:
        """Create a backup of the existing presentation"""
        if os.path.exists(original_file):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.basename(original_file)
            backup_file = os.path.join(self.backup_dir, f"backup_{timestamp}_{filename}")
            shutil.copy2(original_file, backup_file)
            logger.info(f"Created backup: {backup_file}")
            return backup_file
        return ""

    def generate_presentation(self, module: str, lesson_title: str) -> Optional[str]:
        """Generate a presentation for a specific lesson"""
        try:
            print("\nGenerating presentation...")
            logger.info(f"Generating presentation for module: {module}, lesson: {lesson_title}")
            
            # Generate output filename
            output_filename = self._generate_filename(module, lesson_title)
            output_path = os.path.join(self.output_dir, output_filename)
            
            # Create backup if file exists
            if os.path.exists(output_path):
                self.create_backup(output_path)
            
            # Show progress bar for content generation
            with tqdm(total=4, desc="Progress") as pbar:
                # Generate content
                pbar.set_description("Generating lesson plan")
                lesson_plan = self.content_generator.generate_lesson_plan(module, lesson_title)
                logger.info(f"Generated lesson plan: {lesson_plan.title}")
                pbar.update(1)
                
                # Initialize slide generator
                pbar.set_description("Initializing slide generator")
                slide_generator = EnhancedSlideGenerator(self.template_path)
                pbar.update(1)
                
                # Generate slides
                pbar.set_description("Generating slides")
                slide_generator.generate_lesson_slides(lesson_plan)
                pbar.update(1)
                
                # Save presentation
                pbar.set_description("Saving presentation")
                slide_generator.save_presentation(output_path)
                logger.info(f"Presentation saved as {output_path}")
                pbar.update(1)
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error generating presentation: {str(e)}", exc_info=True)
            return None

def clear_screen():
    """Clear the console screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu() -> None:
    """Display the main menu"""
    clear_screen()
    print("\n=== CyberAgent Slide Generator ===")
    print("\nComprehensive Cybersecurity Data Analytics Course")
    print("\nOptions:")
    print("1. Generate Complete Presentation (60 slides)")
    print("2. View Presentation Structure")
    print("3. Help")
    print("4. Exit")
    print("\nType 'help' for more information or 'exit' to quit")

def display_structure():
    """Display the presentation structure"""
    clear_screen()
    print("\n=== Presentation Structure ===")
    print("\nTitle: Comprehensive Data Analytics in Cybersecurity")
    print("\nSections:")
    print("1. Introduction and Fundamentals (9 slides)")
    print("   - Course Overview")
    print("   - Basic Concepts")
    print("   - Industry Context")
    print("\n2. Data Collection and SIEM (12 slides)")
    print("   - Data Sources")
    print("   - SIEM Systems")
    print("   - Collection Methods")
    print("\n3. Data Cleaning and Preprocessing (12 slides)")
    print("   - Cleaning Techniques")
    print("   - Data Quality")
    print("   - Preprocessing Steps")
    print("\n4. Data Analysis and Detection (12 slides)")
    print("   - Analysis Methods")
    print("   - Threat Detection")
    print("   - Pattern Recognition")
    print("\n5. Visualization and Reporting (10 slides)")
    print("   - Visualization Tools")
    print("   - Dashboard Design")
    print("   - Reporting Best Practices")
    print("\n6. Practical Applications (5 slides)")
    print("   - Case Studies")
    print("   - Real-world Examples")
    print("   - Future Trends")
    input("\nPress Enter to return to the main menu...")

def display_help():
    """Display help information"""
    clear_screen()
    print("\n=== Help Information ===")
    print("\nThis application generates a comprehensive 60-slide PowerPoint presentation")
    print("covering the complete Cybersecurity Data Analytics curriculum.")
    print("\nPresentation Features:")
    print("- Complete coverage of all major topics")
    print("- Interactive exercises and practical examples")
    print("- Real-world case studies")
    print("- Assessment questions")
    print("\nNotes:")
    print("- Backups are automatically created")
    print("- Check 'slide_generator.log' for detailed information")
    print("- Requires 'template.pptx' in the current directory")
    input("\nPress Enter to return to the main menu...")

def main():
    try:
        presentation_manager = PresentationManager()
        
        while True:
            display_menu()
            choice = input("\nEnter your choice (1-4): ").lower()
            
            if choice == '3' or choice == 'help':
                display_help()
                continue
                
            if choice in ['4', 'exit', 'quit']:
                logger.info("Exiting program")
                print("\nThank you for using CyberAgent Slide Generator!")
                break
            
            if choice == '2':
                display_structure()
                continue
            
            if choice == '1':
                print("\nGenerating comprehensive presentation...")
                output_path = presentation_manager.generate_presentation(
                    "comprehensive",
                    "Comprehensive Data Analytics in Cybersecurity"
                )
                
                if output_path:
                    print(f"\nPresentation generated successfully!")
                    print(f"File saved as: {output_path}")
                    print("\nA backup of any previous presentation was created automatically.")
                else:
                    print("\nError generating presentation. Check the logs for details.")
                
                input("\nPress Enter to continue...")
            else:
                print("Please enter a valid choice (1-4)")
                time.sleep(2)
                
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        print("\nAn unexpected error occurred. Check the logs for details.")
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main() 