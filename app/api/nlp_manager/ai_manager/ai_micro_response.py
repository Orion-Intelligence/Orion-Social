import traceback

import httpx
from api.nlp_manager.ai_manager.ai_helper_methods import ai_helper_methods
from api.nlp_manager.ai_manager.ai_enums import ai_enums


class ai_micro_response:
    def __init__(self, api_url=None, timeout_seconds=None):
        self.api_url = api_url or ai_enums.S_API_URL
        self.timeout_seconds = timeout_seconds or ai_enums.S_TIMEOUT_SECONDS

    async def chat(self, system: str, user: str, model: str, stream: bool = False) -> str:
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user}
            ],
            "stream": stream
        }
        return await self._send_request(data)

    async def chat_with_history(self, messages: list, model: str, stream: bool = False) -> str:
        data = {"model": model, "messages": messages, "stream": stream}
        return await self._send_request(data)

    async def _send_request(self, data: dict) -> str:
        try:
            async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                r = await client.post(self.api_url, json=data)
                if r.status_code == 200:
                    j = r.json()
                    c = j.get("message", {}).get("content", "")
                    return c.strip()
                return f"[LLaMA API Error {r.status_code}] {r.text}"
        except Exception as ex:
            return str(ex)

    async def summarize_darkweb_report(
        self,
        text: str,
        model: str = ai_enums.S_SUMMARY_MODEL,
        force_llama32_when_summarize: bool = True
    ) -> str:
        trimmed = text[0:1000]
        chosen = ai_enums.S_DEFAULT_MODEL if force_llama32_when_summarize else model
        system_prompt = "Treat this prompt as a standalone request. Do not retain or use any previous context."
        user_prompt = (
            "this is data posted on darkweb by a threat actor. Write executive summary only about what is in the report "
            "dont add conclusion or any suggestions. dont add what is not in report. "
            "Start directly with the incident. Do not include any introductions, headings, or phrases like "
            "'Executive summary:', 'Sure', 'Here is the summary:', etc.\n\n" + trimmed
        )

        content = await self.chat(system=system_prompt, user=user_prompt, model=chosen, stream=False)

        cc = ai_helper_methods.strip_common_prefixes(content)

        return cc
