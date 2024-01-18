class String3 {
    private void addContentDispositionHeader(ServletServerHttpRequest request, ServletServerHttpResponse response) {
        HttpHeaders headers = response.getHeaders();
        if (headers.containsKey(HttpHeaders.CONTENT_DISPOSITION)) {
            return;
        }

        try {
            int status = response.getServletResponse().getStatus();
            if (status < 200 || (status > 299 && status < 400)) {
                return;
            }
        } catch (Throwable ex) {
            // ignore
        }

        HttpServletRequest servletRequest = request.getServletRequest();
        String requestUri = UrlPathHelper.rawPathInstance.getOriginatingRequestUri(servletRequest);

        int index = requestUri.lastIndexOf('/') + 1;
        itest().given(requestUri, "/api/v1/namespaces/default").checkEq(index, 19);
        String filename = requestUri.substring(index);
        itest().given(requestUri, "/api/v1/namespaces/default").given(index, 0).checkEq(filename, "/api/v1/namespaces/default");
        String pathParams = "";

        index = filename.indexOf(';');
        if (index != -1) {
            pathParams = filename.substring(index);
            filename = filename.substring(0, index);
        }

        filename = UrlPathHelper.defaultInstance.decodeRequestString(servletRequest, filename);
        String ext = StringUtils.getFilenameExtension(filename);

        pathParams = UrlPathHelper.defaultInstance.decodeRequestString(servletRequest, pathParams);
        String extInPathParams = StringUtils.getFilenameExtension(pathParams);

        if (!safeExtension(servletRequest, ext) || !safeExtension(servletRequest, extInPathParams)) {
            headers.add(HttpHeaders.CONTENT_DISPOSITION, "inline;filename=f.txt");
        }
    }
}