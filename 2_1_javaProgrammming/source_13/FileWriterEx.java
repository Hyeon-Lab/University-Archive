import java.io.*;

public class FileWriterEx {
	public static void main(String[] args) {
		InputStreamReader in = new InputStreamReader(System.in); // 문자 입력 스트림 생성
		
		FileWriter fout = null;
		int c;
		try {
			fout = new FileWriter("c:\\Temp\\test.txt"); // 파일과 연결된 출력 문자 스트림 생성
			while ((c = in.read()) != -1) {
				fout.write(c); // 키보드로부터 입력받은 문자를 파일에 저장
			}
            in.close();
            fout.close();
		} catch (IOException e) {
			System.out.println("입출력  오류");
		}
	}
}