import java.sql.*;

public class Sample1 {

    public static void main(String[] args) {
        String url = "jdbc:mysql://localhost:3306/week7";
        //String url = "jdbc:mysql://155.230.118.28:3306/week7";
        String user = "root";
        String passwd = "1234";
    
  
        try {
            //Class.forName("com.mysql.jdbc.Driver");
            Connection conn = DriverManager.getConnection(url, user, passwd);
            
            String sql = "SELECT nickname,section FROM student";
            Statement stmt = conn.createStatement();
 
            ResultSet rs = stmt.executeQuery(sql);
 
            
            while (rs.next()) {
                System.out.println("index> "+rs.getString(1)+"\t"+rs.getString(2));
                System.out.println("name> "+rs.getString("nickname")+"\t"+rs.getString("section"));
            }  

 
            rs.close();
            stmt.close();
            conn.close();

        } catch (SQLException e) {
            e.printStackTrace();
 
        }
    }
}