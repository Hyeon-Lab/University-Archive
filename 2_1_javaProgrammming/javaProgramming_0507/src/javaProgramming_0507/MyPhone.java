package javaProgramming_0507;

import java.awt.*;
import javax.swing.*;

public class MyPhone extends JFrame{
	public MyPhone() {
		
		setTitle("Panel Demo");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		
		Container c = getContentPane();
		
		JPanel lcdJPanel = new JPanel();
		JPanel keyJPanel = new JPanel();
		lcdJPanel.setLayout(new GridLayout (1, 1));
		keyJPanel.setLayout (new GridLayout(5, 3));
		
		String lcdOutput = "";
		JTextArea lcdJTextArea = new JTextArea(lcdOutput, 5, 10 ); 
		lcdJPanel.add(lcdJTextArea);
		
		JButton keyJButton[];
		keyJButton = new JButton[15];
		
		String button[] = {"Send", "clr", "End", "1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "0", "#"};
		
		for(int i=0 ; i<15 ; i++) {
			keyJButton[i] = new JButton(button[i]);
			keyJPanel.add(keyJButton[i]);
		}
		
		c.setLayout(new BorderLayout(2,1));
		c.add(lcdJPanel, BorderLayout.NORTH);
		c.add(keyJPanel, BorderLayout.CENTER);
		
		setSize(300,500);
		setVisible(true);
	}
	
	public static void main(String[] args) {
		MyPhone frame = new MyPhone();
	}
}
