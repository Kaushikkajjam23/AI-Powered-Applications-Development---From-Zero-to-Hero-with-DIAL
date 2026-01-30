import asyncio

from task.clients.custom_client import DialClient
from task.constants import DEFAULT_SYSTEM_PROMPT
from task.models.conversation import Conversation
from task.models.message import Message
from task.models.role import Role


async def start(stream: bool) -> None:
    #TODO:
    # 1.1. Create DialClient
    # (you can get available deployment_name via https://ai-proxy.lab.epam.com/openai/models
    #  you can import Postman collection to make a request, file in the project root `dial-basics.postman_collection.json`
    #  don't forget to add your API_KEY)
    client=DialClient(deployment_name="gpt-4o")
    # 1.2. Create CustomDialClient (using same custom client implementation)
    customeclient=DialClient(deployment_name="gpt-4o")
    # 2. Create Conversation object
    conversation=Conversation()
    # 3. Get System prompt from console or use default -> constants.DEFAULT_SYSTEM_PROMPT and add to conversation
    #    messages.
    print("Enter system prompt or press enter to use default:")
    prompt=input(">").strip()
    if prompt:
        conversation.add_message(Message(Role.SYSTEM,prompt))
        print("System prompt added to conversation successfully")
    else:
        conversation.add_message(Message(Role.SYSTEM,DEFAULT_SYSTEM_PROMPT))
    # 4. Use infinite cycle (while True) and get user message from console
    print("Type your question or 'exit' to quit:")
    while True:
        user_input=input("User:").strip()

        # 5. If user message is `exit` then stop the loop
        if user_input.lower()=='exit':
            print("Exiting the chat. Goodbye!")
            break
        # 6. Add user message to conversation history (role 'user')
        conversation.add_message(Message(Role.USER,user_input))
        # 7. If `stream` param is true -> call DialClient#stream_completion()
        #    else -> call DialClient#get_completion()
        print("AI:")
        if stream:
            response=await customeclient.stream_completion(conversation.get_messages())
        else:
            response=customeclient.get_completion(conversation.get_messages())
    # 8. Add generated message to history
        conversation.add_message(response)
    # 9. Test it with DialClient and CustomDialClient
    # 10. In CustomDialClient add print of whole request and response to see what you send and what you get in response
    # end of program


asyncio.run(
    start(False)
)
