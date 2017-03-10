package com.eha.flirt;

public class Coordinates {
 
    public final double latitude;
    public final double longitude;

    public Coordinates(double lat, double lon) {
        latitude = lat;
        longitude = lon;
    }
	public double getLatitude() {
		return latitude;
	}
	public double getLongitude() {
		return longitude;
	}
	
}
