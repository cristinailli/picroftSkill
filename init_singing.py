import random
import time
from os.path import dirname, join

from adapt.intent import IntentBuilder
from mycroft.messagebus.message import Message
from mycroft.skills.core import MycroftSkill
from mycroft.util import play_mp3
from mycroft.util.log import getLogger

__author__ = 'kfezer'

LOGGER = getLogger(__name__)


class SingingSkill(MycroftSkill):
    def __init__(self):
        super(SingingSkill, self).__init__(name="SingingSkill")
        self.process = None
        self.play_list = {
            0: join(dirname(__file__), "popey-favourite.mp3"),
            1: join(dirname(__file__), "popey-jackson.mp3"),
            2: join(dirname(__file__), "popey-jerusalem.mp3"),
            3: join(dirname(__file__), "popey-lose-yourself.mp3"),
            4: join(dirname(__file__), "popey-lovemetender.mp3"),
            5: join(dirname(__file__), "popey-rocketman.mp3"),
        }

    def initialize(self):
        intent = IntentBuilder("SingingIntent").require(
            "SingingKeyword").build()
        self.register_intent(intent, self.handle_intent)
        self.add_event("mycroft.sing", self.sing, False)

    def sing(self, message):
        self.process = play_mp3(self.play_list[3])

    def handle_intent(self, message):
        rando = random.randint(0, 5)
        file = self.play_list[rando]
        try:
            self.speak_dialog('singing')
            time.sleep(3)
            self.process = play_mp3(file)

        except Exception as e:
            LOGGER.error("Error: {0}".format(e))

    def stop(self):
        if self.process and self.process.poll() is None:
            self.speak_dialog('singing.stop')
            self.process.terminate()
            self.process.wait()


def create_skill():
    return SingingSkill()