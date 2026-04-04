from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.core.star.filter.command import CommandFilter
from astrbot.core.star.filter.command_group import CommandGroupFilter


@register("astrbot_plugin_no_ai_on_non_commands", "grassblock", "在没有对应命令的情况下，阻止检测到 / 开头的消息时调用 AI", "1.0.1")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    @filter.regex(r"^/")
    async def block_non_command_slash_message(self, event: AstrMessageEvent):
        """拦截 / 开头但未命中任何指令的消息，终止事件传播。"""
        activated_handlers = event.get_extra("activated_handlers", [])
        has_real_command = False

        for handler in activated_handlers:
            if handler.handler_full_name.endswith("_block_non_command_slash_message"):
                continue

            if any(
                isinstance(f, CommandFilter | CommandGroupFilter)
                for f in handler.event_filters
            ):
                has_real_command = True
                break

        if not has_real_command:
            event.stop_event()
            print("这大概不是一个命令，跳过处理")
            return

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
