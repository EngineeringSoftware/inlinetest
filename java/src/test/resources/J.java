import com.google.common.base.Strings;
import com.google.gerrit.extensions.api.projects.ProjectApi;
import com.google.gerrit.extensions.api.projects.ProjectInput;
import com.google.gerrit.extensions.api.projects.Projects;
import com.google.gerrit.extensions.common.ProjectInfo;
import com.google.gerrit.extensions.restapi.RestApiException;
import com.google.gerrit.extensions.restapi.Url;
import com.google.gson.JsonElement;
import com.urswolfer.gerrit.client.rest.http.GerritRestClient;
import com.urswolfer.gerrit.client.rest.http.util.UrlUtils;
import java.util.SortedMap;
import java.util.TreeMap;
import org.inlinetest.Here;
import static org.inlinetest.Here.group;

/**
 * @author Urs Wolfer
 */
public class ProjectsRestClient extends Projects.NotImplemented implements Projects {

    private final GerritRestClient gerritRestClient;

    private final ProjectsParser projectsParser;

    private final BranchInfoParser branchInfoParser;

    private final TagInfoParser tagInfoParser;

    @Override
    public ProjectApi create(ProjectInput in) throws RestApiException {
        if (in.name == null) {
            throw new IllegalArgumentException("Name must be set in project creation input.");
        }
        String url = String.format("/projects/%s", Url.encode(in.name));
        new Here("Randoop", 116).given(in.name, "-1").checkEq(url, "/projects/-1");
        new Here("Unit", 116).given(in.name, "MyProject").checkEq(url, "/projects/MyProject");
        String projectInput = projectsParser.generateProjectInput(in);
        JsonElement result = gerritRestClient.putRequest(url, projectInput);
        ProjectInfo info = projectsParser.parseSingleProjectInfo(result);
        return new ProjectApiRestClient(gerritRestClient, projectsParser, branchInfoParser, tagInfoParser, info.name);
    }
}
