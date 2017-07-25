public class User {
    private String userName;
    private int followers;
    private int retweet_count;
    private int mentionedCount;
    private int followerRank;
    private int retweetRank;
    private int mentionedRank;
    private double spearmanCorrelationCoefficient;
    public int getRetweet_count() {
        return retweet_count;
    }
    public void setRetweet_count(final int retweet_count) {
        this.retweet_count = retweet_count;
    }
    public int getFollowers() {
        return followers;
    }
    public void setFollowers(final int followers) {
        this.followers = followers;
    }
    public int getFollowerRank() {
        return followerRank;
    }
    public void setFollowerRank(final int followerRank) {
        this.followerRank = followerRank;
    }
    public int getRetweetRank() {
        return retweetRank;
    }
    public void setRetweetRank(final int retweetRank) {
        this.retweetRank = retweetRank;
    }
    public int getMentionedRank() {
        return mentionedRank;
    }
    public void setMentionedRank(final int mentionedRank) {
        this.mentionedRank = mentionedRank;
    }
    public String getUserName() {
        return userName;
    }
    public void setUserName(final String userName) {
        this.userName = userName;
    }
    public int incrementMentionedCount() {
        return mentionedCount++;
    }
    public int getMentionedCount() {
        return mentionedCount;
    }
    public double getSpearmanCorrelationCoefficient() {
        return spearmanCorrelationCoefficient;
    }
    public void setSpearmanCorrelationCoefficient(final double spearmanCorrelationCoefficient) {
        this.spearmanCorrelationCoefficient = spearmanCorrelationCoefficient;
    }
    @Override
    public String toString() {
        return "User [userName=" + userName + ", followers=" + followers + ", retweet_count=" + retweet_count + ", mentionedCount=" + mentionedCount
                + ", followerRank=" + followerRank + ", retweetRank=" + retweetRank + ", mentionedRank=" + mentionedRank
                + ", spearmanCorrelationCoefficient=" + spearmanCorrelationCoefficient + "]";
    }
}
