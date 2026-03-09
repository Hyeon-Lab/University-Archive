import java.util.ArrayList;
import java.io.BufferedReader;
import java.io.FileReader;
import java.nio.charset.StandardCharsets;
import java.io.InputStreamReader;

import java.sql.*;
import java.io.File;

public class MyDBMSTool {
 
    private String url, user, passwd;
    private String curr_database;
    private Connection conn = null;

      
    public MyDBMSTool(String url, String user, String passwd) { 
        this.url = url;
        this.user = user;
        this.passwd = passwd;

        int s = url.indexOf("//");
        int e = -1;
        if(s>=0) {
            e = url.indexOf("/", s+2);
            if(e>=0) {
                curr_database = url.substring(e);
                curr_database = this.curr_database.replace("/", "");
            }
            else curr_database = "";
        }
        else curr_database = "";

        System.out.println("Current DB is "+curr_database);
    }
 

    public boolean connect() {
        try {
            conn = DriverManager.getConnection(url, user, passwd);
            return true;
        } catch(Exception e) {
            e.printStackTrace();
        }
        return false;
    }

    public boolean disconnect(String url, String user, String passwd) {
        try {
            conn.close();
            return true;
        } catch(Exception e) {
            e.printStackTrace();
        }
        return false;
    }
 

    // This function converts ResultSet to the string.
    // Note that the string contains multiple lines with separater \n
    public String convertToString(ResultSet rs) {
        try {
            ResultSetMetaData rsm = rs.getMetaData();
            String str = "";

            ///////////// YOUR CODE //////////////////////
            int colCount = rsm.getColumnCount();

            for (int i=1; i<=colCount; i++) {
                str += rsm.getColumnName(i);
                if (i < colCount) {
                    str += "\t";
                }
            }
            str += "\n";
            str += "-------------------------------------------------------------------------------------\n";

            while (rs.next()) {
                for (int i=1; i<=colCount; i++) {
                    str += rs.getString(i);
                    if(i<colCount) {
                        str += "\t";
                    }
                }
                str += "\n";
            }

            str += "=====================================================================================\n";
            //////////////////////////////////////
            return str;
        }
        catch (Exception e) {
            e.printStackTrace();;
        }
        return "";
    }


    // This function runs the SELECT statement and convert the results to the string
    public String runSelect(String select) {       
        try {
            String resultStr = "";
            /////////////////// YOUR CODE //////////////////////
            // use convertToString()
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery(select);
            resultStr = convertToString(rs);
            rs.close();
            stmt.close();
            ////////////////////////////////////////
            return resultStr;
        } catch(Exception e) {
            e.printStackTrace();
        }

        return "";
    }



    // This function runs the CREATE DATABASE, CREATE TABLE, INSERT, DELETE or Update statement
    public void runUpdate(String sql) {    
         try {
            /////////////// YOUR CODE /////////////////
            Statement stmt = conn.createStatement();
            stmt.executeUpdate(sql);
            stmt.close();
            ///////////////////////////////////////
            
         } catch(Exception e) {
             e.printStackTrace();
         }
    }

 
    
    // This function converts each line to the INSERT INTO statement.
    // * Thie code is the same as that of the Week5 exercise.
    private String convert(String line, String tableName) {

        //////////////// YOUR CODE /////////////////////////
        String[] tokens = line.split(",");

        for (int i=0; i<tokens.length; i++) {
            tokens[i] = "'" + tokens[i].trim() + "'";
        }

        String values = String.join(", ", tokens);
        return "INSERT INTO " + tableName + " VALUES (" + values + ");";
        ////////////////////////////////////////////////////
    }


    // This function reads the table-like file and generates SQL statements as follows:
    //  - Table Creation Statement: Generate the CREATE TABLE statement from the first line (header)  
    //  - Insert Statements:  Generate the INSERT statements from each line
    // Assume the we have only one attribute type varchar(100)
     public ArrayList<String> convertToSQLsWithTableSchema(String fileName, String tableName) {
        try {
            BufferedReader br = new BufferedReader(new FileReader(fileName, StandardCharsets.UTF_8));
            String header = br.readLine();  // read the header
            String line = null;

            ArrayList<String> sqlList = new ArrayList<String>();

            //////////////////// YOUR CODE //////////////////////////////
            // Use the convert(line, tableName) method
            String[] cols = header.split(",");
            StringBuilder create = new StringBuilder("CREATE TABLE " + tableName + " (");
            for (int i=0; i<cols.length; i++) {
                create.append(cols[i].trim()).append(" varchar(100)");
                if (i<cols.length - 1) {
                    create.append(", ");
                }
            }
            create.append(");");
            sqlList.add(create.toString());

            while((line = br.readLine()) != null) {
                if (line.trim().isEmpty()) {
                    continue;
                }
                sqlList.add(convert(line, tableName));
            }
            //////////////////////////////////////////////////

            br.close();
            return sqlList;

        } catch(Exception e) {
            e.printStackTrace();
        }

        return null;
    } 

    


    // This fucntion runs multiple queries using "executeBatch()"
    public void runMultipleQueries(ArrayList<String> sqlList) {
        
        try {

            //////////////////// YOUR CODE ////////////////////////////
            Statement stmt = conn.createStatement();

            for (String sql : sqlList) {
                stmt.addBatch(sql);
            }

            stmt.executeBatch();
            stmt.close();
            //////////////////////////////////////////////////////
        } catch(Exception e) {
            e.printStackTrace();
        }
        return;
    }



    // This fucntion imports csvFile to the table named tabName
    // 1) create a table schema
    // 2) insert data in csvFile into the table
    public void importData(String csvFile, String tabName) {

        ArrayList<String> sqlList = convertToSQLsWithTableSchema(csvFile, tabName);

        runMultipleQueries(sqlList);
    }


    // This fucntion imports all the csv files in "path" to the database named dbName
    //   1) create a database if it does not exist (ref. CREATE DATABASE IF NOT EXISTS ...)
    //   2) get csv file names in "path"
    //   3) import each csv file using importData()  (ref. You can create a table in a different database using DB_NAME.TABLE_NAME)
    public void dimportData(String path, String dbName) {

        //////////////////// YOUR CODE ////////////////////////////
        runUpdate("CREATE DATABASE IF NOT EXISTS " + dbName + ";");

        File folder = new File(path);
        File[] files = folder.listFiles((File dir, String name) -> name.endsWith(".csv"));
        if (files == null) return;

        for (File f : files) {
            String fileName = f.getAbsolutePath();
            String tableName = f.getName().replace(".csv", "");
            importData(fileName, dbName + "." + tableName);
        }
        /////////////////////////////////////////////////
    }

 
 
    // This function interprets the command "cmd"
    // Available commands:
    //   - help, pwd, ls, exit: implemnated
    //   - import, dimport, read, show databases, show tables, desc, find table: You should implement the commands
    public String interpret(String cmd) {
        cmd = cmd.toLowerCase();
        cmd = cmd.trim();
        
        String resultStr = "";

        // print avaiable commands
        if(cmd.equals("help")) {
            resultStr = 
"\n#Usage#\n"+
"help : print tool commands\n"+
"pwd: print the current working directory \n"+
"ls [path]: print files in \"path\" \n"+
"exit  : exit the tool\n"+
"show databases: print all database names\n"+
"show tables DB_NAME: print all tables in the DB_NAME database\n"+
"import FILE_NAME TAB_NAME: import FILE_NAME to TAB_NAME\n"+
"dimport DIR DB_NAME: import all csv files in DIR to the database named DB_NAME\n"+
"read TAB_NAME: print all records in TAB_NAME\n"+
"desc TAB_NAME: print column names and column types for TAB_NAME in the column order\n"+
"find tables column=COL_NAME: find tables that contain an attribute named COL_NAME in all the databases\n"+
"find tables tab_prefix=TAB_PREFIX: find tables whose table name starts with TAB_PREFIX in all the databases\n"
;

        }
        // print the current working directory
        else if(cmd.equals("pwd")) {
            resultStr = "\n"+System.getProperty("user.dir")+"\n";
        }
        // show the file list in the current directy (ls) or in the specified directory (ls PATH)
        else if(cmd.equals("ls") || cmd.startsWith("ls ")) {
            String specifiedPath = cmd.replaceFirst("ls","").trim();
            File dir = null;
            if(specifiedPath.equals("")) dir = new File(".");
            else dir = new File(specifiedPath);
            resultStr = "\n";
            for (File file: dir.listFiles()) {
                if(file.isDirectory()) resultStr += "("+file.getName() +")\n";
                else resultStr += file.getName() +"\n";
            }
        }
        // Show all the databases
        // - Usage: show databases
        else if(cmd.equals("show databases")) {  
            ///////////// YOUR CODE ////////////////
            // Use runSelect()
            resultStr = runSelect("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA " + 
                "ORDER BY SCHEMA_NAME;");
            ///////////////////////////////////////        
        }  
        // show tables in the database called DB_NAME
        // - Usage: show tables DB_NAME
        else if(cmd.startsWith("show tables")) { 
            ///////////// YOUR CODE ////////////////
            // Use runSelect()
            String[] tokens = cmd.split("\\s+");
            if (tokens.length == 3) {
                String dbName = tokens[2];
                resultStr = runSelect("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES " +
                "WHERE TABLE_SCHEMA = '" + dbName + "'" + 
                "ORDER BY TABLE_NAME;");
            }
            ///////////////////////////////////////        
        }

        // import the csv file to the table in DBMS  
        // - Usage: import FILE_NAME TAB_NAME
        else if(cmd.startsWith("import ")) { 
            String [] toks = cmd.split(" ");
            if(toks.length<3) {
                resultStr = " #command error";
            }
            else {
                String filePath = toks[1]; // csv file path
                String tabName = toks[2]; // table name to be created
                importData(filePath, tabName);
            }
        }
        // import all the csv files in filePath to the database named dbName  
        // - Usage: dimport DIR DB_NAME: import all csv files in DIR to the database named DB_NAME
        // * Remove the file extension from each file name and use it as the table name
        else if(cmd.startsWith("dimport ")) { 
            String [] toks = cmd.split(" ");
            if(toks.length<2) {
                resultStr = " #command error";
            }
            else {
                String filePath = toks[1]; // csv file path
                String dbName = toks[2]; // database name
                dimportData(filePath, dbName);
            }
        }
        // Show data in the table
        // You should support both TABLE_NAME and DB_NAME.TABLE_NAME notations         
        // - Usage: read TAB_NAME 
        else if(cmd.startsWith("read ")) { 
            ///////////// YOUR CODE ////////////////
            // Use runSelect()
            String table = cmd.replaceFirst("read ", "").trim();
            resultStr = runSelect("SELECT * FROM " + table + ";");
            ///////////////////////////////////////
        }

        // print the column names and column type names of the TAB_NAME table in the column order
        // You should support both TABLE_NAME and DB_NAME.TABLE_NAME notations         
        // - Usage: desc TAB_NAME
        else if(cmd.startsWith("desc ")) {  
            String name = cmd.replaceFirst("desc ", "");

            ///////////// YOUR CODE ////////////////
            // Use runSelect()
            // Use the ORDINAL_POSITION attribute in the COLUMNS table to sort the results in the column order
            String schema = null;
            String table = name;

            if(name.contains(".")) {
                String[] parts = name.split("\\.");
                schema = parts[0];
                table = parts[1];
            }
            String query;

            if (schema == null) {
                query = "SELECT COLUMN_NAME, COLUMN_TYPE " +
                "FROM INFORMATION_SCHEMA.COLUMNS " +
                "WHERE (TABLE_NAME = '" + table + "')" +
                "ORDER BY ORDINAL_POSITION;";
            } else {
                query = "SELECT COLUMN_NAME, COLUMN_TYPE " +
                "FROM INFORMATION_SCHEMA.COLUMNS " +
                "WHERE TABLE_SCHEMA = '" + schema + "' " +
                "AND TABLE_NAME = '" + table + "' " +
                "ORDER BY ORDINAL_POSITION;";
            }

            resultStr = runSelect(query);
            ///////////////////////////////////////         
        }

        // find tables that contain an attribute named COL_NAME in all the databases
        // - Usage: find tables column=COL_NAME
        else if(cmd.startsWith("find tables column=")) { 
            String colName = cmd.replaceFirst("find tables column=", "");

            ///////////// YOUR CODE ////////////////
            // Use runSelect()
            String query = "SELECT TABLE_SCHEMA, TABLE_NAME " +
            "FROM INFORMATION_SCHEMA.COLUMNS " +
            "WHERE COLUMN_NAME = '" + colName + "'" +
            "ORDER BY TABLE_SCHEMA, TABLE_NAME;";

            resultStr = runSelect(query);
            ///////////////////////////////////////         
        }
        
        // find tables whose table name starts with TAB_PREFIX in all the databases
        // - Usage: find tables tab_prefix=TAB_PREFIX
        else if(cmd.startsWith("find tables tab_prefix=")) { 
            String prefix = cmd.replaceFirst("find tables tab_prefix=", "");

            ///////////// YOUR CODE ////////////////
            // Use runSelect()
            String query = "SELECT TABLE_SCHEMA, TABLE_NAME " +
            "FROM INFORMATION_SCHEMA.TABLES " +
            "WHERE TABLE_NAME LIKE '" + prefix + "%'" +
            "ORDER BY TABLE_SCHEMA, TABLE_NAME;";

            resultStr = runSelect(query);
            ///////////////////////////////////////         
        }
        
        return resultStr;
    }



    public static void main(String [] args) throws Exception {
 
        String url = "jdbc:mysql://localhost:3306/week9"; // Change the database name properly
        
        // Change user and passwd properly
        String user = "root";
        String passwd = "3738";
    
        MyDBMSTool tool = new MyDBMSTool(url, user, passwd);
        if(tool.connect()==false) {
            System.out.println("# Connection Error");
            return;
        }

        BufferedReader consolReader = new BufferedReader(new InputStreamReader(System.in));
        while(true) {
            System.out.print("des>");  // Your Name
            String cmd = consolReader.readLine();

            if(cmd.trim().toLowerCase().equals("exit")) break;
            String cmdResult = tool.interpret(cmd);
            System.out.println(cmdResult);
        }
    }

}
