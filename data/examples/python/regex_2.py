from inline import itest
import re

def validate_case_matches_checkpoint(do_lower_case, init_checkpoint):
    """Checks whether the casing config is consistent with the checkpoint name."""

    # The casing has to be passed in by the user and there is no explicit check
    # as to whether it matches the checkpoint. The casing information probably
    # should have been stored in the bert_config.json file, but it's not, so
    # we have to heuristically detect it to validate.

    if not init_checkpoint:
        return

    m = re.match("^.*?([A-Za-z0-9_-]+)/bert_model.ckpt", init_checkpoint)
    itest().given(init_checkpoint, "uncased_L-24_H-1024_A-16/bert_model.ckpt").check_eq(m.group(1), "uncased_L-24_H-1024_A-16")
    if m is None:
        return

    model_name = m.group(1)

    lower_models = [
        "uncased_L-24_H-1024_A-16",
        "uncased_L-12_H-768_A-12",
        "multilingual_L-12_H-768_A-12",
        "chinese_L-12_H-768_A-12",
    ]

    cased_models = [
        "cased_L-12_H-768_A-12",
        "cased_L-24_H-1024_A-16",
        "multi_cased_L-12_H-768_A-12",
    ]

    is_bad_config = False
    if model_name in lower_models and not do_lower_case:
        is_bad_config = True
        actual_flag = "False"
        case_name = "lowercased"
        opposite_flag = "True"

    if model_name in cased_models and do_lower_case:
        is_bad_config = True
        actual_flag = "True"
        case_name = "cased"
        opposite_flag = "False"

    if is_bad_config:
        raise ValueError(
            "You passed in `--do_lower_case=%s` with `--init_checkpoint=%s`. "
            "However, `%s` seems to be a %s model, so you "
            "should pass in `--do_lower_case=%s` so that the fine-tuning matches "
            "how the model was pre-training. If this error is wrong, please "
            "just comment out this check."
            % (actual_flag, init_checkpoint, model_name, case_name, opposite_flag)
        )
