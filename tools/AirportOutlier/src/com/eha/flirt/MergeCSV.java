package com.eha.flirt;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

public class MergeCSV {

	//Util for taking this file: https://developers.google.com/public-data/docs/canonical/countries_csv
	//And making it into nice easy to consume map
	public static void main(String[] args) throws FileNotFoundException {

		File file = new File("./res/countries.txt");
		try(BufferedReader br = new BufferedReader(new FileReader(file))) {
		    for(String line; (line = br.readLine()) != null; ) {
		 
		    	// process the line.
		    	//AM  40.069099 45.038189 Armenia
		    	String[] split = line.split("\\s+");
		    	String lat = split[1];
		    	String lng = split[2];
		    	String rest = split[3];
		    	
		    	if(split.length > 4)
		    		rest += " " + split[4];
		        if(split.length > 5)
		    		rest += " " + split[5];
		        if(split.length > 6)
		    		rest += " " + split[6];   
		        if(split.length > 7)
		    		rest += " " + split[7];   
		        if(split.length > 8)
		    		rest += " " + split[8];   
		    	
				//countries.put("United Arab Emirates", new AirportCoordinates(23.424076, 53.847818));
		    	System.out.println("countries.put(\"" + rest + "\", new Coordinates("+ lat +", " + lng + "));");
		    	
		    }
		} catch (IOException e) {
			e.printStackTrace();
		}
		
	}

}
