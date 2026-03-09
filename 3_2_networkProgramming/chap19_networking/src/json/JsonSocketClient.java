/**
 * 컴파일: src % javac -cp ../lib/json-20250517.jar -d out json/JsonSocketClient.java
 * 실행(Mac)  : src % java -cp "out:../lib/json-20250517.jar" json.JsonSocketClient
 * 실행(Windows)  : src % java -cp "out;../lib/json-20250517.jar" json.JsonSocketClient
 */
package json;

import java.io.*;
import java.net.Socket;
import org.json.JSONObject;

public class JsonSocketClient {
    public static void main(String[] args) throws Exception {
        Socket socket = new Socket("localhost", 6000);

        BufferedWriter out = new BufferedWriter(
        		new OutputStreamWriter(socket.getOutputStream()));
        BufferedReader in = new BufferedReader(
        		new InputStreamReader(socket.getInputStream()));

        // 전송할 JSON 데이터 생성
        JSONObject obj = new JSONObject();
        obj.put("name", "Hong Gil-Dong");        
        obj.put("message", "Json message test!");
        

        // 서버로 JSON 문자열 전송
        out.write(obj.toString());
        out.newLine();
        out.flush();

        // 서버에서 응답 수신
        String respStr = in.readLine();
        JSONObject resp = new JSONObject(respStr);
        System.out.println("Server 응답: " + resp.toString(4));

        socket.close();
    }
}
