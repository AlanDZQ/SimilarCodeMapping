import JavaExtractor.Common.Common;
import JavaExtractor.Common.MethodContent;
import JavaExtractor.ExtractFeaturesTask;
import JavaExtractor.FeaturesEntities.ProgramFeatures;
import JavaExtractor.Visitors.FunctionVisitor;
import com.github.javaparser.JavaParser;
import com.github.javaparser.ParseException;
import com.github.javaparser.ParseProblemException;
import com.github.javaparser.ast.CompilationUnit;
import com.github.javaparser.ast.Node;
import com.github.javaparser.ast.body.ClassOrInterfaceDeclaration;
import com.github.javaparser.ast.type.ClassOrInterfaceType;
import org.apache.commons.io.FileUtils;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.List;
import java.util.concurrent.Executors;
import java.util.concurrent.ThreadPoolExecutor;

public class Test {

    public static void main(String[] args) throws IOException {
//        exractMethods();
//        generateSimMethod();
        generateDiffMethod();


//        try {
//            Files.walk(Paths.get("/Users/apple/Desktop/test")).filter(Files::isRegularFile)
//                    .filter(p -> p.toString().toLowerCase().endsWith(".java")).forEach(f -> {
//                String code = null;
//                try {
//                    code = new String(Files.readAllBytes(f));
////                    System.out.println(f);
//                } catch (IOException e) {
//                    e.printStackTrace();
//                    code = Common.EmptyString;
//                }
//                try {
//                    CompilationUnit compilationUnit = parseFileWithRetries(code);
//                    System.out.println(f);
//                    FunctionVisitor functionVisitor = new FunctionVisitor();
//                    functionVisitor.visit(compilationUnit, null);
//                    ArrayList<MethodContent> methods = functionVisitor.getMethodContents();
//                    System.out.println(methods.size());
////                    for (MethodContent n : methods){
////                        System.out.println("name: "+n.getName() + "\n");
////                        System.out.println("body: "+n.getBody() + "\n");
////                        System.out.println("length: "+n.getLength() + "\n");
////                    }
//
//                } catch (IOException e) {
//                    e.printStackTrace();
//                }
//
//            });
//        } catch (IOException e) {
//            e.printStackTrace();
//            return;
//        }
    }

    private static void generateDiffMethod(){
        List<File> files = new ArrayList<>();
        getFile("sample", files);
        for (File f1 : files) {
            File f2 = files.get((int)(Math.random()*files.size()));
            if (f1 == f2) continue;
            String code1 = null;
            String code2 = null;
            try {
                code1 = new String(Files.readAllBytes(f1.toPath()));
                code2 = new String(Files.readAllBytes(f2.toPath()));
            } catch (IOException e) {
                e.printStackTrace();
            }

            try {
                CompilationUnit compilationUnit1 = parseFileWithRetries(code1);
                FunctionVisitor functionVisitor1 = new FunctionVisitor();
                functionVisitor1.visit(compilationUnit1, null);
                ArrayList<MethodContent> methods1 = functionVisitor1.getMethodContents();
                
                CompilationUnit compilationUnit2 = parseFileWithRetries(code2);
                FunctionVisitor functionVisitor2 = new FunctionVisitor();
                functionVisitor2.visit(compilationUnit2, null);
                ArrayList<MethodContent> methods2 = functionVisitor2.getMethodContents();

                int index = 0;
                for (int i = 0; i < methods1.size(); i++) {
                    for (int j = 0; j < methods2.size(); j++) {
                        String str = "Test_Neg/" + f1.toString().substring(0,f1.toString().length()-5) + index + ".java";
                        createFile(str);
                        FileWriter writer = new FileWriter(str,true);
                        writer.write(methods1.get(i).getBody() + "\n");
                        writer.write(methods2.get(j).getBody() + "\n");
                        writer.close();
                        index++;
                    }
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }


    private static void generateSimMethod() {
        try {
            Files.walk(Paths.get("sample")).filter(Files::isRegularFile)
                    .filter(p -> p.toString().toLowerCase().endsWith(".java")).forEach(f -> {
                String code = null;
                try {
                    code = new String(Files.readAllBytes(f));
                } catch (IOException e) {
                    e.printStackTrace();
                    code = Common.EmptyString;
                }
                System.out.println(f.toString());
                try {
                    CompilationUnit compilationUnit = parseFileWithRetries(code);
                    FunctionVisitor functionVisitor = new FunctionVisitor();
                    functionVisitor.visit(compilationUnit, null);
                    ArrayList<MethodContent> methods = functionVisitor.getMethodContents();

                    int index = 0;
                    for (int i = 0; i < methods.size(); i++) {
                        for (int j = 0; j < methods.size(); j++) {
                            long m = methods.get(i).getLength();
                            long n = methods.get(j).getLength();
                            if (i != j && !methods.get(i).getBody().equals(methods.get(j).getBody()) &&
                                    m > 1 && n > 1 && Math.min(m, n) * 3 >= Math.max(m, n)) {

                                String str = "Test/" + f.toString().substring(0,f.toString().length()-5) + index + ".java";
                                createFile(str);
                                FileWriter writer = new FileWriter(str,true);
                                writer.write(methods.get(i).getBody() + "\n");
                                writer.write(methods.get(j).getBody() + "\n");
                                writer.close();
                                index++;
                            }
                        }
                    }

                } catch (IOException e) {
                    e.printStackTrace();
                }

            });
        } catch (IOException e) {
            e.printStackTrace();
            return;
        }
    }

    private static void exractMethods() {
        ThreadPoolExecutor executor = (ThreadPoolExecutor) Executors.newFixedThreadPool(64);
        LinkedList<ExtractFeaturesTask> tasks = new LinkedList<>();
        try {
            Files.walk(Paths.get("/Users/apple/Desktop/J2EE/")).filter(Files::isRegularFile)
                    .filter(p -> p.toString().toLowerCase().endsWith(".java")).forEach(f -> {
                String code = null;
                try {
                    code = new String(Files.readAllBytes(f));
//                    System.out.println(f);
                } catch (IOException e) {
                    e.printStackTrace();
                    code = Common.EmptyString;
                }
                try {
                    CompilationUnit compilationUnit = parseFileWithRetries(code);
//                    FileWriter writer=new FileWriter("wildfly_interface.txt", true);
//                    System.out.println(f);
//                    FunctionVisitor functionVisitor = new FunctionVisitor();
//                    functionVisitor.visit(compilationUnit, null);
//                    ArrayList<MethodContent> methods = functionVisitor.getMethodContents();
//                    for (MethodContent n : methods){
////                        writer.write(n.getName() + "\n");
//                        System.out.println("name: "+n.getName() + "\n");
//                        System.out.println("body: "+n.getBody() + "\n");
//                        System.out.println("length: "+n.getLength() + "\n");
//                    }
                    for (int i = 0; i < compilationUnit.getTypes().size(); i++) {
                        if (compilationUnit.getTypes().get(i)
                                instanceof ClassOrInterfaceDeclaration &&
                                !((ClassOrInterfaceDeclaration) compilationUnit.getTypes().get(i)).isInterface()) {
                            List<ClassOrInterfaceType> list = ((ClassOrInterfaceDeclaration) compilationUnit.getTypes().get(i)).getImplements();

                            for (ClassOrInterfaceType x : list) {
//                                writer.write(compilationUnit.getTypes().get(i).toString() + "\n");
                                FunctionVisitor functionVisitor = new FunctionVisitor();
                                functionVisitor.visit(compilationUnit, null);
                                ArrayList<MethodContent> methods = functionVisitor.getMethodContents();
                                for (MethodContent n : methods) {
                                    if (n.getLength() < 3) continue;
                                    String fileName = "Interface/" + x + "/" + n.getName() + ".java";
                                    createFile(fileName);
                                    FileWriter writer = new FileWriter(fileName, true);
                                    writer.write(n.getBody() + "\n" + "\n");
                                    writer.close();
                                }
                            }
                        }
                    }


//                    FunctionVisitor functionVisitor = new FunctionVisitor();
//                    functionVisitor.visit(compilationUnit, null);
//                    ArrayList<MethodContent> methods = functionVisitor.getMethodContents();
//                    FileWriter writer=new FileWriter("x.txt", true);
//                    for (MethodContent n : methods){
//                        writer.write(n.getName() + "\n");
////                        System.out.println(n.getBody() + "\n" + "\n");
//                    }
//                    writer.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }

            });
        } catch (IOException e) {
            e.printStackTrace();
            return;
        }
    }


    private static CompilationUnit parseFileWithRetries(String code) throws IOException {
        final String classPrefix = "public class Test {";
        final String classSuffix = "}";
        final String methodPrefix = "SomeUnknownReturnType f() {";
        final String methodSuffix = "return noSuchReturnValue; }";

        String originalContent = code;
        String content = originalContent;
        CompilationUnit parsed = null;
        try {
            parsed = JavaParser.parse(content);
        } catch (ParseProblemException e1) {
            // Wrap with a class and method
            try {
                content = classPrefix + methodPrefix + originalContent + methodSuffix + classSuffix;
                parsed = JavaParser.parse(content);
            } catch (ParseProblemException e2) {
                // Wrap with a class only
                content = classPrefix + originalContent + classSuffix;
//                System.out.println(code);
                parsed = JavaParser.parse(content);
            }
        }
        return parsed;
    }


    public static boolean createFile(String destFileName) {
        File file = new File(destFileName);
        if (file.exists()) {
            System.out.println("creat file: " + destFileName + " fail, the file is already there");
            return false;
        }
        if (destFileName.endsWith(File.separator)) {
            return false;
        }
        if (!file.getParentFile().exists()) {
            if (!file.getParentFile().mkdirs()) {
                return false;
            }
        }
        try {
            if (file.createNewFile()) {
                return true;
            } else {
                return false;
            }
        } catch (IOException e) {
            e.printStackTrace();
            return false;
        }
    }

    private static void copyFileUsingApacheCommonsIO(File source, File dest)
            throws IOException {
        FileUtils.copyFile(source, dest);
    }

    private static void getFile(String path, List<File> res){
        // get file list where the path has
        File file = new File(path);
        // get the folder list
        File[] array = file.listFiles();
        for (File anArray : array) {
            if (anArray.isFile() && !anArray.getName().equals(".DS_Store")) {
                res.add(anArray);
            } else if (anArray.isDirectory()) {
                getFile(anArray.getPath(), res);
            }
        }
    }
}