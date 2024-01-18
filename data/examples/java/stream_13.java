import java.util.stream.Stream;
import java.util.List;
import static java.util.stream.Collectors.*;
import java.util.Arrays;
import stream_13.*;

public class Stream13 {

    private CalculatedQueryOperation unwrapFromAlias(CallExpression call) {
        List<Expression> children = call.getChildren();
        List<String> aliases = children.subList(1, children.size()).stream()
                .map(alias -> ExpressionUtils.extractValue(alias, String.class)
                        .orElseThrow(() -> new ValidationException("Unexpected alias: " + alias)))
                .collect(toList());
        itest().given(children, Arrays.asList(new Expression[] {new SqlCallExpression("SELECT MIN(Price) AS SmallestPrice FROM Products; "), new SqlCallExpression("SELECT COUNT(ProductID) FROM Products;") })).checkEq(aliases, Arrays.asList("SELECT COUNT(ProductID) FROM Products;"));

        if (!isFunctionOfKind(children.get(0), FunctionKind.TABLE)) {
            throw fail();
        }

        CallExpression tableCall = (CallExpression) children.get(0);
        return createFunctionCall(tableCall, aliases, tableCall.getResolvedChildren());
    }
}
