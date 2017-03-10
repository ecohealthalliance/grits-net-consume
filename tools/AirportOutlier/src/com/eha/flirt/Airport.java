package com.eha.flirt;

public class Airport {
	
    public final String _id;
    public final Coordinates _coord;
    
    public Airport(String id, Coordinates coord) {
    	_id = id;
    	_coord = coord;
    }
	public String getId() {
		return _id;
	}
	public Coordinates getCoordinates() {
		return _coord;
	}
}
