import base64

def convert_base64_to_image(img_base64_string: str, image_uuid: str, save_path: str) -> None:
    """This function decode and convert a base64 string to a image file.

    Args:
        img_base64_string (str): The base64 string you want to decode.
        image_uuid (str): A unique uuid to name the image file
        save_path (str): The path you want to save the image in.
    """

    imgdata = base64.b64decode(img_base64_string)
    filename = f'{image_uuid}.jpg'  # I assume you have a way of picking unique filenames
    with open(f'{save_path}/{filename}', 'wb') as f:
        f.write(imgdata)