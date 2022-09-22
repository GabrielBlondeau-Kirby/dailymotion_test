
def check_required_fields(f, items, required_fields):
    if not f(map(lambda x: x in items, required_fields)):
        return False
    return True


def check_all_required_fields(items, required_fields):
    return check_required_fields(all, items, required_fields)


def check_any_required_fields(items, required_fields):
    return check_required_fields(any, items, required_fields)


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'