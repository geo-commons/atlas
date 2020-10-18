var vectorLayer, vectorSource;

// styling stembureau 2018
var stembureauStyl = new ol.style.Text({
	text: '\ue021',
	font : 'normal 18px "Glyphicons Halflings"',
	textBaseline: 'Bottom',
	fill: new ol.style.Fill({
			color: '#5cb85c',
	})
});

// get curent time
function getDate(param){
	var currentTime = new Date()
	var month = currentTime.getMonth() + 1
	var day = currentTime.getDate()
	var year = currentTime.getFullYear()

	if(param == 'month'){ // get month
		return month + '/' + year;
	} else if(param == 'day'){ // get day
		return day + '/' + year;
	} else if(param == 'year'){ //get year
		return year;
	} else if (param == 'full'){
		return day + '/' + month + '/' + year
	}
}

// Grijs 2019 Purmerend
var brt_topo_kaart = new ol.layer.Tile({
	id: "brt_topo_kaart_totaal",
	sldDiv: "slddiv_brt_topo_kaart_totaal",
	infoDiv: "infodiv_brt_topo_kaart_totaal",
	sld: "sld_brt_topo_kaart_totaal",
	lgnd: "lgn_brt_topo_kaart_totaal",
	// metadata attributen
	meta_naam: "Kaart Grijs",
	meta_soort: "Onderlegger",
	meta_org: "Gemeente Datalab",
	meta_bijgewerkt:"25-07-2019",
	// metadata attributen
	title: "Kaart grijs",
	opacity: 0.9,
	visible:true,
	isBaseLayer: true,
	isQueryable: false,
	source: new ol.source.TileWMS({
		projection: 'EPSG:28992', //HERE IS THE DATA SOURCE PROJECTION
		url: 'https://datalab.purmerend.nl/geoserver/topp/wms?',
		params: {'layers': 'topp:topografische_kaart_grijs'},
		serverType: 'geoserver'
	})
});

// Lufo totaal 2020
var lufo_totaal_2020 = new ol.layer.Tile({
	id: "lufo_totaal_2020",
	sldDiv: "slddiv_lufo_totaal_2020",
	infoDiv: "infodiv_lufo_totaal_2020",
	sld: "sld_lufo_totaal_2020",
	lgnd: "lgn_lufo_totaal_2020",
	// metadata attributen
	meta_naam: "Luchtfoto 2020 Purmerend en Beemster",
	meta_soort: "Raster kaart",
	meta_org: "Geo Informatie</a>",
	meta_bijgewerkt:"2020 (Jaarlijks)",
	// metadata attributen
	title: "Luchtfoto 2020",
	opacity: 0.9,
	visible:false,
	isBaseLayer: true,
	isQueryable: false,
	source: new ol.source.TileWMS({
		projection: 'EPSG:28992', //HERE IS THE DATA SOURCE PROJECTION
		url: 'https://datalab.purmerend.nl/geoserver/topp/wms?',
		params: {'layers': 'topp:Lufo_Totaal_2020'},
		serverType: 'geoserver'
	})
});

// BGT - het tiling schema in RD-coÃƒÂ¶rdinaten:
var projectionExtent = [-285401.92, 22598.08, 595401.9199999999, 903401.9199999999];
var projection = new ol.proj.Projection({ code: 'EPSG:28992', units: 'm', extent: projectionExtent });
// Resoluties (pixels per meter) van de zoomniveaus:
var resolutions = [3440.640, 1720.320, 860.160, 430.080, 215.040, 107.520, 53.760, 26.880, 13.440, 6.720, 3.360, 1.680, 0.840, 0.420, 0.210];
var size = ol.extent.getWidth(projectionExtent) / 256;
// Er zijn 15 (0 tot 14) zoomniveaus beschikbaar van de WMTS-service voor de BRT-Achtergrondkaart:
var matrixIds = new Array(15);
for (var z = 0; z < 15; ++z) {
		matrixIds[z] = 'EPSG:28992:' + z;
}
// END BGT PDOK config

// marker layers
vectorSource = new ol.source.Vector({});
vectorLayer = new ol.layer.Vector({
	title: "Marker Layer",
	source: vectorSource
});

var layerList = [
	brt_topo_kaart,
	lufo_totaal_2020,
	vectorLayer
];
