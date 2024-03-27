from language_model import openai_api
import logging

logger = logging.getLogger(__name__)

def reflect(generated_content):
    prompt = f"Please provide a short reflection on the following generated content:\n{generated_content}"
    try:
        reflection = openai_api.complete(prompt)
        logger.info(f"Reflection generated: {reflection}")
        return reflection
    except Exception as e:
        logger.error(f"Error generating reflection: {e}")
        return "Error generating reflection."

def rate_response(generated_content):
    prompt = f"Please rate the quality of the following generated content on a scale from 0 to 1:\n{generated_content}"
    try:
        score_str = openai_api.complete(prompt)
        score = float(score_str)
        logger.info(f"Response rated: {score}")
        return score
    except Exception as e:
        logger.error(f"Error rating response: {e}")
        return 0.0