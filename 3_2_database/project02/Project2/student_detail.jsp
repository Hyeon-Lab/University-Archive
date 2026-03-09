<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ page language="java" import="java.sql.*" %>

<!DOCTYPE html>
<html>
<head> 
<title> COMP322: Databases </title>
</head>
<body>
 
<p>
<i> ------ For Debugging ------ <br>
<%

String nickName = request.getParameter("nickname");
 
out.println("Nickname parameter: <b>"+nickName+"</b>");
out.println("<br>");
%> 
</p>
<hr>

<%!
   
	String getStudentInfo(String selectedNickName, String tabName, Statement stmt, boolean isFriendInfo ) {

		String result = "<h3> # " +tabName+"</h3>";

		try {
			result = result + "<table border=\"1\">\n";
			String query;
			ResultSet rs;
			ResultSetMetaData rsm;

			////// YOUR CODE: 1. write an SQL query to get the information of
			//                    the "selectedNickName" student in the "tabName" table 
			//                2. run the SQL query
			//                3. display the results in the table format   
			//                      (header information: use rs.getMetaData() )
			//                   - add a hyperlink for each friend if "isFriendInfo" is true	

			query = "SELECT * FROM "+tabName+" WHERE nickname = \""+selectedNickName+"\";";
			rs = stmt.executeQuery(query);
			rsm = rs.getMetaData();
			String name = "";

			int colCount = rsm.getColumnCount();

			result += "<tr>";
			for (int i=1; i<=colCount; i++) {
				result += "<th>";
				result += rsm.getColumnName(i);
				result += "</th>";
			}
			result += "</tr>";

			while (rs.next()) {
				result += "<tr>";
				for (int i=1; i<=colCount; i++) {
					result += "<td>";
					name = rs.getString(i);
					if(isFriendInfo == true)
						if(i == 2)
							result += "<a href=\"http://localhost:8080/student_detail.jsp?nickname="+name+"\">"+name+"</a>";
						else
							result += name;
					else
						result += name;
					result += "</td>";
				}
				result += "</tr>";
			}
			////////////////////////// END OF YOUR CODE ////////////

			result = result + "</table>\n";
		} catch (Exception SQLException) {
			return "# getStudentInfo Error";
		}
		return result;
	}
 
%>

 

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


<% 

		
    out.println("<h2> All Information about <u>" + nickName + "</u></h2> \n");

	////// YOUR CODE ///////
	// generate HTML tables using getStudentInfo()	
	
	out.println(getStudentInfo(nickName, "new_student", stmt, false));
	out.println(getStudentInfo(nickName, "friend_info", stmt, true));
	out.println(getStudentInfo(nickName, "favorite_course", stmt, false));
	out.println(getStudentInfo(nickName, "favorite_food", stmt, false));
	out.println(getStudentInfo(nickName, "preferred_pl", stmt, false));
     
	///////////// END OF YOUR CODE //////////
	
	stmt.close();
	conn.close();
%>



</body>
</html>