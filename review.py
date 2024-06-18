import requests
import json
import time
import logging

API_KEY = 'f1a6b3b9-7a04-47e1-b010-78da80bf4613:66621d30-9b6c-4293-aad9-44257cce4638'
MOHIR_AI_API_URL = 'https://mohir.ai/api/v1/stt'
AUDIO_FILE = 'mus.wav'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def transcribe_audio_realtime(file_path):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
    }

    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}

            response = requests.post(MOHIR_AI_API_URL, headers=headers, files=files, params={'start': 'true'})

            if response.status_code != 200:
                logger.error(f"Failed to start real-time transcription. Status code: {response.status_code}")
                logger.error(response.text)
                return

            logger.info("Real-time transcription started:")
            logger.info(json.dumps(response.json(), indent=4))

            chunk_size = 1024
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break

                response = requests.post(MOHIR_AI_API_URL, headers=headers, data=chunk)

                if response.status_code == 200:
                    result = response.json()
                    if 'is_final' in result and result['is_final']:
                        logger.info("Final transcription result:")
                    else:
                        logger.info("Intermediate transcription result:")
                    logger.info(json.dumps(result, indent=4))
                else:
                    logger.error(f"Failed to transcribe audio. Status code: {response.status_code}")
                    logger.error(response.text)
                    break

                time.sleep(1)

    except Exception as e:
        logger.error(f"An error occurred: {e}")

transcribe_audio_realtime(AUDIO_FILE)
