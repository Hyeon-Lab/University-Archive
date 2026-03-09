package Chapter9_EventListener_Adapter_Key_Mouse;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.*;

public class ex01 extends JFrame{
	public ex01() {
		setTitle("ex01");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		Container c = getContentPane();
		c.setLayout(new FlowLayout());
		
		JButton b1 = new JButton("Button1");
		JButton b2 = new JButton("Button2");
		
		b1.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				JOptionPane.showMessageDialog(null, "You Pressed : " + e.getActionCommand());	
			}
		});
		
		b2.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				JOptionPane.showMessageDialog(null, "You Pressed : " + e.getActionCommand());	
			}
		});
		
		c.add(b1);
		c.add(b2);
		
		setSize(300, 300);
		setVisible(true);
	}
	public static void main(String[] args) {
		new ex01();
	}
}
