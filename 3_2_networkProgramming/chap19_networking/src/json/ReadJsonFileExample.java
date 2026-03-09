package json;
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.io.Reader;

import org.json.JSONArray;
import org.json.JSONObject;

public class ReadJsonFileExample {

	public static void openBufferedReader() {	
		try(BufferedReader br = new BufferedReader(new FileReader("sample.json"))) {
			
			String json = br.readLine(); // '\n'때문에 1줄만 읽어옴 
			
			System.out.println(json);
			br.close();
		}catch(IOException e) {
			e.printStackTrace();
		}		
	}
	
	
	public static void openFileReader() {
		// JSON 파일 읽기
		try(Reader reader = new FileReader("sample.json")) {
			char[] buffer = new char[1024];
			int len = reader.read(buffer);
			String jsonReadString = new String(buffer, 0, len);
			
			JSONObject obj = new JSONObject(jsonReadString);
			// 들여 쓰기(4칸)
			System.out.println(obj.toString(4));
						
			System.out.println("name" + obj.getString("name"));
			System.out.println("city: " + obj.getJSONObject("address").getString("city"));
			
			// JSONArray 객체 읽기 
			JSONArray hobbies = obj.getJSONArray("hobbies");
			System.out.println("hobbies: " + hobbies);
			
			for(int i=0; i<hobbies.length(); i++) {
				//System.out.print(hobbies.getString(i) + " ");
				System.out.println(hobbies.get(i));
			}			
			
			reader.close();
			
		}catch(IOException e) {
			e.printStackTrace();
		}
	}
	
	
	public static void main(String[] args) {
		//openBufferedReader();
		// JSON 파일 읽기
		try(Reader reader = new FileReader("sample.json")) {
			char[] buffer = new char[1024];
			int len = reader.read(buffer);
			String jsonReadString = new String(buffer, 0, len);
					
			JSONObject obj = new JSONObject(jsonReadString);
			// 들여 쓰기(4칸)
			System.out.println(obj.toString(4));
								
			System.out.println("name: " + obj.getString("name"));
			System.out.println("city: " + obj.getJSONObject("address").getString("city"));
					
			// JSONArray 객체 읽기 
			JSONArray hobbies = obj.getJSONArray("hobbies");
			System.out.println("hobbies: " + hobbies);
					
			for(int i=0; i<hobbies.length(); i++) {
				//System.out.print(hobbies.getString(i) + " ");
				System.out.println(hobbies.get(i));
			}			
					
			reader.close();
					
		}catch(IOException e) {
			e.printStackTrace();
		}
	}
}
