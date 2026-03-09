<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ page language="java" import="java.sql.*" %>

<!DOCTYPE html>
<html>
<head>
<title>COMP322: Databases</title>
</head>
<body>
 
<% 
	String user = "root";
	String passwd = "3738";
	String url = "jdbc:mysql://localhost/project2";
 
	Connection conn = null;
	Statement stmt;
	ResultSet rs;
	Class.forName("com.mysql.jdbc.Driver");
	conn = DriverManager.getConnection(url,user,passwd);
	String query = "select * from my_board";

	stmt = conn.createStatement();
	rs = stmt.executeQuery(query);
%>

<h2>--- Class Board ---</h2>

<% 
	ResultSetMetaData rsm = rs.getMetaData();
	
	out.println("<table border=\"1\">");
	int cnt = rsm.getColumnCount();
	out.println("<tr>");
	for(int i =1;i<=cnt;i++){
		out.println("<th>"+rsm.getColumnName(i)+"</th>");
	}   
	out.println("</tr>");
	

	while(rs.next()){
		out.println("<tr>");
		for(int i=1; i<=cnt; i++) {
            out.println("<td>"+rs.getString(i)+"</td>");
        }
		out.println("</tr>");		
	}
        
	out.println("</table>");
	rs.close();
	stmt.close();
	conn.close();
%>


 
</body>
</html>