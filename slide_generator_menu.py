import os
import logging
import shutil
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv
from gemini_content_generator import GeminiContentGenerator
from deneme import SlideGenerator
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
        template_path = "template.pptx"
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template file '{template_path}' not found. Please ensure it exists in the current directory.")
        return template_path

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
                slide_generator = SlideGenerator(self.template_path)
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
    print("\nAvailable Modules:")
    print("1. Data Collection")
    print("2. Data Cleaning")
    print("3. Data Analysis")
    print("4. Data Visualization")
    print("5. Applications")
    print("6. Exit")
    print("\nType 'help' for more information or 'exit' to quit")

def display_help():
    """Display help information"""
    clear_screen()
    print("\n=== Help Information ===")
    print("\nThis application generates PowerPoint presentations for the CyberAgent cybersecurity curriculum.")
    print("\nInstructions:")
    print("1. Select a module number (1-5)")
    print("2. Choose a lesson from the available options")
    print("3. Wait for the presentation to generate")
    print("4. Find your presentation in the current directory")
    print("\nNotes:")
    print("- Backups are automatically created before generating new presentations")
    print("- Check 'slide_generator.log' for detailed information")
    print("- The template file 'template.pptx' must be present in the current directory")
    input("\nPress Enter to return to the main menu...")

def get_module_info(choice: int) -> tuple:
    """Get module and lesson information based on menu choice"""
    module_map = {
        1: ("data_collection", [
            "Introduction to Data Sources",
            "SIEM Systems",
            "Practical Data Collection"
        ]),
        2: ("data_cleaning", [
            "Importance of Data Cleaning",
            "Data Cleaning Techniques",
            "Python and Pandas Demo"
        ]),
        3: ("data_analysis", [
            "Analysis Techniques",
            "Exploratory Data Analysis",
            "Threat Detection Examples"
        ]),
        4: ("data_visualization", [
            "Visualization Basics",
            "Tools and Libraries",
            "Security Metrics Visualization"
        ]),
        5: ("applications", [
            "Case Studies",
            "SME Anomaly Detection",
            "Course Summary"
        ])
    }
    
    if choice not in module_map:
        return None, []
    
    return module_map[choice]

def display_lessons(lessons: list) -> None:
    """Display available lessons for selected module"""
    print("\nAvailable Lessons:")
    for i, lesson in enumerate(lessons, 1):
        print(f"{i}. {lesson}")
    print(f"{len(lessons) + 1}. Back to main menu")

def main():
    try:
        presentation_manager = PresentationManager()
        
        while True:
            display_menu()
            choice = input("\nEnter your choice (1-6 or 'help'): ").lower()
            
            if choice == 'help':
                display_help()
                continue
                
            if choice in ['6', 'exit', 'quit']:
                logger.info("Exiting program")
                print("\nThank you for using CyberAgent Slide Generator!")
                break
            
            try:
                choice = int(choice)
                if choice < 1 or choice > 5:
                    logger.warning("Invalid choice selected")
                    print("Please enter a valid choice (1-6)")
                    time.sleep(2)
                    continue
                
                module, lessons = get_module_info(choice)
                if not module:
                    logger.error("Invalid module selected")
                    continue
                
                while True:
                    clear_screen()
                    display_lessons(lessons)
                    try:
                        lesson_choice = input(f"\nSelect a lesson (1-{len(lessons) + 1}): ")
                        
                        if lesson_choice.lower() in ['b', 'back']:
                            break
                            
                        lesson_choice = int(lesson_choice)
                        if lesson_choice == len(lessons) + 1:
                            break
                        
                        if lesson_choice < 1 or lesson_choice > len(lessons):
                            logger.warning("Invalid lesson choice selected")
                            print(f"Please enter a valid choice (1-{len(lessons) + 1})")
                            time.sleep(2)
                            continue
                        
                        lesson_title = lessons[lesson_choice - 1]
                        logger.info(f"Selected module: {module}, lesson: {lesson_title}")
                        
                        output_path = presentation_manager.generate_presentation(module, lesson_title)
                        if output_path:
                            print(f"\nPresentation generated successfully!")
                            print(f"File saved as: {output_path}")
                            print("\nA backup of any previous presentation was created automatically.")
                        else:
                            print("\nError generating presentation. Check the logs for details.")
                        
                        input("\nPress Enter to continue...")
                        break
                        
                    except ValueError:
                        logger.warning("Invalid input for lesson choice")
                        print("Please enter a valid number")
                        time.sleep(2)
                
            except ValueError:
                logger.warning("Invalid input for main menu choice")
                print("Please enter a valid number")
                time.sleep(2)
                
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        print("\nAn unexpected error occurred. Check the logs for details.")
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main() 