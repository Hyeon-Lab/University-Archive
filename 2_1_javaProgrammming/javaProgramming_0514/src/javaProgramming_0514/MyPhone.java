package javaProgramming_0514;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.*;

public class MyPhone extends JFrame{
	String lcdOutput = "";
	JTextArea lcdJTextArea = new JTextArea(lcdOutput, 5, 10 );
	
	public MyPhone() {
		Container c = getContentPane();
		setTitle("Panel Demo");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		
		JPanel lcdJPanel = new JPanel();
		JPanel keyJPanel = new JPanel();
		
		lcdJPanel.setLayout(new GridLayout (1, 1));
		keyJPanel.setLayout (new GridLayout(5, 3));
		lcdJPanel.add(lcdJTextArea);
		
		JButton keyJButton[];
		keyJButton = new JButton[15];
		
		String button[] = {"Send", "clr", "End", "1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "0", "#"};
		
		for(int i=0 ; i<15 ; i++) {
			keyJButton[i] = new JButton(button[i]);
			keyJButton[i].addActionListener(new buttonListener());;
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
	
	class buttonListener implements ActionListener {
		public void actionPerformed(ActionEvent e) {
			switch(e.getActionCommand()) {
			case "Send":
				lcdOutput += "\n전화거는중...";
				MyPhone.this.lcdJTextArea.setText(lcdOutput);
				lcdOutput = "";
				break;
			case "clr":
				int a = lcdOutput.length();
				if(a>=1) {
					lcdOutput = lcdOutput.substring(0, a - 1);
					MyPhone.this.lcdJTextArea.setText(lcdOutput);
				}
				break;
			case "End":
				lcdOutput = "";
				MyPhone.this.lcdJTextArea.setText(lcdOutput);
				break;
			default:
				lcdOutput += e.getActionCommand();
				MyPhone.this.lcdJTextArea.setText(lcdOutput);
			}
		}
	}
}
