package Chapter14_Server_Client_Socket;

import java.io.*;
import java.net.*;
import java.util.Scanner;

public class ex02_Client {
	public static void main(String[] args) {
		Socket socket = null;
		BufferedWriter out = null;
		Scanner scanner = new Scanner(System.in);
		try {
			socket = new Socket("localhost", 9999);
			System.out.println("서버에 접속하였습니다.");
			out = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
			while (true) {
				System.out.print("보낼 정수 입력>>");
				String outputMessage = scanner.nextLine();
				try {
					int n = Integer.parseInt(outputMessage);
					out.write(outputMessage+"\n");
					out.flush();
					if(n < 0) {
						System.out.print("연결을 종료합니다.");
						break;
					}
				} catch (NumberFormatException e) {
					System.out.println("오류. 다시 입력...");
					continue;
				}
			}
		} catch (IOException e) {
			System.out.println("입출력 오류가 발생했습니다.");
		}
		try {
			socket.close();
		} catch (Exception e) {}
	}

}
