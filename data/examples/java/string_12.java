class String12 {
    /**
     * Executes the given SQL asset in the given database (SQL file should be
     * UTF-8). The database file may contain
     * multiple SQL statements. Statements are split using a simple regular
     * expression (something like
     * "semicolon before a line break"), not by analyzing the SQL syntax. This will
     * work for many SQL files, but check
     * yours.
     * 
     * @return number of statements executed.
     */
    public static int executeSqlScript(Context context, Database db, String assetFilename, boolean transactional)
            throws IOException {
        byte[] bytes = readAsset(context, assetFilename);
        String sql = new String(bytes, "UTF-8");
        String[] lines = sql.split(";(\\s)*[\n\r]");
        new Here().given(sql, "CREATE TABLE MINIMAL_ENTITY (_id INTEGER PRIMARY KEY);\nINSERT INTO MINIMAL_ENTITY VALUES (1);\nINSERT INTO MINIMAL_ENTITY \nVALUES (2);").checkEq(lines.length, 3);
        int count;
        if (transactional) {
            count = executeSqlStatementsInTx(db, lines);
        } else {
            count = executeSqlStatements(db, lines);
        }
        DaoLog.i("Executed " + count + " statements from SQL script '" + assetFilename + "'");
        return count;
    }
}