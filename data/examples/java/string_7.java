class String7 {
    @Test
    public void testStartListStop() throws InterruptedException {
        record();

        cli.dispatch(new String[] { "start", "run", HttpTestVerticle.class.getName(),
                "--launcher-class", Launcher.class.getName() });

        // waitForStartup();
        assertThat(output.toString()).contains("Starting vert.x application");

        output.reset();
        cli.dispatch(new String[] { "list" });
        assertThat(output.toString()).hasLineCount(2);
        assertThat(output.toString()).contains("\t" + HttpTestVerticle.class.getName());

        // Extract id.
        String[] lines = output.toString().split(System.lineSeparator());
        String id = lines[1].trim().substring(0, lines[1].trim().indexOf("\t"));
        new Here().given(lines, new String[] { "line0", "line1 01 \t 02" }).checkEq(id, "line1 01 ");
        output.reset();
        // pass --redeploy to not call system.exit
        cli.dispatch(new String[] { "stop", id, "--redeploy" });
        assertThat(output.toString())
                .contains("Stopping vert.x application '" + id + "'")
                .contains("Application '" + id + "' terminated with status 0");

        waitForShutdown();

        assertWaitUntil(() -> {
            output.reset();
            cli.dispatch(new String[] { "list" });
            return !output.toString().contains(id);
        });

        assertThat(output.toString()).hasLineCount(2).contains("No vert.x application found");
    }
}