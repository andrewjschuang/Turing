import java.util.Date;
import java.util.SortedSet;

public class Version implements Historic{
    private String name, description;
    private SortedSet<Attachment> attachments;
}
