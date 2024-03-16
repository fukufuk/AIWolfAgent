role_dict = {
    'FREEMASON': 'フリーメイソン',
    'POSSESSED': '狂人(人狼陣営)',
    'VILLAGER': '村人(村人陣営)',
    'SEER': '占い師(村人陣営)',
    'FOX': '妖狐',
    'WEREWOLF': '人狼(人狼陣営)',
    'MEDIUM': '霊媒師(村人陣営)',
    'BODYGUARD': 'ボディガード(村人陣営)',
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
- 人狼ゲームとは: 人狼ゲームとは、プレイヤーが村人陣営または人狼陣営となり、相互に推理しながら人狼を判断するゲームであり、推理と騙し合いが重要な要素となり、村人たちが人狼を見つけ出すか、人狼が村人を騙し切るかで勝敗が決まる。
- 人狼ゲームのポイント: 
  1. 発言の内容や論理は一貫しているかを確認する
  2. プレイヤー同士で協力するそぶりはないか(人狼陣営同士で協力する可能性がある)
  3. 他のプレイヤーに自分の意見を明瞭に表明する
- 役職一覧 -> {",".join([f"{role_dict[key]}:{roleNumMap[key]}人"
                   for key in roleNumMap if roleNumMap[key] != 0])}
"""
# - スキップ上限 -> {game_setting['maxSkip']}回
# - 1日の発言回数 -> {game_setting['maxTalk']}回まで
# - 最大ターン数 -> {game_setting['maxTalkTurn']}ターン
# - 0日目は簡潔な挨拶のみ(役職は開示しないでください)
# - 禁止事項 -> {",".join([rule_dict[key]
#                      for key in game_setting if game_setting[key] is True])}
# - 認可事項 -> {",".join([rule_dict[key]
#                      for key in game_setting if game_setting[key] is False])}
# """
    return rule_text
