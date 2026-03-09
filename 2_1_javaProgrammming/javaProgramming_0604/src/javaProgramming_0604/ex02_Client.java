package javaProgramming_0604;
import java.io.*;
import java.net.*;
import java.util.*;

public class ex02_Client {
	public static void main(String[] args) {
		Socket socket = null;
		BufferedWriter out = null;
		Scanner scanner = new Scanner(System.in);
		try {
			socket = new Socket("localhost", 9999);
			out = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
			System.out.println("서버에 접속하였습니다...");
			while (true) {
				System.out.print("텍스트 입력 >> ");
				String outputMessage = scanner.nextLine();
				out.write(outputMessage+"\n");
				out.flush();
				if(outputMessage.equalsIgnoreCase("끝")) {
					System.out.print("연결을 종료합니다.");
					break;
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

