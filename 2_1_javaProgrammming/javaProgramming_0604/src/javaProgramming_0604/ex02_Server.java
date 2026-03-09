package javaProgramming_0604;
import java.io.*;
import java.net.*;
import java.util.StringTokenizer;

public class ex02_Server {
	public static void main(String[] args) {
		ServerSocket listener = null;
		Socket socket = null;
		BufferedReader in = null;
		int n1 = 0; int n2 = 0;
		System.out.println("서버입니다. 클라이언트를 기다립니다...");
		try {
			listener = new ServerSocket(9999);
			socket = listener.accept();
			System.out.println("연결되었습니다.");
			in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
			while (true) {
				String inputMessage = in.readLine();
				if(inputMessage.equalsIgnoreCase("끝")) {
					System.out.println("서버를 종료합니다.");
					break;
				}
				System.out.println("... "+ inputMessage);
			}
		} catch (IOException e) {
			System.out.println("입출력 오류가 발생했습니다.");
		}
		try {
			listener.close();
			socket.close();
		} catch (Exception e) {}
	}

}

