import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.io.UnsupportedEncodingException;
import java.io.Writer;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.TimeZone;
import java.util.TreeMap;

public class NewRetweetsEvaluator {
    static List<File> listOfFiles = new ArrayList<File>();
    static Map<String, Set<String>> connectionDetails = new TreeMap<String, Set<String>>();
    static Date startDate;
    static Date endDate;

    static SimpleDateFormat targetFormatFinal = new SimpleDateFormat("dd/MM/yyyy");

    public static void main(final String[] args) throws Exception {
        final String inputFolderName = args[0];
        if (inputFolderName == null || inputFolderName.trim().isEmpty()) {
            throw new Exception("Please enter valid input folder name.");
        }
        if (args[1] == null || args[1].trim().isEmpty()) {
            throw new Exception("Please enter valid start date.");
        }
        targetFormatFinal.setTimeZone(TimeZone.getTimeZone("UTC"));
        startDate = targetFormatFinal.parse(args[1]);

        if (args[2] == null || args[2].trim().isEmpty()) {
            throw new Exception("Please enter valid end date.");
        }
        endDate = targetFormatFinal.parse(args[2]);

        final String outputFileName = args[3];
        if (outputFileName == null || outputFileName.trim().isEmpty()) {
            throw new Exception("Please enter valid output file name.");
        }

        System.out.println("Starting loading of all files....");

        loadAllFiles(inputFolderName);

        System.out.println("Loading of all files is complete.");

        System.out.println("Started processing all files....");

        listOfFiles.stream().forEach(file -> {
            try {
                processFile(file);
            } catch (final IOException | ParseException e) {
                System.out.println("Exception occured processing file: " + file.getAbsolutePath() + ". Exception Message : " + e.getMessage());
            }
        });

        System.out.println("Processing all files is complete.");

        System.out.println("Started writing output to file....");

        writeToFile(outputFileName);

        System.out.println("Writing output to file is complete.");

    }

    private static void processFile(final File file) throws FileNotFoundException, IOException, ParseException {
        System.out.println("Started processing file : " + file.getAbsolutePath());
        try (final BufferedReader br = new BufferedReader(new FileReader(file))) {
            String line = null;
            final SimpleDateFormat targetFormatLocal = new SimpleDateFormat("E MMM dd HH:mm:ss Z yyyy");
            targetFormatLocal.setTimeZone(TimeZone.getTimeZone("UTC"));

            while ((line = br.readLine()) != null) {
                final String[] tweetDetails = line.trim().split("\t");
                if (tweetDetails != null && tweetDetails.length == 3) {
                    final String tweet = tweetDetails[0];
                    if (tweet != null && !tweet.isEmpty()) {
                        final String userInfo = tweetDetails[1];
                        if (userInfo != null && !userInfo.isEmpty()) {
                            final String[] userInfoArray = userInfo.trim().split(",");
                            if (userInfoArray != null && userInfoArray.length == 2) {
                                final String userName = userInfoArray[1];
                                if (userName != null && !userName.equalsIgnoreCase("N/A")) {
                                    final String userdate = userInfoArray[0];
                                    if (userdate != null && !userdate.equalsIgnoreCase("N/A")) {
                                        final Date userRetweetDateOriginal = targetFormatLocal.parse(userdate.trim());
                                        final Date userRetweetDate = targetFormatFinal.parse(targetFormatFinal.format(userRetweetDateOriginal));
                                        if (userRetweetDate != null && withinDateRange(userRetweetDate)) {
                                            final String ownerInfo = tweetDetails[2];
                                            if (ownerInfo != null && !ownerInfo.isEmpty()) {
                                                final String[] ownerInfoArray = ownerInfo.trim().split(",");
                                                if (ownerInfoArray != null && ownerInfoArray.length == 2) {
                                                    final String ownerName = ownerInfoArray[0];
                                                    if (ownerName != null && !ownerName.equalsIgnoreCase("N/A")) {
                                                        final String ownerdate = ownerInfoArray[1];
                                                        if (ownerdate != null && !ownerdate.equalsIgnoreCase("N/A")) {
                                                            final Date ownerRetweetDateOriginal = new SimpleDateFormat("E MMM dd HH:mm:ss z yyyy")
                                                                    .parse(ownerdate.trim());
                                                            final Date ownerRetweetDate = targetFormatFinal
                                                                    .parse(targetFormatFinal.format(ownerRetweetDateOriginal));
                                                            if (ownerRetweetDate != null) {
                                                                if (isConnectionDateAvailable(targetFormatFinal.format(userRetweetDate))) {
                                                                    addOrUpdateConnection(false, targetFormatFinal.format(userRetweetDate), userName,
                                                                            ownerName);
                                                                } else {
                                                                    addOrUpdateConnection(true, targetFormatFinal.format(userRetweetDate), userName,
                                                                            ownerName);
                                                                }
                                                            }
                                                        }

                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        System.out.println("Completed processing file : " + file.getAbsolutePath());
    }

    private static void addOrUpdateConnection(final boolean isNewConnection, final String connectionDate, final String name1,
            final String name2) {
        if (isNewConnection) {
            final String userOwnerName = new StringBuilder(name1.trim()).append("->").append(name2.trim()).toString();
            final Set<String> userOwnernames = new HashSet<String>();
            userOwnernames.add(userOwnerName);

            connectionDetails.put(connectionDate, userOwnernames);
        } else {
            final Set<String> userOwnernames = connectionDetails.get(connectionDate);
            final String userOwnerName = new StringBuilder(name1.trim()).append("->").append(name2.trim()).toString();
            userOwnernames.add(userOwnerName);
        }
    }

    private static boolean isConnectionDateAvailable(final String date) {
        return connectionDetails.containsKey(date);
    }

    private static boolean withinDateRange(final Date date) {
        return (date.after(startDate) && date.before(endDate));
    }

    private static void loadAllFiles(final String folderName) {
        final File folder = new File(folderName);
        if (folder.isFile()) {
            listOfFiles.add(folder);
        } else if (folder.isDirectory()) {
            final File[] listOfLocalFiles = folder.listFiles();
            if (listOfLocalFiles != null) {
                for (int i = 0; i < listOfLocalFiles.length; i++) {
                    final File file = listOfLocalFiles[i];
                    if (file.isDirectory()) {
                        loadAllFiles(file.getAbsolutePath());
                    } else if (file.isFile()) {
                        listOfFiles.add(file);
                    }
                }
            }
        }
    }

    private static void writeToFile(final String outputFileName) throws UnsupportedEncodingException, FileNotFoundException, IOException {
        try (final Writer writer = new BufferedWriter(new OutputStreamWriter(
                new FileOutputStream(outputFileName), "utf-8"))) {
            writer.write("Date\t\t\t" + "Connections\t\t\t" + "Count");
            writer.write("\n");
            for (final String date : connectionDetails.keySet()) {
                final Set<String> connections = connectionDetails.get(date);
                writer.write(date + "\t\t\t");
                connections.stream().forEach(connection -> {
                    try {
                        writer.write(connection + ", ");
                    } catch (final IOException e) {
                        System.out.println("Exception occured writing connections to file.");
                    }
                });
                writer.write("\t\t\t" + connections.size());
                writer.write("\n\n");
                writer.flush();
            }
        }
    }
}
