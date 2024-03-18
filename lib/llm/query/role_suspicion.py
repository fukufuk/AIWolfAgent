def role_suspicion(info: dict):
    text = "今までの各プレイヤーの重要な発言:\n"
    for day in info:
        text += f"[{day}日目]\n"
        for conv in info[day]:
            text += f"Agent[0{conv['agent']}]: {conv['text']}" + "\n"
    return text
