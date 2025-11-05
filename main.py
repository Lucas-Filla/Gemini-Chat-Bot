from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

import os
import requests

# Configure the client
client = genai.Client()
MODEL = "gemini-2.5-flash"

def main():
    check = 'y'
    while(check == 'y'):
        print("Hello user.")
        action = input("Would you like to chat? (enter: chat) Generate an image? (enter: generate) Or Analyze an Image? (enter: analyze): ")

        if action == "chat":
            print("You can echo text, bring it to upper case/lower case, reverse it, count words, or something else.")
            prompt = input("What would you like to do? : ")
            chat(prompt)
            print()
        elif action == "generate":
            desc = input("Describe the image you would like to generate: ")
            gen_img(desc)
            print()
            print("Image saved to generated_images folder")
            print()
        elif action == "analyze":
            img_path = input("Enter the full image url of the image you would like analyzed: ")
            anal_img(img_path)
            print()
        else:
            print("Invalid input.")
            print()

        check = input("Would you like to prompt again? (y/n): ")

    print("Goodbye.")


def anal_img(img_path: str):
    print()
    print("Oh I'm analyzing it!")

    try:
        image_bytes = requests.get(img_path).content
        image = types.Part.from_bytes(
            data = image_bytes,
            mime_type = "image/jpeg",
        )

        response=client.models.generate_content(
            model = MODEL,
            contents = ["What is this image?", image],
        )

    except:
        print("Error with submitted image")
        return

    print(response.text)

def gen_img(prompt: str):
    img_name = input("What should be the name of this image?: ")

    print()
    print("Oh I'm generating it!")

    try:
        response = client.models.generate_content(
            model = MODEL + "-image",
            contents = [prompt],
        )
    except:
        print("Image could not be generated.")
        return

    # Create file directory if needed
    if not os.path.exists("generated_images"):
        os.makedirs("generated_images")

    for part in response.candidates[0].content.parts: # type: ignore
        if part.text is not None:
            print(part.text)
        elif part.inline_data is not None:
            image = Image.open(BytesIO(part.inline_data.data)) # type: ignore
            image.save("generated_images/" + img_name  + ".png")

def chat(prompt: str):
    config = types.GenerateContentConfig(
        tools = [echo, convert_lower, convert_upper, count_words, reverse],
        system_instruction = "If you are able to use the tools, do so. If not, create the answer yourself"
    )

    response = client.models.generate_content(
        model = MODEL,
        contents = prompt,
        config = config,
    )

    print()
    print(f"Response: {response.text}")

#Simple functions for gemini to use
def echo(text: str):
    """Returns the exact same text back at the user"""
    return text

def convert_upper(text: str):
    """Returns the text in ALL CAPS."""
    return text.upper()

def convert_lower(text: str):
    """Returns the text in all lowercase."""
    return text.lower()

def count_words(text: str):
    """Counts words by simple whitespace split."""
    return len(text.split())

def reverse(text: str):
    """Reverses the characters in the text."""
    return text[::-1]

#runs
if __name__ == "__main__":
    main()
