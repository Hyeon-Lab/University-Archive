package javaProgramming_0521;

import java.awt.*;
import java.awt.event.*;
import javax.swing.*;

public class Report12 extends JFrame {
	Report12() {
		super("쓰레드를 가진 겜블링");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setContentPane(new GamePanel()); //GamePanel을 컨텐트팬으로 등록
		setSize(300, 200);
		setVisible(true);
	}		
	class GamePanel extends JPanel { //화면 디자인
		JLabel[] label = new JLabel[3]; //3개의 레이블
		JLabel result = new JLabel("마우스를 클릭할 때마다 게임합니다."); //결과 출력
		Thread thread;/* TO DO 스레드(thread) 생성 */
		public GamePanel() {
			setLayout(null); //절대 위치에 컴포넌트 배치
			for(int i=0; i<label.length; i++) {
				label[i] = new JLabel("0"); //초기 레이블 생성
				label[i].setSize(60, 30); //레이블 크기
				label[i].setLocation(30+80*i, 50); //레이블 위치
				label[i].setHorizontalAlignment(JLabel.CENTER);
				label[i].setOpaque(true); //레이블에 배경색 설정이 가능하도록 설정
				label[i].setBackground(Color.MAGENTA);
				label[i].setForeground(Color.YELLOW);
				label[i].setFont(new Font("Tahoma", Font.ITALIC, 30));
				add(label[i]);
			}
			result.setHorizontalAlignment(JLabel.CENTER); //결과를 출력할 레이블 생성
			result.setSize(250, 20);
			result.setLocation(30, 120);
			add(result);
			
			thread = new GamblingThread(label, result); /* TO DO 쓰레드 시작 */
			thread.start(); 
			
			addMouseListener(new MouseAdapter() { //마우스 리스너 구현
				public void mousePressed(MouseEvent e) {
					if(((GamblingThread) thread).isReady()) ((GamblingThread) thread).startGambling();
				}
			});
		}
	}
	class GamblingThread extends Thread {
		JLabel[] label; //게임 숫자를 출력
		JLabel result; //결과를 출력
		long delay = 200;//지연시간(sleep) 값
		boolean gambling = false; //게임을 할 것인지 결정
		public GamblingThread(JLabel[] label, JLabel result) {
			this.label = label;
			this.result = result;
		}
		boolean isReady() {
			return !gambling; //게임 중이면 준비되지 않았음
		}
		synchronized public void waitForGambling() {//게임하지 않으면 기다림
			if(!gambling) {
				try{
					wait();
				}catch(Exception e) {
					{return;}
				}
			}
		}
		synchronized public void startGambling() { //마우스 클릭으로 게임을 진행
			gambling = true;
			notify();
		}
		public void run() { 
			while(true) {
				try{
					sleep(delay);
					waitForGambling();
					addKeyListener(new KeyAdapter() {
						synchronized public void keyPressed(KeyEvent e) {
							if(gambling == true) {
								int n1 = (int) (Math.random() * 4); 
								int n2 = (int) (Math.random() * 4); 
								int n3 = (int) (Math.random() * 4); 

								if(e.getKeyChar() == '\n') {
									label[0].setText(""+n1);
									label[1].setText(""+n2);
									label[2].setText(""+n3);
								}
								if(label[0].getText().equals(label[1].getText()) && label[1].getText().equals(label[2].getText())) {
									result.setText("축하합니다!!");
								}
								else {
									result.setText("아쉽군요");
								}
								gambling = false;
							}
						}
					});
				}catch(Exception e) {}
			}
		}
	}
	
	public static void main(String[] arg) {
		new Report12();
	}
}
