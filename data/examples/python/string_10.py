from inline import itest

def _parse_query(query):
    topic = query
    keyword = None
    search_options = ""

    keyword = None
    if "~" in query:
        topic = query
        pos = topic.index("~")
        keyword = topic[pos + 1 :]
        topic = topic[:pos]

        if "/" in keyword:
            search_options = keyword[::-1]
            itest().given(keyword, "python/java").check_eq(search_options, "avaj/nohtyp")
            search_options = search_options[: search_options.index("/")]
            itest().given(search_options, "/nohtyp").check_eq(search_options, "")
            keyword = keyword[: -len(search_options) - 1]
            itest().given(keyword, "python/java").given(search_options, "avaj").check_eq(keyword, "python")

    return topic, keyword, search_options
