import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, List, Optional, Tuple
import os
import logging

# Configure logging
logger = logging.getLogger(__name__)

# Create directories for temporary files
os.makedirs("temp_graphs", exist_ok=True)
os.makedirs("temp_icons", exist_ok=True)

class VisualizationTools:
    def __init__(self):
        # Set style for graphs
        plt.style.use('seaborn')
        sns.set_palette("husl")
        
        # Default settings
        self.default_graph_size = (6, 4)
        self.default_icon_size = (1, 1)
        self.default_colors = sns.color_palette("husl", 8).as_hex()
        
        # Icon mappings
        self.icon_map = {
            "warning": "⚠️",
            "info": "ℹ️",
            "check": "✓",
            "cross": "✗",
            "security": "🔒",
            "data": "📊",
            "network": "🌐",
            "user": "👤",
            "server": "🖥️",
            "cloud": "☁️",
            "alert": "🚨",
            "success": "✅",
            "error": "❌",
        }

    def create_graph(
        self,
        graph_type: str,
        data: Dict[str, List],
        title: str,
        colors: Optional[List[str]] = None,
        size: Tuple[int, int] = None
    ) -> str:
        """Creates a graph and saves it as an image."""
        try:
            # Set figure size
            size = size or self.default_graph_size
            plt.figure(figsize=size)
            
            # Use default colors if none provided
            colors = colors or self.default_colors
            
            # Create graph based on type
            if graph_type == "pie":
                plt.pie(data["values"], labels=data["labels"], colors=colors, autopct='%1.1f%%')
                plt.axis('equal')
            
            elif graph_type == "bar":
                plt.bar(data["labels"], data["values"], color=colors[:len(data["values"])])
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
            
            elif graph_type == "line":
                plt.plot(data["labels"], data["values"], marker='o', color=colors[0])
                plt.xticks(rotation=45, ha='right')
                plt.grid(True, linestyle='--', alpha=0.7)
                plt.tight_layout()
            
            elif graph_type == "scatter":
                plt.scatter(data["x_values"], data["y_values"], c=colors[0])
                plt.grid(True, linestyle='--', alpha=0.7)
                plt.tight_layout()
            
            else:
                raise ValueError(f"Unsupported graph type: {graph_type}")
            
            # Add title and styling
            plt.title(title, pad=20, fontsize=12, fontweight='bold')
            
            # Save the graph
            output_path = f"temp_graphs/{title.lower().replace(' ', '_')}.png"
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Successfully created {graph_type} graph: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating graph: {str(e)}")
            plt.close()  # Make sure to close the figure in case of error
            raise

    def add_icon(
        self,
        icon_name: str,
        position: Tuple[float, float],
        size: Optional[Tuple[float, float]] = None,
        color: str = "black"
    ) -> str:
        """Creates an icon and saves it as an image."""
        try:
            # Use default size if none provided
            size = size or self.default_icon_size
            
            # Convert size to pixels (assuming 100 pixels per inch)
            pixel_size = (int(size[0] * 100), int(size[1] * 100))
            
            # Create a new image with transparency
            img = Image.new('RGBA', pixel_size, (255, 255, 255, 0))
            draw = ImageDraw.Draw(img)
            
            # Get icon symbol
            icon = self.icon_map.get(icon_name.lower())
            if not icon:
                logger.warning(f"Icon '{icon_name}' not found, using default")
                icon = "•"
            
            # Calculate font size (80% of smallest dimension)
            font_size = int(min(pixel_size) * 0.8)
            
            try:
                # Try to load Arial font
                font = ImageFont.truetype("arial.ttf", font_size)
            except OSError:
                # Fallback to default font
                font = ImageFont.load_default()
                logger.warning("Arial font not found, using default font")
            
            # Calculate text position to center it
            text_bbox = draw.textbbox((0, 0), icon, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            x = (pixel_size[0] - text_width) // 2
            y = (pixel_size[1] - text_height) // 2
            
            # Draw the icon
            draw.text((x, y), icon, fill=color, font=font)
            
            # Save the icon
            output_path = f"temp_icons/{icon_name.lower()}_{color.lower()}.png"
            img.save(output_path)
            
            logger.info(f"Successfully created icon: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Error creating icon: {str(e)}")
            raise

    def cleanup_temp_files(self):
        """Cleanup temporary files after they're added to the presentation."""
        try:
            for directory in ["temp_graphs", "temp_icons"]:
                for file in os.listdir(directory):
                    file_path = os.path.join(directory, file)
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        logger.warning(f"Error removing temporary file {file_path}: {str(e)}")
        except Exception as e:
            logger.error(f"Error during cleanup: {str(e)}")

# Example usage
if __name__ == "__main__":
    # Create visualization tools instance
    viz_tools = VisualizationTools()
    
    # Example: Create a pie chart
    data = {
        "labels": ["A", "B", "C", "D"],
        "values": [30, 20, 25, 25]
    }
    viz_tools.create_graph("pie", data, "Sample Pie Chart")
    
    # Example: Create an icon
    viz_tools.add_icon("security", (0.5, 0.5))
    
    # Cleanup
    viz_tools.cleanup_temp_files() 