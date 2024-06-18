import time
import logging
import requests
import json

MOHIR_API_URL = 'https://mohir.ai/api/v1/stt'
MOHIR_API_KEY = 'f1a6b3b9-7a04-47e1-b010-78da80bf4613:66621d30-9b6c-4293-aad9-44257cce4638'

DEEPGRAM_API_URL = 'https://api.deepgram.com/v1/listen'
DEEPGRAM_API_KEY = '78e0ec524cf64f4f9627b82a67412ebb6d83da30'
DEEPGRAM_PROJECT_KEY = '71aac4da-81e3-4b20-b10e-04c00182c28e' 
AUDIO_FILE = 'ret.wav'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def transcribe_audio_deepgram(file_path):
    headers = {
        'Authorization': f'Bearer {DEEPGRAM_API_KEY}',
        'Deepgram-Project': DEEPGRAM_PROJECT_KEY,
    }

    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}

            response = requests.post(DEEPGRAM_API_URL, headers=headers, files=files)

            if response.status_code == 200:
                result = response.json()
                logger.info("Transcription result from Deepgram:")
                logger.info(json.dumps(result, indent=4))
                return result

            elif response.status_code == 401:
                logger.error("Unauthorized: Invalid credentials.")
                logger.error(response.json())
                return None

            else:
                logger.error(f"Failed to transcribe audio with Deepgram. Status code: {response.status_code}")
                logger.error(response.text)
                return None

    except Exception as e:
        logger.error(f"An error occurred during transcription with Deepgram: {e}")
        return None


def transcribe_audio_mohir(result_from_deepgram):
    headers = {
        'Authorization': f'Bearer {MOHIR_API_KEY}',
    }

    try:
        if result_from_deepgram and 'id' in result_from_deepgram:
            data = {
                'id': result_from_deepgram['id'],
                'range': [0, 1000],
            }

            response = requests.post(MOHIR_API_URL, headers=headers, json=data)

            if response.status_code == 200:
                result = response.json()
                logger.info("Final transcription result from Mohir AI:")
                logger.info(json.dumps(result, indent=4))
                return result

            else:
                logger.error(f"Failed to transcribe audio with Mohir AI. Status code: {response.status_code}")
                logger.error(response.text)
                return None

    except Exception as e:
        logger.error(f"An error occurred during transcription with Mohir AI: {e}")
        return None

def main():
    deepgram_result = transcribe_audio_deepgram(AUDIO_FILE)
    if not deepgram_result:
        return
    
    transcribe_audio_mohir(deepgram_result)

if __name__ == "__main__":
    main()
