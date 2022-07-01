def judge(value1, value2, condition):
    if condition == '>':
        return int(value1) > int(value2)
    if condition == '<':
        return int(value1) < int(value2)
    if condition == '=':
        return int(value1) == int(value2)
    if condition == '>=':
        return int(value1) >= int(value2)
    if condition == '<':
        return int(value1) <= int(value2)
    if condition == 'Set':
        return (int(value1, 16) & int(value2, 16)) == int(value2, 16)
    if condition == 'Reset':
        return (int(value1, 16) | int(value2, 16)) == int(value2, 16)
