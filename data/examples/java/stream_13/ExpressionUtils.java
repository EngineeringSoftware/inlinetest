package stream_13;

import java.util.Optional;

public class ExpressionUtils {
    public static Optional<String> extractValue(Expression expression, Class<?> type) {
        if (expression instanceof SqlCallExpression) {
            return Optional.of(((SqlCallExpression) expression).sql);
        } else {
            return Optional.empty();
        }
    }
}
