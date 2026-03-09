<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ page language="java" import="java.sql.*" %>
 
<%!
	int sum(int a, int b) { 
		return a+b;
	}
%>
 
<!DOCTYPE html>
<html>
<head> 
<title> Test </title>
</head>
<body>
<h1> # Heading Test (Heading 1) </h1>	 
<h2> Heading 2</h2>
<h3> Heading 3</h3>

<h1> # Table </h1>	 
<table border="1">
  <tr> <th> attr1</th>  <th>  attr2</th>  </tr>
  <tr> <td> data1</td>  <td>  data2</td>  </tr>
  <tr> <td> data3</td>  <td>  data4</td>  </tr>
</table>



<br>

<h1> # Example1 </h1>	 
<%
   int a = 10;
   int b = 15;
   
   out.println("<h3> a=10, b=15 </h3>");
   out.println("<h4>a+b=");
   out.println(sum(a,b));
   out.println("</h4>");
%>

 

<h1> # Example2 </h1>	 
<%
   String [] addrList = {"a1", "a2", "a3", "a4"};
   
   for(String v: addrList) {
	 out.println("<a href=\"test2.jsp?myparam1="+v+"\">"+v+"</a> <br>"); 
}
%>


<h1> # Example3 </h1>	 
<form action="test2.jsp" method="POST">
	myparam1: <input type="text" name="myparam1" value="Value1">
	<input type="submit" value="Submit"> 
</form>

</body>
</html>