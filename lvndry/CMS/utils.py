import tempfile
from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile



def create_test_image (
        filename="test.jpg",
        size=(100, 100),
        color="red" ,
        image_format="JPEG" ,
        content_type="image/jpeg",
):
    image = Image.new("RGB", size , color)


    extension = "jpg" if image_format.upper() == "JPEG" else image_format.lower()

    with tempfile.NamedTemporaryFile(suffix=f".{extension}") as temp:
        image.save(temp , format=image_format)
        temp.seek(0)

        return SimpleUploadedFile(
            filename ,
            temp.read() ,
            content_type = content_type ,
        )
    


def create_test_rgba_image ():
    image = Image.new("RGBA", (100,100),(255,0,0,120))

    with tempfile.NamedTemporaryFile(suffix=".png") as temp :
        image.save(temp , format="PNG")
        temp.seek(0)

        return SimpleUploadedFile(
            "rgba.png" , 
            temp.read() ,
            content_type="image/png",
        )