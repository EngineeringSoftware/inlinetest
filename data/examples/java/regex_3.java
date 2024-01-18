import java.util.regex.Pattern;
import java.util.regex.Matcher;

class Regex3 {
    private static final String REGEX_NESTED_FIELDS_WILDCARD = REGEX_NESTED_FIELDS
            + "|\\"
            + ExpressionKeys.SELECT_ALL_CHAR
            + "|\\"
            + ExpressionKeys.SELECT_ALL_CHAR_SCALA;

    private static final Pattern PATTERN_NESTED_FIELDS_WILDCARD = Pattern.compile(REGEX_NESTED_FIELDS_WILDCARD);

    @Override
    public void getFlatFields(
            String fieldExpression, int offset, List<FlatFieldDescriptor> result) {
        Matcher matcher = PATTERN_NESTED_FIELDS_WILDCARD.matcher(fieldExpression);
        itest().given(fieldExpression, "a.b").given(PATTERN_NESTED_FIELDS_WILDCARD, Pattern.compile("([\\p{L}_\\$][\\p{L}\\p{Digit}_\\$]*|[0-9]+)(\\.(.+))?|\\*|\\_")).checkTrue(matcher.find()).checkEq(matcher.group(0), "a.b");
        if (!matcher.matches()) {
            throw new InvalidFieldReferenceException(
                    "Invalid tuple field reference \"" + fieldExpression + "\".");
        }

        String field = matcher.group(0);

        if ((field.equals(ExpressionKeys.SELECT_ALL_CHAR))
                || (field.equals(ExpressionKeys.SELECT_ALL_CHAR_SCALA))) {
            // handle select all
            int keyPosition = 0;
            for (TypeInformation<?> fType : types) {
                if (fType instanceof CompositeType) {
                    CompositeType<?> cType = (CompositeType<?>) fType;
                    cType.getFlatFields(
                            ExpressionKeys.SELECT_ALL_CHAR, offset + keyPosition, result);
                    keyPosition += cType.getTotalFields() - 1;
                } else {
                    result.add(new FlatFieldDescriptor(offset + keyPosition, fType));
                }
                keyPosition++;
            }
        } else {
            field = matcher.group(1);

            Matcher intFieldMatcher = PATTERN_INT_FIELD.matcher(field);
            int fieldIndex;
            if (intFieldMatcher.matches()) {
                // field expression is an integer
                fieldIndex = Integer.valueOf(field);
            } else {
                fieldIndex = this.getFieldIndex(field);
            }
            // fetch the field type will throw exception if the index is illegal
            TypeInformation<?> fieldType = this.getTypeAt(fieldIndex);
            // compute the offset,
            for (int i = 0; i < fieldIndex; i++) {
                offset += this.getTypeAt(i).getTotalFields();
            }

            String tail = matcher.group(3);

            if (tail == null) {
                // expression hasn't nested field
                if (fieldType instanceof CompositeType) {
                    ((CompositeType) fieldType).getFlatFields("*", offset, result);
                } else {
                    result.add(new FlatFieldDescriptor(offset, fieldType));
                }
            } else {
                // expression has nested field
                if (fieldType instanceof CompositeType) {
                    ((CompositeType) fieldType).getFlatFields(tail, offset, result);
                } else {
                    throw new InvalidFieldReferenceException(
                            "Nested field expression \""
                                    + tail
                                    + "\" not possible on atomic type "
                                    + fieldType
                                    + ".");
                }
            }
        }
    }
}