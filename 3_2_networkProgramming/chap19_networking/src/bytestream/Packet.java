package bytestream;

import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.nio.charset.StandardCharsets;

public class Packet {		// 66 bytes
	private String name;	// 50 bytes
	private int id;			// 4 bytes
	private int score;		// 4 bytes
	private double average;	// 8 bytes

	public Packet(String name, int id, int score, double average) {
		this.name = name;
		this.id = id;
		this.score = score;
		this.average = average;
	}
	
	/**
	 * 생성자에서 byte[]을 Packet 객체로 변환 
	 * @param data
	 */
	public Packet(byte[] data) {
		// wrap(byte[] b): byte[]을 ByteBuffer 객체로 변환 
		ByteBuffer buffer = ByteBuffer.wrap(data);
		buffer.order(ByteOrder.LITTLE_ENDIAN);
				
		byte[] nameBytes = new byte[50];
		buffer.get(nameBytes);
		
		this.name = new String(nameBytes, 
								StandardCharsets.UTF_8).strip();				
		this.id = buffer.getInt();
		this.score = buffer.getInt();
		this.average = buffer.getDouble();
	}
	
	/**
	 * Packet 객체를 byte[] 배열로 변환해서 리턴 
	 * - C Server로 전송하기 전에 Packet 객체를 byte[]로 변환
	 *  
	 * @return: byte[]
	 */
	public byte[] convertToBytes() {
		ByteBuffer buffer = ByteBuffer.allocate(66); // 66 바이트의 ByteBuffer 객체 생성
		buffer.order(ByteOrder.LITTLE_ENDIAN);	// Little Endian으로 설정 
		
		byte[] nameBytes = new byte[50];	// 50 bytes로 고정 
		byte[] nameRawBytes = name.getBytes(StandardCharsets.UTF_8);		
		int length = nameRawBytes.length;
		
		// arraycopy(src, srcPos, dest, destPos, length)
		// 빈 공간은 0으로 padding
		System.arraycopy(nameRawBytes, 0, nameBytes, 0, length);
		
		buffer.put(nameBytes);		
		buffer.putInt(id);
		buffer.putInt(score);
		buffer.putDouble(average);
		
		return buffer.array();
	}

	public String toString() {
		return String.format("name: %s, id: %d, score: %d, avarage: %.1f", 
				this.name, this.id, this.score, this.average);
	}
}
