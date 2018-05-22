import java.util.Date;
import java.util.SortedSet;

public class Meeting implements Permited, Historic{
    private String name, description;
    private Date starTime, endTime, finishedTime;
    private SortedSet<Task> toDecide;
    private SortedSet<User> invited, shownedUp;
}
