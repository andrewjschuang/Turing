import java.util.Date;
import java.util.SortedMap;
import java.util.SortedSet;

public class Task implements Permited, Historic{
    private int id;
    private String name;
    private String description;
    private Date finishes;
    private SortedSet<Task> subTasks;
    private SortedSet<User> watching;
    private SortedSet<Attachment> addons;
    private boolean isDone;
}
