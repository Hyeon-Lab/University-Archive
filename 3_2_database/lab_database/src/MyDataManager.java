import java.io.BufferedReader;
import java.io.FileReader;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.util.ArrayList;
import java.util.Random;
import java.util.Scanner;


class CustomerData {
	String name;
	String address;
	String phone;
	public CustomerData(String name, String address, String phone) {
		this.name = name;
		this.address = address;
		this.phone = phone;
	}

	public String toString() {
		return name + ","+ address + "," + phone;
	}
}


class RentedData {
	String customerName;
	String dvdName;
	String date;
	static int rentIDCounter = -1;

	public RentedData(String customerName, String dvdName, String date) {
		this.customerName = customerName;
		this.dvdName = dvdName;
		this.date = date;
	}


	public String toString() {
		return customerName + ","+ dvdName + "," + date;
	}
}
 


public class MyDataManager {

	// Generate rented.txt and customer.txt
	public void makeDataGen(int numCumstomer, int numRent) {

		Random rnd = new Random();
		rnd.setSeed(0);

		int numDVD = 1000;
		try {
			 

			// customer info
			String outFileName = "customer"+numCumstomer+".txt";
			BufferedWriter bw = new BufferedWriter(new FileWriter(outFileName));

			for (int i=0; i<numCumstomer; i++) {
				String name = "Person"+i;
				String address = "address"+i;
				String phone = "111-"+i;
				CustomerData r = new CustomerData(name, address, phone);
				bw.write(r+""); bw.newLine();

			}		
			bw.close();


			// rent info
			outFileName = "rented"+numRent+".txt";
			bw = new BufferedWriter(new FileWriter(outFileName));

			for (int i=0; i<numRent; i++) {
				String customer = "Person"+rnd.nextInt(numCumstomer); 
				String dvd = "dvd"+rnd.nextInt(numDVD);
				String date = "date_2024_"+i;
				RentedData r = new RentedData(customer, dvd, date);
				bw.write(r+""); bw.newLine();
			}		
			bw.close();

		}
		catch (Exception e) {
			e.printStackTrace();

		}

	}


	// Find a customer in customerN.txt according to the address
	public ArrayList<String> findCustomer(String addrHint, String customerFileName) {
		ArrayList<String> result = new ArrayList<String>();
		try {
			BufferedReader br = new BufferedReader(new FileReader(customerFileName));
			String line = null;

			while ( (line = br.readLine()) != null) {
				String [] toks = line.split(",");
				String addr = toks[1];
				if(addr.contains(addrHint)) {
					result.add(line);
				}
			}

			br.close();

		} 
		catch(Exception e) {
			e.printStackTrace();
		}

		return result;

	}

 
 
	// Get the rent information for customers whose address has "addrHint"  
	public ArrayList<String> join(String rentedFileName, String customerFileName, String addrHint) {
		ArrayList<String> result = new ArrayList<String>();
		try {
			BufferedReader br1 = new BufferedReader(new FileReader(rentedFileName));

			String line1 = null;

			// rented data
			while ( (line1 = br1.readLine()) != null) {
				String [] toks1 = line1.split(",");
				String personName1 = toks1[0];
				
				// customer data
				BufferedReader br2 = new BufferedReader(new FileReader(customerFileName));
				String line2 = null;
				while ( (line2 = br2.readLine()) != null) {
					String [] toks2 = line2.split(",");
					String personName2 = toks2[0];
					String addr2 = toks2[1];
					if(personName1.equals(personName2)) {
						if(addr2.contains(addrHint)) {
							result.add(line1+":"+line2);
						}
					}
				}

				br2.close();
			}
			br1.close();

		} 
		catch(Exception e) {
			e.printStackTrace();
		}

		return result;

	}


	

	// Get the rent information for customers whose have "nameHint" in their name
	public ArrayList<String> join_improved(String rentedFileName, String customerFileName, String addrHint) {
		ArrayList<String> result = new ArrayList<String>();
		try {

			/////////////// YOUR CODE ////////////////////
			BufferedReader br2 = new BufferedReader(new FileReader(customerFileName));

			String line2 = null;

			// customer data
			while ((line2 = br2.readLine()) != null) {
				String [] toks2 = line2.split(",");
				String personName2 = toks2[0];
				String addr2 = toks2[1];
				
				if(addr2.contains(addrHint)) {
					// rented data
					BufferedReader br1 = new BufferedReader(new FileReader(rentedFileName));
					String line1 = null;
					while ((line1 = br1.readLine()) != null) {
						String [] toks1 = line1.split(",");
						String personName1 = toks1[0];
						if(personName1.equals(personName2)) {
								result.add(line1+":"+line2);
						}
					}
					br1.close();
				}
				
			}
			br2.close();
			
			//////////////////////////////////////////////
		} 
		catch(Exception e) {
			e.printStackTrace();
		}

		return result;
	
	}	
 
 

	public static void main(String [] args) {
		
		MyDataManager my = new MyDataManager();
		int [] dataSize = {2000, 20000, 200000, 2000000};
		// for(int i: dataSize) {
		//    my.makeDataGen(i, i);
		// }
		

		String addrHint = "1111";

		System.out.print("Run Option(0:find customers, 1: naive join, 2: improved join):");
		Scanner keyboardIn = new Scanner(System.in);
		int opt = keyboardIn.nextInt();
		keyboardIn.close();

		if (opt==0) {
			// Simple Retrieval
			for(int i: dataSize) {
				long startTime = System.currentTimeMillis();
				ArrayList<String> res = my.findCustomer(addrHint, "src/customer"+i+".txt");
				long endTime = System.currentTimeMillis();
				System.out.println("Search Time(data"+i+"):"+(endTime-startTime)+" ms\t"+"Number of records:"+res.size());
			}
		}

		else if(opt==1) {
			// Join
			for(int i: dataSize) {
				long startTime = System.currentTimeMillis();
				ArrayList<String> res = my.join("src/rented"+i+".txt", "src/customer"+i+".txt", addrHint);
				long endTime = System.currentTimeMillis();
				//for(String r: res) System.out.println(">"+r);
				System.out.println("Join Time(data"+i+"):"+(endTime-startTime)+" ms\t"+"Number of records:"+res.size());
			}
	 	}
		else {
			// Improved Join (Next Class)
			for(int i: dataSize) {
				long startTime = System.currentTimeMillis();
				ArrayList<String> res = my.join_improved("src/rented"+i+".txt", "src/customer"+i+".txt", addrHint);
				long endTime = System.currentTimeMillis();
				//for(String r: res) System.out.println(">"+r);
				System.out.println("Improved Join Time(data"+i+"):"+(endTime-startTime)+" ms\t"+"Number of records:"+res.size());
			}
		}
		 
	}

}
 
