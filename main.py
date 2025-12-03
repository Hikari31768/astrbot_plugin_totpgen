import logging
import random
import requests  # 导入requests库
from typing import List, Dict, Optional
from astrbot.api.star import Context, Star, register
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.event.filter import event_message_type, EventMessageType
import pyotp


logger = logging.getLogger(__name__)

totp_secret_list = {
    'gpt': '',
    'sora': ''
}

@register("astrbot_plugin_totp", "Hikarin", "一个TOTP生成插件", "1.0", "https://github.com/Hikari31768/astrbot_plugin_totpgen")
class TOTPGeneratorPlugin(Star):
    def __init__(self, context: Context, config: Optional[Dict] = None):
        super().__init__(context)
        self.config = config if config else {}
        self.group_whitelist: List[int] = self.config.get("group_whitelist", [])
        self.group_whitelist = [int(gid) for gid in self.group_whitelist]

    @event_message_type(EventMessageType.ALL)
    async def on_message(self, event: AstrMessageEvent) -> MessageEventResult:
        """
        当消息中包含“原神”时随机发送一条圣经。
        """
        group_id_str = event.get_group_id()
        if group_id_str:  # 如果是群聊
            if self.group_whitelist and group_id_str not in self.group_whitelist:
                return
        # 如果是私聊，则不检查白名单

        msg_obj = event.message_obj
        text = msg_obj.message_str or ""

        logger.debug("=== Debug: AstrBotMessage ===")
        logger.debug("Bot ID: %s", msg_obj.self_id)
        logger.debug("Session ID: %s", msg_obj.session_id)
        logger.debug("Message ID: %s", msg_obj.message_id)
        logger.debug("Sender: %s", msg_obj.sender)
        logger.debug("Group ID: %s", msg_obj.group_id)
        logger.debug("Message Chain: %s", msg_obj.message)
        logger.debug("Raw Message: %s", msg_obj.raw_message)
        logger.debug("Timestamp: %s", msg_obj.timestamp)
        logger.debug("============================")

        if event.is_at_or_wake_command:
            if "验证码" in text:
                if "gpt" in text.lower() or "openai" in text.lower():
                    otp = pyotp.TOTP(totp_secret_list["gpt"]).now()
                    yield event.plain_result(otp)

