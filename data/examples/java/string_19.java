public class String19 {
    private void handleNodeReport(final CommandLine cmd, TextStringBuilder result,
            final String nodeFormat, final String volumeFormat) throws Exception {
        String outputLine = "";
        /*
         * get value that identifies DataNode(s) from command line, it could be
         * UUID, IP address or host name.
         */
        final String nodeVal = cmd.getOptionValue(DiskBalancerCLI.NODE);

        if (StringUtils.isBlank(nodeVal)) {
            outputLine = "The value for '-node' is neither specified or empty.";
            recordOutput(result, outputLine);
        } else {
            /*
             * Reporting volume information for specific DataNode(s)
             */
            outputLine = String.format(
                    "Reporting volume information for DataNode(s). "
                            + "These DataNode(s) are parsed from '%s'.",
                    nodeVal);
            new Here().given(nodeVal, "a").given(outputLine, "").checkEq(outputLine, "Reporting volume information for DataNode(s). These DataNode(s) are parsed from 'a'.");
            recordOutput(result, outputLine);

            List<DiskBalancerDataNode> dbdns;
            try {
                dbdns = getNodes(nodeVal);
            } catch (DiskBalancerException e) {
                // If there are some invalid nodes that contained in nodeVal,
                // the exception will be threw.
                recordOutput(result, e.getMessage());
                return;
            }

            if (!dbdns.isEmpty()) {
                for (DiskBalancerDataNode node : dbdns) {
                    recordNodeReport(result, node, nodeFormat, volumeFormat);
                    result.append(System.lineSeparator());
                }
            }
        }
    }
}
