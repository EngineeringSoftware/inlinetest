from inline import itest
import re

def _login(self, webpage_url, display_id):
    username, password = self._get_login_info()
    if username is None or password is None:
        self.report_warning(
            "It looks like "
            + webpage_url
            + " requires a login. Try specifying a username and password and try again."
        )
        return None

    mobj = re.match(r"(?P<root_url>https?://.*?/).*", webpage_url)
    itest().given(webpage_url, "https://www.youtube.com/abc").check_eq(mobj.group("root_url"), "https://www.youtube.com/")
    login_url = mobj.group("root_url") + "api/login.php"
    logout_url = mobj.group("root_url") + "logout"

    login_form = {
        "email": username,
        "password": password,
    }

    request = sanitized_Request(login_url, urlencode_postdata(login_form))
    request.add_header("Content-Type", "application/x-www-form-urlencoded")
    self._download_webpage(request, display_id, "Logging in")
    start_page = self._download_webpage(
        webpage_url, display_id, "Getting authenticated video page"
    )
    self._download_webpage(logout_url, display_id, "Logging out")

    return start_page
