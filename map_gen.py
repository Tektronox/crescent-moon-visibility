import json
import os
import subprocess
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

# Load new_moons.json
with open("new_moons.json", "r") as json_file:
    new_moons = json.load(json_file)

# Define constants
TYPE = "evening"
METHOD = "yallop"
MAP_IMAGE = "map.png"  # Reference map image

# Function to capitalize the first letter
def capitalize_first_letter(word):
    return word[0].upper() + word[1:]

# Loop through each year and date in new_moons.json
for year, dates in new_moons.items():
    for date_key, day_info in dates.items():
        for day, details in day_info.items():
            date_str = details["date"]
            # Check if 'img' entry already exists
            if "img" in details:
                print(f"Image already exists for {date_str}. Skipping.")
                continue

            print(f"Processing date: {date_str}")
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")

            # Create filename and path
            img_directory = f"img/{date_obj.year}/{date_key}"
            os.makedirs(img_directory, exist_ok=True)
            img_path = os.path.join(img_directory, f"{date_str}.png")

            # Run visibility.out command to generate base image
            visibility_command = [
                "./visibility.out",
                date_str,
                "map",
                TYPE,
                METHOD,
                img_path
            ]

            # Run visibility.out and check for success
            try:
                subprocess.run(visibility_command, check=True)
                print(f"Visibility calculated for {date_str}")
            except subprocess.CalledProcessError:
                print(f"Error generating image for {date_str}. Skipping.")
                continue

            # Blend with map.png
            try:
                # Open generated image and map image
                base_image = Image.open(img_path).convert("RGBA")
                map_image = Image.open(MAP_IMAGE).convert("RGBA")
                # Blend images with 60% opacity on top of base image
                blended_image = Image.blend(base_image, map_image, alpha=0.6)
            except Exception as e:
                print(f"Error blending image for {date_str}: {e}")
                continue

            # Add label text
            draw = ImageDraw.Draw(blended_image)
            label_text = f"{capitalize_first_letter(TYPE)}, {capitalize_first_letter(METHOD)}, {date_str}"
            font = ImageFont.load_default()  # Use default font

            # Draw the text at the bottom center of the image
            text_width, text_height = draw.textsize(label_text, font=font)
            text_position = ((blended_image.width - text_width) // 2, blended_image.height - text_height - 10)
            draw.text(text_position, label_text, fill="black", font=font)

            # Save the final image
            blended_image.save(img_path)
            print(f"Image saved: {img_path}")

            # Update JSON entry with image path
            details["img"] = img_path

# Save updated new_moons.json
with open("new_moons.json", "w") as json_file:
    json.dump(new_moons, json_file, indent=4)

print("Image generation completed and new_moons.json updated.")
