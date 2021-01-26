var map, vectorLayer, vectorSource, panorama, cql_filter;

function init(){
	// Projection naar 28992 RD
	proj4.defs("EPSG:28992","+proj=sterea +lat_0=52.15616055555555 +lon_0=5.38763888888889 +k=0.9999079 +x_0=155000 +y_0=463000 +ellps=bessel +towgs84=565.417,50.3319,465.552,-0.398957,0.343988,-1.8774,4.0725 +units=m +no_defs");

	var select = new ol.interaction.Select({
   wrapX: false
 });

 var modify = new ol.interaction.Modify({
   features: select.getFeatures()
 });

 	// google street view API
	panorama = new google.maps.StreetViewPanorama(
	document.getElementById('street-view'),
	{
		position: {lat:52.506549, lng:4.953913},
		pov: {heading: 165, pitch: 0},
		zoom: 1
	});

	// create vector source for selected objects
	vectorSource = new ol.source.Vector({});

	var viewProjection = view.getProjection();
	var viewResolution = view.getResolution();

	// Elements that make up the popup.
	var container = document.getElementById('popup');
	var content = document.getElementById('popup-content');
	var closer = document.getElementById('popup-closer');

	// Create an overlay to anchor the popup to the map.
	var overlay = new ol.Overlay({
			element: container,
			autoPan: true,
			autoPanAnimation: {
					duration: 250
			}
	});

	// map class
	map = new ol.Map({
		interactions: ol.interaction.defaults().extend([select]),
		layers:layerList,
		target: 'map',
		controls: ol.control.defaults({
			attribution: false
		}).extend([mousePositionControl, zoomSlider]),
		view: view
	}); // END Map Class


	// create a dynamisch table
	var start_tabelregel = "<table class='table'  width='100%' cellspacing = '0'>";
	var header_regel = "<tbody>";
	var content_thema = " ";
	var content_basisreg = " ";
	var content_baselayer = " ";
	var einde_tabelregel = "</tbody></table>";

	var content_legendlink = " ";
	// filter div content
	var content_zoekdatamodal = " ";
	// slider modal content
	var content_slidermodal = " ";
	// data filter div
	var content_filter_data = " ";
	// metadata informatie div
	var content_infomodal = " ";

	// add layers to the html div
	layerList.forEach(function(layer, i) {

		var name = layer.get('title');
		var visiblity = layer.get('visible');
		var transparantie = layer.get('opacity');
		var lyrID = layer.get('id');
		var sldID = layer.get('sld');
		var lgndID = layer.get('lgnd');
		var basisregistratie = layer.get('basisreg');
		var luchtfotokaart = layer.get('isLufo');
		var filterID = layer.get('filterId');
		var sldDiv = layer.get('sldDiv');
		var dataFilterID = layer.get('dataFilterId');
		var infoDiv = layer.get('infoDiv');
		var zoekOpData = layer.get('dataZoekId');

		content_zoekdatamodal += "<div class='modal fade' id='"+filterID+"' role='dialog'>";
		content_zoekdatamodal += "<div class='modal-dialog'>";
		content_zoekdatamodal += "<div class='modal-content'>";
		content_zoekdatamodal += "<div class='modal-header'>";
		content_zoekdatamodal += "<button type='button' class='close' data-dismiss='modal'>&times;</button>";
		content_zoekdatamodal += "<h5 class='modal-title'>Zoek op Data</h5>";
		content_zoekdatamodal += "</div>";
		content_zoekdatamodal += "<div class='modal-body'>";
		content_zoekdatamodal += "<div class='form-group'>";
		content_zoekdatamodal += "<div class='p-3 mb-2 bg-info text-white'>* U kunt zoeken op data [ "+layer.get('search_fields')+" ] </div></br>";
		content_zoekdatamodal += "<label for='"+ zoekOpData+ "'>"+name+"</label>";
		content_zoekdatamodal += "<input name='datafilterinput' type='text' class='form-control' placeholder='Filter data...' id='"+ zoekOpData +"'/>";
		content_zoekdatamodal += "</div>";
		content_zoekdatamodal += "<div class='zoekDataResult'>";
		content_zoekdatamodal += "</div>";
		content_zoekdatamodal += "</div>";
		content_zoekdatamodal += "</div>";
		content_zoekdatamodal += "<div class='modal-footer'>";
		content_zoekdatamodal += "</div>";
		content_zoekdatamodal += "</div>";
		content_zoekdatamodal += "</div>";

		// legend model popup slider
		content_slidermodal += "<div class='modal fade' id='"+sldDiv+"' role='dialog'>";
		content_slidermodal += "<div class='modal-dialog'>";
		content_slidermodal += "<div class='modal-content'>";
		content_slidermodal += "<div class='modal-header'>";
		content_slidermodal += "<button type='button' class='close' data-dismiss='modal'>&times;</button>";
		content_slidermodal += "<h5 class='modal-title'>Zichtbaarheid - "+ name +" </h5>";
		content_slidermodal += "</div>";
		content_slidermodal += "<div class='modal-body'>";
		content_slidermodal += "<div class='slidertabel' id='"+ sldID +"'>";
		content_slidermodal += "<div class='ui-slider-handle'></div>";
		content_slidermodal += "</div>"
		content_slidermodal += "</div>";
		content_slidermodal += "<div class='modal-footer'>";
		content_slidermodal += "</div>";
		content_slidermodal += "</div>";
		content_slidermodal += "</div>";
		content_slidermodal += "</div>";


		// Metadata info div - modal
		content_infomodal += "<div class='modal fade' id='"+infoDiv+"' role='dialog'>";
		content_infomodal += "<div class='modal-dialog'>";
		content_infomodal += "<div class='modal-content'>";
		content_infomodal += "<div class='modal-body'>";

		// metadata informatie content
		content_infomodal += "<table class='table'  width='100%' cellspacing = '0'>"
		content_infomodal += "<tbody>";

		content_infomodal += "<tr>";
		content_infomodal += "<td class='eerste_div'><b>Naam</b></td>";
		content_infomodal += "<td class='tweede_div'>";
		content_infomodal += layer.get('meta_naam');
		content_infomodal += "</td>";
		content_infomodal += "</tr>";

		content_infomodal += "<tr>";
		content_infomodal += "<td class='eerste_div'><b>Soort</b></td>";
		content_infomodal += "<td class='tweede_div'>";
		content_infomodal += layer.get('meta_soort');
		content_infomodal += "</td>";
		content_infomodal += "</tr>";

		content_infomodal += "<tr>";
		content_infomodal += "<td class='eerste_div'><b>Organisatie beheerder</b></td>";
		content_infomodal += "<td class='tweede_div'>";
		content_infomodal += layer.get('meta_org');
		content_infomodal += "</td>";
		content_infomodal += "</tr>";

		content_infomodal += "<tr>";
		content_infomodal += "<td class='eerste_div'><b>Bijgewerkt per</b></td>";
		content_infomodal += "<td class='tweede_div'>";
		content_infomodal += layer.get('meta_bijgewerkt');
		content_infomodal += "</td>";
		content_infomodal += "</tr>";

		content_infomodal += "</tbody>";

		content_infomodal += "</table>";


		content_infomodal += "</div>";
		content_infomodal += "</div>";
		content_infomodal += "</div>";
		content_infomodal += "</div>";


		// get layer name for NOT baseLayer
		if(!layer.get('isBaseLayer') && name != "Marker Layer"){

			var linkSrc = "https://datalab.purmerend.nl/geoserver/topp/wms?REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&WIDTH=20&HEIGHT=20&LAYER="+ layer.get('layerName') +"";

			// legend model popup content
			content_legendlink += "<div class='modal fade' id='"+lgndID+"' role='dialog'>";
			content_legendlink += "<div class='modal-dialog'>";
			content_legendlink += "<div class='modal-content'>";
			content_legendlink += "<div class='modal-header'>";
			content_legendlink += "<button type='button' class='close' data-dismiss='modal'>&times;</button>";
			content_legendlink += "<h5 class='modal-title'> Legenda - "+ name +"</h5>";
			content_legendlink += "</div>";
			content_legendlink += "<div class='modal-body'>";
			content_legendlink += "<img src='"+ linkSrc +"' />";
			content_legendlink += "</div>";
			content_legendlink += "<div class='modal-footer'>";
			content_legendlink += "</div>";
			content_legendlink += "</div>";
			content_legendlink += "</div>";
			content_legendlink += "</div>";

		}

		// get layer name for GeoJSON layers
		if(layer.get('isgeojson')){
			// legend model popup content
			content_legendlink += "<div class='modal fade' id='"+lgndID+"' role='dialog'>";
			content_legendlink += "<div class='modal-dialog'>";
			content_legendlink += "<div class='modal-content'>";
			content_legendlink += "<div class='modal-header'>";
			content_legendlink += "<button type='button' class='close' data-dismiss='modal'>&times;</button>";
			content_legendlink += "<h5 class='modal-title'>Legenda - "+ name +"</h5>";
			content_legendlink += "</div>";
			content_legendlink += "<div class='modal-body'>";
			//content_legendlink += "<img src='"+ linkSrc +"' />";
			content_legendlink += "</div>";
			content_legendlink += "<div class='modal-footer'>";
			content_legendlink += "</div>";
			content_legendlink += "</div>";
			content_legendlink += "</div>";
			content_legendlink += "</div>";

		}

		// check for baseLayer
		if(layer.get('isBaseLayer')){
			content_baselayer += "<tr>";
			content_baselayer += "<td class='eerste'>";
			if(visiblity){ //check the visibility
				content_baselayer += "<input checked type='radio' id='"+ lyrID +"' name='achtergronden'> <label for='"+ lyrID +"'>"+ name +" </label>";
			}else{
				content_baselayer += "<input type='radio' id='"+ lyrID +"' name='achtergronden'> <label for='"+ lyrID +"'>"+ name +" </label>";
			}
			content_baselayer += "</td>";

			// metadata informatie
			content_baselayer += "<td class='tweede'>";
			content_baselayer += "<a data-tooltip='tooltip' title='Informatie'  data-toggle='modal' data-target='#"+infoDiv+"' >";
			content_baselayer += "<img src='" + informatie_png + "' height='20' width='20'/>";
			content_baselayer += "</a>";
			content_baselayer += "</td>";

			content_baselayer += "<td class='tweede'>";
			content_baselayer += "<a data-tooltip='tooltip' title='Zichtbaarheid' data-toggle='modal' data-target='#"+sldDiv+"'>";
			content_baselayer += "<img src='" + transparantie_png + "' height='20' width='20'/>";
			content_baselayer += "</a>";
			content_baselayer += "</td>";

			content_baselayer += "</tr>";

		}

		// Thema kaarten - check for NOT base layer and NOT marker layer and NOT PDOK layer
		if(!layer.get('isBaseLayer') && name != "Marker Layer" && !basisregistratie && !luchtfotokaart){
			// dynamisch legenda content
			content_thema += "<tr>";
			content_thema += "<td class='eerste'>";

			if(visiblity){ //check the visibility
				content_thema += "<span class='layerName'>" + name + "</span>";
				content_thema += "<div class ='layer-switch pull-right'>";
				content_thema += "<input checked id='"+ lyrID +"' value='"+ lyrID +"' type='checkbox'/><label class='label-success' for='"+ lyrID +"'></label>";
				content_thema += "</div>";
			} else{
				content_thema += "<span class='layerName'>" + name + "</span>";
				content_thema += "<div class ='layer-switch pull-right'>";
				content_thema += "<input id='"+ lyrID +"' value='"+ lyrID +"' type='checkbox'/><label class='label-success' for='"+ lyrID +"'></label>";
				content_thema += "</div>";
			}
			content_thema += "</td>";

			content_thema += "<td class='tweede'>";
			content_thema += "<a data-tooltip='tooltip' title='Legenda' data-toggle='modal' data-target='#"+lgndID+"'>";
			content_thema += "<img src='" + legendicon_png + "' height='20' width='20'/>";
			content_thema += "</a>";
			content_thema += "</td>";

			content_thema += "<td class='tweede'>";
			content_thema += "<a class='filterempty' data-tooltip='tooltip' title='Zoek op data'  data-toggle='modal' data-target='#"+filterID+"'>";
			content_thema += "<img src='" + filter_png + "' height='20' width='20'/>";
			content_thema += "</a>";
			content_thema += "</td>";

			content_thema += "<td class='tweede'>";
			content_thema += "<a data-tooltip='tooltip' title='Metadata informatie'  data-toggle='modal' data-target='#"+infoDiv+"'>";
			content_thema += "<img src='" + informatie_png + "' height='20' width='20'/>";
			content_thema += "</a>";
			content_thema += "</td>";

			content_thema += "<td class='tweede'>";
			content_thema += "<a data-tooltip='tooltip' title='Zichtbaarheid'  data-toggle='modal' data-target='#"+sldDiv+"'>";
			content_thema += "<img src='" + transparantie_png + "' height='20' width='20'/>";
			content_thema += "</a>";
			content_thema += "</td>";

			content_thema += "</tr>";
		}

		// check for basisregistratie layers
		if(basisregistratie){

			content_basisreg+= "<tr>";
			content_basisreg += "<td class='eerste'>";

			if(visiblity){ //check the visibility
				content_basisreg += "<span class='layerName'>" + name + "</span>";
				content_basisreg += "<div class ='layer-switch pull-right'>";
				content_basisreg += "<input checked id='"+ lyrID +"' value='"+ lyrID +"' type='checkbox'/><label class='label-success' for='"+ lyrID +"'></label>";
				content_basisreg += "</div>";
			} else{
				content_basisreg += "<span class='layerName'>" + name + "</span>";
				content_basisreg += "<div class ='layer-switch pull-right'>";
				content_basisreg += "<input id='"+ lyrID +"' value='"+ lyrID +"' type='checkbox'/><label class='label-success' for='"+ lyrID +"'></label>";
				content_basisreg += "</div>";
			}
			content_basisreg += "</td>";

			content_basisreg += "<td class='tweede'>";
			content_basisreg += "<a data-tooltip='tooltip' title='Legenda'  data-toggle='modal' data-target='#"+lgndID+"'>";
			content_basisreg += "<img src='" + legendicon_png + "' height='20' width='20'/>";
			content_basisreg += "</a>";
			content_basisreg += "</td>";

			content_basisreg += "<td class='tweede'>";
			content_basisreg += "<a data-tooltip='tooltip' title='Metadata informatie'  data-toggle='modal' data-target='#"+infoDiv+"'>";
			content_basisreg += "<img src='" + informatie_png + "' height='20' width='20'/>";
			content_basisreg += "</a>";
			content_basisreg += "</td>";

			content_basisreg += "<td class='tweede'>";
			content_basisreg += "<a data-tooltip='tooltip' title='Zichtbaarheid'  data-toggle='modal' data-target='#"+sldDiv+"'>";
			content_basisreg += "<img src='" + transparantie_png + "' height='20' width='20'/>";
			content_basisreg += "</a>";
			content_basisreg += "</td>";

			content_basisreg += "</tr>";
		}
	}); // END foreach LayerList

	// add thema layers
	$( "#themakaarten" ).append(start_tabelregel+header_regel+content_thema+einde_tabelregel);

	// add basisregistratie layers
	$( "#basiskaarten" ).append(start_tabelregel+header_regel+content_basisreg+einde_tabelregel);

	// add baselayer layers
	$( "#achtergronden" ).append("<table class='table' width='100%' cellspacing='0'><tbody>"+content_baselayer+"</tbody></table>");

	// add metadata info popup
	$("#metadaInfoDiv").append(content_infomodal);

	// add legend img popup
	$("#legengimgdiv").append(content_legendlink);

	// add filter layer div
	// $("#filterDataInput").append(content_filtermodal);

	// add slider layer div
	$("#sliderdiv").append(content_slidermodal);

	// add zoek op data layer div
	$("#zoekopdataDiv").append(content_zoekdatamodal);

	// slider tool tip
	$('[data-tooltip="tooltip"]').tooltip();

	// clear datafilkter div
	$('input[name="datafilterinput"]').click(function(){
			$(".zoekDataResult").empty();
	});

	// empty data result div when fiter button is cliked
	$('.filterempty').on('click', function(){
		$(".zoekDataResult").empty();
	}); // END click function

	map.getLayers().forEach(function (lyr) {
		// zoek op data functie // geen baselayer en geen mark layer
		if((!lyr.get('isBaseLayer')) && (lyr.get('title') != "Marker Layer") && (!lyr.get('basisreg')) && (!lyr.get('isLufo'))){
			// laagnaam ophalen
			var layerName = lyr.get('layerName');

			// data filter zoek ajax
			$('#'+ (lyr.get('dataZoekId'))+'').autocomplete({

				source: function(request, response){
					var matcher = new RegExp( $.ui.autocomplete.escapeRegex(request.term), "i" );

					// dynamisch filter
					function LayerDataFilter(){

						if(lyr.get('search_fields')){

							var attr_str_list = [];


							for (var i = 0; i < lyr.get('search_fields').length; i++) {
								// create list for search_fields attributes
								attr_str_list.push(lyr.get('search_fields')[i]+" ILIKE '"+request.term+"'");
							}

							cql_filter = "CQL_FILTER=" + attr_str_list.join(' OR ');

							console.log(cql_filter);

						}
						// filter param.
						return cql_filter;
					}

					// create wfs layer URL
					var url_val = "https://datalab.purmerend.nl/geoserver/topp/ows?service=WFS&" +
						"version=1.1.0&request=GetFeature&typename=" + layerName+ "&" +
						LayerDataFilter() +
						"&outputFormat=application/json&srsname=EPSG:28992";

					$.ajax({
							url: url_val,
							dataType: "json",
							success: function (data) {
								$(".zoekDataResult").empty();

								response($.map(data.features, function(v,i){
									var json_obj = {};
									$.each(v.properties, function(prop_name,prop_val){
										for (var i = 0; i < lyr.get('search_fields').length; i++) {

											// attributen from layer list
											if (prop_name == lyr.get('search_fields')[i]) {
												json_obj[prop_name] = prop_val;
											}
										}

									}); // END forEach


	 								var label_val = "";

									for (var key in json_obj){
										 if(json_obj[key] && (!request.term || matcher.test(json_obj[key]) ) ){
											 for (var i = 0; i < lyr.get('search_fields').length; i++) {
												 label_val += lyr.get('search_fields')[0]+ " : " + json_obj[lyr.get('search_fields')[0]] + ", " +  lyr.get('search_fields')[1] + " : " + json_obj[lyr.get('search_fields')[1]];

												 return {
													 label: label_val,
													 attribute_name: [lyr.get('search_fields')[0], lyr.get('search_fields')[1]],
													 attribute_value: [json_obj[lyr.get('search_fields')[0]], json_obj[lyr.get('search_fields')[1]]]
												 };

											 }

										 }
									}
								})); // END response
							}
					});

				},
				select: function(event, ui){
					var content_result = " ";
					content_result += "<tr><td class='eerste'><b>"+ui.item.attribute_name[0]+"</b></td>";
					content_result += "<td>" + ui.item.attribute_value[0]+ "</td>";
					content_result += "</tr>";
					content_result += "<tr><td class='eerste'><b>"+ui.item.attribute_name[1]+"</b></td>";
					content_result += "<td>" + ui.item.attribute_value[1] + "</td>";
					content_result += "</tr>";

					// zoom at map link
					var lookAtMapLink = "<button type='button' class='btn btn-primary btn-sm'>Bekijk op de kaart > <span class='glyphicon glyphicon-globe'></span></button>";

					// append data result table
					$( ".zoekDataResult" ).append(start_tabelregel+header_regel+content_result+einde_tabelregel);
					$( ".zoekDataResult" ).append(lookAtMapLink);

				} // END select
			});

		} // END if


		// Layer on-off if the layer is baselayer
		if(lyr.get('isBaseLayer')){
			// basemap OSM
			$( "input[name='achtergronden']" ).change(function() {
				if($('#'+ (lyr.get('id'))+'').is(":checked")) {
					lyr.setVisible(true);
				}
				else{
					lyr.setVisible(false);
				}
			});

		} // END if ! isBaseLayer

		// Layer on-off if the layer is NOT baselayer
		if(!lyr.get('isBaseLayer')){
			// layer change functie
			$('#'+ (lyr.get('id'))+'').change(function(){
				if($(this).is(":checked")){
					lyr.setVisible(true);

					if (window.vueStore) {
						window.vueStore.commit('addLayer', { 'id': lyr.get('id'), 'is_visible': true });
					}
				}
				else{
					lyr.setVisible(false);

					if (window.vueStore) {
						window.vueStore.commit('deleteLayer', { 'id': lyr.get('id'), 'is_visible': true });
					}
				}
			}); // END change function
		} // END if NOT isBaseLayer

		// slider
		$('#'+ (lyr.get('sld'))+'').slider({
			range: "min",
			min: 0,
			max: 100,
			value: (lyr.get('opacity')*100),
			create: function(event, ui) {
				var value = $(this).slider("option","value");
				$(this).find(".ui-slider-handle").text(value);
			},
			slide: function( event, ui ) {
					$(this).find('.ui-slider-handle').text(ui.value);
					lyr.setOpacity(ui.value/100);
			}
		}); // END slider

  }); //END getLayers()

	// get streetviewCoordinates
	function streetViewCoordinates(evt) {
		var lat_value = evt.coordinate[1];
		var lng_value = evt.coordinate[0];

		// to convert coordinate from lat long to x-y RD
		var convrt = ol.proj.transform([lng_value, lat_value], 'EPSG:28992','EPSG:4326');

		var lat_val_conv = convrt[0];
		var lot_val_conv = convrt[1];

		var streetViewPlace = {lat:lot_val_conv, lng:lat_val_conv};

		if (panorama) {
			panorama.setPosition(streetViewPlace);
		}
	}

	//first leeter Capital
	function jsUcfirst(string)
	{
	    return string.charAt(0).toUpperCase() + string.slice(1);
	}

	// get selected fature URL
	function getUrlSelected(layer, evt){
		// create URL
		var layer_url_before = layer.getSource().getGetFeatureInfoUrl(
			evt.coordinate, map.getView().getResolution(), 'EPSG:28992',
			{'INFO_FORMAT': 'application/json'}
		);

		// create url for getGetFeatureInfoUrl
		var layer_url = layer_url_before + "&QUERY_LAYERS=" + layer.get('layerName');

		return layer_url;
	}

	// set the images
	function imageselect(jaofnee){
		if (jaofnee == "1"){
			return "<img height='26' width='26' src='img/yes.png'/>";
		} else if(jaofnee == "0"){
			return "<img height='22' width='25' src='img/no.png'/>";
		}
	}

	// set pin by select object
	function selected_object(evt){
		// clear all selected objects
		vectorSource.clear();

		var cor_x = evt.coordinate[0];
		var cor_y = evt.coordinate[1];

		var iconFeature = new ol.Feature({
			geometry: new ol.geom.Point(ol.proj.transform([parseInt(cor_x), parseInt(cor_y)], 'EPSG:28992', 'EPSG:28992'))
		});

		var iconStyle = new ol.style.Style({
		 image: new ol.style.Icon(({
			 anchor: [0.5, 46],
			 anchorXUnits: 'fraction',
			 anchorYUnits: 'pixels',
			 opacity: 1,
			 src: icon_selected_png
		 }))
	 });
	 // set style
		iconFeature.setStyle(iconStyle);

		// add marker
		vectorSource.addFeature(iconFeature);
		// get vector layer
		vectorLayer = new ol.layer.Vector({
			source: vectorSource
		});
		// vector to map
		map.addLayer(vectorLayer);
	}

	// Layer Order Z-Index
	map.getLayers().forEach(function(layer){
		// layer draw order for baselayers
		if (layer.get('isBaseLayer')) {
			console.log('Base layer: ', layer.get('title'));
			layer.setZIndex(-999);
		}
		// layer draw order for basisreg
		if (layer.get('basisreg')) {
			console.log('Basis-reg layer: ', layer.get('title'));
			layer.setZIndex(-99);
		}
		// layer draw order for themelayer
		if (layer.get('themelayer')) {
			console.log('Theme-layer: ', layer.get('title'));
			layer.setZIndex(0);
		}
	}); // END getLayers()

	// click on map function
	map.on('click', function(evt) {

		// selected object
		selected_object(evt);

		var cor_x = evt.coordinate[0];
		var cor_y = evt.coordinate[1];

		var totaal_coordinaat = cor_x + "," + cor_y;
	 	var content_popup = "";

		// set Streetview Positie
		streetViewCoordinates(evt);

	var isFirstItem = true;

	//get layerList
	layerList.forEach(function(layer) {
		// if layer visible and not Basigreg not MarkerLayer not
		if(layer.getVisible() && !layer.get('isBaseLayer') && layer.get('title') != "Marker Layer" && layer.get('isQueryable') == true){

			// get layer URL
			var layer_url = getUrlSelected(layer, evt);

			// if url true
			if (layer_url) {
				$.ajax({
					url: layer_url,
					method:'get',
					success:function(data){
						data.features.map(function (v, i) {
							content_popup += "<a class='accordion-toggle " + (isFirstItem ? '' : 'collapsed') + "' data-toggle='collapse' data-parent='#categorieen-accordion' href='#" + layer.get('filterdataId') + "'>";
							content_popup += "<span class='text'>" + layer.get('title') + "</span>";
							content_popup += "<span class='icon-caret icon-caret-right'></span></a>";
							content_popup += "<br/>";
							content_popup += "<div id='" + layer.get('filterdataId') + "' class='" + (isFirstItem ? 'collapse in' : 'collapse') + "'>";

							isFirstItem = false;

							$.each(v.properties, function(prop_name,prop_val){
								// get popup info
								function get_popup(attr_nm, attr_val){
									var result = "";
									if (attr_nm == "meer_informatie") {
										content_popup += "<a target='_blank' href='"+prop_val+"'>Meer info</a>";
										content_popup += "<br>";

									} else if (attr_nm == "foto"){
										content_popup += "<a href='"+attr_val+"' target='_blank'><img style='width:100%;' src='"+attr_val+"'/></a>";
										content_popup += "<br>";
									} else if (attr_nm == "url"){
										content_popup += "<a href='"+attr_val+"' target='_blank'>"+attr_val+"</a>";
										content_popup += "<br>";
									} else{ // the other attribute values
										content_popup += "<b>"+jsUcfirst(attr_nm)+": </b>";
										content_popup += attr_val;
										content_popup += "<br>";
									}
									return content_popup;
								}

									// has layer the popupAttributes properties?
									if(layer.get('popupAttributes')){

										// get feature attributes from param: popupAttributes per layer
										for (var i = 0; i < layer.get('popupAttributes').length; i++) {

											//create popup content if NOT empty
											if(prop_val != "" && prop_val != null && prop_name == layer.get('popupAttributes')[i]){

												// call get popup info function
												get_popup(prop_name, prop_val);

											}
										}

									} else{
										//create popup content if NOT empty
										if(prop_val != "" && prop_val != null){

											// call get popup info function
											get_popup(prop_name, prop_val);

										}

									}

								});

							 content_popup += "</div>";

							 });

							// add pop-up info content
							$("#dataResult").html(content_popup);
							$("#popupTitle").html("Geselecteerde objecten");
							$('#dataresulmodal').modal('show');

						} // END success

					}); // END Ajax

				} // END if layer url

			} // END if layer visibility

		}); // END layersList forEach

	}); // END map.on.click

	// Zoek op adres button
	$(".btn_zoek_adres_style").click(function(){
		$(".btn_zoek_adres_style").toggleClass("zoek_adres_actief");
		if ($(this).hasClass('zoek_adres_actief')){
			// set zoek op adres On
			$("#zoekopadresDiv").show();
			// specifiek for IE-11
			$(".btn_zoek_adres_style").css('background-color', '#afc812');
		} else {
			// set zoek op adres Off
			$("#zoekopadresDiv").hide();
			// specifiek for IE-11
			$(".btn_zoek_adres_style").css('background-color', '#fff');
		}

	});

	$(".btn_embed_style").click(function() {
		$("#embedModal").modal('toggle');
	});

	map.on('moveend', function() {
		var view = map.getView();

		coord = view.getCenter();
		dynamisch_adres_coordinate = coord[0] + ", " + coord[1];

		if (!window.vueStore) {
			return;
		}

		window.vueStore.commit('setPosition', {
			center: coord,
			zoom: view.getZoom(),
			tool: ''
		});
	});

	// update de layers when de db changed
	map.updateSize();

} // END Init()
