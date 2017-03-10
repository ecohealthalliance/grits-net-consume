package com.eha.flirt;

import java.io.FileNotFoundException;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

import org.apache.commons.math3.distribution.NormalDistribution;
import org.apache.commons.math3.stat.descriptive.DescriptiveStatistics;
import org.bson.Document;

import com.mongodb.Block;
import com.mongodb.MongoClient;
import com.mongodb.client.FindIterable;
import com.mongodb.client.MongoDatabase;

public class Run {

	/**
	 * Main entry point for this tool
	 * 
	 * Replace host and database information as required here
	 * 
	 * @param args
	 * @throws FileNotFoundException
	 * @throws UnsupportedEncodingException
	 */
	public static void main(String[] args) throws FileNotFoundException, UnsupportedEncodingException {
		String 	mongoHost 	= "localhost";
		int 	mongoPort	= 27017;
		String  mongoDb		= "grits-net-meteor";
		String  airportsCol	= "airports";
		
		List<String> countries = getUniqueCountryList(mongoHost, mongoPort, mongoDb, airportsCol );
		
		PrintWriter writer = new PrintWriter("./res/output.txt", "UTF-8");
		for(String country : countries) {
			writer.println(" ");
			writer.println("Now analyzing country: " + country);
			
			//Our database has a country that is "Unknown Country"
			if(!country.equals("Unknown Country")) {
				Coordinates countryCenter = getCountryCenter(country);
				
				List<Airport> airports = getAirportsInCountry(mongoHost, mongoPort, mongoDb, airportsCol, country);
				writer.println("Number airports in country: " + airports.size());
				
				DescriptiveStatistics stats = new DescriptiveStatistics();
				for(Airport airport : airports){
					double lat1 = airport.getCoordinates().getLatitude();
					double lon1 = airport.getCoordinates().getLongitude();
					double lat2 = countryCenter.getLatitude();
					double lon2 = countryCenter.getLongitude();
					double distance = Haversine.haversine(lat1, lon1, lat2, lon2);
					stats.addValue(distance);
				}
 
				// Compute some statistics
				double mean = stats.getMean();
				double std 	= stats.getStandardDeviation();
				
				//Only remove outliers if relatively normal
				if(std > 0 && airports.size() > 5) {
					
					NormalDistribution normalDistribution = new NormalDistribution(mean, std);
					for(Airport airport : airports) {
						
						double lat1 = airport.getCoordinates().getLatitude();
						double lon1 = airport.getCoordinates().getLongitude();
						double lat2 = countryCenter.getLatitude();
						double lon2 = countryCenter.getLongitude();
						double distance = Haversine.haversine(lat1, lon1, lat2, lon2);
						double pValue = normalDistribution.cumulativeProbability(distance);
						 
						//Could tighten up RIGHT HERE. TODO Add significance value maybe
						if( (pValue > 0.97) && distance > mean)  
{
							writer.println("Possible Outlier: " + airport.getId() + " distance to country center: " + distance + " pValue: " + pValue);
						}
					}	
				}
			}	
		}		
		writer.close();
	}	
	 
	/**
	 * Gets the current center of the country. 
	 * @param country name
	 * @return Coordinates of the approximate center of the country
	 */
	private static Coordinates getCountryCenter(String country) {
	
		Coordinates countryCenter = null;
		Map<String, Coordinates> countries = CountryUtil.getInstance().getCountries();
		countryCenter = countries.get(country);
		return countryCenter;
	}
	
	/**
	 * Checks the mongo database airports collection for all the airports in a country by country name
	 * @param mongoHost
	 * @param mongoPort
	 * @param mongoDb
	 * @param collection
	 * @param country
	 * @return List of airports in the country
	 */
	private static List<Airport> getAirportsInCountry(String mongoHost, int mongoPort, String mongoDb, String collection, String country) {
		
		List<Airport> airports = new ArrayList<Airport>();	
		MongoClient mongoClient = new MongoClient( mongoHost , mongoPort );
		MongoDatabase db = mongoClient.getDatabase( mongoDb );
		FindIterable<Document> iterable = db.getCollection(collection).find();
		iterable.forEach(new Block<Document>() {
			public void apply(final Document doc) {
				
				String countryName = (String) doc.get( "countryName" );
				if(countryName.equals(country))
				{
					String airportCode = (String) doc.get("_id");
					Document loc = (Document) doc.get("loc");
					List coord = (List)loc.get("coordinates");
					double lat = (double) coord.get(1);
					double lng = (double) coord.get(0);
					Airport airport = new Airport(airportCode, new Coordinates(lat, lng));
					airports.add(airport);
				}
		    
			}
		});
		mongoClient.close();
		return airports;
	}
	
	/**
	 * Get all the unique countries in the database. 
	 * @param mongoHost
	 * @param mongoPort
	 * @param mongoDb
	 * @param collection
	 * @return List of unique countries in our database
	 */
	private static List<String> getUniqueCountryList(String mongoHost, int mongoPort, String mongoDb, String collection) {
		
		List<String> countries = new ArrayList<String>();	
		MongoClient mongoClient = new MongoClient( mongoHost , mongoPort );
		MongoDatabase db = mongoClient.getDatabase( mongoDb );
		FindIterable<Document> iterable = db.getCollection(collection).find();
		iterable.forEach(new Block<Document>() {
			public void apply(final Document doc) {
				String countryName = (String) doc.get( "countryName" );
				if(!countries.contains(countryName))
					countries.add(countryName);
		    }
		});
		mongoClient.close();
		return countries;
	}
} 