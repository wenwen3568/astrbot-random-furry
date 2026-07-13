# -*- coding: utf-8 -*-
import aiohttp
import tempfile
import os
import time
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star
from astrbot.api import logger
from astrbot.api.message_components import Image

class RandomFurryPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.save_dir = "/vol1/1000/Photos"

    @filter.command("\u968f\u673a\u517d\u56fe")
    async def random_furry(self, event: AstrMessageEvent):
        yield event.plain_result("\U0001f43e \u6b63\u5728\u5bfb\u627e\u798f\u745e\u56fe\u7247\uff0c\u8bf7\u7a0d\u5019...")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://furry.axzt.top") as resp:
                    if resp.status != 200:
                        yield event.plain_result(f"\u274c API \u8bf7\u6c42\u5931\u8d25\uff0c\u72b6\u6001\u7801: {resp.status}")
                        return
                    img_data = await resp.read()
            try:
                os.makedirs(self.save_dir, exist_ok=True)
                filename = f"furry_{int(time.time())}.png"
                filepath = os.path.join(self.save_dir, filename)
                with open(filepath, "wb") as f:
                    f.write(img_data)
                logger.info(f"Image saved to {filepath}")
            except Exception as e:
                logger.error(f"Save failed: {e}")
            try:
                img_component = Image.fromBytes(img_data)
                yield event.chain_result([img_component])
            except AttributeError:
                with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp:
                    tmp.write(img_data)
                    tmp_path = tmp.name
                img_component = Image.fromFileSystem(tmp_path)
                yield event.chain_result([img_component])
                os.unlink(tmp_path)
        except aiohttp.ClientError as e:
            logger.error(f"Request failed: {e}")
            yield event.plain_result("\u274c \u83b7\u53d6\u798f\u745e\u56fe\u7247\u5931\u8d25\uff0c\u8bf7\u7a0d\u540e\u518d\u8bd5~")
        except Exception as e:
            logger.error(f"Unknown error: {e}")
            yield event.plain_result("\u274c \u51fa\u9519\u4e86\uff0c\u8bf7\u7a0d\u540e\u518d\u8bd5~")

    async def terminate(self):
        pass
