package Chapter8_Gui_Swing_Layout;

import java.awt.*;
import javax.swing.*;
public class MyFrame extends JFrame {
	public MyFrame() {
		setTitle("Title....");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		Container c = getContentPane();
		c.setLayout(new FlowLayout());
		
		
		
		setSize(300, 300);
		setVisible(true);
	}
	public static void main(String[] args) {
		new MyFrame();
	}
}