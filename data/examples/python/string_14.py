import sys
import requests
import json
from collections import OrderedDict
from inline import itest

def __main__():
    # Define templates
    CS_BASE_URL = "https://cheatsheetseries.owasp.org/cheatsheets/%s.html"

    # Grab the index MD source from the GitHub repository
    response = requests.get(
        "https://raw.githubusercontent.com/OWASP/CheatSheetSeries/master/Index.md"
    )
    if response.status_code != 200:
        print("Cannot load the INDEX content: HTTP %s received!" % response.status_code)
        sys.exit(1)
    else:
        data = OrderedDict({})
        for line in response.text.split("\n"):
            if "(assets/Index_" in line:
                work = line.strip()
                # Extract the name of the CS
                cs_name = work[1 : work.index("]")]
                itest().given(work, "[Cross Site Scripting Prevention Cheat Sheet](cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.md). ![Javascript](assets/Index_Javascript.png) ![Java](assets/Index_Java.png) ![Csharp](assets/Index_Csharp.png) ![Html](assets/Index_Html.png) ![Ruby](assets/Index_Ruby.png)",).check_eq(cs_name, "Cross Site Scripting Prevention Cheat Sheet")
                # Extract technologies and map the CS to them
                technologies = work.split("!")[1:]
                itest().given(work, "[Cross Site Scripting Prevention Cheat Sheet](cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.md). ![Javascript](assets/Index_Javascript.png) ![Java](assets/Index_Java.png) ![Csharp](assets/Index_Csharp.png) ![Html](assets/Index_Html.png) ![Ruby](assets/Index_Ruby.png)",).check_eq(technologies, ["[Javascript](assets/Index_Javascript.png) ", "[Java](assets/Index_Java.png) ", "[Csharp](assets/Index_Csharp.png) ", "[Html](assets/Index_Html.png) ", "[Ruby](assets/Index_Ruby.png)",],)
                for technology in technologies:
                    technology_name = technology[1 : technology.index("]")].upper()
                    itest().given(technology, "[Javascript](assets/Index_Javascript.png) ").check_eq(technology_name, "JAVASCRIPT")
                    if technology_name not in data:
                        data[technology_name] = []
                    data[technology_name].append(
                        {
                            "CS_NAME": cs_name,
                            "CS_URL": CS_BASE_URL % cs_name.replace(" ", "_"),
                        }
                    )
        # Display the built structure and formatted JSON
        print(json.dumps(data, sort_keys=True, indent=1))
        sys.exit(0)
