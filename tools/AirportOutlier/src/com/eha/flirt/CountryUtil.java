package com.eha.flirt;

import java.util.HashMap;
import java.util.Map;

public class CountryUtil {

	   private static CountryUtil instance = null;
	   
	   protected CountryUtil() {
	   }
	   public static CountryUtil getInstance() {
	      if(instance == null) {
	         instance = new CountryUtil();
	      }
	      return instance;
	   }
	   
	   public Map<String, Coordinates> getCountries() {
		   
		   Map<String, Coordinates> countries = new HashMap<String, Coordinates>();
		   	
		   countries.put("Afghanistan", new Coordinates(33.93911, 67.709953));
		   countries.put("Antigua and Barbuda", new Coordinates(17.060816, -61.796428));
		   countries.put("Anguilla", new Coordinates(18.220554, -63.068615));
		   countries.put("Albania", new Coordinates(41.153332, 20.168331));
		   countries.put("Armenia", new Coordinates(40.069099, 45.038189));
		   countries.put("Netherlands Antilles", new Coordinates(12.226079, -69.060087));
		   countries.put("Angola", new Coordinates(-11.202692, 17.873887));
		   countries.put("Antarctica", new Coordinates(-75.250973, -0.071389));
		   countries.put("Argentina", new Coordinates(-38.416097, -63.616672));
		   countries.put("American Samoa", new Coordinates(-14.270972, -170.132217));
		   countries.put("Austria", new Coordinates(47.516231, 14.550072));
		   countries.put("Australia", new Coordinates(-25.274398, 133.775136));
		   countries.put("Aruba", new Coordinates(12.52111, -69.968338));
		   countries.put("Azerbaijan", new Coordinates(40.143105, 47.576927));
		   countries.put("Bosnia and Herzegovina", new Coordinates(43.915886, 17.679076));
		   countries.put("Barbados", new Coordinates(13.193887, -59.543198));
		   countries.put("Bangladesh", new Coordinates(23.684994, 90.356331));
		   countries.put("Belgium", new Coordinates(50.503887, 4.469936));
		   countries.put("Burkina Faso", new Coordinates(12.238333, -1.561593));
		   countries.put("Bulgaria", new Coordinates(42.733883, 25.48583));
		   countries.put("Bahrain", new Coordinates(25.930414, 50.637772));
		   countries.put("Burundi", new Coordinates(-3.373056, 29.918886));
		   countries.put("Benin", new Coordinates(9.30769, 2.315834));
		   countries.put("Bermuda", new Coordinates(32.321384, -64.75737));
		   countries.put("Brunei", new Coordinates(4.535277, 114.727669));
		   countries.put("Bolivia", new Coordinates(-16.290154, -63.588653));
		   countries.put("Brazil", new Coordinates(-14.235004, -51.92528));
		   countries.put("Bahamas", new Coordinates(25.03428, -77.39628));
		   countries.put("Bhutan", new Coordinates(27.514162, 90.433601));
		   countries.put("Bouvet Island", new Coordinates(-54.423199, 3.413194));
		   countries.put("Botswana", new Coordinates(-22.328474, 24.684866));
		   countries.put("Belarus", new Coordinates(53.709807, 27.953389));
		   countries.put("Belize", new Coordinates(17.189877, -88.49765));
		   countries.put("Canada", new Coordinates(56.130366, -106.346771));
		   countries.put("Cocos [Keeling] Islands", new Coordinates(-12.164165, 96.870956));
		   countries.put("Congo [DRC]", new Coordinates(-4.038333, 21.758664));
		   countries.put("Central African Republic", new Coordinates(6.611111, 20.939444));
		   countries.put("Congo [Republic]", new Coordinates(-0.228021, 15.827659));
		   countries.put("Switzerland", new Coordinates(46.818188, 8.227512));
		   countries.put("Côte d'Ivoire", new Coordinates(7.539989, -5.54708));
		   countries.put("Cook Islands", new Coordinates(-21.236736, -159.777671));
		   countries.put("Chile", new Coordinates(-35.675147, -71.542969));
		   countries.put("Cameroon", new Coordinates(7.369722, 12.354722));
		   countries.put("China", new Coordinates(35.86166, 104.195397));
		   countries.put("Colombia", new Coordinates(4.570868, -74.297333));
		   countries.put("Costa Rica", new Coordinates(9.748917, -83.753428));
		   countries.put("Cuba", new Coordinates(21.521757, -77.781167));
		   countries.put("Cape Verde", new Coordinates(16.002082, -24.013197));
		   countries.put("Christmas Island", new Coordinates(-10.447525, 105.690449));
		   countries.put("Cyprus", new Coordinates(35.126413, 33.429859));
		   countries.put("Czech Republic", new Coordinates(49.817492, 15.472962));
		   countries.put("Germany", new Coordinates(51.165691, 10.451526));
		   countries.put("Djibouti", new Coordinates(11.825138, 42.590275));
		   countries.put("Denmark", new Coordinates(56.26392, 9.501785));
		   countries.put("Dominica", new Coordinates(15.414999, -61.370976));
		   countries.put("Dominican Republic", new Coordinates(18.735693, -70.162651));
		   countries.put("Algeria", new Coordinates(28.033886, 1.659626));
		   countries.put("Ecuador", new Coordinates(-1.831239, -78.183406));
		   countries.put("Estonia", new Coordinates(58.595272, 25.013607));
		   countries.put("Egypt", new Coordinates(26.820553, 30.802498));
		   countries.put("Western Sahara", new Coordinates(24.215527, -12.885834));
		   countries.put("Eritrea", new Coordinates(15.179384, 39.782334));
		   countries.put("Spain", new Coordinates(40.463667, -3.74922));
		   countries.put("Ethiopia", new Coordinates(9.145, 40.489673));
		   countries.put("Finland", new Coordinates(61.92411, 25.748151));
		   countries.put("Fiji", new Coordinates(-16.578193, 179.414413));
		   countries.put("Falkland Islands [Islas Malvinas]", new Coordinates(-51.796253, -59.523613));
		   countries.put("Micronesia", new Coordinates(7.425554, 150.550812));
		   countries.put("Faroe Islands", new Coordinates(61.892635, -6.911806));
		   countries.put("France", new Coordinates(46.227638, 2.213749));
		   countries.put("Gabon", new Coordinates(-0.803689, 11.609444));
		   countries.put("United Kingdom", new Coordinates(55.378051, -3.435973));
		   countries.put("Grenada", new Coordinates(12.262776, -61.604171));
		   countries.put("Georgia", new Coordinates(42.315407, 43.356892));
		   countries.put("French Guiana", new Coordinates(3.933889, -53.125782));
		   countries.put("Guernsey", new Coordinates(49.465691, -2.585278));
		   countries.put("Ghana", new Coordinates(7.946527, -1.023194));
		   countries.put("Gibraltar", new Coordinates(36.137741, -5.345374));
		   countries.put("Greenland", new Coordinates(71.706936, -42.604303));
		   countries.put("Gambia", new Coordinates(13.443182, -15.310139));
		   countries.put("Guinea", new Coordinates(9.945587, -9.696645));
		   countries.put("Guadeloupe", new Coordinates(16.995971, -62.067641));
		   countries.put("Equatorial Guinea", new Coordinates(1.650801, 10.267895));
		   countries.put("Greece", new Coordinates(39.074208, 21.824312));
		   countries.put("South Georgia and the South Sandwich", new Coordinates(-54.429579, -36.587909));
		   countries.put("Guatemala", new Coordinates(15.783471, -90.230759));
		   countries.put("Guam", new Coordinates(13.444304, 144.793731));
		   countries.put("Guinea-Bissau", new Coordinates(11.803749, -15.180413));
		   countries.put("Guyana", new Coordinates(4.860416, -58.93018));
		   countries.put("Gaza Strip", new Coordinates(31.354676, 34.308825));
		   countries.put("Hong Kong", new Coordinates(22.396428, 114.109497));
		   countries.put("Heard Island and McDonald Islands", new Coordinates(-53.08181, 73.504158));
		   countries.put("Honduras", new Coordinates(15.199999, -86.241905));
		   countries.put("Croatia", new Coordinates(45.1, 15.2));
		   countries.put("Haiti", new Coordinates(18.971187, -72.285215));
		   countries.put("Hungary", new Coordinates(47.162494, 19.503304));
		   countries.put("Indonesia", new Coordinates(-0.789275, 113.921327));
		   countries.put("Ireland", new Coordinates(53.41291, -8.24389));
		   countries.put("Israel", new Coordinates(31.046051, 34.851612));
		   countries.put("Isle of Man", new Coordinates(54.236107, -4.548056));
		   countries.put("India", new Coordinates(20.593684, 78.96288));
		   countries.put("British Indian Ocean Territory", new Coordinates(-6.343194, 71.876519));
		   countries.put("Iraq", new Coordinates(33.223191, 43.679291));
		   countries.put("Iran", new Coordinates(32.427908, 53.688046));
		   countries.put("Iceland", new Coordinates(64.963051, -19.020835));
		   countries.put("Italy", new Coordinates(41.87194, 12.56738));
		   countries.put("Jersey", new Coordinates(49.214439, -2.13125));
		   countries.put("Jamaica", new Coordinates(18.109581, -77.297508));
		   countries.put("Jordan", new Coordinates(30.585164, 36.238414));
		   countries.put("Japan", new Coordinates(36.204824, 138.252924));
		   countries.put("Kenya", new Coordinates(-0.023559, 37.906193));
		   countries.put("Kyrgyzstan", new Coordinates(41.20438, 74.766098));
		   countries.put("Cambodia", new Coordinates(12.565679, 104.990963));
		   countries.put("Kiribati", new Coordinates(-3.370417, -168.734039));
		   countries.put("Comoros", new Coordinates(-11.875001, 43.872219));
		   countries.put("Saint Kitts and Nevis", new Coordinates(17.357822, -62.782998));
		   countries.put("North Korea", new Coordinates(40.339852, 127.510093));
		   countries.put("South Korea", new Coordinates(35.907757, 127.766922));
		   countries.put("Kuwait", new Coordinates(29.31166, 47.481766));
		   countries.put("Cayman Islands", new Coordinates(19.513469, -80.566956));
		   countries.put("Kazakhstan", new Coordinates(48.019573, 66.923684));
		   countries.put("Laos", new Coordinates(19.85627, 102.495496));
		   countries.put("Lebanon", new Coordinates(33.854721, 35.862285));
		   countries.put("Saint Lucia", new Coordinates(13.909444, -60.978893));
		   countries.put("Liechtenstein", new Coordinates(47.166, 9.555373));
		   countries.put("Sri Lanka", new Coordinates(7.873054, 80.771797));
		   countries.put("Liberia", new Coordinates(6.428055, -9.429499));
		   countries.put("Lesotho", new Coordinates(-29.609988, 28.233608));
		   countries.put("Lithuania", new Coordinates(55.169438, 23.881275));
		   countries.put("Luxembourg", new Coordinates(49.815273, 6.129583));
		   countries.put("Latvia", new Coordinates(56.879635, 24.603189));
		   countries.put("Libya", new Coordinates(26.3351, 17.228331));
		   countries.put("Morocco", new Coordinates(31.791702, -7.09262));
		   countries.put("Monaco", new Coordinates(43.750298, 7.412841));
		   countries.put("Moldova", new Coordinates(47.411631, 28.369885));
		   countries.put("Montenegro", new Coordinates(42.708678, 19.37439));
		   countries.put("Madagascar", new Coordinates(-18.766947, 46.869107));
		   countries.put("Marshall Islands", new Coordinates(7.131474, 171.184478));
		   countries.put("Macedonia [FYROM]", new Coordinates(41.608635, 21.745275));
		   countries.put("Mali", new Coordinates(17.570692, -3.996166));
		   countries.put("Myanmar [Burma]", new Coordinates(21.913965, 95.956223));
		   countries.put("Mongolia", new Coordinates(46.862496, 103.846656));
		   countries.put("Macau", new Coordinates(22.198745, 113.543873));
		   countries.put("Northern Mariana Islands", new Coordinates(17.33083, 145.38469));
		   countries.put("Martinique", new Coordinates(14.641528, -61.024174));
		   countries.put("Mauritania", new Coordinates(21.00789, -10.940835));
		   countries.put("Montserrat", new Coordinates(16.742498, -62.187366));
		   countries.put("Malta", new Coordinates(35.937496, 14.375416));
		   countries.put("Mauritius", new Coordinates(-20.348404, 57.552152));
		   countries.put("Maldives", new Coordinates(3.202778, 73.22068));
		   countries.put("Malawi", new Coordinates(-13.254308, 34.301525));
		   countries.put("Mexico", new Coordinates(23.634501, -102.552784));
		   countries.put("Malaysia", new Coordinates(4.210484, 101.975766));
		   countries.put("Mozambique", new Coordinates(-18.665695, 35.529562));
		   countries.put("Namibia", new Coordinates(-22.95764, 18.49041));
		   countries.put("New Caledonia", new Coordinates(-20.904305, 165.618042));
		   countries.put("Niger", new Coordinates(17.607789, 8.081666));
		   countries.put("Norfolk Island", new Coordinates(-29.040835, 167.954712));
		   countries.put("Nigeria", new Coordinates(9.081999, 8.675277));
		   countries.put("Nicaragua", new Coordinates(12.865416, -85.207229));
		   countries.put("Netherlands", new Coordinates(52.132633, 5.291266));
		   countries.put("Norway", new Coordinates(60.472024, 8.468946));
		   countries.put("Nepal", new Coordinates(28.394857, 84.124008));
		   countries.put("Nauru", new Coordinates(-0.522778, 166.931503));
		   countries.put("Niue", new Coordinates(-19.054445, -169.867233));
		   countries.put("New Zealand", new Coordinates(-40.900557, 174.885971));
		   countries.put("Oman", new Coordinates(21.512583, 55.923255));
		   countries.put("Panama", new Coordinates(8.537981, -80.782127));
		   countries.put("Peru", new Coordinates(-9.189967, -75.015152));
		   countries.put("French Polynesia", new Coordinates(-17.679742, -149.406843));
		   countries.put("Papua New Guinea", new Coordinates(-6.314993, 143.95555));
		   countries.put("Philippines", new Coordinates(12.879721, 121.774017));
		   countries.put("Pakistan", new Coordinates(30.375321, 69.345116));
		   countries.put("Poland", new Coordinates(51.919438, 19.145136));
		   countries.put("Saint Pierre and Miquelon", new Coordinates(46.941936, -56.27111));
		   countries.put("Pitcairn Islands", new Coordinates(-24.703615, -127.439308));
		   countries.put("Puerto Rico", new Coordinates(18.220833, -66.590149));
		   countries.put("Palestinian Territories", new Coordinates(31.952162, 35.233154));
		   countries.put("Portugal", new Coordinates(39.399872, -8.224454));
		   countries.put("Palau", new Coordinates(7.51498, 134.58252));
		   countries.put("Paraguay", new Coordinates(-23.442503, -58.443832));
		   countries.put("Qatar", new Coordinates(25.354826, 51.183884));
		   countries.put("Réunion", new Coordinates(-21.115141, 55.536384));
		   countries.put("Romania", new Coordinates(45.943161, 24.96676));
		   countries.put("Serbia", new Coordinates(44.016521, 21.005859));
		   countries.put("Russia", new Coordinates(61.52401, 105.318756));
		   countries.put("Rwanda", new Coordinates(-1.940278, 29.873888));
		   countries.put("Saudi Arabia", new Coordinates(23.885942, 45.079162));
		   countries.put("Solomon Islands", new Coordinates(-9.64571, 160.156194));
		   countries.put("Seychelles", new Coordinates(-4.679574, 55.491977));
		   countries.put("Sudan", new Coordinates(12.862807, 30.217636));
		   countries.put("Sweden", new Coordinates(60.128161, 18.643501));
		   countries.put("Singapore", new Coordinates(1.352083, 103.819836));
		   countries.put("Saint Helena", new Coordinates(-24.143474, -10.030696));
		   countries.put("Slovenia", new Coordinates(46.151241, 14.995463));
		   countries.put("Svalbard and Jan Mayen", new Coordinates(77.553604, 23.670272));
		   countries.put("Slovakia", new Coordinates(48.669026, 19.699024));
		   countries.put("Sierra Leone", new Coordinates(8.460555, -11.779889));
		   countries.put("San Marino", new Coordinates(43.94236, 12.457777));
		   countries.put("Senegal", new Coordinates(14.497401, -14.452362));
		   countries.put("Somalia", new Coordinates(5.152149, 46.199616));
		   countries.put("Suriname", new Coordinates(3.919305, -56.027783));
		   countries.put("São Tomé and Príncipe", new Coordinates(0.18636, 6.613081));
		   countries.put("El Salvador", new Coordinates(13.794185, -88.89653));
		   countries.put("Syria", new Coordinates(34.802075, 38.996815));
		   countries.put("Swaziland", new Coordinates(-26.522503, 31.465866));
		   countries.put("Turks and Caicos Islands", new Coordinates(21.694025, -71.797928));
		   countries.put("Chad", new Coordinates(15.454166, 18.732207));
		   countries.put("French Southern Territories", new Coordinates(-49.280366, 69.348557));
		   countries.put("Togo", new Coordinates(8.619543, 0.824782));
		   countries.put("Thailand", new Coordinates(15.870032, 100.992541));
		   countries.put("Tajikistan", new Coordinates(38.861034, 71.276093));
		   countries.put("Tokelau", new Coordinates(-8.967363, -171.855881));
		   countries.put("Timor-Leste", new Coordinates(-8.874217, 125.727539));
		   countries.put("Turkmenistan", new Coordinates(38.969719, 59.556278));
		   countries.put("Tunisia", new Coordinates(33.886917, 9.537499));
		   countries.put("Tonga", new Coordinates(-21.178986, -175.198242));
		   countries.put("Turkey", new Coordinates(38.963745, 35.243322));
		   countries.put("Trinidad and Tobago", new Coordinates(10.691803, -61.222503));
		   countries.put("Tuvalu", new Coordinates(-7.109535, 177.64933));
		   countries.put("Taiwan", new Coordinates(23.69781, 120.960515));
		   countries.put("Tanzania", new Coordinates(-6.369028, 34.888822));
		   countries.put("Ukraine", new Coordinates(48.379433, 31.16558));
		   countries.put("Uganda", new Coordinates(1.373333, 32.290275));
		   countries.put("United States", new Coordinates(37.09024, -95.712891));
		   countries.put("Uruguay", new Coordinates(-32.522779, -55.765835));
		   countries.put("Uzbekistan", new Coordinates(41.377491, 64.585262));
		   countries.put("Vatican City", new Coordinates(41.902916, 12.453389));
		   countries.put("Saint Vincent and the Grenadines", new Coordinates(12.984305, -61.287228));
		   countries.put("Venezuela", new Coordinates(6.42375, -66.58973));
		   countries.put("British Virgin Islands", new Coordinates(18.420695, -64.639968));
		   countries.put("U.S. Virgin Islands", new Coordinates(18.335765, -64.896335));
		   countries.put("Vietnam", new Coordinates(14.058324, 108.277199));
		   countries.put("Vanuatu", new Coordinates(-15.376706, 166.959158));
		   countries.put("Wallis and Futuna", new Coordinates(-13.768752, -177.156097));
		   countries.put("Samoa", new Coordinates(-13.759029, -172.104629));
		   countries.put("Kosovo", new Coordinates(42.602636, 20.902977));
		   countries.put("Yemen", new Coordinates(15.552727, 48.516388));
		   countries.put("Mayotte", new Coordinates(-12.8275, 45.166244));
		   countries.put("South Africa", new Coordinates(-30.559482, 22.937506));
		   countries.put("Zambia", new Coordinates(-13.133897, 27.849332));
		   countries.put("Zimbabwe", new Coordinates(-19.015438, 29.154857));

		   
		   countries.put("Ivory Coast (Cote d'Ivoire)", new Coordinates(7.516655, -5.509573));
		   countries.put("South Sudan", new Coordinates(7.056036, 30.963611));
		   countries.put("Russian Federation", new Coordinates(61.52401, 105.318756));			 
		   countries.put("United Arab Emirates", new Coordinates(23.437402, 53.928251));
		   countries.put("Western Samoa", new Coordinates(-13.687228, -172.231330));
		   countries.put("Myanmar", new Coordinates(21.990039, 95.900393));
		   countries.put("Andorra", new Coordinates(42.537312, 1.559449));
		   countries.put("Congo", new Coordinates(-4.025809, 21.790719));
		   countries.put("Democratic Republic of the Congo", new Coordinates(-4.025809, 21.790719));
		   countries.put("East Timor", new Coordinates(-8.829635, 125.793970));
		   countries.put("United States Minor Outlying Islands", new Coordinates(19.281570, 166.643254));
		   countries.put("Guinea Bissau", new Coordinates(11.873407, -15.077911));
		   countries.put("Saint Vincent and Grenadines", new Coordinates(13.246459, -61.190985));
		   countries.put("Brunei Darussalam", new Coordinates(4.529671, 114.727839));
		   countries.put("Bonaire, Saint Eustatius & Saba", new Coordinates(12.202597, -68.249697));
		   countries.put("Cocos (Keeling) Islands", new Coordinates(-12.182312, 96.829731));
		   countries.put("Grenada and South Grenadines", new Coordinates(12.722992, -61.317455));
		   countries.put("Curacao", new Coordinates(12.178606, -68.977153));
		   countries.put("Falkland Islands", new Coordinates(-51.694695, -59.734679));
		   countries.put("Palestinian Territory", new Coordinates(31.917907, 35.290312));
		   countries.put("Macedonia", new Coordinates(41.636002, 21.631460));
		   countries.put("Wallis and Futuna Islands", new Coordinates(-14.291564, -178.120475));
		   countries.put("Sao Tome and Principe", new Coordinates(0.199695, 6.617767));
		   countries.put("Reunion", new Coordinates(-21.118462, 55.541579));
		   countries.put("Sint Maarten", new Coordinates(18.056666, -63.052395));
			   
		   
		  
		   
		   return countries;
		   
	   }


/**
AF	33.93911	67.709953	Afghanistan
AG	17.060816	-61.796428	Antigua and Barbuda
AI	18.220554	-63.068615	Anguilla
AL	41.153332	20.168331	Albania
AM	40.069099	45.038189	Armenia
AN	12.226079	-69.060087	Netherlands Antilles
AO	-11.202692	17.873887	Angola
AQ	-75.250973	-0.071389	Antarctica
AR	-38.416097	-63.616672	Argentina
AS	-14.270972	-170.132217	American Samoa
AT	47.516231	14.550072	Austria
AU	-25.274398	133.775136	Australia
AW	12.52111	-69.968338	Aruba
AZ	40.143105	47.576927	Azerbaijan
BA	43.915886	17.679076	Bosnia and Herzegovina
BB	13.193887	-59.543198	Barbados
BD	23.684994	90.356331	Bangladesh
BE	50.503887	4.469936	Belgium
BF	12.238333	-1.561593	Burkina Faso
BG	42.733883	25.48583	Bulgaria
BH	25.930414	50.637772	Bahrain
BI	-3.373056	29.918886	Burundi
BJ	9.30769	2.315834	Benin
BM	32.321384	-64.75737	Bermuda
BN	4.535277	114.727669	Brunei
BO	-16.290154	-63.588653	Bolivia
BR	-14.235004	-51.92528	Brazil
BS	25.03428	-77.39628	Bahamas
BT	27.514162	90.433601	Bhutan
BV	-54.423199	3.413194	Bouvet Island
BW	-22.328474	24.684866	Botswana
BY	53.709807	27.953389	Belarus
BZ	17.189877	-88.49765	Belize
CA	56.130366	-106.346771	Canada
CC	-12.164165	96.870956	Cocos [Keeling] Islands
CD	-4.038333	21.758664	Congo [DRC]
CF	6.611111	20.939444	Central African Republic
CG	-0.228021	15.827659	Congo [Republic]
CH	46.818188	8.227512	Switzerland
CI	7.539989	-5.54708	Côte d'Ivoire
CK	-21.236736	-159.777671	Cook Islands
CL	-35.675147	-71.542969	Chile
CM	7.369722	12.354722	Cameroon
CN	35.86166	104.195397	China
CO	4.570868	-74.297333	Colombia
CR	9.748917	-83.753428	Costa Rica
CU	21.521757	-77.781167	Cuba
CV	16.002082	-24.013197	Cape Verde
CX	-10.447525	105.690449	Christmas Island
CY	35.126413	33.429859	Cyprus
CZ	49.817492	15.472962	Czech Republic
DE	51.165691	10.451526	Germany
DJ	11.825138	42.590275	Djibouti
DK	56.26392	9.501785	Denmark
DM	15.414999	-61.370976	Dominica
DO	18.735693	-70.162651	Dominican Republic
DZ	28.033886	1.659626	Algeria
EC	-1.831239	-78.183406	Ecuador
EE	58.595272	25.013607	Estonia
EG	26.820553	30.802498	Egypt
EH	24.215527	-12.885834	Western Sahara
ER	15.179384	39.782334	Eritrea
ES	40.463667	-3.74922	Spain
ET	9.145	40.489673	Ethiopia
FI	61.92411	25.748151	Finland
FJ	-16.578193	179.414413	Fiji
FK	-51.796253	-59.523613	Falkland Islands [Islas Malvinas]
FM	7.425554	150.550812	Micronesia
FO	61.892635	-6.911806	Faroe Islands
FR	46.227638	2.213749	France
GA	-0.803689	11.609444	Gabon
GB	55.378051	-3.435973	United Kingdom
GD	12.262776	-61.604171	Grenada
GE	42.315407	43.356892	Georgia
GF	3.933889	-53.125782	French Guiana
GG	49.465691	-2.585278	Guernsey
GH	7.946527	-1.023194	Ghana
GI	36.137741	-5.345374	Gibraltar
GL	71.706936	-42.604303	Greenland
GM	13.443182	-15.310139	Gambia
GN	9.945587	-9.696645	Guinea
GP	16.995971	-62.067641	Guadeloupe
GQ	1.650801	10.267895	Equatorial Guinea
GR	39.074208	21.824312	Greece
GS	-54.429579	-36.587909	South Georgia and the South Sandwich Islands
GT	15.783471	-90.230759	Guatemala
GU	13.444304	144.793731	Guam
GW	11.803749	-15.180413	Guinea-Bissau
GY	4.860416	-58.93018	Guyana
GZ	31.354676	34.308825	Gaza Strip
HK	22.396428	114.109497	Hong Kong
HM	-53.08181	73.504158	Heard Island and McDonald Islands
HN	15.199999	-86.241905	Honduras
HR	45.1	15.2	Croatia
HT	18.971187	-72.285215	Haiti
HU	47.162494	19.503304	Hungary
ID	-0.789275	113.921327	Indonesia
IE	53.41291	-8.24389	Ireland
IL	31.046051	34.851612	Israel
IM	54.236107	-4.548056	Isle of Man
IN	20.593684	78.96288	India
IO	-6.343194	71.876519	British Indian Ocean Territory
IQ	33.223191	43.679291	Iraq
IR	32.427908	53.688046	Iran
IS	64.963051	-19.020835	Iceland
IT	41.87194	12.56738	Italy
JE	49.214439	-2.13125	Jersey
JM	18.109581	-77.297508	Jamaica
JO	30.585164	36.238414	Jordan
JP	36.204824	138.252924	Japan
KE	-0.023559	37.906193	Kenya
KG	41.20438	74.766098	Kyrgyzstan
KH	12.565679	104.990963	Cambodia
KI	-3.370417	-168.734039	Kiribati
KM	-11.875001	43.872219	Comoros
KN	17.357822	-62.782998	Saint Kitts and Nevis
KP	40.339852	127.510093	North Korea
KR	35.907757	127.766922	South Korea
KW	29.31166	47.481766	Kuwait
KY	19.513469	-80.566956	Cayman Islands
KZ	48.019573	66.923684	Kazakhstan
LA	19.85627	102.495496	Laos
LB	33.854721	35.862285	Lebanon
LC	13.909444	-60.978893	Saint Lucia
LI	47.166	9.555373	Liechtenstein
LK	7.873054	80.771797	Sri Lanka
LR	6.428055	-9.429499	Liberia
LS	-29.609988	28.233608	Lesotho
LT	55.169438	23.881275	Lithuania
LU	49.815273	6.129583	Luxembourg
LV	56.879635	24.603189	Latvia
LY	26.3351	17.228331	Libya
MA	31.791702	-7.09262	Morocco
MC	43.750298	7.412841	Monaco
MD	47.411631	28.369885	Moldova
ME	42.708678	19.37439	Montenegro
MG	-18.766947	46.869107	Madagascar
MH	7.131474	171.184478	Marshall Islands
MK	41.608635	21.745275	Macedonia [FYROM]
ML	17.570692	-3.996166	Mali
MM	21.913965	95.956223	Myanmar [Burma]
MN	46.862496	103.846656	Mongolia
MO	22.198745	113.543873	Macau
MP	17.33083	145.38469	Northern Mariana Islands
MQ	14.641528	-61.024174	Martinique
MR	21.00789	-10.940835	Mauritania
MS	16.742498	-62.187366	Montserrat
MT	35.937496	14.375416	Malta
MU	-20.348404	57.552152	Mauritius
MV	3.202778	73.22068	Maldives
MW	-13.254308	34.301525	Malawi
MX	23.634501	-102.552784	Mexico
MY	4.210484	101.975766	Malaysia
MZ	-18.665695	35.529562	Mozambique
NA	-22.95764	18.49041	Namibia
NC	-20.904305	165.618042	New Caledonia
NE	17.607789	8.081666	Niger
NF	-29.040835	167.954712	Norfolk Island
NG	9.081999	8.675277	Nigeria
NI	12.865416	-85.207229	Nicaragua
NL	52.132633	5.291266	Netherlands
NO	60.472024	8.468946	Norway
NP	28.394857	84.124008	Nepal
NR	-0.522778	166.931503	Nauru
NU	-19.054445	-169.867233	Niue
NZ	-40.900557	174.885971	New Zealand
OM	21.512583	55.923255	Oman
PA	8.537981	-80.782127	Panama
PE	-9.189967	-75.015152	Peru
PF	-17.679742	-149.406843	French Polynesia
PG	-6.314993	143.95555	Papua New Guinea
PH	12.879721	121.774017	Philippines
PK	30.375321	69.345116	Pakistan
PL	51.919438	19.145136	Poland
PM	46.941936	-56.27111	Saint Pierre and Miquelon
PN	-24.703615	-127.439308	Pitcairn Islands
PR	18.220833	-66.590149	Puerto Rico
PS	31.952162	35.233154	Palestinian Territories
PT	39.399872	-8.224454	Portugal
PW	7.51498	134.58252	Palau
PY	-23.442503	-58.443832	Paraguay
QA	25.354826	51.183884	Qatar
RE	-21.115141	55.536384	Réunion
RO	45.943161	24.96676	Romania
RS	44.016521	21.005859	Serbia
RU	61.52401	105.318756	Russia
RW	-1.940278	29.873888	Rwanda
SA	23.885942	45.079162	Saudi Arabia
SB	-9.64571	160.156194	Solomon Islands
SC	-4.679574	55.491977	Seychelles
SD	12.862807	30.217636	Sudan
SE	60.128161	18.643501	Sweden
SG	1.352083	103.819836	Singapore
SH	-24.143474	-10.030696	Saint Helena
SI	46.151241	14.995463	Slovenia
SJ	77.553604	23.670272	Svalbard and Jan Mayen
SK	48.669026	19.699024	Slovakia
SL	8.460555	-11.779889	Sierra Leone
SM	43.94236	12.457777	San Marino
SN	14.497401	-14.452362	Senegal
SO	5.152149	46.199616	Somalia
SR	3.919305	-56.027783	Suriname
ST	0.18636	6.613081	São Tomé and Príncipe
SV	13.794185	-88.89653	El Salvador
SY	34.802075	38.996815	Syria
SZ	-26.522503	31.465866	Swaziland
TC	21.694025	-71.797928	Turks and Caicos Islands
TD	15.454166	18.732207	Chad
TF	-49.280366	69.348557	French Southern Territories
TG	8.619543	0.824782	Togo
TH	15.870032	100.992541	Thailand
TJ	38.861034	71.276093	Tajikistan
TK	-8.967363	-171.855881	Tokelau
TL	-8.874217	125.727539	Timor-Leste
TM	38.969719	59.556278	Turkmenistan
TN	33.886917	9.537499	Tunisia
TO	-21.178986	-175.198242	Tonga
TR	38.963745	35.243322	Turkey
TT	10.691803	-61.222503	Trinidad and Tobago
TV	-7.109535	177.64933	Tuvalu
TW	23.69781	120.960515	Taiwan
TZ	-6.369028	34.888822	Tanzania
UA	48.379433	31.16558	Ukraine
UG	1.373333	32.290275	Uganda
UM			U.S. Minor Outlying Islands
US	37.09024	-95.712891	United States
UY	-32.522779	-55.765835	Uruguay
UZ	41.377491	64.585262	Uzbekistan
VA	41.902916	12.453389	Vatican City
VC	12.984305	-61.287228	Saint Vincent and the Grenadines
VE	6.42375	-66.58973	Venezuela
VG	18.420695	-64.639968	British Virgin Islands
VI	18.335765	-64.896335	U.S. Virgin Islands
VN	14.058324	108.277199	Vietnam
VU	-15.376706	166.959158	Vanuatu
WF	-13.768752	-177.156097	Wallis and Futuna
WS	-13.759029	-172.104629	Samoa
XK	42.602636	20.902977	Kosovo
YE	15.552727	48.516388	Yemen
YT	-12.8275	45.166244	Mayotte
ZA	-30.559482	22.937506	South Africa
ZM	-13.133897	27.849332	Zambia
ZW	-19.015438	29.154857	Zimbabwe
 
*/
}
