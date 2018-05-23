import java.util.List;
import java.util.ArrayList;


public class Research{
	private String name, decription;
	private List<String> questions;
	private List<FeedBack> feedBacks;

	public Research(String name, String decription, List<String> questions, List<FeedBack> feedBacks) {
		this.name = name;
		this.decription = decription;
		this.questions = new ArrayList<String>();
		this.feedBacks = new ArrayList<FeedBack>();
	}

	public String getName() {
		return name;
	}

	public void setName(String name) {
		this.name = name;
	}

	public String getDecription() {
		return decription;
	}

	public void setDecription(String decription) {
		this.decription = decription;
	}

	public List<String> getQuestions() {
		return questions;
	}

	public void setQuestions(List<String> questions) {
		this.questions = questions;
	}

	public List<FeedBack> getFeedBacks() {
		return feedBacks;
	}

	public void setFeedBacks(List<FeedBack> feedBacks) {
		this.feedBacks = feedBacks;
	}

	
	
}
