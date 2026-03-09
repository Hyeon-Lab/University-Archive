
import java.net.InetAddress;
import java.net.UnknownHostException;

public class InetAddressExample {

	public static void main(String[] args) {
		try {
			InetAddress local = InetAddress.getLocalHost();
			System.out.println("local: " + local);
			System.out.println("HostName: " + local.getHostName());
			System.out.println("My Computer IP address: " + local.getHostAddress());
			
			InetAddress[] iaArray = InetAddress.getAllByName("www.google.com");
			for(InetAddress remote : iaArray)
				System.out.println("Google IP 주소: " + remote.getHostAddress());
			   
		}catch(UnknownHostException e) {
			e.printStackTrace();
		}
	}
}
