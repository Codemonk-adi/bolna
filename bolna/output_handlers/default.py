import base64
from dotenv import load_dotenv
from bolna.helpers.logger_config import CustomLogger

custom_logger = CustomLogger(__name__)
load_dotenv()


class DefaultOutputHandler:
    def __init__(self, websocket=None, log_dir_name=None):
        self.websocket = websocket
        self.is_interruption_task_on = False
        self.logger = custom_logger.update_logger(log_dir_name)

    # @TODO Figure out the best way to handle this
    async def handle_interruption(self):
        message_clear = {
            "event": "clear"
        }

    async def handle(self, packet):
        try:
            self.logger.info(f"Packet received:")
            data = None
            if packet["meta_info"]['type'] in ('audio', 'text'):
                if packet["meta_info"]['type'] == 'audio':
                    self.logger.info(f"Sending audio")
                    data = base64.b64encode(packet['data']).decode("utf-8")
                elif packet["meta_info"]['type'] == 'text':
                    self.logger.info(f"Sending text response {packet['data']}")
                    data = packet['data']

                response = {"data": data, "type": packet["meta_info"]['type']}
                await self.websocket.send_json(response)

            else:
                self.logger.error("Other modalities are not implemented yet")
        except Exception as e:
            self.logger.error(f"something went wrong in speaking {e}")
