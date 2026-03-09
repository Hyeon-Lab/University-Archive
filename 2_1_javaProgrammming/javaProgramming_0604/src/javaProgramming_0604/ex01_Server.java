package javaProgramming_0604;
import java.io.*;
import java.net.*;
import java.util.*;

public class ex01_Server {
	public static void main(String[] args) {
		ServerSocket listener = null;
		Socket socket = null;
		BufferedReader in = null;
		BufferedWriter out = null;
		int n1 = 0; int n2 = 0;
		System.out.println("연결을 기다리고 있습니다.....");
		try {
			listener = new ServerSocket(9999);
			socket = listener.accept();
			System.out.println("연결되었습니다.");
			in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
			out = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));
			while (true) {
				String inputMessage = in.readLine();
				if(inputMessage.equalsIgnoreCase("bye")) {
					System.out.println("클라이언트에서 연결을 종료하였음");
					break;
				}
				Integer sum = 0;
				StringTokenizer st = new StringTokenizer(inputMessage, " ");
				n1 = Integer.parseInt(st.nextToken());
				n2 = Integer.parseInt(st.nextToken());
				sum = n1 + n2;
				out.write("계산 결과 : "+sum.toString()+"\n");
				out.flush();
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

