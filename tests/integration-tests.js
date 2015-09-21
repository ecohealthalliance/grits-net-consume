/* globals db, print */

var grits = db.getSiblingDB("grits");
var airportCount = grits.airports.count();
var flightCount = grits.flights.count();
var invalidCount = grits.invalidRecords.count();
print("Airport count: " + airportCount);
print("Flight count: " + flightCount);
print("Invalid records: " + invalidCount);
if (airportCount <= 0) {
  throw new Error("No airports found in database.");
}
if (flightCount <= 0) {
  throw new Error("No flights found in database.");
}
if ((invalidCount / (airportCount + flightCount)) > 0.01) {
  throw new Error("Too many invalid records.");
}
