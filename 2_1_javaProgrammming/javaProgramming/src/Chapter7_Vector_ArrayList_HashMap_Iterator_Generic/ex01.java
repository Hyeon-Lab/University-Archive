package Chapter7_Vector_ArrayList_HashMap_Iterator_Generic;

import java.util.*;

public class ex01 {
	public static void main(String[] args) {
		ArrayList<String> a = new ArrayList<String>(5);
		Scanner s = new Scanner(System.in); 
		
		for(int i=0; i<5; i++) {
			System.out.print("학점을 입력하시오 >> ");
			a.add(s.next());
		}
		
		for(int i=0;i<5;i++) {
			switch(a.get(i)) {
			case "A":
				System.out.print("A:4.0 ");
				break;
			case "B":
				System.out.print("B:3.0 ");
				break;
			case "C":
				System.out.print("C:2.0 ");
				break;
			case "D":
				System.out.print("D:1.0 ");
				break;
			case "F":
				System.out.print("F:0.0 ");
				break;
			default:
				System.out.print(a.get(i) + ": 잘 못 입력하였습니다. ");
			}
		}
	}
}
