import java.util.SortedSet;

public class Project implements Historic, Permited{
    private String name, desctiption;
    private SortedSet<Task> tasks;
    private SortedSet<Meeting> toMeet;
    private SortedSet<Research> research;
}
