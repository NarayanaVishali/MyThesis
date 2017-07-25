import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.text.ParseException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
public class Twitter {
    public static Map<String, User> users = new HashMap<String, User>();
    public static void main(final String[] args) throws IOException, ParseException {
        final File inputFile = new File(args[0]);
        final File outputFile = new File(args[1]);
        final BufferedReader br = new BufferedReader(new FileReader(inputFile));
        String line = null;
        System.out.println("Started processing tweets file.");
        while ((line = br.readLine()) != null) {
            final String[] inputArray = line.trim().split(",");
            final String name = inputArray[0].trim();
            try {
                if (users.containsKey(name)) {
                    final User user = users.get(name);
                    final int currentFollowers = Integer.parseInt(inputArray[1].trim());
                    if (user.getFollowers() < currentFollowers) {
                        user.setFollowers(currentFollowers);
                    }
                    user.setRetweet_count(Integer.parseInt(inputArray[2].trim()) + user.getRetweet_count());
                } else {
                    final User user = new User();
                    user.setUserName(name);
                    user.setFollowers(Integer.parseInt(inputArray[1].trim()));
                    user.setRetweet_count(Integer.parseInt(inputArray[2].trim()));
                    users.put(name, user);
                }
            } catch (final Exception e) {
            }
            final String mentionedName = inputArray[3].trim();
            if (users.containsKey(mentionedName)) {
                users.get(mentionedName).incrementMentionedCount();
            } else {
                users.put(mentionedName, createDummyUser(mentionedName));
            }
        }
        br.close();
        final List<User> listOfUsers = new ArrayList<User>(users.values());
        // get ranks based on Follwers
        System.out.println("Getting ranks based on Follwers.");
        getRanksBasedOnFollwers(listOfUsers);
        // get ranks based on Retweet count
        System.out.println("Getting ranks based on Retweet Count.");
        getRanksBasedOnRetweetCount(listOfUsers);
        // get ranks based on mentioned count
        System.out.println("Getting ranks based on Mentioned Count.");
        getRanksBasedOnMentionedCount(listOfUsers);
        System.out.println("Started wrting to output file.");
        writeToFile(outputFile, listOfUsers);
        System.out.println("Succesfully calculated SpearmanCorrelationCoefficient and wrote to file.");
    }
    public static void getRanksBasedOnMentionedCount(final List<User> listOfUsers) {
        Collections.sort(listOfUsers, new Comparator<User>() {
            @Override
            public int compare(final User u1, final User u2) {
                return u2.getMentionedCount() - u1.getMentionedCount();
            }
        });
        for (int i = 0; i < listOfUsers.size(); i++) {
            final User listUser = listOfUsers.get(i);
            users.get(listUser.getUserName()).setMentionedRank(i + 1);
        }
    }
    public static void getRanksBasedOnRetweetCount(final List<User> listOfUsers) {
        Collections.sort(listOfUsers, new Comparator<User>() {
            @Override
            public int compare(final User u1, final User u2) {
                return u2.getRetweet_count() - u1.getRetweet_count();
            }
        });
        for (int i = 0; i < listOfUsers.size(); i++) {
            final User listUser = listOfUsers.get(i);
            users.get(listUser.getUserName()).setRetweetRank(i + 1);
        }
    }
    public static void getRanksBasedOnFollwers(final List<User> listOfUsers) {
        Collections.sort(listOfUsers, new Comparator<User>() {
            @Override
            public int compare(final User u1, final User u2) {
                return u2.getFollowers() - u1.getFollowers();
            }
        });
        for (int i = 0; i < listOfUsers.size(); i++) {
            final User listUser = listOfUsers.get(i);
            users.get(listUser.getUserName()).setFollowerRank(i + 1);
        }
    }
    public static void writeToFile(final File outputFile, final List<User> listOfUsers) throws IOException {
        final int usersSize = listOfUsers.size();
        final FileWriter fileWriter = new FileWriter(outputFile);
        fileWriter.append("UserName,Followers,FollowersRank,Retweets,RetweetsRank,MentionedCount,MentionedRank,SpearmanCorrelationCoefficient");
        fileWriter.append("\n");
        for (int i = 0; i < usersSize; i++) {
            final User user = users.get(listOfUsers.get(i).getUserName());
            user.setSpearmanCorrelationCoefficient(getSpearmanCorrelationCoefficient(user, usersSize));
            fileWriter.append(user.getUserName());
            fileWriter.append(",");
            fileWriter.append(String.valueOf(user.getFollowers()));
            fileWriter.append(",");
            fileWriter.append(String.valueOf(user.getFollowerRank()));
            fileWriter.append(",");
            fileWriter.append(String.valueOf(user.getRetweet_count()));
            fileWriter.append(",");
            fileWriter.append(String.valueOf(user.getRetweetRank()));
            fileWriter.append(",");
            fileWriter.append(String.valueOf(user.getMentionedCount()));
            fileWriter.append(",");
            fileWriter.append(String.valueOf(user.getMentionedRank()));
            fileWriter.append(",");
            fileWriter.append(String.valueOf(user.getSpearmanCorrelationCoefficient()));
            fileWriter.append("\n");
        }
        fileWriter.flush();
        fileWriter.close();
    }
    public static User createDummyUser(final String name) {
        final User user = new User();
        user.setUserName(name);
        user.incrementMentionedCount();
        return user;
    }
    public static double getSpearmanCorrelationCoefficient(final User user, final int usersSize) {
        final double sum = 6 * (Math.pow(user.getFollowerRank() - user.getRetweetRank(), 2) +
                Math.pow(user.getRetweetRank() - user.getMentionedRank(), 2) +
                Math.pow(user.getFollowerRank() - user.getMentionedRank(), 2));
        final double divideValue = Math.pow(usersSize, 3) - usersSize;
        return 1 - (sum / divideValue);
    }
}
