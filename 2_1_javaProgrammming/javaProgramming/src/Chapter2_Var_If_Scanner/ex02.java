package Chapter2_Var_If_Scanner;

import java.util.Scanner;

public class ex02 {
	public static void main(String[] args) {
		System.out.print("커피 주문 히세요 >> ");
		
		Scanner s = new Scanner(System.in);
		
		String menu = s.next();
		int num = s.nextInt();
		
		if(menu.equals("카푸치노")) {
			System.out.println(3000 * num + "원 입니다.(if)");
		}
		else if(menu.equals("에스프레소")) {
			System.out.println(2000 * num + "원 입니다.(if)");
		}
		else if(menu.equals("아메리카노")) {
			System.out.println(2500 * num + "원 입니다.(if)");
		}
		else if(menu.equals("카페라테")) {
			System.out.println(3500 * num + "원 입니다.(if)");
		}
		else {
			System.out.println("잘못된 입력입니다.(if)");
		}
		
		switch(menu) {
		case "카푸치노":
			System.out.println(3000 * num + "원 입니다.(switch)");
			break;
		case "에스프레소":
			System.out.println(2000 * num + "원 입니다.(switch)");
			break;
		case "아메리카노":
			System.out.println(2500 * num + "원 입니다.(switch)");
			break;
		case "카페라테":
			System.out.println(3500 * num + "원 입니다.(switch)");
			break;
		default:
				System.out.println("잘못된 입력입니다.(switch)");
		}
		
		s.close();
	}
}
