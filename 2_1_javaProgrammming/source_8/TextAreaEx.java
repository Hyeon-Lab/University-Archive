import javax.swing.*;
import java.awt.event.*;
import java.awt.*;

public class TextAreaEx extends JFrame {
	private JTextField tf = new JTextField(20);
	private JTextArea ta = new JTextArea(7, 20); // 한줄에 20개 입력가능 x 7줄 입력창
	
	public TextAreaEx() {
		setTitle("텍스트영역 만들기  예제");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		Container c = getContentPane();
		c.setLayout(new FlowLayout());

		c.add(new JLabel("입력 후 <Enter> 키를 입력하세요"));
		c.add(tf);
		c.add(new JScrollPane(ta));
		
				
		setSize(300,250);
		setVisible(true);
	}
		
	public static void main(String [] args) {
		new TextAreaEx();
	}
}