package Chapter6_Wrapper_String_StringBuffer_Token;

class BasicMath{
	public static double sum(double a, double b) {return a + b;}
	public static double sub(double a, double b) {return a - b;}
	public double mul(double a, double b) {return a * b;}
}

class Basic2Math{
	private double a; private double b;
	public Basic2Math(double a, double b) {
		this.a = a; this.b = b;
	}
	public void setA(double a) {
		this.a = a;
	}
	public void setB(double b) {
		this.b = b;
	}
	public double sum() {
		return BasicMath.sum(a, b);
	}
	public double sub() {
		return BasicMath.sub(a, b);
	}
	public double mul() {
		BasicMath m = new BasicMath();
		return m.mul(a, b);
	}
	@Override
	public boolean equals(Object obj) {
		Basic2Math m = (Basic2Math) obj;
		if(a == m.a && b == m.b) return true;
		else return false;
	}
}

public class ex01 {
	public static void main(String[] args) {
		Basic2Math m = new Basic2Math(3.0, 2.0);
		System.out.println("Sum a + b = " + m.sum());
		System.out.println("Sub a - b = " + m.sub());
		System.out.println("Mul a * b = " + m.mul());
		
		Basic2Math m2 = new Basic2Math(3.0, 2.0);
		if(m.equals(m2)) {
			System.out.println("두 인스턴스는 값이 같다.");
		}
	}
}
