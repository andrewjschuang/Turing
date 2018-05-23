import java.util.TreeSet;
import java.util.SortedSet;


public class Project implements Historic, Permited{
	private static int globalCount = 0;
	private int id;
    private String name, description;
    private TreeSet<Task> tasks;
    private TreeSet<Meeting> toMeet;
    private TreeSet<Research> research;
	
	public Project (String name, String description) {
		this.name = name;
		this.description = description;
		this.id = globalCount;
		this.tasks = new TreeSet<Task>();
		this.toMeet = new TreeSet<Meeting>();
		this.research = new TreeSet<Research>();
		globalCount ++;
		
	}
	
	public void createTask() {
		Task t = new Task();
		this.tasks.add(t);
	}

	public int getId() {
		return id;
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getDescription() {
		return description;
	}

	public void setDescription(String description) {
		this.description = description;
	}

	public TreeSet<Task> getTasks() {
		return tasks;
	}

	public void setTasks(TreeSet<Task> tasks) {
		this.tasks = tasks;
	}

	public TreeSet<Meeting> getToMeet() {
		return toMeet;
	}

	public void setToMeet(TreeSet<Meeting> toMeet) {
		this.toMeet = toMeet;
	}

	public TreeSet<Research> getResearch() {
		return research;
	}

	public void setResearch(TreeSet<Research> research) {
		this.research = research;
	}
	
	
}
