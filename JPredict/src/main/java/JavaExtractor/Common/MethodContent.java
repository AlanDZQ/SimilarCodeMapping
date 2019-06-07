package JavaExtractor.Common;

import java.util.ArrayList;
import com.github.javaparser.ast.Node;

public class MethodContent {
	private ArrayList<Node> leaves;
	private String name;
	private long length;
	private String body;

	public MethodContent(ArrayList<Node> leaves, String name, long length, String body) {
		this.leaves = leaves;
		this.name = name;
		this.length = length;
		this.body = body;
	}

	public ArrayList<Node> getLeaves() {
		return leaves;
	}

	public String getName() {
		return name;
	}

	public long getLength() {
		return length;
	}

	public String getBody() {
		return body;
	}

}
