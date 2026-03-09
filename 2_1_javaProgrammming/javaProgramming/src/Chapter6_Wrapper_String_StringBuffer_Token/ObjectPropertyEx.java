package Chapter6_Wrapper_String_StringBuffer_Token;

class Point1 {
	private int x, y;
	public Point1(int x, int y) {
		this.x = x; this.y = y;
	}
}

public class ObjectPropertyEx {
	public static void main(String[] args) {
		Point1 p = new Point1(2, 3);
		System.out.println(p.getClass().getName());
		System.out.println(p.hashCode());
		System.out.println(p.toString());
	}
}
