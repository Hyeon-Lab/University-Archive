package Chapter4_Class_Static_Final;

class Sample {
	public int a;
	private int b;
	int c;
	
	public int getB() {
		return b;
	}
	public void setB(int b) {
		this.b = b;
	}
}

public class AccessEx {
	public static void main(String[] args) {
		Sample aClass = new Sample();
		aClass.a = 10;
		//aClass.b = 10; 사용시 오류 발생
		aClass.setB(10);
		aClass.c = 10;
		
		System.out.println(aClass.a);
		System.out.println(aClass.getB());
		System.out.println(aClass.c);
	}
}
