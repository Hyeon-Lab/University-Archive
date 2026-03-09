<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ page language="java" import="java.sql.*" %>

<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>COMP322: Databases</title>
</head>
<body>
 
<% 

	///// YOUR CODE: change user, passwd, and url properly ///////
	String user = "root";
	String passwd = "3738";
	String url = "jdbc:mysql://localhost:3306/project2";
	///////////// END OF YOUR CODE //////////
	 
	Connection conn = null;
	Statement stmt;
	ResultSet rs;
	Class.forName("com.mysql.jdbc.Driver");
	conn = DriverManager.getConnection(url,user,passwd);
	stmt = conn.createStatement();
%>

<h2>--- List of Students ---</h2>
<% 
	////////// YOUR CODE ///////////
	// run the SQL statement to read the "new_student" table
	// display the student information with "<table>" tag in a html.
	// add a hyperlink for each nickname as follows:
	//   student_detail.jsp?nickname=apt (If nickname is apt) 

	String sql = "SELECT * FROM new_student";

	rs = stmt.executeQuery(sql);
	ResultSetMetaData rsm = rs.getMetaData();
	String name = "";

	int colCount = rsm.getColumnCount();
	
	out.println("<table border=\"1\">");
	out.println("<tr>");
	for (int i=1; i<=colCount; i++) {
		out.println("<th>");
		out.println(rsm.getColumnName(i));
		out.println("</th>");
	}
	out.println("</tr>");

	while (rs.next()) {
		out.println("<tr>");
		for (int i=1; i<=colCount; i++) {
			out.println("<td>");
			name = rs.getString(i);
			if(i == 1) 
				out.println("<a href=\"http://localhost:8080/student_detail.jsp?nickname="+name+"\">"+name+"</a>");
			else
				out.println(name);
			out.println("</td>");
		}
		out.println("</tr>");
	}
     
	//////////////// END OF YOUR CODE ////////////

	rs.close();
	stmt.close();
	conn.close();
%>
</table>


</body>
</html>