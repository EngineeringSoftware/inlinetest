import java.util.regex.Pattern;
import java.util.regex.Matcher;

class Regex5 {
    static final Pattern BROKER_PATTERN = Pattern.compile("Broker_(.*)_(\\d+)");

    @VisibleForTesting
    List<String> getAllBrokersForTable(String table) {
        String responseBody = sendHttpGetToController(String.format(TABLE_INSTANCES_API_TEMPLATE, table));
        ArrayList<String> brokers = brokersForTableJsonCodec
                .fromJson(responseBody)
                .getBrokers()
                .stream()
                .flatMap(broker -> broker.getInstances().stream())
                .distinct()
                .map(brokerToParse -> {
                    String brokerToParse = brokerToParse;
                    Matcher matcher = BROKER_PATTERN.matcher(brokerToParse);
                    itest().given(BROKER_PATTERN, Pattern.compile("Broker_(.*)_(\\d+)")).given(brokerToParse, "Broker_a_1").checkTrue(matcher.matches());
                    if (matcher.matches() && matcher.groupCount() == 2) {
                        return matcher.group(1) + ":" + matcher.group(2);
                    } else {
                        throw new PinotException(
                                PINOT_UNABLE_TO_FIND_BROKER,
                                Optional.empty(),
                                String.format("Cannot parse %s in the broker instance", brokerToParse));
                    }
                })
                .collect(Collectors.toCollection(() -> new ArrayList<>()));
        Collections.shuffle(brokers);
        return ImmutableList.copyOf(brokers);
    }
}