depth = 0
visible_values = set()
stack = [set()] * 64

def enter_context()->bool:
    global depth
    for value in stack[depth]:
        visible_values.add(value)
    depth += 1
    return True

def exit_context()->bool:
    global depth
    for value in stack[depth]:
        visible_values.remove(value)
    stack[depth].clear()
    depth -= 1
    if depth < 0:
        return False
    return True
