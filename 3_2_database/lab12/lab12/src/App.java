import java.sql.*;

public class App {

    public static void main(String[] args) {
        long st, et, exetime;
        Statement stmt;
        ResultSet rs;
        String sql, dvd_idx_sql, name_idx_sql;
        
        String url = "jdbc:mysql://localhost:3306/week12";
        String user = "root";
        String passwd = "3738";
    
  
        try {
            //Class.forName("com.mysql.jdbc.Driver");
            Connection conn = DriverManager.getConnection(url, user, passwd);
            stmt = conn.createStatement();
            
            sql = "SELECT count(*) FROM rented  r, customer  c  WHERE r.customerName= c.name and c.address like '%1111%'";
            dvd_idx_sql = "create index dvd_idx on rented(dvdName)";
            name_idx_sql = "create index name_idx on rented(customerName)";

            st = System.currentTimeMillis();
            rs = stmt.executeQuery(sql);
            et = System.currentTimeMillis();
            exetime = et-st;
            System.out.println("#Execution Time:" + exetime);

            stmt.executeUpdate(dvd_idx_sql);
            
            st = System.currentTimeMillis();
            rs = stmt.executeQuery(sql);
            et = System.currentTimeMillis();
            exetime = et-st;
            System.out.println("#Execution Time:" + exetime);

            stmt.executeUpdate(name_idx_sql);

            st = System.currentTimeMillis();
            rs = stmt.executeQuery(sql);
            et = System.currentTimeMillis();
            exetime = et-st;
            System.out.println("#Execution Time:" + exetime);

 
            rs.close();
            stmt.close();
            conn.close();

        } catch (SQLException e) {
            e.printStackTrace();
 
        }
    }
}