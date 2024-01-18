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


def game_info(game_info: dict, role: str) -> str:
    """ゲーム情報の作成"""
    game_info_text = f"""人狼ゲームの現在の進行状況
- あなたの名前: Agent[{game_info['agent']}]
- あなたの役職: {role_dict[role]}
- 日付: {game_info['day']}日目
- 生存者: {",".join([f"Agent[{key}]" for key in game_info["statusMap"] if game_info["statusMap"][key] == "ALIVE"])}
- 死亡者: {",".join([f"Agent[{key}]" for key in game_info["statusMap"] if game_info["statusMap"][key] == "DEAD"])}
- 前日の犠牲者: {",".join([f"Agent[{agent}]" for agent in game_info['lastDeadAgentList']]) if len(game_info['lastDeadAgentList'])>0 else "なし"}
- 前日の投票: {", ".join([f"Agent[{vote['agent']}]->Agent[{vote['target']}]" for vote in game_info['voteList']])}
"""
    return game_info_text