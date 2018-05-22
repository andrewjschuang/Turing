import java.util.SortedSet;

public class User implements Historic{
    private int id;
    private String name;
    private SortedSet<Task> todo;
    private SortedSet<Permited> read, write, share;
    private SortedSet<Project> projects;
}
