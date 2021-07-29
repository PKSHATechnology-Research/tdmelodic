def add_accent_column(line, idx_accent=None):
    line = line + ['' for i in range(10)]
    line[idx_accent] = '@'
    return line