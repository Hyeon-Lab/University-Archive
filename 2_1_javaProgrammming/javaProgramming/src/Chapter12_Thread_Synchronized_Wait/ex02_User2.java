package Chapter12_Thread_Synchronized_Wait;

public class ex02_User2 extends Thread {
	private ex02_Calculator calculator;

	public void setCalculator(ex02_Calculator calculator) {
		this.setName("User2");
		this.calculator = calculator;
	}
	@Override
	public void run() {
		calculator.setMemory(50);
	}
}
