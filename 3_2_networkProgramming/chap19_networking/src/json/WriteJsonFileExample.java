package json;

import java.io.*;

import org.json.JSONArray;
import org.json.JSONObject;

/*
  // 저장할 JSON 객체 타입 
  {
   “name” : “홍길동”,
   “age”: 28,
   “address”: {“city” : “Seoul”, “zip”: “12345”}, // 중첩 JSONObject 
   “hobbies”: [“reading”, “swimming”],			// JSONArray 객체 
   “spouse”: null
   }
*/

public class WriteJsonFileExample {

	public static void main(String[] args) {
		// 1. JSONObject 생성 
		JSONObject obj = new JSONObject();
		
		// 속성 추가 
		obj.put("name", "홍길동");
		obj.put("age", 28);
		
		JSONObject address = new JSONObject();
		address.put("city", "서울");
		address.put("zip", "12345");
		obj.put("address", address);
		
		// JSONArray 객체 생성 
		JSONArray hobbies = new JSONArray();
		hobbies.put("reading");
		hobbies.put("swimming");
		
		// JSONArray객체를 JSONObject에 추가 
		obj.put("hobbies", hobbies);		
		obj.put("spouse", false);
		
		String jsonString = obj.toString(4); // 들여쓰기(4칸)
		
		System.out.println(jsonString);
		
		// 2. JSON 객체를 파일로 저장 
		try(Writer file = new FileWriter("sample.json")) {
			file.write(jsonString);
			file.flush();
			file.close();
		}catch(IOException e) {
			e.printStackTrace();
		}
		System.out.println("sample.json 파일 저장 완료");
		
		
		// 3. 파일 읽기
		try(Reader reader = new FileReader("sample.json")) {
			char[] buffer = new char[1024];
			int len = reader.read(buffer);
			String jsonReadString = new String(buffer, 0, len);
			
			JSONObject readObj = new JSONObject(jsonReadString);
			System.out.println(readObj.toString());
			System.out.println("이름: " + readObj.getString("name"));
			System.out.println("도시: " + readObj.getJSONObject("address").getString("city"));
			reader.close();
			
		}catch(IOException e) {
			e.printStackTrace();
		}
		
	}
}
