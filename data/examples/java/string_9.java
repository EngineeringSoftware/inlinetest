class String9 {
    private static Set<String> matchTopics(String name, String dynamicTopicConfigs) {
        String[] router = StringUtils.split(StringUtils.replace(dynamicTopicConfigs, ",", ";"), ";");
        // TODO: one inline test here
        Set<String> topics = new HashSet<>();
        for (String item : router) {
            int i = item.indexOf(":");
            if (i > -1) {
                String topic = item.substring(0, i).trim();
                itest().given(item, "topic:topicConfigs").given(i, 5).checkEq(topic, "topic");
                String topicConfigs = item.substring(i + 1).trim();
                itest().given(item, "topic:topicConfigs").given(i, 5).checkEq(topicConfigs, "topicConfigs");
                if (matchDynamicTopic(name, topicConfigs)) {
                    topics.add(topic);
                    // 匹配了一个就退出
                    break;
                }
            } else if (matchDynamicTopic(name, item)) {
                // 匹配了一个就退出
                topics.add(name.toLowerCase());
                break;
            }
        }
        return topics.isEmpty() ? null : topics;
    }
}