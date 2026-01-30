import os
DEFAULT_SYSTEM_PROMPT = "You are an assistant who answers concisely and informatively."
# Allow overriding the endpoint and API key via environment variables for flexibility.
# The application expects a real API key to be provided in the `DIAL_API_KEY` environment
# variable. No hardcoded fallback is provided to avoid accidental usage of invalid keys.
DIAL_ENDPOINT = os.getenv('DIAL_ENDPOINT', "https://ai-proxy.lab.epam.com")
API_KEY = os.getenv('DIAL_API_KEY')
import os

DEFAULT_SYSTEM_PROMPT = "You are an assistant who answers concisely and informatively."
# Allow overriding the endpoint and API key via environment variables for flexibility.
# The application expects a real API key to be provided in the `DIAL_API_KEY` environment
# variable. No hardcoded fallback is provided to avoid accidental usage of invalid keys.
DIAL_ENDPOINT = os.getenv('DIAL_ENDPOINT', "https://ai-proxy.lab.epam.com")
API_KEY = os.getenv('DIAL_API_KEY')
