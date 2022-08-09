def judge(value1, value2, condition):
    try:
        if condition == '>':
            return float(value1) > float(value2)
        if condition == '<':
            return float(value1) < float(value2)
        if condition == '=':
            return float(value1) == float(value2)
        if condition == '>=':
            return float(value1) >= float(value2)
        if condition == '<=':
            return float(value1) <= float(value2)
        if condition == 'Set':
            return (int(value1, 16) & int(value2, 16)) == int(value2, 16)
        if condition == 'Reset':
            return (int(value1, 16) | int(value2, 16)) == int(value2, 16)
    except:
        return False
