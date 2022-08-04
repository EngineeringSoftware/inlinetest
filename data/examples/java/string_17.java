public class String17 {
    protected void onAttachedToWindow() {
        super.onAttachedToWindow();
        VoIPService service = VoIPService.getSharedInstance();
        if (service != null && service.groupCall != null) {
            int color2 = AvatarDrawable.getColorForId(service.getChat().id);
            AvatarDrawable avatarDrawable = new AvatarDrawable();
            avatarDrawable.setColor(color2);
            avatarDrawable.setInfo(service.getChat());
            avatarImageView.setImage(ImageLocation.getForLocal(service.getChat().photo.photo_small), "50_50", avatarDrawable, null);

            String titleStr;
            if (!TextUtils.isEmpty(service.groupCall.call.title)) {
                titleStr = service.groupCall.call.title;
            } else {
                titleStr = service.getChat().title;
            }
            if (titleStr != null) {
                titleStr = titleStr.replace("\n", " ").replaceAll(" +", " ").trim();
                new Here().given(titleStr, "I am a Title\n\nAnd:  Subtitle\n").checkEq(titleStr, "I am a Title And: Subtitle");
            }
            titleView.setText(titleStr);

            updateMembersCount();
            service.registerStateListener(this);

            if (VoIPService.getSharedInstance() != null) {
                mutedByAdmin = VoIPService.getSharedInstance().mutedByAdmin();
            }
            mutedByAdminProgress = mutedByAdmin ? 1f : 0;
            boolean isMute = VoIPService.getSharedInstance() == null || VoIPService.getSharedInstance().isMicMute() || mutedByAdmin;
            muteProgress = isMute ? 1f : 0f;
        }
        NotificationCenter.getInstance(currentAccount).addObserver(this,NotificationCenter.groupCallUpdated);
        updateButtons(false);
    }    
}
