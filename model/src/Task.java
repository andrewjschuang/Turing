import java.util.Date;
import java.util.SortedMap;
import java.util.SortedSet;

public class Task implements Permited, Historic{
	private static int globalCount = 0;
    private int id;
    private String name;
    private String description;
    private Date finishes;
    private SortedSet<Task> subTasks;
    private SortedSet<User> watching;
    private SortedSet<Attachment> addons;
    private boolean isDone;
    
    public void Task() {
    
    }
    
    public void Task(String name, String description) {
    	this.id = globalCount;
		globalCount ++;
		this.name = name;
		this.description = description;
		this.isDone = false;
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

	public Date getFinishes() {
		return finishes;
	}

	public void setFinishes(Date finishes) {
		this.finishes = finishes;
	}

	public SortedSet<Task> getSubTasks() {
		return subTasks;
	}

	public void setSubTasks(SortedSet<Task> subTasks) {
		this.subTasks = subTasks;
	}

	public SortedSet<User> getWatching() {
		return watching;
	}

	public void setWatching(SortedSet<User> watching) {
		this.watching = watching;
	}

	public SortedSet<Attachment> getAddons() {
		return addons;
	}

	public void setAddons(SortedSet<Attachment> addons) {
		this.addons = addons;
	}

	public boolean isDone() {
		return isDone;
	}

	public void setDone(boolean isDone) {
		this.isDone = isDone;
	}
    
    
    
}
