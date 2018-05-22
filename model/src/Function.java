import java.util.Date;
import java.util.SortedSet;

public class Function implements Historic{
    private String name, description;
    private SortedSet<Task> related;
    private SortedSet<Version> versions;
}

