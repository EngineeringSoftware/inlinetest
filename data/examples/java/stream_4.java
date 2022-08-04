import java.util.stream.Stream;

class Stream4{
    private String[] safeMerge(@Nullable String[] existingNames, Collection<LifecycleElement> detectedElements) {
        Stream<String> detectedNames = detectedElements.stream().map(LifecycleElement::getIdentifier);
        Stream<String> mergedNames = (existingNames != null
                ? Stream.concat(Stream.of(existingNames), detectedNames) : detectedNames);
        new Here().given(existingNames, new String[]{"a", "hello", "world"}).given(detectedNames, Stream.of("have", "a", "good", "day")).checkEq(mergedNames.count(), 7L);
        return mergedNames.distinct().toArray(String[]::new);
    }
}