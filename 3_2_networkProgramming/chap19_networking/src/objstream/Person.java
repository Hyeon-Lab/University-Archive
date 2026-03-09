package objstream;

import java.io.Serializable;

public class Person implements Serializable {
    private static final long serialVersionUID = 1L;
    public int id;
    public String name;    
    public String email; 

    public Person(int id, String name, String email) {
    	this.id = id;
    	this.name = name;
    	this.email = email;        
    }
    
    public String toString() {
    	return String.format("id: %d, name: %s, email: %s", this.id, this.name, this.email);
    }
}
