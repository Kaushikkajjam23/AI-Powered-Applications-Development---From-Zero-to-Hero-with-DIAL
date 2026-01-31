import asyncio
from io import BytesIO
from pathlib import Path

from task._models.custom_content import Attachment, CustomContent
from task._utils.constants import API_KEY, DIAL_URL, DIAL_CHAT_COMPLETIONS_ENDPOINT
from task._utils.bucket_client import DialBucketClient
from task._utils.model_client import DialModelClient
from task._models.message import Message
from task._models.role import Role


async def _put_image() -> Attachment:
    file_name = 'dialx-banner.png'
    image_path = Path(__file__).parent.parent.parent / file_name
    mime_type_png = 'image/png'
    # TODO:
    #  1. Create DialBucketClient
    #  2. Open image file
    #  3. Use BytesIO to load bytes of image
    #  4. Upload file with client
    #  5. Return Attachment object with title (file name), url and type (mime type)
    async with DialBucketClient(api_key=API_KEY, base_url=DIAL_URL) as bucket_client:
        # load file bytes into BytesIO
        with open(image_path, 'rb') as f:
            content = BytesIO(f.read())

        # upload file
        response = await bucket_client.put_file(name=file_name, mime_type=mime_type_png, content=content)

        # try to determine storage path/bucket to build url
        bucket_path = await bucket_client._get_bucket()
        url = f"files/{bucket_path}/{file_name}"

        return Attachment(title=file_name, url=url, type=mime_type_png)


def start() -> None:
    # TODO:
    #  1. Create DialModelClient
    client = DialModelClient(
        endpoint=DIAL_CHAT_COMPLETIONS_ENDPOINT,
        deployment_name="gpt-4o",
        api_key=API_KEY,
    )
    #  2. Upload image (use `_put_image` method )
    attachment = asyncio.run(_put_image())

    #  3. Print attachment to see result
    print(attachment)   
    #  4. Call chat completion via client with list containing one Message:
    #    - role: Role.USER
    #    - content: "What do you see on this picture?"
    #    - custom_content: CustomContent(attachments=[attachment])
    response = client.get_completion(
        messages=[
            Message(
                role=Role.USER,
                content="What do you see on this picture?",
                custom_content=CustomContent(
                    attachments=[attachment]
                )
            )
        ]
    )
    #  ---------------------------------------------------------------------------------------------------------------
    #  Note: This approach uploads the image to DIAL bucket and references it via attachment. The key benefit of this
    #        approach that we can use Models from different vendors (OpenAI, Google, Anthropic). The DIAL Core
    #        adapts this attachment to Message content in appropriate format for Model.
    #  TRY THIS APPROACH WITH DIFFERENT MODELS!
    #  Optional: Try upload 2+ pictures for analysis
    print("Model response:", response)


start()
