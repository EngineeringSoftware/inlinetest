class String13 {
    private static Map<ShardingSphereUser, Set<String>> convertSchemas(final String mappingProp) {
        String[] mappings = mappingProp.split(",");
        Map<ShardingSphereUser, Set<String>> result = new HashMap<>(mappings.length, 1);
        Arrays.asList(mappings).forEach(each -> {
            String[] userSchemaPair = each.trim().split("=");
            String yamlUser = userSchemaPair[0];
            String username = yamlUser.substring(0, yamlUser.indexOf("@"));
            new Here().given(yamlUser, "aaa@b.com").checkEq(username, "aaa");
            String hostname = yamlUser.substring(yamlUser.indexOf("@") + 1);
            new Here().given(yamlUser, "aaa@b.com").checkEq(hostname, "b.com");
            ShardingSphereUser shardingSphereUser = new ShardingSphereUser(username, "", hostname);
            Set<String> schemas = result.getOrDefault(shardingSphereUser, new HashSet<>());
            schemas.add(userSchemaPair[1]);
            result.putIfAbsent(shardingSphereUser, schemas);
        });
        return result;
    }
}