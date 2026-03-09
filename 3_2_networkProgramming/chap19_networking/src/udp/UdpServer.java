package udp;

import java.net.DatagramPacket;
import java.net.DatagramSocket;

public class UdpServer {
    public static void main(String[] args) throws Exception {
        DatagramSocket socket = new DatagramSocket(9000); // 서버 포트 지정
        byte[] buf = new byte[1024];

        System.out.println("UDP 서버 대기 중...");
        while (true) {
            // [Rx] Server <-- Client
            DatagramPacket recvPacket = new DatagramPacket(buf, buf.length);
            socket.receive(recvPacket);
            
            String msg = new String(recvPacket.getData(), 0, recvPacket.getLength(), "UTF-8");
            System.out.println("수신: " + msg);

            // [Tx] Server --> Client
            String resp = "서버가 받은 데이터: " + msg;
            byte[] sendBuf = resp.getBytes("UTF-8");
            
            DatagramPacket sendPacket =
                new DatagramPacket(sendBuf, sendBuf.length, recvPacket.getAddress(), recvPacket.getPort());
            socket.send(sendPacket);
        }
    }
}
