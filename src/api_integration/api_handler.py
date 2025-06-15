import requests
import time
from config.settings import settings
from src.utils.logger import logger


class DeepSeekAPIHandler:
    def __init__(self):
        self.config = settings.DEEPSEEK_API_CONFIG
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config['api_key']}"
        }

    def send_request(self, messages: list) -> dict:
        """发送请求到DeepSeek API"""
        payload = {
            "model": self.config["model"],
            "messages": messages,
            "temperature": self.config["temperature"],
            "max_tokens": settings.MAX_TOKENS,
            "top_p": 0.95,
            "frequency_penalty": 0,
            "presence_penalty": 0
        }

        try:
            response = requests.post(
                f"{self.config['base_url']}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=60
            )

            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"API error: {response.status_code} - {response.text}")
                return {"error": f"API error {response.status_code}"}

        except requests.exceptions.RequestException as e:
            logger.error(f"Network error: {str(e)}")
            return {"error": f"Network error: {str(e)}"}

    def generate_response(self, prompt: str) -> str:
        """生成响应并处理重试逻辑"""
        messages = [{"role": "user", "content": prompt}]
        retries = 0
        max_retries = 3

        while retries < max_retries:
            response = self.send_request(messages)

            if "error" in response:
                if "rate limit" in response["error"].lower():
                    logger.warning(f"Rate limit exceeded, retrying... ({retries + 1}/{max_retries})")
                    time.sleep(3 * (retries + 1))
                    retries += 1
                    continue
                else:
                    return f"API Error: {response['error']}"

            # 成功响应处理
            if "choices" in response and len(response["choices"]) > 0:
                content = response["choices"][0]["message"]["content"]
                logger.info("Successfully received response from DeepSeek API")

                # 记录API使用情况
                usage = response.get("usage", {})
                logger.info(f"API Usage: Prompt tokens - {usage.get('prompt_tokens', 0)}, "
                            f"Completion tokens - {usage.get('completion_tokens', 0)}")

                return content

            retries += 1
            time.sleep(2)

        return "Failed to get valid response after retries"