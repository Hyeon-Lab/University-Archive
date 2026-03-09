package javaProgramming_0604;
import java.io.*;
import java.net.*;
import java.util.*;

public class ex01_Client {
	public static void main(String[] args) {
		Socket socket = null;
		BufferedReader in = null;
		BufferedWriter out = null;
		Scanner scanner = new Scanner(System.in);
		try {
			socket = new Socket("localhost", 9999);
			out = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
			while (true) {
				System.out.print("두 정수를 빈칸으로 띄어 입력, 예:24 42) >>");
				String outputMessage = scanner.nextLine();
				out.write(outputMessage+"\n");
				out.flush();
				if(outputMessage.equalsIgnoreCase("bye")) {
					break;
				}
				in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
				String inputMessage = in.readLine();
				System.out.println(inputMessage);
			}
		} catch (IOException e) {
			System.out.println("입출력 오류가 발생했습니다.");
		}
		try {
			socket.close();
		} catch (Exception e) {}
	}

}

