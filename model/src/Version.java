import java.util.Date;
import java.util.SortedSet;

public class Version implements Historic{
    private String name, description;
    private SortedSet<Attachment> attachments;
    
    
	public Version(String name, String description, SortedSet<Attachment> attachments) {
		this.name = name;
		this.description = description;
		this.attachments = attachments;
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


	public SortedSet<Attachment> getAttachments() {
		return attachments;
	}


	public void setAttachments(SortedSet<Attachment> attachments) {
		this.attachments = attachments;
	}
	
	
    
    
}
