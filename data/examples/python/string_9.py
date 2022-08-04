from typing import Dict, List
from inline import Here

def extract_sota_table(table_lines: List[str]) -> Dict:
    """
    Parse a SOTA table out of lines in markdown

    :param table_lines: lines in the SOTA table
    :return:
    """

    sota = {}

    header = table_lines[0]
    header_cols = [h.strip() for h in header.split("|") if h.strip()]
    Here().given(header, "a | b + | C**").check_eq(header_cols, ["a", "b +", "C**"])
    cols_sanitized = [h.lower() for h in header_cols]
    Here().given(header_cols, ["a", "b +", "C**"]).check_eq(cols_sanitized, ["a", "b +", "c**"])
    cols_sanitized = [re.sub(" +", "", h).replace("**", "") for h in cols_sanitized]
    Here().given(cols_sanitized, ["a", "b+**", "c"]).check_eq(cols_sanitized, ["a", "b+", "c"])

    # find the model name column (usually the first one)
    if "model" in cols_sanitized:
        model_inx = cols_sanitized.index("model")
    else:
        print(
            "ERROR: Model name not found in this SOTA table, skipping...\n",
            file=sys.stderr,
        )
        print("".join(table_lines), file=sys.stderr)
        return {}

    if "paper/source" in cols_sanitized:
        paper_inx = cols_sanitized.index("paper/source")
    elif "paper" in cols_sanitized:
        paper_inx = cols_sanitized.index("paper")
    else:
        print(
            "ERROR: Paper reference not found in this SOTA table, skipping...\n",
            file=sys.stderr,
        )
        print("".join(table_lines), file=sys.stderr)
        return {}

    if "code" in cols_sanitized:
        code_inx = cols_sanitized.index("code")
    else:
        code_inx = None

    metrics_inx = set(range(len(header_cols))) - set([model_inx, paper_inx, code_inx])
    metrics_inx = sorted(list(metrics_inx))

    metrics_names = [header_cols[i] for i in metrics_inx]

    sota["metrics"] = metrics_names
    sota["rows"] = []

    min_cols = len(header_cols)

    # now parse the table rows
    rows = table_lines[2:]
    for row in rows:
        row_cols = [h.strip() for h in row.split("|")][1:]

        if len(row_cols) < min_cols:
            print(
                "This row doesn't have enough columns, skipping: %s" % row,
                file=sys.stderr,
            )
            continue

        # extract all the metrics
        metrics = {}
        for i in range(len(metrics_inx)):
            metrics[metrics_names[i]] = row_cols[metrics_inx[i]]

        # extract paper references
        paper_title, paper_link = extract_paper_title_and_link(row_cols[paper_inx])

        # extract model_name and author
        model_name, model_author = extract_model_name_and_author(row_cols[model_inx])

        sota_row = {
            "model_name": model_name,
            "metrics": metrics,
        }

        if paper_title is not None and paper_link is not None:
            sota_row["paper_title"] = paper_title
            sota_row["paper_url"] = paper_link

        # and code links if they exist
        if code_inx is not None:
            sota_row["code_links"] = extract_code_links(row_cols[code_inx])

        sota["rows"].append(sota_row)

    return sota
