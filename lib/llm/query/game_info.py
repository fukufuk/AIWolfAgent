role_dict = {
    'FREEMASON': 'フリーメイソン',
    'POSSESSED': '狂人',
    'VILLAGER': '村人',
    'SEER': '占い師',
    'FOX': '妖狐',
    'WEREWOLF': '人狼',  # (※バレないよう村人や占い師になりすましてください)
    'MEDIUM': '霊媒師',
    'BODYGUARD': 'ボディガード',
    'HUMAN': '人間陣営',
}


def game_info(game_info: dict, role: str, divine_results: list[dict]) -> str:
    """ゲーム情報の作成"""
    game_info_text = f"""人狼ゲームの現在の進行状況
- あなたの名前: Agent[0{game_info['agent']}]
- あなたの役職: {role_dict[role]}
- 現在: {game_info['day']}日目
- 生存者: {",".join([f"Agent[0{key}]" for key in game_info["statusMap"] if game_info["statusMap"][key] == "ALIVE"])}
- 死亡者: {",".join([f"Agent[0{key}]" for key in game_info["statusMap"] if game_info["statusMap"][key] == "DEAD"])}
"""
    if game_info['day'] > 0:
        game_info_text += f"""- 前日の犠牲者: {",".join([f"Agent[0{agent}]" for agent in game_info['lastDeadAgentList']]) if len(game_info['lastDeadAgentList'])>0 else "なし"}
- 前日の投票: {", ".join([f"Agent[0{vote['agent']}]->Agent[0{vote['target']}]" for vote in game_info['voteList']]) if len(game_info['voteList'])>0 else "なし"}
"""
    if len(divine_results) > 0:
        game_info_text += f"""- 前日の占い結果: {', '.join([f"Agent[0{divine_result['target']}] = {role_dict[divine_result['result']]}" for divine_result in divine_results])}"""
    return game_info_text
