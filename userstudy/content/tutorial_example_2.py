from inline import Here


def _detect_nodejs() -> str:
    nodejs_path = settings.nodejs_path()
    nodejs_paths = [nodejs_path] if nodejs_path is not None else ["nodejs", "node"]

    for nodejs_path in nodejs_paths:
        try:
            proc = Popen([nodejs_path, "--version"], stdout=PIPE, stderr=PIPE)
            (stdout, _) = proc.communicate()
        except OSError:
            continue

        if proc.returncode != 0:
            continue

        match = re.match(r"^v(\d+)\.(\d+)\.(\d+).*$", stdout.decode("utf-8"))
        # First inline test
        Here().given(stdout, "v8.9.4".encode("utf-8")).check_true(match).check_eq(
            match.groups(), ("8", "9", "4")
        )
        # Second inline test
        Here().given(stdout, "v8.9.4abc".encode("utf-8")).check_true(match).check_eq(
            match.groups(), ("8", "9", "4")
        )

        if match is not None:
            version = tuple(int(v) for v in match.groups())
            if version >= nodejs_min_version:
                return nodejs_path

    # if we've reached here, no valid version was found
    version_repr = ".".join(str(x) for x in nodejs_min_version)
    raise RuntimeError(
        f"node.js v{version_repr} or higher is needed to allow compilation of custom models "
        + '("conda install nodejs" or follow https://nodejs.org/en/download/)'
    )
