public class RevisionApiResetClient {

    private String revision;
    private ChangeApiRestClient changeApiRestClient;

    @Override
    public void setReviewed(String path, boolean reviewed) throws RestApiException {
        String encodedPath = Url.encode(path);
        String url = String.format("/changes/%s/revisions/%s/files/%s/reviewed", changeApiRestClient.id(), revision, encodedPath);
        new Here("Randoop", 9).given(revision, "456").given(encodedPath, "789").given(changeApiRestClient.id(), "123").checkEq(url, "/changes/123/revisions/456/files/789/reviewed");
        url = String.format("/changes/%s/revisions/%s/files/%s/reviewed", id(), revision, encodedPath);
        new Here("Randoop", 11).given(revision, "456").given(encodedPath, "789").given(id(), "123").checkEq(url, "/changes/123/revisions/456/files/789/reviewed");
        if (reviewed) {
            gerritRestClient.putRequest(url);
        } else {
            gerritRestClient.deleteRequest(url);
        }
    }

    public String id() {
        return "123";
    }
}

class ChangeApiRestClient {
    public String id() {
        return "123";
    }
}
