goshu_list = [
    "和",
    "漢",
    "外",
    "混",
    "固",
    "記号",
    "他"
]

goshu_map = { p : i+1 for i, p in enumerate(goshu_list) }
goshu_map[None] = 0
goshu_invmap = {v:k for k, v in goshu_map.items()}
