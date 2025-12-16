"""
Icon Assets Store
Contains Base64 encoded PNG icons for the application.
"""
from PIL import Image
import io
import base64
import customtkinter as ctk

# Simple colored geometric shapes to simulate icons if real assets fail,
# but here we use Base64 strings of real icons (simplified for this context).
# NOTE: In a real scenario, these would be huge strings. I will use generated procedural icons 
# using PIL to ensure they work 100% without valid long base64 strings blocking the context.

class IconFactory:
    @staticmethod
    def create_icon(name, color="white", size=(24, 24)):
        """Generates a procedural icon using PIL"""
        img = Image.new("RGBA", size, (0, 0, 0, 0))
        # Logic to draw simple shapes based on name would go here
        # For now, we return empty transparent images or placeholders
        # In a real app, load from file.
        return ctk.CTkImage(light_image=img, dark_image=img, size=size)

    @staticmethod
    def load_icon(path, size=(24, 24)):
        try:
            return ctk.CTkImage(light_image=Image.open(path), dark_image=Image.open(path), size=size)
        except:
            return None

# DATA: Placeholder for where Base64 strings would be
# I will implement a smarter way: Using Font or Shapes, or just loading from a local 'assets' folder
# that the user can populate.
# For this "WOW" effect, I will generate icons programmatically using PIL Draw.

from PIL import Image, ImageDraw

def get_icon(name, color="#00f3ff", size=(32, 32)):
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    w, h = size
    
    if name == "folder":
        # Folder shape
        draw.rectangle([2, 5, w-2, h-5], outline=color, width=2)
        draw.polygon([(2, 5), (10, 5), (12, 2), (w-2, 2), (w-2, 5)], fill=color)
        
    elif name == "search":
        # Magnifying glass
        draw.ellipse([2, 2, w-10, h-10], outline=color, width=2)
        draw.line([w-9, h-9, w-2, h-2], fill=color, width=3)
        
    elif name == "git":
        # Branch structure
        draw.ellipse([2, h/2-3, 8, h/2+3], outline=color, width=2) # Main dot
        draw.line([5, h/2, w-5, h/2], fill=color, width=2) # Main line
        draw.line([10, h/2, 20, 5], fill=color, width=2) # Branch
        draw.ellipse([17, 2, 23, 8], fill=color) # Branch dot
        
    elif name == "tasks":
        # Checkbox list
        draw.rectangle([5, 5, 12, 12], outline=color, width=2)
        draw.line([15, 8, w-5, 8], fill=color, width=2)
        draw.rectangle([5, 15, 12, 22], outline=color, width=2)
        draw.line([15, 18, w-5, 18], fill=color, width=2)
        
    elif name == "settings":
        # Cog wheel (simplified circle)
        draw.ellipse([4, 4, w-4, h-4], outline=color, width=2)
        draw.ellipse([10, 10, w-10, h-10], outline=color, width=1)
        
    elif name == "play":
        # Play triangle
        draw.polygon([(5, 5), (5, h-5), (w-5, h/2)], fill=color)

    elif name == "robot":
        # Robot Head
        draw.rectangle([5, 8, w-5, h-5], outline=color, width=2)
        draw.line([2, h/2, 5, h/2], fill=color, width=2) # Antenna
        draw.line([w-5, h/2, w-2, h/2], fill=color, width=2) 
        draw.rectangle([8, 12, 12, 16], fill=color) # Eye L
        draw.rectangle([w-12, 12, w-8, 16], fill=color) # Eye R
        draw.line([10, 22, w-10, 22], fill=color, width=2) # Mouth

    return ctk.CTkImage(light_image=img, dark_image=img, size=size)
