import java.sql.*;

public class Sample3 {

    public static void main(String[] args) {
        String url = "jdbc:mysql://localhost:3306/week7";
        String user = "root";
        String passwd = "1234";
    
  
        try {
            //Class.forName("com.mysql.jdbc.Driver");
            Connection conn = DriverManager.getConnection(url, user, passwd);
            
            String sql = "create table tab (a int, b int)";
            //String sql = "insert into tab values (3,4)"; 
            //String sql = "delete from tab"; 
            Statement stmt = conn.createStatement();
 
            System.out.println(stmt.executeUpdate(sql));

            stmt.close();
            conn.close();
            
        } catch (SQLException e) {
            e.printStackTrace();
 
        }
    }
}