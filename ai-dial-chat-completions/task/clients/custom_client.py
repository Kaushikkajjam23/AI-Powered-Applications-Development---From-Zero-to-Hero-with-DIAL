import json
import aiohttp
import requests

from task.clients.base import BaseClient
from task.constants import DIAL_ENDPOINT
from task.models.message import Message
from task.models.role import Role
from aiohttp import ClientTimeout
import traceback


class DialClient(BaseClient):
    _endpoint: str

    def __init__(self, deployment_name: str):
        super().__init__(deployment_name)
        self._endpoint = DIAL_ENDPOINT + f"/openai/deployments/{deployment_name}/chat/completions"

    def get_completion(self, messages: list[Message]) -> Message:
        #TODO:
        # Take a look at README.md of how the request and regular response are looks like!
        # 1. Create headers dict with api-key and Content-Type
        headers={
            "api-key": self._api_key,
            "Content-Type": "application/json"
        }
        # 2. Create request_data dictionary with:
        #   - "messages": convert messages list to dict format using msg.to_dict() for each message
        request_data = {
            "messages": [msg.to_dict() for msg in messages]
        }
        # 3. Make POST request using requests.post() with:
        #   - URL: self._endpoint
        #   - headers: headers from step 1
        #   - json: request_data from step 2
        try:
            resp = requests.post(
                url=self._endpoint,
                headers=headers,
                json=request_data,
                timeout=30
            )
            if resp.status_code == 200:
                data = resp.json()
                choices = data.get("choices", [])
                if choices:
                    message = choices[0].get("message", {})
                    content = message.get("content", "")
                    print(content)
                    return Message(Role.AI, content)
                else:
                    print("No choices in response")
                    return Message(Role.AI, "")
            else:
                err = f"HTTP {resp.status_code}: {resp.text}"
                print(err)
                return Message(Role.AI, err)
        except Exception as exc:
            print("Request failed:", exc)
            traceback.print_exc()
            return Message(Role.AI, f"Request failed: {exc}")

    async def stream_completion(self, messages: list[Message]) -> Message:
        #TODO:
        # Take a look at README.md of how the request and streamed response chunks are looks like!
        # 1. Create headers dict with api-key and Content-Type
        headers={
            "api-key": self._api_key,
            "Content-Type": "application/json"
        }
        # 2. Create request_data dictionary with:
        #    - "stream": True  (enable streaming)
        #    - "messages": convert messages list to dict format using msg.to_dict() for each message
        request_data = {
            "stream": True,
            "messages": [msg.to_dict() for msg in messages]
        }
        # 3. Create empty list called 'contents' to store content snippets
        contents = []
        # 4. Create aiohttp.ClientSession() using 'async with' context manager
        timeout = ClientTimeout(total=60)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            try:
                print("--- Request to DIAL endpoint ---")
                print(self._endpoint)
                print(json.dumps(request_data, ensure_ascii=False))
                async with session.post(url=self._endpoint, json=request_data, headers=headers) as response:
                    if response.status == 200:
                        async for raw_chunk in response.content:
                            line_str = raw_chunk.decode('utf-8').strip()
                            if not line_str:
                                continue
                            if line_str.startswith("data: "):
                                data = line_str[6:]
                                if data != "[DONE]":
                                    content_snippet = self._get_content_snippet(data)
                                    if content_snippet:
                                        print(content_snippet, end='', flush=True)
                                        contents.append(content_snippet)
                                else:
                                    print()
                        return Message(Role.AI, ''.join(contents))
                    else:
                        err_text = await response.text()
                        err = f"HTTP {response.status}: {err_text}"
                        print(err)
                        return Message(Role.AI, err)
            except Exception as exc:
                print("Streaming request failed:", exc)
                traceback.print_exc()
                return Message(Role.AI, f"Streaming request failed: {exc}")

        # 6. Get content from chunks (don't forget that chunk start with `data: `, final chunk is `data: [DONE]`), print
        #    chunks, collect them and return as assistant message
    def _get_content_snippet(self, data: str) -> str:
        """
        Extract content from streaming data chunk.
        """
        data = json.loads(data)
        if choices := data.get("choices"):
            delta = choices[0].get("delta", {})
            return delta.get("content", '')
        return ''

