package Chapter5_Extend_Override_Abstract_Interface;

interface Payable{
	String play();
}

abstract class Music implements Payable{
	String name; int year;
	
	Music(String name, int year){
		this.name = name; this.year = year; 
	}
	String getName() {
		return name;
	}
	int getYear() {
		return year;
	}
	void print() {
		System.out.println( "곡명 = " + year + ", 연도 = " + name );
	}
}

class Classic extends Music{
	String composer;
	Classic(String name, int year, String composer){
		super(name, year);
		this.composer = composer;
	}
	String getComposer() {
		return composer;
	}
	void setComposer(String composer) {
		this.composer = composer;
	}
	@Override
	public void print() {
		System.out.println( "곡명 = " + year + ", 연도 = " + name + ", 작곡가 = " + composer);
	}
	public String play() {
		return super.getName() + "을 연주합니다.";
	}
}

class Pop extends Music{
	String singer;
	Pop(String name, int year, String singer){
		super(name, year);
		this.singer = singer;
	}
	String getSinger() {
		return singer;
	}
	void setSinger(String singer) {
		this.singer = singer;
	}
	@Override
	public void print() {
		System.out.println( "곡명 = " + year + ", 연도 = " + name + ", 가수 = " + singer);
	}
	public String play() {
		return super.getName() + "을 연주합니다.";
	}
}

public class ex02 {
	public static void main(String[] args) {
		Classic c = new Classic("캐논", 1732, "파헬벨");
		c.print();
		System.out.println(c.play());
		
	}
}
