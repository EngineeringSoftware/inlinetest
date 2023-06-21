package org.inlinetest;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

import org.inlinetest.Constant.StatementType;

import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.NodeList;
import com.github.javaparser.ast.body.VariableDeclarator;
import com.github.javaparser.ast.comments.Comment;
import com.github.javaparser.ast.expr.ArrayAccessExpr;
import com.github.javaparser.ast.expr.AssignExpr;
import com.github.javaparser.ast.expr.Expression;
import com.github.javaparser.ast.expr.FieldAccessExpr;
import com.github.javaparser.ast.expr.MethodCallExpr;
import com.github.javaparser.ast.expr.NameExpr;
import com.github.javaparser.ast.expr.SimpleName;
import com.github.javaparser.ast.type.Type;
import com.github.javaparser.ast.visitor.ModifierVisitor;
import com.github.javaparser.ast.visitor.Visitable;

public class VariableRenameVisitor extends ModifierVisitor<VariableRenameVisitor.Context> {

    static class Context {
        public Map<String, String> givenVariablesToRenamed;
        public StatementType statementType;
        public boolean mustRename;

        public Context() {
            this.givenVariablesToRenamed = new HashMap<String, String>();
            this.mustRename = false;
        }
    }

    @Override
    public Visitable visit(final AssignExpr n, final Context arg) {
        if (arg.statementType == StatementType.TARGET) {
            arg.mustRename = true;
            Expression target = (Expression) n.getTarget().accept(this, arg);
            arg.mustRename = false;
            Expression value = (Expression) n.getValue().accept(this, arg);
            Comment comment = n.getComment().map(s -> (Comment) s.accept(this, arg)).orElse(null);
            if (target == null || value == null)
                return null;
            n.setTarget(target);
            n.setValue(value);
            n.setComment(comment);
            return n;
        } else {
            return super.visit(n, arg);
        }
    }

    @Override
    public Visitable visit(final FieldAccessExpr n, final Context arg) {
        super.visit(n, arg);
        if (arg.givenVariablesToRenamed.containsKey(n.toString())) {
            return new NameExpr(arg.givenVariablesToRenamed.get(n.toString()));
        } else if (arg.mustRename) {
            String varName = n.getScope().toString() + "__" + n.getName().toString();
            arg.givenVariablesToRenamed.put(n.toString(), varName);
            return new NameExpr(varName);
        } else {
            return n;
        }
    }

    @Override
    public Visitable visit(final VariableDeclarator n, final Context arg) {
        Expression initializer = n.getInitializer().map(s -> (Expression) s.accept(this, arg)).orElse(null);
        arg.mustRename = true;
        SimpleName name = (SimpleName) n.getName().accept(this, arg);
        if (name.toString().contains(".") || (name.toString().contains("(") && name.toString().contains(")"))
                || (name.toString().contains("[") && name.toString().contains("]")
                        && name.toString().indexOf("[") < name.toString().indexOf("]"))) {
            SimpleName oldName = name;
            name = new SimpleName(renameHelper(name.toString()));
            arg.givenVariablesToRenamed.put(oldName.toString(), name.toString());
        }
        arg.mustRename = false;
        Type type = (Type) n.getType().accept(this, arg);
        Comment comment = n.getComment().map(s -> (Comment) s.accept(this, arg)).orElse(null);
        if (name == null || type == null)
            return null;
        n.setInitializer(initializer);
        n.setName(name);
        n.setType(type);
        n.setComment(comment);
        return n;
    }

    @Override
    public Visitable visit(final ArrayAccessExpr n, final Context arg) {
        Expression index = (Expression) n.getIndex().accept(this, arg);
        Expression name = (Expression) n.getName().accept(this, arg);
        if (arg.givenVariablesToRenamed.containsKey(name.toString())) {
            return new NameExpr(arg.givenVariablesToRenamed.get(name.toString()));
        } else if (arg.mustRename) {
            String varName = renameHelper(name.toString() + "__" + index.toString());
            arg.givenVariablesToRenamed.put(name.toString(), varName);
            return new NameExpr(varName);
        }
        Comment comment = n.getComment().map(s -> (Comment) s.accept(this, arg)).orElse(null);
        if (index == null || name == null)
            return null;
        n.setIndex(index);
        n.setName(name);
        n.setComment(comment);
        return n;
    }

    @Override
    public Visitable visit(final MethodCallExpr n, final Context arg) {
        if (arg.givenVariablesToRenamed.containsKey(n.toString())) {
            return new NameExpr(arg.givenVariablesToRenamed.get(n.toString()));
        } else if (arg.mustRename) {
            String varName = renameHelper(n.toString());
            arg.givenVariablesToRenamed.put(n.toString(), varName);
            return new NameExpr(varName);
        }
        NodeList<Expression> arguments = modifyList(n.getArguments(), arg);
        SimpleName name = (SimpleName) n.getName().accept(this, arg);
        Expression scope = n.getScope().map(s -> (Expression) s.accept(this, arg)).orElse(null);
        NodeList<Type> typeArguments = modifyList(n.getTypeArguments(), arg);
        Comment comment = n.getComment().map(s -> (Comment) s.accept(this, arg)).orElse(null);
        if (name == null)
            return null;
        n.setArguments(arguments);
        n.setName(name);
        n.setScope(scope);
        n.setTypeArguments(typeArguments);
        n.setComment(comment);
        return n;
    }

    private String renameHelper(String input) {
        return input.replace("*", "time").replace("+", "plus").replace("-", "minus").replace("/", "divide")
                .replace("=", "equal").replace("!", "not").replace(">", "greater").replace("<", "less")
                .replace("&", "and").replace("|", "or").replace("^", "xor").replace("%", "mod").replace("?", "question")
                .replace("(", "_").replace(")", "_").replace(" ", "").replace("[", "__").replace("]", "")
                .replace(".", "__");
    }

    private <N extends Node> NodeList<N> modifyList(NodeList<N> list, Context arg) {
        return (NodeList<N>) list.accept(this, arg);
    }

    private <N extends Node> NodeList<N> modifyList(Optional<NodeList<N>> list, Context arg) {
        return list.map(ns -> modifyList(ns, arg)).orElse(null);
    }
}
