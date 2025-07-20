package com.example.demo;

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

public class Gui extends Application {

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
                new Label("Positive Generalities Evaluator"),
                new Label("Stereotypes Evaluator"),
                new Label("Final Result")
        };
        Label[] solverResults = new Label[5];
        for (int i = 0; i < 5; i++) {
            solverResults[i] = new Label("");
            resultsGrid.add(solverNames[i], 0, i);
            resultsGrid.add(solverResults[i], 1, i);
        }

        // Set up the button action
        checkButton.setOnAction(e -> {
            Random rand = new Random();
            for (int i = 0; i < 4; i++) {
                // Generate random floating-point numbers between 0.0 and 1.0
                double randomValue = rand.nextDouble(); // This generates a value between 0.0 (inclusive) and 1.0 (exclusive)
                solverResults[i].setText(String.format("%.2f", randomValue)); // Set the text formatted to 2 decimal places
            }
            // For the final result, generate only 0 or 1
            int finalResult = rand.nextInt(2); // Generates either 0 or 1
            solverResults[4].setText(Integer.toString(finalResult)); // Set the text as "0" or "1" for the Final Result
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
