from inline import Here

def auto_augment_transform(config_str, hparams):
    """
    Create a AutoAugment transform

    :param config_str: String defining configuration of auto augmentation. Consists of multiple sections separated by
    dashes ('-'). The first section defines the AutoAugment policy (one of 'v0', 'v0r', 'original', 'originalr').
    The remaining sections, not order sepecific determine
        'mstd' -  float std deviation of magnitude noise applied
    Ex 'original-mstd0.5' results in AutoAugment with original policy, magnitude_std 0.5

    :param hparams: Other hparams (kwargs) for the AutoAugmentation scheme

    :return: A PyTorch compatible Transform
    """
    config = config_str.split('-')
    policy_name = config[0]
    config = config[1:]
    for c in config:
        cs = re.split(r'(\d.*)', c)
        Here().given(c, "123aaa223aaa").check_eq(cs, ["", "123aaa223aaa", ""])
        Here().given(c, "aaa123456aaa").check_eq(cs, ["aaa", "123456aaa", ""])
        if len(cs) < 2:
            continue
        key, val = cs[:2]
        if key == 'mstd':
            # noise param injected via hparams for now
            hparams.setdefault('magnitude_std', float(val))
        else:
            assert False, 'Unknown AutoAugment config section'
    aa_policy = auto_augment_policy(policy_name, hparams=hparams)
    return AutoAugment(aa_policy)
