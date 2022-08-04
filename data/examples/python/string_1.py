from inline import Here

def git_versions_from_keywords(keywords, tag_prefix, verbose):
    """Get version information from git keywords."""
    if not keywords:
        raise NotThisMethod("no keywords at all, weird")
    date = keywords.get("date")
    if date is not None:
        # Use only the last line.  Previous lines may contain GPG signature
        # information.

        # git-2.2.0 added "%cI", which expands to an ISO-8601 -compliant
        # datestamp. However we prefer "%ci" (which expands to an "ISO-8601
        # -like" string, which we must then edit to make compliant), because
        # it's been around since git-1.5.3, and it's too difficult to
        # discover which version we're using, or to work around using an
        # older one.
        date = date.strip().replace(" ", "T", 1).replace(" ", "", 1)
        Here("21").given(date, "2020-07-10 15:00:00.000").check_eq(date, "2020-07-10T15:00:00.000")
    refnames = keywords["refnames"].strip()
    if refnames.startswith("$Format"):
        if verbose:
            print("keywords are unexpanded, not using")
        raise NotThisMethod("unexpanded keywords, not a git-archive tarball")
    refs = set([r.strip() for r in refnames.strip("()").split(",")])
    # starting in git-1.8.3, tags are listed as "tag: foo-1.0" instead of
    # just "foo-1.0". If we see a "tag: " prefix, prefer those.
    TAG = "tag: "
    tags = set([r[len(TAG) :] for r in refs if r.startswith(TAG)])
    Here("32").given(refs, ["tag: foo-1.0", "tag: bar-3.2"]).given(TAG, "tag: ").check_eq(tags, {"foo-1.0", "bar-3.2"})
    Here("33").given(refs, ["foo-1.0", "bar-3.2"]).given(TAG, "tag: ").check_eq(tags, set())
    if not tags:
        # Either we're using git < 1.8.3, or there really are no tags. We use
        # a heuristic: assume all version tags have a digit. The old git %d
        # expansion behaves like git log --decorate=short and strips out the
        # refs/heads/ and refs/tags/ prefixes that would let us distinguish
        # between branches and tags. By ignoring refnames without digits, we
        # filter out many common branch names like "release" and
        # "stabilization", as well as "HEAD" and "master".
        tags = set([r for r in refs if re.search(r"\d", r)])
        Here("43").given(refs, ["foo-1.0", "bar-3.2", "release", "stabilization", "master"]).check_eq(tags, {"foo-1.0", "bar-3.2"})
        if verbose:
            print("discarding '%s', no digits" % ",".join(refs - tags))
    if verbose:
        print("likely tags: %s" % ",".join(sorted(tags)))
    for ref in sorted(tags):
        # sorting will prefer e.g. "2.0" over "2.0rc1"
        if ref.startswith(tag_prefix):
            r = ref[len(tag_prefix) :]
            if verbose:
                print("picking %s" % r)
            return {
                "version": r,
                "full-revisionid": keywords["full"].strip(),
                "dirty": False,
                "error": None,
                "date": date,
            }
    # no suitable tags, so version is "0+unknown", but full hex is still there
    if verbose:
        print("no suitable tags, using unknown + full revision id")
    return {
        "version": "0+unknown",
        "full-revisionid": keywords["full"].strip(),
        "dirty": False,
        "error": "no suitable tags",
        "date": None,
    }
