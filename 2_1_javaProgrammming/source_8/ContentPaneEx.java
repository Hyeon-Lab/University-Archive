import javax.swing.*;
import java.awt.*;
public class ContentPaneEx extends JFrame {
	public ContentPaneEx() {
		setTitle("ContentPane Example");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		
		Container contentPane = getContentPane();
		JButton b1 = new JButton("OK");
		JButton b2 = new JButton("Cancel");
		JButton b3 = new JButton("Ignore");
		
		contentPane.setBackground(Color.ORANGE);
		contentPane.setLayout(new FlowLayout()); 
		
		contentPane.add(b1);
		contentPane.add(b2);
		contentPane.add(b3);
		
		setSize(300, 150);
		setVisible(true);
	}
	public static void main (String[] args) {
		new ContentPaneEx();
	}

}
