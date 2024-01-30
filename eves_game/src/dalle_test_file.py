from openai import OpenAI
import src.config as config

# Set your OpenAI API key
api_key = config.openai['api_key']


def generate_image(prompt):
    # Customize 'model' and 'n' based on your requirements
    client = OpenAI(api_key=api_key)
    response = client.images.generate(
        model="dall-e-3",  # Choose the model engine
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,  # Number of completions
    )

    # Extract the generated image URL from the API response
    image_url = response.data[0].url

    return image_url


# Example prompt for a location description
prompt = "A two year olds bedroom. With white walls. One one wall wall is an painting of a teddy bear sat on a cloud. The bedroom has two doors, one door leads to the living room and the other door out to a balcony. There is cot, a set of draws/changing table and trundle bed. All the bedroom future is made from white wood. The floor is pine. In one corner is a pink chair with lots of stuffed toys."

# Generate image based on the prompt
image_url = generate_image(prompt)

print(f"Generated Image URL: {image_url}")
