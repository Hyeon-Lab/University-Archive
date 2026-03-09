package bytestream;
import java.io.*;
import java.util.Arrays;

public class ByteArrayOutputEx01 {
	
	public static void main(String[] args) {
		try {
			Packet packet = new Packet("Hong GilDong", 1000, 95, 90.2);			

			ByteArrayOutputStream bout = new ByteArrayOutputStream();
			ObjectOutputStream oos = new ObjectOutputStream(bout);
			
			/*
			 *  packet 객체를 ObjectOutputStream에 저장
			 *  -> ByteArrayOutputStream에 저장됨: Memory-Based byte Array Stream
			 */
			oos.writeObject(packet);	 
			oos.flush();
			
			// ByteArrayOutputStrema 데이터를 byte[]로 저장 
			byte[] bytePacket = bout.toByteArray();
			System.out.println(Arrays.toString(bytePacket));
			
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}

}
