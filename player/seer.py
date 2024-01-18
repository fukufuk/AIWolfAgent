import configparser
import json

import lib
import player


class Seer(player.agent.Agent):
    def __init__(self, inifile: configparser.ConfigParser, name: str) -> None:
        print("init")
        super().__init__(inifile=inifile, name=name)

    def parse_info(self, receive: str) -> None:
        print("parse_info")
        return super().parse_info(receive)

    def get_info(self):
        print("get_info")
        return super().get_info()

    def initialize(self) -> None:
        print("initialize")
        return super().initialize()

    def daily_initialize(self) -> None:
        print("daily_initialize")
        return super().daily_initialize()

    def daily_finish(self) -> None:
        print("daily_finish")
        return super().daily_finish()

    def get_name(self) -> str:
        print("get_name")
        return super().get_name()

    def get_role(self) -> str:
        print("get_role")
        return super().get_role()

    def talk(self) -> str:
        print("talk")
        return super().talk()

    def vote(self) -> str:
        print("vote")
        return super().vote()

    def whisper(self) -> None:
        print("whisper")
        return super().whisper()

    def divine(self) -> str:
        print("divine")
        data = {"agentIdx": lib.util.random_select(self.alive)}

        return json.dumps(data, separators=(",", ":"))

    def action(self) -> str:
        print("action")
        if self.request == "DIVINE":
            return self.divine()
        else:
            return super().action()
