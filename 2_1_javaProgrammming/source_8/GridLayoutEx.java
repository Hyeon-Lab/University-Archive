import java.awt.*;
import javax.swing.*;

public class GridLayoutEx extends JFrame {
	public GridLayoutEx() {
		super("GridLayout 예제");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);		
		Container contentPane = getContentPane(); // 컨텐트팬 알아내기
		
		contentPane.setLayout(new GridLayout(1, 10)); // 1x10의 GridLayout 배치관리자
		
		for(int i=0; i<10; i++) { // 10 개의 버튼 부착
 			String text = Integer.toString(i);	// 정수 i를 문자열로 변환
			JButton button = new JButton(text); // 버튼 컴포넌트 생성
			contentPane.add(button); // 컨텐트팬에 버튼 부착
		}
		setSize(500,200);
		setVisible(true);
	}
	public static void main(String[] args) {
		new GridLayoutEx();
	}
}
