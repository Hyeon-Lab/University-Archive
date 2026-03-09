/**
 * ByteArrayOutputStream 을 이용한 소켓 통신 클라이언트
 * - 직렬화된 Packet을 byte[]로 변환해서 전송 
 * - 문제점: C server에서 역직렬화를 할 방법이 없음  
 * 
 */
package bytestream;

import java.io.*;
import java.net.*;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;


public class PacketByteArrayOutputClientApp {
	
	public static byte[] convertToByteArray(Packet packet) {
		byte[] bytePacket = null;
		
		ByteArrayOutputStream bout = null;
		ObjectOutputStream oos = null;
		
		try {	
			bout = new ByteArrayOutputStream();
			oos = new ObjectOutputStream(bout);
			
			/*
			 *  packet 객체를 ObjectOutputStream에 저장
			 *  -> ByteArrayOutputStream에 저장됨: Memory-Based byte Array Stream
			 */
			oos.writeObject(packet);	 
			oos.flush();
			
			// ByteArrayOutputStrema 데이터를 byte[]로 저장 
			bytePacket = bout.toByteArray();
			//System.out.println(Arrays.toString(bytePacket));
			
			bout.close();
			oos.close();
			
		}catch(IOException e) {
			e.printStackTrace();
		}
		
		return bytePacket;
	}
	
	public static Packet convertToPacket(byte[] data) {
		// wrap(byte[] b): byte[]을 ByteBuffer 객체로 변환 
		ByteBuffer buffer = ByteBuffer.wrap(data);
		buffer.order(ByteOrder.LITTLE_ENDIAN);
		
		byte[] nameBytes = new byte[50];
		buffer.get(nameBytes);
		String name = new String(nameBytes, StandardCharsets.UTF_8).strip();
		
		int id = buffer.getInt();
		int score = buffer.getInt();
		double average = buffer.getDouble();
		
		return new Packet(name, id, score, average);
	}
	
	public static void main(String[] args) {
		Socket socket = null;
			
		//byte[] rxData = new byte[66];
		//System.out.println("[Tx]: " + packet);
		
		try {
			socket = new Socket("155.230.120.235", 9999);
			
			InputStream in = socket.getInputStream();
			OutputStream out = socket.getOutputStream();
			
			Packet packet = new Packet("Hong GilDong", 1000, 95, 90.2);
			byte[] txPacket = convertToByteArray(packet);
			
			System.out.printf("[Tx] len: %d\n", txPacket.length);
			
			out.write(txPacket); 	// 서버로 전송
			out.flush();
			
			in.close();
			out.close();
		}catch(IOException e) {
			System.out.println("IOException: " + e.toString());
		}finally {
			try {
				if(socket != null)
					socket.close();
				
			}catch(IOException e) {
				e.printStackTrace();
			}
		}
	}
}
