import java.io.*;

public class FileReaderEx {
	public static void main(String[] args) {
		FileReader in = null;
		try {
			in = new FileReader("c:\\windows\\system.ini"); // 문자 입력 스트림 생성
	        int c;
            while ((c = in.read()) != -1) { // 문자 단위로 파일 끝까지 읽는다.
                System.out.print((char)c);
            }
			in.close();
		}
		catch (IOException e) {
			System.out.println("입출력 오류");
		}
	}
}