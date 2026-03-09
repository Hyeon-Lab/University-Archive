import java.sql.*;
 
public class Sample4 {

    public static void main(String[] args) {
        String url = "jdbc:mysql://localhost:3306/week7";
        String user = "root";
        String passwd = "1234";
    
        try {
            //Class.forName("com.mysql.jdbc.Driver");
            Connection conn = DriverManager.getConnection(url, user, passwd);
            conn.setAutoCommit(false); 

            Statement stmt = conn.createStatement();
            stmt.addBatch("create table tab2(a int, b int)");
            for(int i=0; i<100; i++) stmt.addBatch("insert into tab2 values ("+i+","+i+")");
  
            stmt.executeBatch();

            conn.commit();
            conn.setAutoCommit(true);

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}