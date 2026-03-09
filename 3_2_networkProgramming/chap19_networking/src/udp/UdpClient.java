package udp;

import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class UdpClient {
    public static void main(String[] args) throws Exception {
        DatagramSocket socket = new DatagramSocket();
        InetAddress addr = InetAddress.getByName("127.0.0.1");
        int port = 9000;

        String msg = "Hello UDP Server!";
        byte[] buf = msg.getBytes("UTF-8");
        DatagramPacket sendPacket = new DatagramPacket(buf, buf.length, addr, port);
        socket.send(sendPacket);

        // 응답 수신
        byte[] recvBuf = new byte[1024];
        DatagramPacket recvPacket = new DatagramPacket(recvBuf, recvBuf.length);
        socket.receive(recvPacket);
        String response = new String(recvPacket.getData(), 0, recvPacket.getLength(), "UTF-8");
        System.out.println("서버 응답: " + response);
        socket.close();
    }
}
