public class Example {
    protected void onAttachedToWindow() {
      VoIPService service = VoIPService.getSharedInstance();
      if (service != null && service.groupCall != null) {
        String titleStr;
        if (!TextUtils.isEmpty(service.groupCall.call.title)) {
          titleStr = service.groupCall.call.title;
        } else {
          titleStr = service.getChat().title;
        }
        if (titleStr != null) {
          titleStr = titleStr.replace("\n", " ").replaceAll(" +", " ").trim();
          itest().given(titleStr, "I am a Title\n\nAnd:  Subtitle\n").checkEq(titleStr, "I am a Title And: Subtitle");
        }
      }
    } 
}