package Chapter5_Extend_Override_Abstract_Interface;

class MyPoint{
	private int x, y;
	protected MyPoint() {
		x = 100; y = 200;
	}
	protected void disp() {
		System.out.println("점(x, y) = (" + x + ", " + y + ")");
	}
}

class MyCircle extends MyPoint{
	int r;
	public MyCircle(){
		r = 50;
	}
	//@Override
	public void disp() {
		super.disp();
		System.out.println("반지름 r = " + r);
	}
}

class MyRect extends MyPoint{
	int w, h;
	public MyRect() {
		w = 200; h = 300;
	}
	//@Override
	public void disp() {
		super.disp();
		System.out.println("폭 = " + w + ", 높이 = " + h);
	}
}

public class ex01 {
	public static void main(String args) {
		MyCircle c = new MyCircle();
		MyRect r = new MyRect();
		
		c.disp();
		r.disp();
	}
}
