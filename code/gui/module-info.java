module com.example.better_project_2_2 {
    requires javafx.controls;
    requires javafx.fxml;
    requires org.apache.httpcomponents.httpclient;
    requires org.apache.httpcomponents.httpcore;
    requires com.google.gson;


    opens gui to javafx.fxml;
    exports gui;
}