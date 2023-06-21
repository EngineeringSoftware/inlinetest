package org.inlinetest;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Deque;
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.function.Function;
import com.github.javaparser.StaticJavaParser;
import com.github.javaparser.ast.body.TypeDeclaration;
import com.github.javaparser.ast.type.ClassOrInterfaceType;
import com.github.javaparser.ast.type.Type;
import com.github.javaparser.resolution.UnsolvedSymbolException;
import com.github.javaparser.resolution.declarations.ResolvedReferenceTypeDeclaration;
import com.github.javaparser.resolution.types.ResolvedReferenceType;
import com.github.javaparser.resolution.types.ResolvedType;
import com.github.javaparser.symbolsolver.JavaSymbolSolver;
import com.github.javaparser.symbolsolver.resolution.typesolvers.CombinedTypeSolver;
import com.github.javaparser.symbolsolver.resolution.typesolvers.JarTypeSolver;
import com.github.javaparser.symbolsolver.resolution.typesolvers.JavaParserTypeSolver;
import com.github.javaparser.symbolsolver.resolution.typesolvers.ReflectionTypeSolver;

public class TypeResolver {

    public static CombinedTypeSolver sTypeSolver = new CombinedTypeSolver();
    public static JavaSymbolSolver sSymbolResolver = new JavaSymbolSolver(sTypeSolver);

    public static void setup() {
        // add rt.jar to the resolver
        try {
            sTypeSolver.add(new ReflectionTypeSolver());
            sTypeSolver.add(
                    new JarTypeSolver(Paths.get(System.getProperty("java.home"), "lib", "rt.jar")));

            if (Util.depClassPaths != null) {
                // add all jars in the classpaths to the resolver
                for (String path : Util.depClassPaths.split(File.pathSeparator)) {
                    if (path.endsWith(".jar") || path.endsWith(".zip") || path.endsWith(".war")) {
                        // use JarTypeSolver for jar files if possible (which does not require loading
                        // class)
                        sTypeSolver.add(new JarTypeSolver(Paths.get(path)));
                    }
                }
            }
            if (Util.appSrcPath != null) {
                // add all source paths to the solver
                for (String path : Util.appSrcPath.split(File.pathSeparator)) {
                    if (Paths.get(path).toFile().isDirectory()) {
                        sTypeSolver.add(new JavaParserTypeSolver(path));
                    } else {
                        // assume it is a file
                        if (Util.appSrcPath.contains("src/main/java")) {
                            sTypeSolver
                                    .add(new JavaParserTypeSolver(Util.appSrcPath.split("src")[0] + "src/main/java"));
                        } else {
                            sTypeSolver
                                    .add(new JavaParserTypeSolver(Paths.get(Util.appSrcPath).getParent().toString()));
                        }
                    }
                }
            }
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        StaticJavaParser.getConfiguration().setSymbolResolver(TypeResolver.sSymbolResolver);
    }

    public static String resolveType(Type type) {
        return resolveType(type, null);
    }

    /**
     * Resolve and erase the type of a type node, handling some corner cases: type
     * parameters (need typeParams), and inner class of parent class.
     */
    public static String resolveType(Type type, Map<String, String> typeParams) {
        try {
            // handle references to type parameters
            if (type.isClassOrInterfaceType()) {
                ClassOrInterfaceType classOrInterfaceType = type.asClassOrInterfaceType();
                String name = classOrInterfaceType.getNameAsString();
                if (typeParams != null && typeParams.containsKey(name)) {
                    return typeParams.get(name);
                }

                return normalizeType(classOrInterfaceType.resolve());
            }

            // try to resolve with normal resolver
            return normalizeType(type.resolve());
        } catch (UnsolvedSymbolException e) {
            // try to resolve from containing class's parent class
            Optional<TypeDeclaration> containingClass = type.findAncestor(TypeDeclaration.class);
            while (true) {
                if (!containingClass.isPresent()) {
                    break;
                }

                // try to resolve from this containing class's parent class
                for (ResolvedReferenceType t : containingClass.get().resolve()
                        .getAllAncestors(bfsSafeFunc)) {
                    try {
                        return normalizeType(
                                sTypeSolver.solveType(t.getQualifiedName() + "." + type.asString()));
                    } catch (RuntimeException | NoClassDefFoundError e2) {
                        // ignore
                    }
                }

                // try to go one level up
                containingClass = containingClass.get().findAncestor(TypeDeclaration.class);
            }

            // AllCollectors.warning("Unsolved symbol: " + type.asString() + ": " +
            // e.toString());
            // throw e;
        } catch (UnsupportedOperationException | IllegalArgumentException | NoClassDefFoundError
                | TypeNotPresentException | IncompatibleClassChangeError | UnsupportedClassVersionError
                | SecurityException e) {
            // this type is unsolved because of:
            // UnsupportedOperationException: unknown type parameter
            // IllegalArgumentException: inferred lambda parameter type
            // NoClassDefFoundError/TypeNotPresentException/IncompatibleClassChangeError/UnsupportedClassVersionError/SecurityException:
            // JavaParser screw up with class loading
            // AllCollectors.warning("Unsolved symbol: " + type.asString() + ": " +
            // e.toString());
            // throw e;
        }

        // fallback to the literal type name
        return type.asString();
    }

    static Function<ResolvedReferenceTypeDeclaration, List<ResolvedReferenceType>> bfsSafeFunc = (rrtd) -> {
        Set<ResolvedReferenceType> ancestors = new HashSet<>();
        // We want to avoid infinite recursion in case of Object having Object as
        // ancestor
        if (!rrtd.isJavaLangObject()) {
            // init direct ancestors
            Deque<ResolvedReferenceType> queuedAncestors = new LinkedList<ResolvedReferenceType>(
                    rrtd.getAncestors(true));
            ancestors.addAll(queuedAncestors);
            while (!queuedAncestors.isEmpty()) {
                ResolvedReferenceType queuedAncestor = queuedAncestors.removeFirst();
                try {
                    queuedAncestor.getTypeDeclaration().ifPresent(
                            rtd -> new LinkedHashSet<ResolvedReferenceType>(
                                    queuedAncestor.getDirectAncestors()).stream().forEach(ancestor -> {
                                        // add this ancestor to the queue (for a deferred search)
                                        queuedAncestors.add(ancestor);
                                        // add this ancestor to the list of ancestors
                                        ancestors.add(ancestor);
                                    }));
                } catch (RuntimeException | NoClassDefFoundError e) {
                    // ignore
                }
            }
        }
        return new ArrayList<>(ancestors);
    };

    public static String normalizeType(ResolvedType t) {
        if (t.isArray()) {
            return normalizeType(t.asArrayType().getComponentType()) + "[]";
        } else if (t.isReferenceType()) {
            return normalizeType(t.asReferenceType().getTypeDeclaration().get());
        } else {
            // TODO: it's either a primitive/null type, or something we don't expect here
            return t.describe();
        }
    }

    public static String normalizeType(ResolvedReferenceTypeDeclaration t) {
        return t.getPackageName() + "." + t.getClassName().replace('.', '$');
    }
}