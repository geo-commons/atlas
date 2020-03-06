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
	// define a current time
	var currentTime = new Date()
	// returns the month (from 0 to 11)
	var month = currentTime.getMonth() + 1
	// returns the day of the month (from 1 to 31)
	var day = currentTime.getDate()
	// returns the year (four digits)
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

// Osm
var osm = new ol.layer.Tile({
	id: "osm",
	sld: "sldID_osm",
	sldDiv: "sld_div_osm",
	infoDiv: "info_div_osm",
	// metadata attributen
	meta_naam: "<a target='_blank' href='http://www.openstreetmap.org'>OSM</a> (OpenStreetMap)",
	meta_soort: "Achtergrond kaart",
	meta_org: "Vrijwilligers</a>",
	meta_bijgewerkt:getDate('full') + ' (Dagelijks)',
	// metadata attributen
	title: "Open Street Map",
	visible:false,
	isBaseLayer: true,
	isQueryable: false,
	opacity: 0.9,
	source: new ol.source.OSM()
});

// Lufo 2019 Purmerend
var lufo_2019_purm_totaal = new ol.layer.Tile({
id: "lufo_2019_purm_recent",
sldDiv: "slddiv_lufo_2019_purm_recent",
infoDiv: "infodiv_lufo_2019_purnm_recent",
sld: "sld_lufo_2019_purm_recent",
lgnd: "lgn_lufo_2019_purm_recent",
// metadata attributen
meta_naam: "Luchtfoto 2019 Purmerend en Beemster",
meta_soort: "Raster kaart",
meta_org: "Geo Informatie</a>",
meta_bijgewerkt:"2019 (Jaarlijks)",
// metadata attributen
title: "Luchtfoto 2019",
opacity: 0.9,
visible:false,
isBaseLayer: true,
isQueryable: false,
source: new ol.source.TileWMS({
	projection: 'EPSG:28992', //HERE IS THE DATA SOURCE PROJECTION
	url: 'https://datalab.purmerend.nl/geoserver/topp/wms?',
	params: {'layers': 'topp:Lufo_Totaal_Recent'},
	serverType: 'geoserver'
})
});

// Lufo 2019 Purmerend
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

//add BRT PDOk Panden
var pdok_brt = new ol.layer.Tile({
	id: "pdok_brt",
	sld: "sldID_brt",
	sldDiv: "sld_div_brt",
	infoDiv: "info_div_brt",
	// metadata attributen
	meta_naam: "BRT (Basisregistratie Topografie) - <a target='_blank' href='http://pdok.nl'>PDOK</a>",
	meta_soort: "Basisregistratie",
	meta_org: "<a href='https://data.overheid.nl/data/dataset/brt-achtergrondkaart' target='_blank'>Kadaster</a>",
	meta_bijgewerkt: '01/02/2018',
	// metadata attributen
	title: "Topografische kaart",
	visible: true,
	isBaseLayer: true,
	isQueryable: false,
	opacity: 0.9,
	source: new ol.source.TileWMS({
		url: "https://geodata.nationaalgeoregister.nl/wmsc?",
		params: {'layers': 'brtachtergrondkaartpastel'}
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

// BGT PDOk Tiled
var bgt_wmts =  new ol.layer.Tile({
	id: "pdok_bgt_wmts",
	sld: "sld_bgt_wmts",
	sldDiv: "sld_div_bgt_wmts",
	infoDiv: "info_div_bgt_wmts",
	lgnd: "pdok_lgn_bgt",
	// metadata attributen
	meta_naam: "<a href='https://www.geobasisregistraties.nl/basisregistraties/grootschalige-topografie/basisregistratie-grootschalige-topografie' target='_blank'>BGT</a> (Basisregistratie Grootschalige Topografie)",
	meta_soort: "Basisregistratie",
	meta_org: "Lokaal per Gemeente en het <a href='https://www.geobasisregistraties.nl/basisregistraties/grootschalige-topografie' target='_blank'>Kadaster</a> voor landelijk",
	meta_bijgewerkt: getDate('month') + ' (Maandelijks)',
	// metadata attributen
	title: "BGT",
	visible: false,
	basisreg:true,
	isBaseLayer: false,
	isQueryable: false,
	opacity: 1,
	source: new ol.source.WMTS({
			attributions: 'Kaartgegevens: &copy; <a href="https://www.kadaster.nl">Kadaster</a>',
			url: 'https://geodata.nationaalgeoregister.nl/tiles/service/wmts?',
			layer: 'bgtstandaardv2',
			matrixSet: 'EPSG:28992',
			format: 'image/png',
			projection: projection,
			tileGrid: new ol.tilegrid.WMTS({
					origin: ol.extent.getTopLeft(projectionExtent),
					resolutions: resolutions,
					matrixIds: matrixIds
			}),
			style: 'default',
			wrapX: false
	})
});

//add PDOK BAG Panden
var pdok_bag = new ol.layer.Tile({
	id: "pdok_bag",
	sldDiv: "sld_div_bag",
	infoDiv: "info_div_pdok_bag",
	sld: "pdok_sld_bag",
	lgnd: "pdok_lgn_bag",
	filterId: "pdook_flt_bag",
	dataFilterId: "pdok_data_flt_bag",
	// metadata attributen
	meta_naam: "BAG (Basisregistratie Adressen en Gebouwen) - <a target='_blank' href='http://pdok.nl'>PDOK</a>",
	meta_soort: "Basisregistratie",
	meta_org: "Lokaal per Gemeente en het <a href='https://www.geobasisregistraties.nl/basisregistraties/adressen-en-gebouwen' target='_blank'>Kadaster</a> voor landelijk",
	meta_bijgewerkt: getDate('full') +' (Dagelijks)',
	// metadata attributen
	title: "BAG",
	visible: true,
	isBaseLayer: false,
	isQueryable: false,
	basisreg:true,
	opacity: 0.7,
	source: new ol.source.TileWMS({
		url: "https://geodata.nationaalgeoregister.nl/bag/wms",
		params: {
			layers: "pand,ligplaats",
			"SRS": "EPSG:28992"
		}
	})
});

// test wms layer
var wms_layer = new ol.layer.Tile({
source: new ol.source.TileWMS({
	url: 'https://datalab.purmerend.nl/geoserver/topp/wms?',
	params: {'LAYERS': 'topp:BAG_Purmerend_wijken'}
})
});

// BAG_Purmerend_wijken
var wijken_purm = new ol.layer.Tile({
id: "prm_wijken",
sldDiv: "sld_div_wijk",
infoDiv: "info_div_wijken",
sld: "prm_sld_wijken",
lgnd: "prm_lgn_wijken",
filterId: "flt_wijken",
dataFilterId: "prm_data_flt_wijk",
dataZoekId: "prm_zoek_data_wijk",
layerName: 'topp:BAG_Purmerend_wijken',
// metadata attributen
meta_naam: "Wijken Gemeente Purmerend",
meta_soort: "Thema kaart",
meta_org: "Ruimtelijke Ontwikkeling</a>",
meta_bijgewerkt: '2013',
// metadata attributen
title: "Wijken",
opacity: 0.7,
visible:false,
isQueryable: true,
source: new ol.source.TileWMS({
	projection: 'EPSG:28992', //HERE IS THE DATA SOURCE PROJECTION
	url: 'https://datalab.purmerend.nl/geoserver/topp/wms?',
	params: {'layers': 'topp:BAG_Purmerend_wijken'},
	serverType: 'geoserver'
})
});

// Lufo 2017 Purmerend
var data_local = new ol.layer.Tile({
id: "purm_lufo2017_loc",
sldDiv: "sld_div_purm_lufo_17_loc",
infoDiv: "info_div_purm_lufo_17_loc",
sld: "prm_sld_lufo17_loc",
lgnd: "prm_lgn_lufo2017_loc",
layerName: 'topp:Lufo_Purmerend_2012',
// metadata attributen
meta_naam: "Gesloten data",
meta_soort: "Raster kaart",
meta_org: "Geo Informatie</a>",
meta_bijgewerkt:getDate('year') -1 + ' (Jaarlijks)',
// metadata attributen
title: "Gesloten data",
isLufo: false,
opacity: 0.9,
visible:false,
isQueryable: false,
source: new ol.source.TileWMS({
	projection: 'EPSG:28992', //HERE IS THE DATA SOURCE PROJECTION
	url: 'https://datalab.purmerend.nl/geoserver/topp/wms?',
	params: {'layers': 'topp:Lufo_Purmerend_2012'},
	serverType: 'geoserver'
})
});

// Lufo 2019 Purmerend
var lufo_2019_totaal = new ol.layer.Tile({
id: "purm_lufo2019",
sldDiv: "sld_div_purm_lufo_19",
infoDiv: "info_div_purm_lufo_19",
sld: "prm_sld_lufo19",
lgnd: "prm_lgn_lufo2019",
// metadata attributen
meta_naam: "Luchtfoto 2019 Purmerend en Beemster",
meta_soort: "Raster kaart",
meta_org: "Geo Informatie</a>",
meta_bijgewerkt:"2019 (Jaarlijks)",
// metadata attributen
title: "2019",
isLufo: true,
opacity: 0.9,
visible:false,
isQueryable: false,
source: new ol.source.TileWMS({
	projection: 'EPSG:28992', //HERE IS THE DATA SOURCE PROJECTION
	url: 'https://datalab.purmerend.nl/geoserver/topp/wms?',
	params: {'layers': 'topp:Lufo_Totaal_Recent'},
	serverType: 'geoserver'
})
});

// Lufo 2018 Purmerend
var lufo_2018_totaal = new ol.layer.Tile({
id: "purm_lufo2018",
sldDiv: "sld_div_purm_lufo_18",
infoDiv: "info_div_purm_lufo_18",
sld: "prm_sld_lufo18",
lgnd: "prm_lgn_lufo2018",
// metadata attributen
meta_naam: "Luchtfoto 2018 Purmerend en Beemster",
meta_soort: "Raster kaart",
meta_org: "Geo Informatie</a>",
meta_bijgewerkt:"2018 (Jaarlijks)",
// metadata attributen
title: "2018",
isLufo: true,
opacity: 0.9,
visible:false,
isQueryable: false,
source: new ol.source.TileWMS({
	projection: 'EPSG:28992', //HERE IS THE DATA SOURCE PROJECTION
	url: 'https://datalab.purmerend.nl/geoserver/topp/wms?',
	params: {'layers': 'topp:Lufo_Totaal_2018'},
	serverType: 'geoserver'
})
});

// Lufo 2017 Purmerend
var lufo_2017_totaal = new ol.layer.Tile({
id: "purm_lufo2017",
sldDiv: "sld_div_purm_lufo_17",
infoDiv: "info_div_purm_lufo_17",
sld: "prm_sld_lufo17",
lgnd: "prm_lgn_lufo2017",
// metadata attributen
meta_naam: "Luchtfoto 2017 Purmerend en Beemster",
meta_soort: "Raster kaart",
meta_org: "Geo Informatie</a>",
meta_bijgewerkt:getDate('year') -1 + ' (Jaarlijks)',
// metadata attributen
title: "2017",
isLufo: true,
opacity: 0.9,
visible:false,
isQueryable: false,
source: new ol.source.TileWMS({
	projection: 'EPSG:28992', //HERE IS THE DATA SOURCE PROJECTION
	url: 'https://datalab.purmerend.nl/geoserver/topp/wms?',
	params: {'layers': 'topp:Lufo_Totaal_2017'},
	serverType: 'geoserver'
})
});

// Lufo 2016 Purmerend
var lufo_2016_totaal = new ol.layer.Tile({
	id: "purm_lufo2016",
	sldDiv: "sld_div_purm_lufo2016",
	infoDiv: "info_div_purm_lufo2016",
	sld: "purm_sld_lufo2016",
	lgnd: "purm_lgn_lufo2016",
	// metadata attributen
	meta_naam: "Luchtfoto 2016 Purmerend en Beemster",
	meta_soort: "Raster kaart",
	meta_org: "Geo Informatie</a>",
	meta_bijgewerkt:getDate('year') -2 + ' (Jaarlijks)',
	// metadata attributen
	title: "2016",
	isLufo: true,
	opacity: 0.9,
	visible:false,
	isQueryable: false,
	source: new ol.source.TileWMS({
		projection: 'EPSG:28992', //HERE IS THE DATA SOURCE PROJECTION
		url: 'https://datalab.purmerend.nl/geoserver/topp/wms?',
		params: {'LAYERS': 'topp:Lufo_Totaal_2016'},
		serverType: 'geoserver'
	})
});

// Lufo 2015 Purmerend
var lufo_2015_totaal = new ol.layer.Tile({
	id: "purm_lufo2015",
	sldDiv: "sld_div_purm_lufo2015",
	infoDiv: "info_div_purm_lufo2015",
	sld: "purm_sld_lufo2015",
	lgnd: "purm_lgn_lufo2015",
	// metadata attributen
	meta_naam: "Luchtfoto 2015 Purmerend en Beemster",
	meta_soort: "Raster kaart",
	meta_org: "Geo Informatie</a>",
	meta_bijgewerkt:'2015',
	// metadata attributen
	title: "2015",
	isLufo: true,
	opacity: 0.9,
	visible:false,
	isQueryable: false,
	source: new ol.source.TileWMS({
		projection: 'EPSG:28992', //HERE IS THE DATA SOURCE PROJECTION
		url: 'https://datalab.purmerend.nl/geoserver/topp/wms?',
		params: {'LAYERS': 'topp:Lufo_Totaal_2015'},
		serverType: 'geoserver'
	})
});

// Lufo 2014 Purmerend
var lufo_2014_purm = new ol.layer.Tile({
	id: "purm_lufo2014",
	sldDiv: "sld_div_purm_lufo2014",
	infoDiv: "info_div_purm_lufo2014",
	sld: "purm_sld_lufo2014",
	lgnd: "purm_lgn_lufo2014",
	// metadata attributen
	meta_naam: "Luchtfoto 2014 Gemeente Purmerend",
	meta_soort: "Raster kaart",
	meta_org: "Geo Informatie</a>",
	meta_bijgewerkt:'2014',
	// metadata attributen
	title: "2014 Purmerend",
	isLufo: true,
	opacity: 0.9,
	visible:false,
	isQueryable: false,
	source: new ol.source.TileWMS({
		projection: 'EPSG:28992', //HERE IS THE DATA SOURCE PROJECTION
		url: 'https://datalab.purmerend.nl/geoserver/topp/wms?',
		params: {'LAYERS': 'topp:Lufo_Purmerend_2014'},
		serverType: 'geoserver'
	})
});

// Lufo 2013 Purmerend
var lufo_2013_purm = new ol.layer.Tile({
	id: "purm_lufo2013",
	sldDiv: "sld_div_purm_lufo2013",
	infoDiv: "info_div_purm_lufo2013",
	sld: "purm_sld_lufo2013",
	lgnd: "purm_lgn_lufo2013",
	// metadata attributen
	meta_naam: "Luchtfoto 2013 Gemeente Purmerend",
	meta_soort: "Raster kaart",
	meta_org: "Geo Informatie</a>",
	meta_bijgewerkt:'2013',
	// metadata attributen
	title: "2013 Purmerend",
	isLufo: true,
	opacity: 0.9,
	visible:false,
	isQueryable: false,
	source: new ol.source.TileWMS({
		projection: 'EPSG:28992', //HERE IS THE DATA SOURCE PROJECTION
		url: 'https://datalab.purmerend.nl/geoserver/topp/wms?',
		params: {'LAYERS': 'topp:Lufo_Purmerend_2013'},
		serverType: 'geoserver'
	})
});

// Lufo 2013 Beemster
var lufo_2013_beem = new ol.layer.Tile({
	id: "beem_lufo2013",
	sldDiv: "sld_div_beem_lufo2013",
	infoDiv: "info_div_beem_lufo2013",
	sld: "beem_sld_beem_lufo2013",
	lgnd: "beem_lgn_beem_lufo2013",
	// metadata attributen
	meta_naam: "Luchtfoto 2013 Gemeente Beemster",
	meta_soort: "Raster kaart",
	meta_org: "Geo Informatie</a>",
	meta_bijgewerkt:'2013',
	// metadata attributen
	title: "2013 Beemster",
	isLufo: true,
	opacity: 0.9,
	visible:false,
	isQueryable: false,
	source: new ol.source.TileWMS({
		projection: 'EPSG:28992', //HERE IS THE DATA SOURCE PROJECTION
		url: 'https://datalab.purmerend.nl/geoserver/topp/wms?',
		params: {'LAYERS': 'topp:Lufo_Beemster_2013'},
		serverType: 'geoserver'
	})
});

// Lufo 2012 Purmerend
var lufo_2012_purm = new ol.layer.Tile({
	id: "purm_lufo2012",
	sldDiv: "sld_div_purm_lufo2012",
	infoDiv: "info_div_purm_lufo2012",
	sld: "purm_sld_lufo2012",
	lgnd: "purm_lgn_lufo2012",
	// metadata attributen
	meta_naam: "Luchtfoto 2012 Gemeente Purmerend",
	meta_soort: "Raster kaart",
	meta_org: "Geo Informatie</a>",
	meta_bijgewerkt:'2012',
	// metadata attributen
	title: "2012 Purmerend",
	isLufo: true,
	opacity: 0.9,
	visible:false,
	isQueryable: false,
	source: new ol.source.TileWMS({
		projection: 'EPSG:28992', //HERE IS THE DATA SOURCE PROJECTION
		url: 'https://datalab.purmerend.nl/geoserver/topp/wms?',
		params: {'LAYERS': 'topp:Lufo_Purmerend_2012'},
		serverType: 'geoserver'
	})
});

// Lufo 2011 Purmerend
var lufo_2011_purm = new ol.layer.Tile({
	id: "purm_lufo2011",
	sldDiv: "sld_div_purm_lufo2011",
	infoDiv: "info_div_purm_lufo2011",
	sld: "purm_sld_lufo2011",
	lgnd: "purm_lgn_lufo2011",
	// metadata attributen
	meta_naam: "Luchtfoto 2012 Gemeente Purmerend",
	meta_soort: "Raster kaart",
	meta_org: "Geo Informatie</a>",
	meta_bijgewerkt:'2011',
	// metadata attributen
	title: "2011 Purmerend",
	isLufo: true,
	opacity: 0.9,
	visible:false,
	isQueryable: false,
	source: new ol.source.TileWMS({
		projection: 'EPSG:28992', //HERE IS THE DATA SOURCE PROJECTION
		url: 'https://datalab.purmerend.nl/geoserver/topp/wms?',
		params: {'LAYERS': 'topp:Lufo_Purmerend_2011'},
		serverType: 'geoserver'
	})
});

// Lufo 2011 Beemster
var beem_2011 = new ol.layer.Tile({
	id: "beem_lufo2011",
	sldDiv: "sld_div_beem_lufo2011",
	infoDiv: "info_div_beem_lufo2011",
	sld: "beem_sld_lufo2011",
	lgnd: "beem_lgn_lufo2011",
	// metadata attributen
	meta_naam: "Luchtfoto 2011 Gemeente Beemster",
	meta_soort: "Raster kaart",
	meta_org: "Geo Informatie</a>",
	meta_bijgewerkt:'2011',
	// metadata attributen
	title: "2011 Beemster",
	isLufo: true,
	opacity: 0.9,
	visible:false,
	isQueryable: false,
	source: new ol.source.TileWMS({
		projection: 'EPSG:28992', //HERE IS THE DATA SOURCE PROJECTION
		url: 'https://datalab.purmerend.nl/geoserver/topp/wms?',
		params: {'LAYERS': 'topp:Lufo_Beemster_2011'},
		serverType: 'geoserver'
	})
});

// Lufo 2011 Purmerend
var lufo_2010_purm = new ol.layer.Tile({
	id: "purm_lufo2010",
	sldDiv: "sld_div_purm_lufo2010",
	infoDiv: "info_div_purm_lufo2010",
	sld: "purm_sld_lufo2010",
	lgnd: "purm_lgn_purm_lufo2010",
	// metadata attributen
	meta_naam: "Luchtfoto 2010 Gemeente Purmerend",
	meta_soort: "Raster kaart",
	meta_org: "Geo Informatie</a>",
	meta_bijgewerkt:'2010',
	// metadata attributen
	title: "2010 Purmerend",
	isLufo: true,
	opacity: 0.9,
	visible:false,
	isQueryable: false,
	source: new ol.source.TileWMS({
		projection: 'EPSG:28992', //HERE IS THE DATA SOURCE PROJECTION
		url: 'https://datalab.purmerend.nl/geoserver/topp/wms?',
		params: {'LAYERS': 'topp:Lufo_Purmerend_2010'},
		serverType: 'geoserver'
	})
});

// add gejson subbuurten
var subbuurten_layer = new ol.layer.Tile({
    id: "id_subrt",
    sldDiv: "sld_div_subburt",
    infoDiv: "info_div_subbuurten",
    sld: "sld_subrt",
    lgnd: "lgnd_subrt",
    filterId: "flt_subrt",
    dataFilterId: "prm_data_flt_subrt",
    dataZoekId: "prm_zoek_data_subbuurt",
    layerName: 'topp:Purmerend_subbuurten',
    // metadata attributen
    meta_naam: "Subbuurten Gemeente Purmerend",
    meta_soort: "Thema kaart",
    meta_org: "Ruimtelijke Ontwikkeling</a>",
    meta_bijgewerkt: '2015',
    // metadata attributen
    title: "Subbuurten",
    isLufo: false,
    opacity: 0.7,
    visible:false,
    isQueryable: true,
    source: new ol.source.TileWMS({
        projection: 'EPSG:28992', //HERE IS THE DATA SOURCE PROJECTION
        url: 'https://datalab.purmerend.nl/geoserver/topp/wms?',
        params: {'layers': 'topp:Purmerend_subbuurten'},
        serverType: 'geoserver'
    })
});

var buurten_layer = new ol.layer.Tile({
    id: "prm_buurten",
    sldDiv: "sld_div_burt",
    infoDiv: "info_div_buurt",
    sld: "prm_sld_buurten",
    lgnd: "prm_lgn_buurten",
    filterId: "flt_buurten",
    dataFilterId: "prm_data_flt_burt",
    dataZoekId: "prm_zoek_data_buurten",
    layerName: 'topp:BAG_Purmerend_buurten',
    // metadata attributen
    meta_naam: "Buurten Gemeente Purmerend",
    meta_soort: "Thema kaart",
    meta_org: "Ruimtelijke Ontwikkeling</a>",
    meta_bijgewerkt: '2017',
    // metadata attributen
    title: "Buurten",
    isLufo: false,
    opacity: 0.7,
    visible:false,
    isQueryable: true,
    source: new ol.source.TileWMS({
        projection: 'EPSG:28992', //HERE IS THE DATA SOURCE PROJECTION
        url: 'https://datalab.purmerend.nl/geoserver/topp/wms?',
        params: {'layers': 'topp:BAG_Purmerend_buurten'},
        serverType: 'geoserver'
    })
});


// marker layers
vectorSource = new ol.source.Vector({});
vectorLayer = new ol.layer.Vector({
title: "Marker Layer",
source: vectorSource
});

var layerList =
[
// pdok_brt,
brt_topo_kaart,
lufo_2019_purm_totaal,
lufo_2019_totaal,
lufo_2018_totaal,
lufo_2017_totaal,
lufo_2016_totaal,
lufo_2015_totaal,
lufo_2014_purm,
lufo_2013_purm,
lufo_2013_beem,
lufo_2012_purm,
lufo_2011_purm,
beem_2011,
lufo_2010_purm,
// bgt_wmts,
// pdok_bag,
vectorLayer
];
