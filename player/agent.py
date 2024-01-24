import configparser
import json
import pickle

from lib import util
from lib.AIWolf.commands import AIWolfCommand
from lib.embedding.embedding import Embedding
from lib.llm.openai_client import OpenAIClient
from lib.llm.query import game_info, game_rule, role_suspicion
from torch.nn.functional import cosine_similarity

LOGGER = util.build_logger(__name__)


class Agent:
    def __init__(self, inifile: configparser.ConfigParser, name: str) -> None:
        self.name = name
        self.received = []
        self.gameContinue = True
        self.game_rule = None
        self.data = []  # テスト用
        self.agent_role_suspect = {}  # 各エージェントがどのような役職だと疑っているか
        # TODO: エージェントの数を反映する
        for i in range(1, 6):
            self.agent_role_suspect[i] = []
        self.client = OpenAIClient()
        self.embedding_model = Embedding()

        # daily_initialize
        self.game_info_text = None

        # talk
        self.todays_talk_history = []
        self.last_talk_emb = []

        randomTalk = inifile.get("randomTalk", "path")
        _ = util.check_config(randomTalk)

        self.comments = util.read_text(randomTalk)

    def set_received(self, received: list) -> None:
        self.received = received

    def parse_info(self, receive: str) -> None:
        received_list = receive.split("}\n{")

        for index in range(len(received_list)):
            received_list[index] = received_list[index].rstrip()

            if received_list[index][0] != "{":
                received_list[index] = "{" + received_list[index]

            if received_list[index][-1] != "}":
                received_list[index] += "}"

            self.received.append(received_list[index])

    def get_info(self):
        data = json.loads(self.received.pop(0))

        self.data.append(data)  # テスト用

        self.gameInfo = data["gameInfo"]
        self.gameSetting = data["gameSetting"]
        if (self.gameSetting is not None) and (self.game_rule is None):
            self.game_rule = game_rule(self.gameSetting)
        self.request = data["request"]
        self.talkHistory = data["talkHistory"]
        if self.talkHistory:
            LOGGER.info(f'f"[{self.name}] start embedding talkHistory')
            suspects = util.map_async(
                func=self.embedding_model.check_role_suspicion,
                data=[talk["text"] for talk in self.talkHistory],
                limit=8
            )
            LOGGER.info(f'f"[{self.name}] end embedding talkHistory')
            for suspect, talk in zip(suspects, self.talkHistory):
                if suspect is not None:
                    if suspect not in self.agent_role_suspect[talk["agent"]]:
                        self.agent_role_suspect[talk["agent"]].append(suspect)
            self.todays_talk_history.append(self.talkHistory)
        self.whisperHistory = data["whisperHistory"]

    def initialize(self) -> None:
        self.index = self.gameInfo["agent"]
        self.role = self.gameInfo["roleMap"][str(self.index)]

    def daily_initialize(self) -> None:
        self.alive = []
        self.todays_talk_history = []
        self.last_talk_emb = None
        for agent_num in self.gameInfo["statusMap"]:
            if (
                self.gameInfo["statusMap"][agent_num] == "ALIVE"
                and int(agent_num) != self.index
            ):
                self.alive.append(int(agent_num))
        self.game_info_text = game_info(self.gameInfo, self.role)

    def daily_finish(self) -> None:
        pass

    def get_name(self) -> str:
        return self.name

    def get_role(self) -> str:
        return self.role

    # TODO: 会話の内容を考える
    def talk(self) -> str:
        LOGGER.info(f"[{self.name}] talk")
        # 1. 前日までの人狼の状況を簡潔にまとめる。
        # (daily_initializeでself.game_info_textに作成)
        # 2. 前日までの会話を追加する。
        role_suspicion_text = role_suspicion(self.agent_role_suspect)
        # 3. 今日の今までの会話を追加する。
        latest_talks = "\n".join(
            [f'Agent[0{talk["agent"]}]: {talk["text"]}'
             for talk in self.talkHistory])
        # 4. gptに聞く。
        response = self.client.talk(  # TODO: 占いの結果が渡されていなかった😭
            agent_index=self.index,
            game_setting=self.game_rule,
            game_info=self.game_info_text,
            role_suspicion=role_suspicion_text,
            talkHistory=latest_talks
        )
        # 5. 回答が前回の回答と似ていたらOverを返す。
        response_emb = self.embedding_model.encode(
            response
        )
        if self.last_talk_emb is not None:
            if (cosine_similarity(response_emb,
                                  self.last_talk_emb,
                                  dim=2).item()) > 0.9:
                response = "Over"
                LOGGER.info('Over')
        self.last_talk_emb = response_emb
        # 回答を返す。
        LOGGER.info(f"[{self.name}] talk end")
        return response

    # TODO: 投票方法を考える
    def vote(self) -> str:
        LOGGER.info(f"[{self.name}] vote")
        role_suspicion_text = role_suspicion(self.agent_role_suspect)
        latest_talks = "\n".join(
            [f'Agent[0{talk["agent"]}]: {talk["text"]}'
             for talk in self.todays_talk_history])
        arguments = self.client.vote(
            game_setting=self.game_rule,
            game_info=self.game_info_text,
            role_suspicion=role_suspicion_text,
            talkHistory=latest_talks
        )
        LOGGER.info(f"[{self.name}] vote end")
        return arguments

    # TODO: 仲間内での会話を考える
    def whisper(self) -> None:
        pass

    def finish(self) -> str:
        # pickleで保存（書き出し）テスト用
        with open(f'data/data_{self.name}.pickle', mode='wb') as f:
            pickle.dump(self.data, f)
        self.gameContinue = False

    def action(self) -> str:
        if AIWolfCommand.is_initialize(request=self.request):
            self.initialize()
        elif AIWolfCommand.is_name(request=self.request):
            return self.get_name()
        elif AIWolfCommand.is_role(request=self.request):
            return self.get_role()
        elif AIWolfCommand.is_daily_initialize(request=self.request):
            self.daily_initialize()
        elif AIWolfCommand.is_daily_finish(request=self.request):
            self.daily_finish()
        elif AIWolfCommand.is_talk(request=self.request):
            return self.talk()
        elif AIWolfCommand.is_vote(request=self.request):
            return self.vote()
        elif AIWolfCommand.is_whisper(request=self.request):
            self.whisper()
        elif AIWolfCommand.is_finish(request=self.request):
            self.finish()

        return ""

    def hand_over(self, new_agent) -> None:
        # __init__
        new_agent.name = self.name
        new_agent.received = self.received
        new_agent.gameContinue = self.gameContinue
        new_agent.comments = self.comments
        new_agent.received = self.received
        new_agent.client = self.client
        new_agent.embedding_model = self.embedding_model
        new_agent.agent_role_suspect = self.agent_role_suspect

        # get_info
        new_agent.gameInfo = self.gameInfo
        new_agent.gameSetting = self.gameSetting
        new_agent.request = self.request
        new_agent.talkHistory = self.talkHistory
        new_agent.whisperHistory = self.whisperHistory

        # initialize
        new_agent.index = self.index
        new_agent.role = self.role

        # daily_initialize
        new_agent.game_info_text = self.game_info_text

        # talk
        new_agent.todays_talk_history = self.todays_talk_history
        new_agent.last_talk_emb = self.last_talk_emb
