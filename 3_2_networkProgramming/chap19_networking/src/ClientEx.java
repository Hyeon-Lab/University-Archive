import java.io.*;
import java.net.*;
import java.util.*;

public class ClientEx {
	public static void main(String[] args) {
		Socket socket = null;
		
		BufferedReader in = null;
		BufferedWriter out = null;		
		Scanner scanner = new Scanner(System.in);
		
		try {
			socket = new Socket("localhost", 5550); // 클라이언트 소켓 생성. 서버와 바로 연결
			in = new BufferedReader(new InputStreamReader(socket.getInputStream())); // 소켓 입력 스트림
			out = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())); // 소켓 출력 스트림
	
			
			while (true) {
				System.out.print("[Tx]>> "); 
				String outputMessage = scanner.nextLine(); // 키보드에서 한 행 읽기
				if (outputMessage.equalsIgnoreCase("bye")) { 
					out.write(outputMessage+"\n"); 
					out.flush();					
					break; 
				}
				
				out.write(outputMessage + "\n"); 
				out.flush();
				
				String inputMessage = in.readLine(); // 서버로부터 한 행 수신
				System.out.println("[Rx]: " + inputMessage); 
			}
		} catch (IOException e) {
			System.out.println(e.getMessage());
		} finally {
			try {
				scanner.close();
				if(socket != null) 
					socket.close(); // 클라이언트 소켓 닫기
			} catch (IOException e) {
				System.out.println("서버와 채팅 중 오류가 발생했습니다.");
			}
		}
	}
}