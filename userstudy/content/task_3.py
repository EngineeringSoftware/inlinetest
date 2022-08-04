from inline import Here


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
    # inline test here
    return checked_list


def sort_json_policy_dict(policy_dict):

    """Sort any lists in an IAM JSON policy so that comparison of two policies with identical values but
    different orders will return true
    Args:
        policy_dict (dict): Dict representing IAM JSON policy.
    Basic Usage:
        >>> my_iam_policy = {'Principle': {'AWS':["31","7","14","101"]}
        >>> sort_json_policy_dict(my_iam_policy)
    Returns:
        Dict: Will return a copy of the policy as a Dict but any List will be sorted
        {
            'Principle': {
                'AWS': [ '7', '14', '31', '101' ]
            }
        }
    """
    ...
