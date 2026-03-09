package Chapter14_Server_Client_Socket;

import java.io.IOException;
import java.net.*;

public class ClientEx2 {
	public static void main(String[] args) {
		Socket socket = null;
		try {
			socket = new Socket("localhost", 9999);
		} catch (IOException e) {}
		try {
			socket.close();
		} catch (Exception e) {}
	}

}
