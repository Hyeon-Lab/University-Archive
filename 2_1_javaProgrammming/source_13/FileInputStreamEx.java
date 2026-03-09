import java.io.*;

public class FileInputStreamEx {
	public static void main(String[] args) {
		byte b[] = new byte [6]; // 비어 있는 byte 배열
		try {
			// "c:\\Temp\\test.out" 파일을 읽어 배열 b에 저장
			FileInputStream fin = new FileInputStream("c:\\Temp\\test.out");
			int n=0, c;
			while((c = fin.read())!= -1) {
				b[n] = (byte)c; // 읽은 바이트를 배열에 저장
				n++;
			}
			// 배열 b의 바이트 값을 모두 화면에 출력
			System.out.println("c:\\Temp\\test.out에서 읽은 배열을 출력합니다.");
			for(int i=0; i<b.length; i++) // 배열 b 출력
				System.out.print(b[i]+" ");
			System.out.println();
			
			fin.close();
		} catch(IOException e) { }
	}
}