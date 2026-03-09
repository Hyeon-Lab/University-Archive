package Chapter6_Wrapper_String_StringBuffer_Token;

class Point2{
	private int x, y;
	public Point2(int x, int y) {
		this.x = x; this.y = y;
	}
	public String toString() {
		return "Point(" + x + ", " + y + ")";
	}
}

public class ToStringEx {
	public static void main(String[] args) {
		Point2 a = new Point2(2,3);
		System.out.println(a.toString());
		System.out.println(a);
	}
}
