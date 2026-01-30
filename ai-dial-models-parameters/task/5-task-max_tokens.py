from task.app.main import run

# TODO:
#  Try `max_tokens` parameter. It sets the maximum length of the AI's response. The AI will stop generating text once it hits this limit.
#  User massage: What is token when we are working with LLM?

run(
    deployment_name='gpt-4o',
    # TODO:
    #  Use `max_tokens` parameter with value 10
    max_tokens=10,
    print_request=True, # Switch to False if you do not want to see the request in  
    print_only_content=False, # Switch to True if you want to see only content from response
)

# Previously, we have seen that the `finish_reason` in choice was `stop`, but now it is `length`, and if you check the
# `content,` it is clearly unfinished.