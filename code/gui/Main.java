package gui;
import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextArea;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;
import org.apache.http.client.methods.CloseableHttpResponse;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;

import java.io.IOException;
import java.util.Random;

public class Main extends Application {

    @Override
    public void start(Stage primaryStage) {
        // Text area for input
        TextArea textInput = new TextArea();
        textInput.setPromptText("Enter your text here...");
        textInput.setWrapText(true);

        // Button to check for propaganda
        Button checkButton = new Button("Check for Propaganda");
        checkButton.getStyleClass().add("check-button");


        // GridPane for solver results
        GridPane resultsGrid = new GridPane();
        resultsGrid.setPadding(new Insets(10));
        resultsGrid.setHgap(10);
        resultsGrid.setVgap(10);

        // Create labels for solver names and results
        Label[] solverNames = {
                new Label("Risk Words Evaluator"),
                new Label("Emotional Evaluator"),
                new Label("Positive Generalities Evaluator")
        };
        Label[] solverResults = new Label[5];
        for (int i = 0; i < 3; i++) {
            solverResults[i] = new Label("0%");
            resultsGrid.add(solverNames[i], 0, i);
            resultsGrid.add(solverResults[i], 1, i);
        }

        // Set up the button for api request action
        checkButton.setOnAction(e -> {
            Random rand = new Random();
            for (int i = 0; i < 3; i++) {
                int percent = rand.nextInt(101); // Generate random propaganda likelihood percentage
                solverResults[i].setText(percent + "%");
            }
        });

        // Button to send data to the Python API
        Button sendButton = new Button("Evaluate");
        sendButton.setOnAction(e -> sendDataToAPI(textInput.getText()));

        // Layout using VBox for inputs and button
        VBox inputLayout = new VBox(10, textInput, checkButton, sendButton);
        inputLayout.setPadding(new Insets(10));

        // Use BorderPane for more flexibility in layout
        BorderPane mainLayout = new BorderPane();
        mainLayout.setCenter(inputLayout);
        mainLayout.setRight(resultsGrid);
        BorderPane.setMargin(resultsGrid, new Insets(10));

        // Setting the scene
        Scene scene = new Scene(mainLayout, 700, 300); // Adjusted width to accommodate GridPane
        primaryStage.setTitle("Propaganda Detector");
        primaryStage.setScene(scene);
        primaryStage.show();
    }

    // Method to send data to the Python API
    private void sendDataToAPI(String data) {
        String url = "http://127.0.0.1:5000/api/data";

        try (CloseableHttpClient client = HttpClients.createDefault()) {
            HttpPost httpPost = new HttpPost(url);
            StringEntity entity = new StringEntity(data);
            httpPost.setEntity(entity);
            httpPost.setHeader("Content-type", "application/json");

            try (CloseableHttpResponse response = client.execute(httpPost)) {
                String responseString = EntityUtils.toString(response.getEntity(), "UTF-8");
                // Handle the response here
                System.out.println(responseString);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        launch(args);
    }
}

/*package gui;

import javafx.application.Application;
import javafx.geometry.Insets;
import javafx.scene.Scene;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.TextArea;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.GridPane;
import javafx.scene.layout.VBox;
import javafx.stage.Stage;

import java.util.Random;

public class Main extends Application {

    @Override
    public void start(Stage primaryStage) {
        // Text area for input
        TextArea textInput = new TextArea();
        textInput.setPromptText("Enter your text here...");
        textInput.setWrapText(true);

        // Button to check for propaganda
        Button checkButton = new Button("Check for Propaganda");
        checkButton.getStyleClass().add("check-button");

        // GridPane for solver results
        GridPane resultsGrid = new GridPane();
        resultsGrid.setPadding(new Insets(10));
        resultsGrid.setHgap(10);
        resultsGrid.setVgap(10);

        // Create labels for solver names and results
        Label[] solverNames = {
                new Label("Risk Words Evaluator"),
                new Label("Emotional Evaluator"),
                new Label("Positive Generalities Evaluator")
        };
        Label[] solverResults = new Label[5];
        for (int i = 0; i < 3; i++) {
            solverResults[i] = new Label("0%");
            resultsGrid.add(solverNames[i], 0, i);
            resultsGrid.add(solverResults[i], 1, i);
        }

        // Set up the button action
        checkButton.setOnAction(e -> {
            Random rand = new Random();
            for (int i = 0; i < 3; i++) {
                int percent = rand.nextInt(101); // Generate random propaganda likelihood percentage
                solverResults[i].setText(percent + "%");
            }
        });

        // Layout using VBox for inputs and button
        VBox inputLayout = new VBox(10, textInput, checkButton);
        inputLayout.setPadding(new Insets(10));

        // Use BorderPane for more flexibility in layout
        BorderPane mainLayout = new BorderPane();
        mainLayout.setCenter(inputLayout);
        mainLayout.setRight(resultsGrid);
        BorderPane.setMargin(resultsGrid, new Insets(10));

        // Setting the scene
        Scene scene = new Scene(mainLayout, 700, 300); // Adjusted width to accommodate GridPane
        primaryStage.setTitle("Propaganda Detector");
        primaryStage.setScene(scene);
        primaryStage.show();
    }

    public static void main(String[] args) {
        launch(args);
    }
}
*/