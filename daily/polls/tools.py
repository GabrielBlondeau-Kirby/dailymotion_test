
def check_required_fields(f, items, required_fields):
    if not f(map(lambda x: x in items, required_fields)):
        return False
    return True


def check_all_required_fields(items, required_fields):
    return check_required_fields(all, items, required_fields)


def check_any_required_fields(items, required_fields):
    return check_required_fields(any, items, required_fields)