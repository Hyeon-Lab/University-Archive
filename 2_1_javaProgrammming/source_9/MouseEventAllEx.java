import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
public class MouseEventAllEx extends JFrame {
	private JLabel la = new JLabel("Move Me");
	public MouseEventAllEx() {
		setTitle("MouseListener¿Í MouseMotionListener ¿¹Á¦");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		Container c = getContentPane();
		c.setLayout(null);
		//TO DO
		MyMouseListener listener = new MyMouseListener();
		c.addMouseListener(listener);
		c.addMouseMotionListener(listener);
		la.setSize(50, 20);
		la.setLocation(30, 30);
		c.add(la);
		
		setSize(300, 300);
		setVisible(true);
	}
	class MyMouseListener implements MouseListener, MouseMotionListener {
		public void mousePressed(MouseEvent e) {
			la.setLocation(e.getX(), e.getY());
			setTitle("mouse Pressed");
		};
		public void mouseReleased(MouseEvent e) {
			la.setLocation(e.getX(), e.getY());
			setTitle("mouse Released");
		};
		public void mouseEntered(MouseEvent e) {
			Component comp = (Component)e.getSource();
			comp.setBackground(Color.CYAN);
		};
		public void mouseClicked(MouseEvent e) {};
		public void mouseExited(MouseEvent e) {
			Component comp = (Component)e.getSource();
			comp.setBackground(Color.YELLOW);
			setTitle("mouse Exited");
		};
		public void mouseDragged(MouseEvent e) {
			la.setLocation(e.getX(), e.getY());
			setTitle("mouse Dragged " + e.getX() + ", " +e.getY());
		};
		public void mouseMoved(MouseEvent e) {
			la.setLocation(e.getX(), e.getY());
			setTitle("mouse Moved " + e.getX() + ", " +e.getY());
		};
		
	}
	
	
	public static void main(String[] args) {
		new MouseEventAllEx();
	}
}