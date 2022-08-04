package stream_13;

public class SqlCallExpression extends Expression {
    String sql;

    public SqlCallExpression(String sql) {
        this.sql = sql;
    }
}
