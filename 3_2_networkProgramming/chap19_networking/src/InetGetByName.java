/**
 * 특정 URL의 IP 주소 출력 프로그램 
 * 	- InetAddress.getByName(url) 사용
 *  
 */


import java.net.InetAddress;
import java.net.UnknownHostException;

public class InetGetByName {

	public static void main(String[] args) {
		String oreilly_host = "www.oreilly.com";
		String googleHostName = "www.google.com";
		String hostName = "www.knu.ac.kr";

		try {			
			/*
			 *  InetAddress 클래스는 public 생성자를 제공하지 않음
			 *  대신 static 함수들을 사용함  
			 *  - getByName(String)
			 *  - getByAddress(byte[] addr)
			 *  - InetAddress.toString() 메소드 제공: 따라서 println(InetAddress 객체) 가능
			 *  	. getHostName()
			 *  	. getHostAddress() 내부 호출  
			 *  
			 */			
			InetAddress address = InetAddress.getByName(googleHostName);
			System.out.println(address);
			
//			address = InetAddress.getByName("155.230.13.40");	//208.201.239.100");
//			System.out.println(address.getHostName());	// IP주소에 대응하는 host name 출력 
			
			System.out.println("--------------------------------------");
			System.out.println("getAllByName()");
			System.out.println("--------------------------------------");
			InetAddress[] addresses = InetAddress.getAllByName(googleHostName);
			for(InetAddress addr: addresses) {
				System.out.println(addr);
			}
			
			System.out.println("--------------------------------------");
			System.out.println("getLocalHost()");
			System.out.println("--------------------------------------");
			// 코드가 실행 중인 호스트 정보 출력 
			InetAddress me = InetAddress.getLocalHost();	
			System.out.println(me.getHostName() +":" + me.getHostAddress());
			
			
		} catch (UnknownHostException e) {
			//e.printStackTrace();
			System.out.println("Could not find " + hostName);
		}
		
		System.out.println("Exit Program");
	}
}
