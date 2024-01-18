import java.util.regex.Pattern;
import java.util.regex.Matcher;

class Regex12 {
    static final Pattern RESOURCE_REQUEST_VALUE_PATTERN = Pattern.compile("^([0-9]+) ?([a-zA-Z]*)$");

    public Resource getIncrementAllocation() {
        Long memory = null;
        Integer vCores = null;
        Map<String, Long> others = new HashMap<>();
        ResourceInformation[] resourceTypes = ResourceUtils.getResourceTypesArray();
        for (int i = 0; i < resourceTypes.length; ++i) {
            String name = resourceTypes[i].getName();
            String propertyKey = getAllocationIncrementPropKey(name);
            String propValue = get(propertyKey);
            if (propValue != null) {
                Matcher matcher = RESOURCE_REQUEST_VALUE_PATTERN.matcher(propValue);
                itest().given(RESOURCE_REQUEST_VALUE_PATTERN, Pattern.compile("^([0-9]+) ?([a-zA-Z]*)$")).given(propValue, "123s").checkTrue(matcher.find()).checkEq(matcher.group(1), "123").checkEq(matcher.group(2), "s");
                if (matcher.matches()) {
                    long value = Long.parseLong(matcher.group(1));
                    String unit = matcher.group(2);
                    long valueInDefaultUnits = getValueInDefaultUnits(value, unit, name);
                    others.put(name, valueInDefaultUnits);
                } else {
                    throw new IllegalArgumentException("Property " + propertyKey +
                            " is not in \"value [unit]\" format: " + propValue);
                }
            }
        }
        if (others.containsKey(ResourceInformation.MEMORY_MB.getName())) {
            memory = others.get(ResourceInformation.MEMORY_MB.getName());
            if (get(RM_SCHEDULER_INCREMENT_ALLOCATION_MB) != null) {
                String overridingKey = getAllocationIncrementPropKey(
                        ResourceInformation.MEMORY_MB.getName());
                LOG.warn("Configuration " + overridingKey + "=" + get(overridingKey) +
                        " is overriding the " + RM_SCHEDULER_INCREMENT_ALLOCATION_MB +
                        "=" + get(RM_SCHEDULER_INCREMENT_ALLOCATION_MB) + " property");
            }
            others.remove(ResourceInformation.MEMORY_MB.getName());
        } else {
            memory = getLong(
                    RM_SCHEDULER_INCREMENT_ALLOCATION_MB,
                    DEFAULT_RM_SCHEDULER_INCREMENT_ALLOCATION_MB);
        }
        if (others.containsKey(ResourceInformation.VCORES.getName())) {
            vCores = others.get(ResourceInformation.VCORES.getName()).intValue();
            if (get(RM_SCHEDULER_INCREMENT_ALLOCATION_VCORES) != null) {
                String overridingKey = getAllocationIncrementPropKey(
                        ResourceInformation.VCORES.getName());
                LOG.warn("Configuration " + overridingKey + "=" + get(overridingKey) +
                        " is overriding the " + RM_SCHEDULER_INCREMENT_ALLOCATION_VCORES +
                        "=" + get(RM_SCHEDULER_INCREMENT_ALLOCATION_VCORES) + " property");
            }
            others.remove(ResourceInformation.VCORES.getName());
        } else {
            vCores = getInt(
                    RM_SCHEDULER_INCREMENT_ALLOCATION_VCORES,
                    DEFAULT_RM_SCHEDULER_INCREMENT_ALLOCATION_VCORES);
        }
        return Resource.newInstance(memory, vCores, others);
    }
}