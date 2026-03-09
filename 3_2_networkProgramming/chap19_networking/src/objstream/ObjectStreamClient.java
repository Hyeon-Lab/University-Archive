package objstream;

import java.io.*;
import java.net.Socket;

public class ObjectStreamClient {
    public static void main(String[] args) throws Exception {
        Socket socket = new Socket("localhost", 9000);

        try (ObjectOutputStream oos = new ObjectOutputStream(socket.getOutputStream());
             ObjectInputStream ois = new ObjectInputStream(socket.getInputStream())) {

            // [Tx] Client ----> Server
        	//           byte stream
            Person p1 = new Person(1234, "Alice", "alice@knu.ac.kr");
            oos.writeObject(p1);
            oos.flush();
            System.out.println("Client [Tx] " + p1);

            // [Rx] Client <---- Server
            Object obj = ois.readObject();
            if (obj instanceof Person) {
                Person p2 = (Person) obj;
                System.out.println("Client [Rx] " + p2);                
            }
        }
        socket.close();
    }
}
