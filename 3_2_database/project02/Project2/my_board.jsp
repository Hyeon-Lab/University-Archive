
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
String rowID = request.getParameter("rid_select");

out.println("Nickname parameter: <b>"+myName+"</b>");
out.println("<br>");
out.println("My text parameter: <b>"+myText+"</b>");
out.println("<br>");
out.println("Row ID: <b>"+rowID+"</b>");
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
    
    Connection conn = null;
    Statement stmt;
    ResultSet rs;
    String sql = null;
    
    Class.forName("com.mysql.jdbc.Driver");
    conn = DriverManager.getConnection(url,user,passwd);
    stmt = conn.createStatement();


    // Insert Operation
    if(myName != null) {
        ///////////// YOUR CODE: write an SQL query to add (Name, Text) to the my_board table///////////////
        //                                 run the query
        
        sql = "INSERT INTO my_board(nickname, mytext) VALUES ('" + myName + "', '" + myText + "');";
        stmt.executeUpdate(sql);
        ///////////// END OF YOUR CODE ///////////////
    }

    // Delete Operation
    if(rowID != null) {
        ///////////// YOUR CODE: write an SQL query to delete the record with rowID from the my_board table///////////////
        //                                 run the query

        sql = "DELETE FROM my_board WHERE id = '"+rowID+"';";
        stmt.executeUpdate(sql);
        ///////////// END OF YOUR CODE ///////////////
    }

 %>

<h2> (Local) My Board </h2>

<% 
    String query = "select * from my_board";
    rs = stmt.executeQuery(query);

    ////// YOUR CODE: Display the my_board table in the table format. //////
    
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

    //////////// END OF YOUR CODE //////////////

    rs.close();
%>



<hr>

<h2> INSERT </h2>

<form action="my_board.jsp" method="POST">
  Name: <input type="text" name="my_nickname" value="Your Name">
  Text: <input type="text" name="my_text" value="Your Text"> <br>
  <input type="submit" value="Add a new text"> 
</form>

<br>

<hr>

<form action="my_board.jsp" method="POST">
    <h2> DELETE </h2>
    <Label> ID to be deleted: </Label>

    <select name="rid_select">
        <% 

        query = "select id from my_board";
        rs = stmt.executeQuery(query);
        
        while(rs.next()){
            out.println("<option value=");
            out.println("\""+rs.getString(1)+"\"");
            out.println(">"+rs.getString(1)+"</option>");		
        }

        rs.close();
        stmt.close();
        conn.close();
        %>
    </select> 

    <br>
    <input type="submit" value="Delete">  
</form>
 
</body>
</html>