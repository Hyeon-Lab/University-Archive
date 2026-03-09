/**
 * Socket() 클래스 생성 
 * - getInputStream(): 소켓에 연결된 입력 스트림 반환 (데이터 수신 용도로 사용) 
 * - setSoTimeout(): 테이터 읽기 타임 아웃 시간 지정(0: 타임아웃 해제)
 * 
 */
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.Socket;

public class DaytimeClient {

	public static void main(String[] args) {
		String hostname = "time.nist.gov";
		Socket socket = null;
		
		try {
			socket = new Socket(hostname, 13);
			// read() 함수 호출에 대해 timeout 시간 설정 
			socket.setSoTimeout(15000);	// Socket option timeout(SO_TIMEOUT)
			
			InputStream in = socket.getInputStream(); // 소켓으로부터 바이트를 읽기 위한 스트림 
			StringBuilder strTime = new StringBuilder();
			InputStreamReader reader = new InputStreamReader(in, "ASCII");
			
			// read() 리턴값: -1: end of the stream
			int c = reader.read();
			while (c != -1) {
				strTime.append((char)c);
				c = reader.read();
			}
			
			System.out.println(strTime);
			
		}catch(IOException ex) {
			System.err.println(ex);
		}finally {
			if(socket != null) {
				try {
					socket.close();
				}catch(IOException ex) {
					ex.printStackTrace();
				}
			}
		}
		System.out.println("Socket closed");
	}
}
