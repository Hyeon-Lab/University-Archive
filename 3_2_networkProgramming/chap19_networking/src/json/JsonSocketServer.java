/**
 * 컴파일   :  src % javac -cp ../lib/json-20250517.jar -d out json/JsonSocketServer.java
 * 실행(Mac):   src % java -cp "out:../lib/json-20250517.jar" json.JsonSocketServer
 * 실행(Windows):   src % java -cp "out;../lib/json-20250517.jar" json.JsonSocketServer
 *
 */
package json;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import org.json.JSONObject;

public class JsonSocketServer {
    public static void main(String[] args) throws Exception {
        ServerSocket serverSocket = new ServerSocket(6000);
        System.out.println("서버 대기 중...");

        try (Socket clientSocket = serverSocket.accept()) {
            BufferedReader in = new BufferedReader(
            					new InputStreamReader(
            						clientSocket.getInputStream()));
            BufferedWriter out = new BufferedWriter(
            					new OutputStreamWriter(
            						clientSocket.getOutputStream()));

            // 클라이언트로부터 JSON 문자열 수신
            String jsonStr = in.readLine();
            JSONObject received = new JSONObject(jsonStr);
            System.out.println("[Server] 수신 데이터: " + received.toString(4));

            // JSON 응답 생성
            JSONObject response = new JSONObject();
            response.put("result", "OK");
            response.put("echo_name", received.getString("name"));

            // 클라이언트로 응답 전송
            out.write(response.toString());
            out.newLine();
            out.flush();
        }
        serverSocket.close();
    }
}
