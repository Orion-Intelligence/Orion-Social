import json
from api.model.report_chat_request import ReportChatRequest
from crawler.crawler_services.redis_manager.redis_enums import REDIS_COMMANDS
from crawler.crawler_services.redis_manager.redis_controller import redis_controller
from api.nlp_manager.ai_manager.ai_enums import ai_enums
from api.nlp_manager.ai_manager.ai_micro_response import ai_micro_response

def default_system_prompt() -> str:
    return (
        "You are an AI analyst. "
        "Use the Reference report as the main source; override chat history if they conflict. "
        "Be concise and precise. "
        "If info is missing, ask one specific follow-up. "
        "Do not invent or guess. "
        "Keep under 300 words unless asked for more. "
    )


class ai_live_api:
    def __init__(
        self,
        model: str = ai_enums.S_DEFAULT_MODEL,
        max_history: int = 10,
        expiry_seconds: int = 60,
        system_prompt: str | None = None,
        pin_first: bool = True
    ):
        self.model = model
        self.max_history = max_history
        self.expiry_seconds = expiry_seconds
        self.system_prompt = system_prompt or default_system_prompt()
        self.pin_first = pin_first
        self.redis = redis_controller()
        self.micro = ai_micro_response()

    @staticmethod
    def _key(user_id: str) -> str:
        return f"chat_session:{user_id}"

    def _load(self, user_id: str) -> list:
        k = self._key(user_id)
        s = self.redis.invoke_trigger(REDIS_COMMANDS.S_GET_STRING, [k, None, self.expiry_seconds])
        if s:
            try:
                return json.loads(s)
            except json.JSONDecodeError:
                return []
        return []

    def _save(self, user_id: str, history: list):
        k = self._key(user_id)
        if self.pin_first and history:
            first = history[0]
            rest = history[1:][-self.max_history:]
            history = [first] + rest
        else:
            history = history[-self.max_history:]
        self.redis.invoke_trigger(REDIS_COMMANDS.S_SET_STRING, [k, json.dumps(history), self.expiry_seconds])

    async def send(self, data: ReportChatRequest) -> str:
        user_id = data.session_id
        user_message = data.message
        report_text = data.report

        history = self._load(user_id)
        ctx = list(history)
        if not ctx and self.system_prompt:
            ctx.append({"role": "system", "content": self.system_prompt})
        if report_text:
            ctx.append({"role": "system", "content": f"Reference report:\n{report_text}"})
        ctx.append({"role": "user", "content": user_message})

        reply = await self.micro.chat_with_history(ctx, self.model, stream=False)

        if not history and self.system_prompt:
            history.append({"role": "system", "content": self.system_prompt})
        history.append({"role": "user", "content": user_message})
        history.append({"role": "assistant", "content": reply})
        self._save(user_id, history)

        return reply
