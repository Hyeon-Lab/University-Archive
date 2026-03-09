/**
 * ByteBuffer를 이용한 소켓 클라이언트 
 * Java Client <--> C Server
 * 
 */
package bytestream;

import java.io.*;
import java.net.*;

public class PacketClient {
	
	public static void main(String[] args) {
		final int PACKET_SIZE = 66;
		int readBytes = 0;
		
		try {
			Socket socket = new Socket("155.230.120.235", 9190);

			OutputStream os = socket.getOutputStream();
			InputStream is = socket.getInputStream();

			/*
			 * [Tx] Java Client -> C Server  
			 */			
			Packet tx_packet = new Packet("Richard Stallman", 1000, 95, 90.2);
			byte[] send_bytes = tx_packet.convertToBytes(); // 크기 고정 
			
			System.out.printf("[Tx] %s (len: %d)\n", tx_packet, send_bytes.length);
			os.write(send_bytes);
			os.flush();
			
			/*
			 * [Rx] Java Client <- C server
			 */
			byte[] recv_bytes = new byte[PACKET_SIZE];
			
			while(readBytes < PACKET_SIZE) {
				// read(byte[] b, int offset, int len)
				int len = is.read(recv_bytes, readBytes, PACKET_SIZE);
				System.out.println("[Rx] received bytes: " + len);
				readBytes += len;
			}

			//Packet rx_packet = convertToPacket(recv_packet);
			// byte[] 데이터를 Packet 객체로 변환
			Packet rx_packet = new Packet(recv_bytes);
			System.out.println("[Rx] " + rx_packet);
						
			socket.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
