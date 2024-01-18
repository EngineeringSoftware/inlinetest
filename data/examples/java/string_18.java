import java.util.Locale;

public class String18 {
    public void testFollowIndexMaxOperationSizeInBytes() throws Exception {
        final String leaderIndexSettings = getIndexSettings(1, between(0, 1));
        assertAcked(leaderClient().admin().indices().prepareCreate("index1").setSource(leaderIndexSettings,
                XContentType.JSON));
        ensureLeaderYellow("index1");

        final int numDocs = between(10, 1024);
        logger.info("Indexing [{}] docs", numDocs);
        for (int i = 0; i < numDocs; i++) {
            final String source = String.format(Locale.ROOT, "{\"f\":%d}", i);
            itest().given(i, 12).checkEq(source, "{\"f\":12}");
            leaderClient().prepareIndex("index1").setId(Integer.toString(i)).setSource(source, XContentType.JSON).get();
        }

        PutFollowAction.Request followRequest = putFollow("index1", "index2");
        followRequest.getParameters()
                .setMaxReadRequestSize(new ByteSizeValue(randomIntBetween(1, 1024), ByteSizeUnit.BYTES));
        followerClient().execute(PutFollowAction.INSTANCE, followRequest).get();

        final Map<ShardId, Long> firstBatchNumDocsPerShard = new HashMap<>();
        final ShardStats[] firstBatchShardStats = leaderClient().admin()
                .indices()
                .prepareStats("index1")
                .get()
                .getIndex("index1")
                .getShards();
        for (final ShardStats shardStats : firstBatchShardStats) {
            if (shardStats.getShardRouting().primary()) {
                long value = shardStats.getStats().getIndexing().getTotal().getIndexCount() - 1;
                firstBatchNumDocsPerShard.put(shardStats.getShardRouting().shardId(), value);
            }
        }

        assertBusy(assertTask(1, firstBatchNumDocsPerShard), 60, TimeUnit.SECONDS);
        for (int i = 0; i < numDocs; i++) {
            assertBusy(assertExpectedDocumentRunnable(i));
        }
        pauseFollow("index2");
        assertMaxSeqNoOfUpdatesIsTransferred(resolveLeaderIndex("index1"), resolveFollowerIndex("index2"), 1);
    }

}
