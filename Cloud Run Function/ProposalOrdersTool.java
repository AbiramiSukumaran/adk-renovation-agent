package gcfv2;


import com.google.cloud.functions.HttpFunction;
import com.google.cloud.functions.HttpRequest;
import com.google.cloud.functions.HttpResponse;
import java.io.BufferedWriter;
import com.zaxxer.hikari.HikariConfig;
import com.zaxxer.hikari.HikariDataSource;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.time.Instant;
import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.JsonArray;
import com.google.gson.JsonParser;
import com.google.cloud.vertexai.VertexAI;
import com.google.cloud.vertexai.api.GenerateContentResponse;
import com.google.cloud.vertexai.api.GenerationConfig;
import com.google.cloud.vertexai.generativeai.preview.GenerativeModel;
import com.google.cloud.vertexai.generativeai.preview.ResponseHandler;
import java.io.IOException;
import java.util.List;
import java.util.Arrays;
import java.util.Map;
import java.util.LinkedHashMap;
import com.google.gson.Gson;

/*      
Function that reads from Supplier database for 
material order status and returns the result in JSON format.
*/

public class ProposalOrdersTool implements HttpFunction {
 @Override
 public void service(HttpRequest request, HttpResponse response) throws Exception {
   BufferedWriter writer = response.getWriter();
   String result = "";
   String query = "select order_id, material_name,supplier_name, order_status from material_order_status";
   HikariDataSource dataSource = AlloyDbJdbcConnector();
   JsonArray jsonArray = new JsonArray(); // Create a JSON array

try (Connection connection = dataSource.getConnection()) {
    try (PreparedStatement statement = connection.prepareStatement(query)) {
        ResultSet resultSet = statement.executeQuery();
        System.out.println(statement.toString());
        while (resultSet.next()) { // Loop through all results
            JsonObject jsonObject = new JsonObject();
           
                jsonObject.addProperty("order_id", resultSet.getString("order_id"));
                jsonObject.addProperty("material_name", resultSet.getString("material_name"));
                jsonObject.addProperty("supplier_name", resultSet.getString("supplier_name"));
                jsonObject.addProperty("order_status", resultSet.getString("order_status"));
            
            jsonArray.add(jsonObject);
        }
    }
    // Set the response content type and write the JSON array
    response.setContentType("application/json");
    result = jsonArray.toString();
    writer.write(result);

    }
 }
 public  HikariDataSource AlloyDbJdbcConnector() {
        HikariDataSource dataSource;
        String ALLOYDB_DB = "postgres";
        String ALLOYDB_USER = "postgres";
        String ALLOYDB_PASS = "alloydb";
        String ALLOYDB_INSTANCE_NAME = "projects/<<YOUR_PROJECT_ID>>/locations/us-central1/clusters/<<YOUR_CLUSTER>>/instances/<<YOUR_INSTANCE>>";
        HikariConfig config = new HikariConfig();
        config.setJdbcUrl(String.format("jdbc:postgresql:///%s", ALLOYDB_DB));
        config.setUsername(ALLOYDB_USER); // e.g., "postgres"
        config.setPassword(ALLOYDB_PASS); // e.g., "secret-password"
        config.addDataSourceProperty("socketFactory", "com.google.cloud.alloydb.SocketFactory");
        config.addDataSourceProperty("alloydbInstanceName", ALLOYDB_INSTANCE_NAME);
        dataSource = new HikariDataSource(config);
        return dataSource;
}
}
