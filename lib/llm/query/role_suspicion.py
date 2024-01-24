def role_suspicion(info: dict):
    text = "前日までの各プレイヤーの重要な発言(後ろの方が最新の発言):\n"
    for agent_num in info:
        if len(info[agent_num]) == 0:
            agent_talk = 'なし'
        else:
            agent_talk = ', '.join(info[agent_num])
        text += f"Agent[0{agent_num}]の発言: {agent_talk}"+"\n"
    return text
