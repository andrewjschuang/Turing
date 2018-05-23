import java.util.SortedSet;

public class Project implements Historic, Permited{
    private String name, description;
    private SortedSet<Task> tasks;
    private SortedSet<Meeting> toMeet;
    private SortedSet<Research> research;
	
	public Project (String name, String description, SortedSet<Task> tasks, SortedSet<Meeting> toMeet, SortedSet<Research> research) {
		this.name = name;
		this.description = description;
		this.tasks = tasks;
		this.toMeet = toMeet;
		this.research = research;
	}
}
