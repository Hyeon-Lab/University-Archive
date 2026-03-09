
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.BufferedReader;
import java.net.URI;
import java.net.URL;
import java.net.URLConnection;

public class URLConnectionExample01 {

	public static void main(String[] args) {

		try {
			// 1. URL 객체 생성: Java 20이후 URL() 생성자 사용 deprecated 			
			URL url = new URI("http://www.google.com").toURL();
			
			// 2. URLConnection 객체 얻기 
			URLConnection conn = url.openConnection();
			conn.setConnectTimeout(5000);	// 5000ms
			
			// 3. 접속 및 데이터 읽기 
			InputStream is = conn.getInputStream();
			BufferedReader reader = new BufferedReader(new InputStreamReader(is));
			String line = "";
			
			while((line = reader.readLine()) != null) {
				System.out.println(line);
			}
			
			reader.close();
		} catch (Exception e) {
			e.printStackTrace();
		} 

	}

}
