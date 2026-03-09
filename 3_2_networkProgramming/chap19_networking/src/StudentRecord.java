import java.io.Serializable;

/**
 * StudentRecord
 * - Network을 통해 서버로 전송할 데이터 구조 
 * 
 */
public record StudentRecord(String name, int id, int score, double average) implements Serializable {
	
	public String toString() {
		String objString = String.format("[%s]: id: %d, score: %d, avarage: %.2f", 
				this.name, this.id, this.score, this.average);
		
		return objString;
	}
}
