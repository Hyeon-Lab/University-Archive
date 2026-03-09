package Chapter14_Server_Client_Socket;

import java.io.*;
import java.net.*;

public class ex02_Server {
	public static void main(String[] args) {
		ServerSocket listener = null;
		Socket socket = null;
		BufferedReader in = null;
		int n;
		int sum = 0;
		System.out.println("서버입니다. 클라이언트를 기다립니다.");
		try {
			listener = new ServerSocket(9999);
			socket = listener.accept();
			System.out.println("연결 되었습니다.");
			in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
			while (true) {
				String inputMessage = in.readLine();
				n = Integer.parseInt(inputMessage);
				if(n < 0) {
					System.out.println("서버를 종료합니다.");
					break;
				}
				sum += n;
				System.out.println("누적합 " + sum);
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
