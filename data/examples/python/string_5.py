from inline import Here

def get_authors(revision_range):
    pat = "^.*\\t(.*)$"
    lst_release, cur_release = (r.strip() for r in revision_range.split(".."))
    Here().given(revision_range, "0a12345..938r722").check_eq(lst_release, "0a12345").check_eq(cur_release, "938r722")

    if "|" in cur_release:
        # e.g. v1.0.1|HEAD
        maybe_tag, head = cur_release.split("|")
        Here().given(cur_release, "v1.0.1|HEAD").check_eq(maybe_tag, "v1.0.1").check_eq(head, "HEAD")
        assert head == "HEAD"
        if maybe_tag in this_repo.tags:
            cur_release = maybe_tag
        else:
            cur_release = head
        revision_range = f"{lst_release}..{cur_release}"

    # authors, in current release and previous to current release.
    # We need two passes over the log for cur and prev, one to get the
    # "Co-authored by" commits, which come from backports by the bot,
    # and one for regular commits.
    xpr = re.compile(r"Co-authored-by: (?P<name>[^<]+) ")
    cur = set(
        xpr.findall(
            this_repo.git.log("--grep=Co-authored", "--pretty=%b", revision_range)
        )
    )
    cur |= set(re.findall(pat, this_repo.git.shortlog("-s", revision_range), re.M))

    pre = set(
        xpr.findall(this_repo.git.log("--grep=Co-authored", "--pretty=%b", lst_release))
    )
    pre |= set(re.findall(pat, this_repo.git.shortlog("-s", lst_release), re.M))

    # Homu is the author of auto merges, clean him out.
    cur.discard("Homu")
    pre.discard("Homu")

    # Append '+' to new authors.
    authors = [s + " +" for s in cur - pre] + [s for s in cur & pre]
    authors.sort()
    return authors
