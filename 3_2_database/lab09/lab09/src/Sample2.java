import java.sql.*;
 
public class Sample2 {

    public static void main(String[] args) {
        String url = "jdbc:mysql://localhost:3306/week5";
        String user = "root";
        String passwd = "3738";
    
  
        try {
            //Class.forName("com.mysql.jdbc.Driver");
            Connection conn = DriverManager.getConnection(url, user, passwd);
            
            String sql = "SELECT * FROM student";
            Statement stmt = conn.createStatement();
 
            ResultSet rs = stmt.executeQuery(sql);
            ResultSetMetaData rsm = rs.getMetaData();
 
            int colCnt = rsm.getColumnCount(); // get the number of attributes
            for (int i=1; i<=colCnt; i++) {
                System.out.println("Attr"+i+"-"+rsm.getColumnName(i)+":"+rsm.getColumnTypeName(i));
            }

            rs.close();
            stmt.close();
            conn.close();

        } catch (SQLException e) {
            e.printStackTrace();
        }
    }
}