DEBUG = False

def debugPrint(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

def set_debug_mode(debug_flag):
    global DEBUG
    DEBUG = debug_flag