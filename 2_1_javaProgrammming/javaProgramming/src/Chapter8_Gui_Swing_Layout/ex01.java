package Chapter8_Gui_Swing_Layout;

import java.awt.*;
import javax.swing.*;

public class ex01 extends JFrame {
	public ex01() {
		setTitle("ex01");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		Container c = getContentPane();
		c.setLayout(new BorderLayout(5, 5));
		c.add(new JButton("Menu"), BorderLayout.NORTH);
		c.add(new JButton("Console"), BorderLayout.SOUTH);
		c.add(new JButton("Dir"), BorderLayout.WEST);
		c.add(new JButton("Editor"), BorderLayout.CENTER);
		setSize(300, 300);
		setVisible(true);
	}
	public static void main(String[] args) {
		new ex01();
	}
}
