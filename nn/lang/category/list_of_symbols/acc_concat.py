# we consider only "Cx"
accent_list = [
    "C1",
    "C2",
    "C3",
    "C4",
    "C5",
]

accent_map = { p : i+1 for i, p in enumerate(accent_list) }
accent_map[None] = 0
accent_map[''] = 0
accent_invmap = {v:k for k, v in accent_map.items()}
