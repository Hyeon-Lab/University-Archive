import java.io.*;
import java.net.*;
import java.util.*;

public class ServerEx {
	public static void main(String[] args) {
		ServerSocket listener = null;
		Socket socket = null;
		Scanner scanner = new Scanner(System.in); 

		BufferedReader in = null;
		BufferedWriter out = null;
		
		try {
			listener = new ServerSocket(5550); // 서버 소켓 생성
			System.out.println("연결을 기다리고 있습니다.....");
			socket = listener.accept(); // 클라이언트로부터 연결 요청 대기
			System.out.println("연결되었습니다.");
			
			in = new BufferedReader(new InputStreamReader(socket.getInputStream())); // 소켓 입력 스트림
			out = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream())); // 소켓 출력 스트림
			
			while (true) {
				String inputMessage = in.readLine(); // 클라이언트로부터 한 행 읽기
				if (inputMessage.equalsIgnoreCase("bye")) {
					System.out.println("클라이언트에서 bye로 연결을 종료하였음"); 
					break;  
				}
				System.out.println("[Rx]: " + inputMessage); 			
				System.out.print("[Tx]>> "); 
				String outputMessage = scanner.nextLine(); 
				out.write(outputMessage + "\n"); 
				out.flush();
			}
		} catch (IOException e) {
			System.out.println(e.getMessage());
		} finally {
			try {
				scanner.close(); // scanner 닫기
				socket.close(); // 통신용 소켓 닫기
				listener.close(); // 서버 소켓 닫기
			} catch (IOException e) {
				System.out.println("클라이언트와 채팅 중 오류가 발생했습니다.");
			}
		}
	}
}