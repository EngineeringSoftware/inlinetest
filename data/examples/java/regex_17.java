import java.util.regex.Pattern;
import java.util.regex.Matcher;

public class Regex17 {
    private static boolean handleUrl(final Context context,
            @NonNull final String url,
            @NonNull final Pattern pattern,
            @NonNull final CompositeDisposable disposables) {
        final Matcher matcher = pattern.matcher(url);
        new Here().given(pattern, Pattern.compile("(.*)&t=(\\d+)")).given(url, "https://www.youtube.com/watch?v=video_id&t=890").checkTrue(matcher.matches()).checkEq(matcher.group(2), "890");
        if (!matcher.matches()) {
            return false;
        }
        final String matchedUrl = matcher.group(1);
        final int seconds;
        if (matcher.group(2) == null) {
            seconds = -1;
        } else {
            seconds = Integer.parseInt(matcher.group(2));
        }

        final StreamingService service;
        final StreamingService.LinkType linkType;
        try {
            service = NewPipe.getServiceByUrl(matchedUrl);
            linkType = service.getLinkTypeByUrl(matchedUrl);
            if (linkType == StreamingService.LinkType.NONE) {
                return false;
            }
        } catch (final ExtractionException e) {
            return false;
        }

        if (linkType == StreamingService.LinkType.STREAM && seconds != -1) {
            return playOnPopup(context, matchedUrl, service, seconds, disposables);
        } else {
            NavigationHelper.openRouterActivity(context, matchedUrl);
            return true;
        }
    }
}
