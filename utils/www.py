import requests
from typing import List, Tuple


def check_email_adress(email: str) -> Tuple[bool, str]:
    message = [True, 'email adress is OK']
    # Make sure it's a string
    if not isinstance(email, str):
        message = [False, 'email adress is not a string']

    # Make sure it has @
    if ('@' not in email) or ('.' not in email):
        message = [False, 'email adress is not a valid string']

    # Make sure has suffix
    splt = email.split('.')
    if any(len(i_)==0 for i_ in splt):
        message = [False, 'email adress is not a valid string']

    return message


def download_image(url: str,
                   save_path: str) -> None:

    # TODO: type url and save path

    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful

        # Get the content of the response
        image_content = response.content

        # Save the image content to a local file
        with open(save_path, 'wb') as file:
            file.write(image_content)

        print(f"Image downloaded successfully and saved at {save_path}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading image from {url}: {e}")



