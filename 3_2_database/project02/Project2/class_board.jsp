
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

<p>
<i> ------ For Debugging ------ <br>
<%

request.setCharacterEncoding("UTF-8");
String myName = request.getParameter("my_nickname");
String myText = request.getParameter("my_text"); 

out.println("Nickname parameter: <b>"+myName+"</b>");
out.println("<br>");
out.println("My text parameter: <b>"+myText+"</b>");
out.println("<br>");
 

%> 
</i>
</p>
<hr>

<% 
    ///// YOUR CODE: change user, passwd, and url properly ///////
    String user = "root";
	String passwd = "3738";
	String url = "jdbc:mysql://localhost:3306/project2";
    ///////////// END OF YOUR CODE //////////
    
    String profServerUser = "guest";
    String profServerPasswd = "";
    String profServerUrl = "jdbc:mysql://155.230.118.28/project2?serverTimezone=Asia/Seoul";
    Connection conn = null;
    Statement stmt;
    ResultSet rs;
    String sql = null;
    
    Class.forName("com.mysql.jdbc.Driver");
    boolean profServerConnected = true;
    
    try {
        conn = DriverManager.getConnection(profServerUrl,profServerUser,profServerPasswd);
    } catch(Exception SQLException) {
        profServerConnected = false;
    }

    if (profServerConnected) out.println("<p><font COLOR=\"red\">Prof's server is working now!</font></p>\n");
    else {
        out.println("<p><font COLOR=\"red\">Prof's server is not working now! Try to connect to your server.</font></p>\n");

        try {
            conn = DriverManager.getConnection(url,user,passwd);
        } catch(Exception SQLException) {
            out.println("<p><font COLOR=\"red\">Your server is not working now! Check your server.</font></p>\n");

            return;
        }
    }

    stmt = conn.createStatement();

    // Insert Operation
    if(myName != null) {
        ///////////// YOUR CODE: write an SQL query to add (Name, Text) to the my_board table///////////////
        //                       run the query
        // Reuse the part of my_board.jsp.
     
        sql = "INSERT INTO my_board(nickname, mytext) VALUES ('" + myName + "', '" + myText + "');";
        stmt.executeUpdate(sql);

        ///////////// END OF YOUR CODE ///////////////
    }

 %>

<h2> (Remote) Class Board</h2>

<% 
    String query = "select * from my_board";
    rs = stmt.executeQuery(query);

    ////// YOUR CODE: Display the my_board table in the table format. /////// 
    //  Reuse the part of my_board.jsp.

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

    //////////// END OF YOUR CODE ////////////
 
    rs.close();
    stmt.close();
    conn.close();

%>



<hr>

<h2> INSERT </h2>

<form action="class_board.jsp" method="POST">
  Name: <input type="text" name="my_nickname" value="Your Name">
  Text: <input type="text" name="my_text" value="Your Text"> <br>
  <input type="submit" value="Add a new text"> 
</form>

<br>

<hr>
 
</body>
</html>