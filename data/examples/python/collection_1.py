from inline import itest

def value_is_list(my_list):

    checked_list = []
    for item in my_list:
        if isinstance(item, dict):
            checked_list.append(sort_json_policy_dict(item))
        elif isinstance(item, list):
            checked_list.append(value_is_list(item))
        else:
            checked_list.append(item)

    # Sort list. If it's a list of dictionaries, sort by tuple of key-value
    # pairs, since Python 3 doesn't allow comparisons such as `<` between dictionaries.
    checked_list.sort(key=lambda x: sorted(x.items()) if isinstance(x, dict) else x)
    itest().given(checked_list, [1, 3, 2]).check_eq(checked_list, [1, 2, 3])
    itest().given(checked_list, [100, 0, -100, -250, 250]).check_eq(checked_list, [-250, -100, 0, 100, 250])
    # inline test here
    return checked_list
