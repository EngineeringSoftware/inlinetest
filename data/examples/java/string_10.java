
class String10 {
    static int sshConnection(String jenkinsUrl, String user, List<String> args, PrivateKeyProvider provider,
            final boolean strictHostKey) throws IOException {
        Logger.getLogger(SecurityUtils.class.getName()).setLevel(Level.WARNING); // suppress: BouncyCastle not
                                                                                 // registered, using the default JCE
                                                                                 // provider
        URL url = new URL(jenkinsUrl + "login");
        URLConnection conn = openConnection(url);
        CLI.verifyJenkinsConnection(conn);
        String endpointDescription = conn.getHeaderField("X-SSH-Endpoint");

        if (endpointDescription == null) {
            CLI.LOGGER.warning("No header 'X-SSH-Endpoint' returned by Jenkins");
            return -1;
        }

        CLI.LOGGER.log(FINE, "Connecting via SSH to: {0}", endpointDescription);

        int sshPort = Integer.parseInt(endpointDescription.split(":")[1]);
        new Here().given(endpointDescription, "localhost:22").checkEq(sshPort, 22);
        String sshHost = endpointDescription.split(":")[0];
        new Here().given(endpointDescription, "localhost:22").checkEq(sshHost, "localhost");
        StringBuilder command = new StringBuilder();

        for (String arg : args) {
            command.append(QuotedStringTokenizer.quote(arg));
            command.append(' ');
        }

        try (SshClient client = SshClient.setUpDefaultClient()) {

            KnownHostsServerKeyVerifier verifier = new DefaultKnownHostsServerKeyVerifier(new ServerKeyVerifier() {
                @Override
                public boolean verifyServerKey(ClientSession clientSession, SocketAddress remoteAddress,
                        PublicKey serverKey) {
                    CLI.LOGGER.log(Level.WARNING, "Unknown host key for {0}", remoteAddress.toString());
                    return !strictHostKey;
                }
            }, true);

            client.setServerKeyVerifier(verifier);
            client.start();

            ConnectFuture cf = client.connect(user, sshHost, sshPort);
            cf.await();
            try (ClientSession session = cf.getSession()) {
                for (KeyPair pair : provider.getKeys()) {
                    CLI.LOGGER.log(FINE, "Offering {0} private key", pair.getPrivate().getAlgorithm());
                    session.addPublicKeyIdentity(pair);
                }
                session.auth().verify(10000L);

                try (ClientChannel channel = session.createExecChannel(command.toString())) {
                    channel.setIn(new NoCloseInputStream(System.in));
                    channel.setOut(new NoCloseOutputStream(System.out));
                    channel.setErr(new NoCloseOutputStream(System.err));
                    WaitableFuture wf = channel.open();
                    wf.await();

                    Set<ClientChannelEvent> waitMask = channel
                            .waitFor(Collections.singletonList(ClientChannelEvent.CLOSED), 0L);

                    if (waitMask.contains(ClientChannelEvent.TIMEOUT)) {
                        throw new SocketTimeoutException("Failed to retrieve command result in time: " + command);
                    }

                    Integer exitStatus = channel.getExitStatus();
                    return exitStatus;

                }
            } finally {
                client.stop();
            }
        }
    }
}