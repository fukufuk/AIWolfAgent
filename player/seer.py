import configparser
import json

import lib
import player
from lib.llm.query import role_suspicion
from lib.logger import build_logger

LOGGER = build_logger(__name__)


class Seer(player.agent.Agent):
    def __init__(self, inifile: configparser.ConfigParser, name: str) -> None:
        super().__init__(inifile=inifile, name=name)

    def parse_info(self, receive: str) -> None:
        return super().parse_info(receive)

    def get_info(self):
        return super().get_info()

    def initialize(self) -> None:
        return super().initialize()

    def daily_initialize(self) -> None:
        return super().daily_initialize()

    def daily_finish(self) -> None:
        return super().daily_finish()

    def get_name(self) -> str:
        
        return super().get_name()

    def get_role(self) -> str:
        return super().get_role()

    def talk(self) -> str:
        return super().talk()

    def vote(self) -> str:
        return super().vote()

    def whisper(self) -> None:
        return super().whisper()

    def divine(self) -> str:
        LOGGER.info(f"[{self.name}] DIVINE")
        if self.day == 0:
            data = {"agentIdx": lib.util.random_select(self.alive)}
            LOGGER.info(f"[{self.name}] DIVINE end.({data})")
            return json.dumps(data, separators=(",", ":"))
        role_suspicion_text = role_suspicion(self.agent_role_suspect)
        # latest_talks = "\n".join(
        #     [f'Agent[0{talk["agent"]}]: {talk["text"]}'
        #      for talk in self.talkHistory])
        arguments = self.client.divine(
            index=self.index,
            game_setting=self.game_rule,
            game_info=self.game_info_text,
            role_suspicion=role_suspicion_text
        )
        if arguments is None:
            arguments = json.dumps({"agentIdx": lib.util.random_select(self.alive)}, separators=(",", ":"))
        LOGGER.info(f"[{self.name}] DIVINE end.(argeuments:{arguments})")
        return arguments

    def action(self) -> str:
        if self.request == "DIVINE":
            return self.divine()
        else:
            return super().action()
