
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
String myparam = request.getParameter("myparam1"); 

out.println("Parameter: <i>"+myparam+"</i>");
%>

</body>
</html>