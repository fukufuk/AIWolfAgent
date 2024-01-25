role_dict = {
    'FREEMASON': 'フリーメイソン',
    'POSSESSED': '狂人',
    'VILLAGER': '村人',
    'SEER': '占い師',
    'FOX': '妖狐',
    'WEREWOLF': '人狼',
    'MEDIUM': '霊媒師',
    'BODYGUARD': 'ボディガード'
}
# rule_dict = {
#     'talkOnFirstDay': "初日の発言",
#     'voteVisible': "投票の開示",
#     'enableNoAttack': "襲撃スキップ",
#     'enableNoExecution': "投票スキップ",
#     'enableRoleRequest': "役職開示",
#     'validateUtterance': "発言フィルター",
#     'votableInFirstDay': "初日の投票",
#     'whisperBeforeRevote': "再投票前の囁き"
# }


def game_rule(game_setting: dict) -> str:
    """ルール説明の作成"""
    roleNumMap = game_setting.get('roleNumMap')
    rule_text = f"""人狼ゲームは以下の条件で行われている。
- 役職 -> {",".join([f"{role_dict[key]}:{roleNumMap[key]}人"
                   for key in roleNumMap if roleNumMap[key] != 0])}
- スキップ上限 -> {game_setting['maxSkip']}回
- 1日の発言回数 -> {game_setting['maxTalk']}回まで
- 最大ターン数 -> {game_setting['maxTalkTurn']}ターン
- 0日目は簡潔な挨拶のみ(役職は開示しない)
"""
# - 禁止事項 -> {",".join([rule_dict[key]
#                      for key in game_setting if game_setting[key] is True])}
# - 認可事項 -> {",".join([rule_dict[key]
#                      for key in game_setting if game_setting[key] is False])}
# """
    return rule_text
