package objstream;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;

public class ObjectStreamServer {
    public static void main(String[] args) throws Exception {
        ServerSocket serverSocket = new ServerSocket(9000);
        System.out.println("서버 대기 중...");
        
        try (Socket client = serverSocket.accept();
             ObjectInputStream ois = new ObjectInputStream(client.getInputStream());
             ObjectOutputStream oos = new ObjectOutputStream(client.getOutputStream())) {

            // 클라이언트로부터 Person 객체 받기
        	// [Rx] Server <---- Client
        	//             byte stream 
            Object obj = ois.readObject();
            if (obj instanceof Person) {
                Person person1 = (Person) obj;
                System.out.println("Server [Rx] " + person1);
            }
            
            // Person 객체 전송 
            // [Tx] Server ----> Client             
            Person person2 = new Person(5678, "Bob", "bob@knu.ac.kr");
            oos.writeObject(person2);
            oos.flush();
            System.out.println("Server [Tx] " + person2);            
        }
        serverSocket.close();
    }
}
