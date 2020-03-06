var map, vector, source, vectorSource, vectorLayer, panorama, cql_filter;
// set generic selected layer, attribute name from list
var layer_name, layer_id, attribute_name;

// map viewer coordinates for the street-view
var coordint_map_viewer = "";
var dynamisch_adres_coordinate = "null";

function init(){
	// Projection naar 28992 RD
	proj4.defs("EPSG:28992","+proj=sterea +lat_0=52.15616055555555 +lon_0=5.38763888888889 +k=0.9999079 +x_0=155000 +y_0=463000 +ellps=bessel +towgs84=565.417,50.3319,465.552,-0.398957,0.343988,-1.8774,4.0725 +units=m +no_defs");

 var select = new ol.interaction.Select();

 var selectedFeatures = select.getFeatures();

	// a DragBox interaction used to select features by drawing boxes
 var dragBox = new ol.interaction.DragBox({
	 condition: ol.events.condition.platformModifierKeyOnly
 });

	// check Street-View
	var isStreetViewActief = false;
	// check interactions
	var is_interaction = false;
	// measure draw source
	source = new ol.source.Vector();

	// create vector source for selected objects
	vectorSource = new ol.source.Vector({});

	// meause draw layer
	vector = new ol.layer.Vector({
	 source: source,
	 style: new ol.style.Style({
		 fill: new ol.style.Fill({
			 color: 'rgba(255, 255, 255, 0.2)'
		 }),
		 stroke: new ol.style.Stroke({
			 color: '#ffcc33',
			 width: 2
		 }),
		 image: new ol.style.Circle({
			 radius: 7,
			 fill: new ol.style.Fill({
				 color: '#ffcc33'
			 })
		 })
	 })
 });

 // mouseover handle
 var mouseMoveHandler = function(evt) {
	 if (sketch) {
		 var output;
		 var geom = (sketch.getGeometry());
		 if (geom instanceof ol.geom.Polygon) {
			 output = formatArea(/** @type {ol.geom.Polygon} */ (geom));

		 } else if (geom instanceof ol.geom.LineString) {
			 output = formatLength( /** @type {ol.geom.LineString} */ (geom));
		 }
		 sketchElement.innerHTML = output;
	 }
 };


	var sketch;
	var sketchElement;

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
		}).extend([mousePositionControl, zoomSlider]),
		view: view
	}); // END Map Class

	// mousemove event
	$(map.getViewport()).on('mousemove', mouseMoveHandler);

	// measure type selection
	// var typeSelect = document.getElementById('type');
	var type = 'LineString';

	// measure draw function
	var draw, draw_adres; // global so we can remove it later
	// interaction for measure function
	function addInteraction() {
		// get select option value from list
	  // var type = (typeSelect.value == 'area' ? 'Polygon' : 'LineString');
	  draw = new ol.interaction.Draw({
	    source: source,
	    type: /** @type {ol.geom.GeometryType} */ type
	  });

	  map.addInteraction(draw);

	  draw.on('drawstart', function(evt) {
			// clean reslt value
			$("#measureOutput").empty();
			$("#measureOutput").show();

	    // set sketch
	    sketch = evt.feature;
	    sketchElement = document.createElement('li');
	    var outputList = document.getElementById('measureOutput');

	    if (outputList.childNodes) {
	      outputList.insertBefore(sketchElement, outputList.firstChild);
	    } else {
	      outputList.appendChild(sketchElement);
	    }
	  }, this);

	  draw.on('drawend', function(evt) {

	      // unset sketch
	      sketch = null;
	      sketchElement = null;
	    }, this);
	}

	// get feature from json -url insie bbox
	function get_json_adres_url(extent){
		// get json url
		var get_feature_url = "https://datalab.purmerend.nl/geoserver/topp/ows?" +
			 "service=WFS&version=1.0.0&" +
			 "request=GetFeature&typeName=BAG_Verblijfseenheid_GEKOPPELD&" +
			 "outputFormat=application%2Fjson&" +
			 "cql_filter=Within(geom,POLYGON(("+extent+")))";
		// push url
		return get_feature_url;

	}

	// interaction for select adres
	function addInteraction_adres() {
		// set interaction for select adress function
		draw_adres = new ol.interaction.Draw({
	    source: source,
	    type: /** @type {ol.geom.GeometryType} */ type
	  });

		// add interaction to map
		map.addInteraction(draw_adres);

		draw_adres.on('drawend', function(evt){
			// get geomtry array
			geom_arry = evt['feature'].getGeometry().getCoordinates()[0];
			// set geom string list
			var geo_array_string = "";

			// get totaal geom string
			for (var i = 0; i < geom_arry.length; i++) {
				// bij y coordinates
				geo_array_string += geom_arry[i][0];
				geo_array_string += " ";
				geo_array_string += geom_arry[i][1];
				// check latste item of array
				if (i == (geom_arry.length -1)) {
					geo_array_string += "";
				} else{
					geo_array_string += ", ";
				}
			}

			// get selected data
			$.ajax({
				 url: get_json_adres_url(geo_array_string),
				 method:'get',
				 success:function(data){
					 // interaction is active
		 			is_interaction = true
					 // pop-up content
					 var content_popup = "";
					 // json object to download
					 var adres_download = JSON.stringify(data);
					 // get popup_content
					 get_popup_content(data, adres_download, CSRF_TOKEN, content_popup);

					 } // END success

			}); // END Ajax
		});

	}

	/**
	 * Let user change the geometry type.
	 * @param {Event} e Change event.
	 */
	$('.measure_type').click(function(){
		 // var type = (typeSelect.value == 'area' ? 'Polygon' : 'LineString');
		 // change measure type
		 if (this.id == 'area') {
		 	type = 'Polygon';
		} else if (this.id == 'length') {
			type = 'LineString';
		}

		// No type selected
		if(this.id == 'selecteer'){
			// hide result
			$("#measureOutput").hide();
			// function not active
			map.removeInteraction(draw);
			// remove features of the vector draw
			source.clear();

			// interaction NOT active
			is_interaction = false

			// Measure NOT actief
			$("#measure_btn").css('background-color', '#fff');

			// clean reslt value
			$("#measureOutput").empty();
		} else{
			map.removeInteraction(draw);
			addInteraction();
			// Measure actief
			$("#measure_btn").css('background-color', '#afc812');

			// interaction is active
			is_interaction = true
		}
	});
	// select type for adress
	$('.adress_select_type').click(function(){
		 // var type = (typeSelect.value == 'area' ? 'Polygon' : 'LineString');
		 // change measure type
		 if (this.id == 'area_adres') {
			type = 'Polygon';
			}
			// else if (this.id == 'length_adres') {
			// 	type = 'LineString';
			// }

		// No type selected
		if(this.id == 'selecteer_adres'){
			// function not active
			map.removeInteraction(draw_adres);
			// remove features of the vector draw
			source.clear();

			// interaction NOT active
			is_interaction = false

			// Measure NOT actief
			$("#adress_select_btn").css('background-color', '#fff');

		} else{
			map.removeInteraction(draw_adres);
			addInteraction_adres();
			// Measure actief
			$("#adress_select_btn").css('background-color', '#afc812');

			// interaction is active
			is_interaction = true
		}
	});

	/**
	 * format length output
	 * @param {ol.geom.LineString} line
	 * @return {string}
	 */
	var formatLength = function(line) {
	  var length = Math.round(line.getLength() * 100) / 100;
	  var output;
	  if (length > 100) {
	    output = 'Resultaat: ' + (Math.round(length / 1000 * 100) / 100) +
	        ' ' + 'km';
	  } else {
	    output = 'Resultaat: ' +  (Math.round(length * 100) / 100) +
	        ' ' + 'm';
	  }
	  return output;
	};

	/**
	 * format length output
	 * @param {ol.geom.Polygon} polygon
	 * @return {string}
	 */
	var formatArea = function(polygon) {
	  var area = polygon.getArea();
	  var output;
	  if (area > 10000) {
	    output = 'Resultaat: ' +  (Math.round(area / 1000000 * 100) / 100) +
	        ' ' + 'km<sup>2</sup>';
	  } else {
	    output = 'Resultaat: ' +  (Math.round(area * 100) / 100) +
	        ' ' + 'm<sup>2</sup>';
	  }
	  return output;
	};

	// add select to map
	map.addInteraction(select);
	// add dragbox to map
	map.addInteraction(dragBox);

	// create a dynamisch table
	var start_tabelregel = "<table class='table'  width='100%' cellspacing = '0'>";
	var header_regel = "<tbody>";
	var dynamish_cont_groen = " ";
	var content_basisreg = " ";
	var content_baselayer = " ";
	var content_luchtfotos = " ";
	var einde_tabelregel = "</tbody></table>";

	// legend mogel content_luchtfotos
	var content_legendlink = " ";
	// slider modal content
	var content_slidermodal = " ";
	// data filter div
	var content_filter_data = " ";
	// metadata informatie div
	var content_infomodal = " ";

	// get legend url from local and public data
	function get_legend_url(layer){
		// return value
		var get_legend_link = "";
		// check local dataset
		var layer_source = "" + layer.get('source').urls;
		var check_local_data = layer_source.search("local");

		if (check_local_data == -1) {
			get_legend_link =
				"https://datalab.purmerend.nl/geoserver/topp/wms?" +
				"REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&WIDTH=20&" +
				"HEIGHT=20&LAYER="+ layer.get('layerName') +"";
		} else{
			get_legend_link =
				"https://geoserver.purmerend.local/geoserver/topp/wms?" +
				"REQUEST=GetLegendGraphic&VERSION=1.0.0&FORMAT=image/png&WIDTH=20&" +
				"HEIGHT=20&LAYER="+ layer.get('layerName') +"";
		}

		return get_legend_link;
	}

	// set category content
	function setCategoryContent(layer) {
		// creat dynamish layer content
		var dynamish_category_content = "";
		// Thema kaarten - check for NOT base layer and NOT marker layer and NOT PDOK layer
		if(!layer.get('isBaseLayer') && name != "Marker Layer" && !basisregistratie && !luchtfotokaart){

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
			// console.log('Layer: ', name, ' category: ', cat_name);

			// get category name
			dynamish_category_content += "<tr>";
			dynamish_category_content += "<td class='eerste'>";

			if(visiblity){ //check the visibility
				dynamish_category_content += "<span class='layerName'>" + name + "</span>";
				dynamish_category_content += "<div class ='layer-switch pull-right'>";
				dynamish_category_content += "<input checked id='"+ lyrID +"' value='"+ lyrID +"' type='checkbox'/><label class='label-success' for='"+ lyrID +"'></label>";
				dynamish_category_content += "</div>";
			} else{
				dynamish_category_content += "<span class='layerName'>" + name + "</span>";
				dynamish_category_content += "<div class ='layer-switch pull-right'>";
				dynamish_category_content += "<input id='"+ lyrID +"' value='"+ lyrID +"' type='checkbox'/><label class='label-success' for='"+ lyrID +"'></label>";
				dynamish_category_content += "</div>";
			}
			dynamish_category_content += "</td>";

			dynamish_category_content += "<td class='tweede'>";
			dynamish_category_content += "<a data-tooltip='tooltip' title='Legenda' data-toggle='modal' data-target='#"+lgndID+"'>";
			dynamish_category_content += "<img src='" + legendicon_png + "' height='20' width='20'/>";
			dynamish_category_content += "</a>";
			dynamish_category_content += "</td>";

			dynamish_category_content += "<td class='tweede'>";
			dynamish_category_content += "<a data-tooltip='tooltip' title='Metadata informatie'  data-toggle='modal' data-target='#"+infoDiv+"'>";
			dynamish_category_content += "<img src='" + informatie_png + "' height='20' width='20'/>";
			dynamish_category_content += "</a>";
			dynamish_category_content += "</td>";

			dynamish_category_content += "<td class='tweede'>";
			dynamish_category_content += "<a data-tooltip='tooltip' title='Zichtbaarheid'  data-toggle='modal' data-target='#"+sldDiv+"'>";
			dynamish_category_content += "<img src='" + transparantie_png + "' height='20' width='20'/>";
			dynamish_category_content += "</a>";
			dynamish_category_content += "</td>";

			dynamish_category_content += "</tr>";

		}

		return dynamish_category_content;

	}

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
			// get legend URL
			var linkSrc = get_legend_url(layer);

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

		// check for the luchtfoto's
		if(luchtfotokaart){
			content_luchtfotos+= "<tr>";
			content_luchtfotos += "<td class='eerste'>";
			if(visiblity){ //check the visibility
				content_luchtfotos += "<span class='layerName'>" + name + "</span>";
				content_luchtfotos += "<div class ='layer-switch pull-right'>";
				content_luchtfotos += "<input checked id='"+ lyrID +"' value='"+ lyrID +"' type='checkbox'/><label class='label-success' for='"+ lyrID +"'></label>";
				content_luchtfotos += "</div>";
			} else{
				content_luchtfotos += "<span class='layerName'>" + name + "</span>";
				content_luchtfotos += "<div class ='layer-switch pull-right'>";
				content_luchtfotos += "<input id='"+ lyrID +"' value='"+ lyrID +"' type='checkbox'/><label class='label-success' for='"+ lyrID +"'></label>";
				content_luchtfotos += "</div>";
			}
			content_luchtfotos += "</td>";

			content_luchtfotos += "<td class='tweede'>";
			content_luchtfotos += "<a data-tooltip='tooltip' title='Metadata informatie'  data-toggle='modal' data-target='#"+infoDiv+"'>";
			content_luchtfotos += "<img src='" + informatie_png + "' height='20' width='20'/>";
			content_luchtfotos += "</a>";
			content_luchtfotos += "</td>";

			content_luchtfotos += "<td class='tweede'>";
			content_luchtfotos += "<a data-tooltip='tooltip' title='Zichtbaarheid'  data-toggle='modal' data-target='#"+sldDiv+"'>";
			content_luchtfotos += "<img src='" + transparantie_png + "' height='20' width='20'/>";
			content_luchtfotos += "</a>";
			content_luchtfotos += "</td>";

			content_luchtfotos += "</tr>";
		}

	}); // END foreach LayerList

	// add baselayer layers
	$( "#achtergronden" ).append("<table class='table' width='100%' cellspacing='0'><tbody>"+content_baselayer+"</tbody></table>");

	// add luchtfoto's layers
	$("#luchtfotos").append(start_tabelregel+header_regel+content_luchtfotos+einde_tabelregel);

	// add metadata info popup
	$("#metadaInfoDiv").append(content_infomodal);

	// add legend img popup
	$("#legengimgdiv").append(content_legendlink);

	// add slider layer div
	$("#sliderdiv").append(content_slidermodal);

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

	// dynamisch data filter params
	function LayerDataFilter(lyr, request){

		if(lyr.get('popupAttributes')){

			var attr_str_list = [];


			for (var i = 0; i < lyr.get('popupAttributes').length; i++) {

				// create list for search_fields attributes
				attr_str_list.push(lyr.get('popupAttributes')[i]+" ILIKE '"+request.term+"'");

			}

			cql_filter = "CQL_FILTER=" + attr_str_list.join(' OR ');

		}

		// filter param.
		return cql_filter;
	}
	// set label and attribute value
	function get_ajax_func(url_val, request, response, lyr, matcher){
		$.ajax({
			url: url_val,
			dataType: "json",
			success: function (data) {
				$(".zoekDataResult").empty();

				response($.map(data.features, function(v,i){

					var json_obj = {};
					$.each(v.properties, function(prop_name,prop_val){

						for (var i = 0; i < lyr.get('popupAttributes').length; i++) {
							// attributen from layer list
							if (prop_name == lyr.get('popupAttributes')[i]) {
								json_obj[prop_name] = prop_val;
							}
						}

					}); // END forEach

					var label_val = "";

					for (var key in json_obj){
						 if(json_obj[key] && (!request.term || matcher.test(json_obj[key])))
						 {
							 for (var i = 0; i < lyr.get('popupAttributes').length; i++) {
								 label_val += lyr.get('popupAttributes')[0]+ " : " +
								 json_obj[lyr.get('popupAttributes')[0]] + ", " +
								 lyr.get('popupAttributes')[1] + " : " +
								 json_obj[lyr.get('popupAttributes')[1]];
								 return {
									 label: label_val,
									 attribute_name: [lyr.get('popupAttributes')[0],
									 lyr.get('popupAttributes')[1]],
									 attribute_value: [json_obj[lyr.get('popupAttributes')[0]],
									 json_obj[lyr.get('popupAttributes')[1]]]
								 };
							 }
						 }
					}

				})); // END response
				}
		});
	} // END get_ajax_func()

	// set content table for result
	function get_result_table(event, ui){
		//$("#filterDataResult").show();
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
	}

	// set layer slider
	function set_layer_slider(lyr){
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
	}

	// set layer on-off
	function set_layer_on_off_not_baslyr(lyr){
		if(!lyr.get('isBaseLayer')){
			// layer change functie
			$('#'+ (lyr.get('id'))+'').change(function(){
				if($(this).is(":checked")){
					lyr.setVisible(true);
				}
				else{
					lyr.setVisible(false);
				}
			}); // END change function
		} // END if NOT isBaseLayer
	}

	function set_layer_on_off_baslyr(lyr){
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
	}

	// set layer list to select
	function set_select_layer_list(lyr_id, lyr){
		// create option
		var option = document.createElement("option");

		var set_option_id = lyr.get('source').urls + "," + lyr.get('layerName');

		option.text = lyr.get('title');
		option.value = lyr.get('layerName');
		option.id = set_option_id;

		// add options to select
		var filterLayerSelect = document.getElementById(lyr_id);
		filterLayerSelect.appendChild(option);
	}

	// sort layers on title
	var sort_lyr_title = function (prop, arr) {
		prop = prop.split('.');
		var len = prop.length;

		arr.sort(function (a, b) {
				var i = 0;
				while( i < len ) {
						a = a[prop[i]];
						b = b[prop[i]];
						i++;
				}
				if (a < b) {
						return -1;
				} else if (a > b) {
						return 1;
				} else {
						return 0;
				}
		});
		return arr;
	};

	// Layer Order Z-Index
	map.getLayers().forEach(function(layer){
		// layer draw order for baselayers
		if (layer.get('isBaseLayer')) {
			layer.setZIndex(-999);
		}
		// layer draw order for basisreg
		if (layer.get('basisreg')) {
			layer.setZIndex(-99);
		}
		// layer draw order for themelayer
		if (layer.get('themelayer')) {
			layer.setZIndex(0);
		}
	}); // END getLayers()

	// get layers sort on title
	sort_lyr_title('N.title', map.getLayers().getArray()).forEach(function (lyr) {

		// zoek op data functie // geen baselayer en geen mark layer
		if((!lyr.get('isBaseLayer')) && (lyr.get('title') != "Marker Layer")
			 && (!lyr.get('isLufo')) && (!lyr.get('basisreg'))
			 && (lyr.get('isQueryable')))
		{
				// local layers
				var checkLocalLayer = lyr.get('source').urls[0].includes('local');
				if (checkLocalLayer) {
				}

			// set layes to select options
			set_select_layer_list('data_filter_layer_select', lyr);

			// laagnaam ophalen
			var layerName = lyr.get('layerName');
			// data filter zoek ajax
			$('#'+ (lyr.get('dataZoekId'))+'').autocomplete({

				source: function(request, response){
					// alert(response);
					var matcher =
						new RegExp( $.ui.autocomplete.escapeRegex(request.term), "i" );

					// create wfs layer URL
					var url_val =
						"https://datalab.purmerend.nl/geoserver/topp/ows?service=WFS&" +
						"version=1.1.0&request=GetFeature&typename=" + layerName+ "&" +
						LayerDataFilter(lyr, request) + // get dynamisch data filter params
						"&outputFormat=application/json&srsname=EPSG:28992";

						// get label and attribute value
						get_ajax_func(url_val, request, response, lyr, matcher);

				},
				select: function(event, ui){
					// get selected result table
					get_result_table(event, ui)
				} // END select
			});
		} // END if

		// Layer on-off if the layer is baselayer
		set_layer_on_off_baslyr(lyr);
		// Layer on-off if the layer is NOT baselayer
		set_layer_on_off_not_baslyr(lyr);
		// get layer slider
		set_layer_slider(lyr);

  }); //END getLayers()

	function set_layer_select_list(url_val, layer_name){
		// set layer select
		$.ajax({
			url: url_val,
			dataType: "json",
			beforeSend: function(){
				// No layer selection
				if (layer_name != 'null') {
					// Show loading image
					$("#loading_gif").show();
				}
		    // hide list menu
				$("#layer_attribute_menu").hide();
		  },
			success: function (data) {
				var attribute_from_admin = false;
				// loading image hide
				$("#loading_gif").hide();

				var selected_attr_list = [];

				layerList.forEach(function(layer, v){

					// attributes from Admin
					if (layer.get('search_fields')) {

						// get the source params
						var source = layer.getSource();
						var params = source.getParams();

						// layer name from layer list
						var layersName = params.layers;
						// selected layer name
						if (layersName == layer_name) {
							// check attribute from admin
							attribute_from_admin = true;
							for (var i = 0; i < layer.get('search_fields').length; i++) {
								selected_attr_list.push(layer.get('search_fields')[i]);
							}
						}
					}
				}); // END layerList

				// when attribute not from Admin
				if (!attribute_from_admin) {
					// get propertie name
					$.each(data.features[0].properties, function(prop_name,prop_val){
							selected_attr_list.push(prop_name);
					});
				}

				var filterLayerSelect = document.getElementById('layer_attribute_list');
				// add selecteer een attribute text
				filterLayerSelect.options[filterLayerSelect.options.length] =
				new Option('selecteer een attribuut', 'null');

				for (var i = 0; i < selected_attr_list.length; i++) {

					filterLayerSelect.options[filterLayerSelect.options.length] =
					new Option(selected_attr_list[i], selected_attr_list[i]);
				}

				// attribute layer list
				$("#layer_attribute_menu").show();

			}
		});
	}

	// change layer list
	$("#data_filter_layer_select").change(function(){
		// hide search layer attribute
		$("#founded_object_div").hide();
		// clear search value input
		$("#layer_search_menu").hide();
		// $("#layer_search_menu").find('input').remove();
		// clear selected values
		$('#layer_attribute_list').find('option').remove();
		// get select layers
		var select_layer = document.getElementById("data_filter_layer_select");
		// get selected values;
		layer_name = select_layer.options[select_layer.selectedIndex].value;
		var layer_text = select_layer.options[select_layer.selectedIndex].text;
		layer_id = select_layer.options[select_layer.selectedIndex].id;

		// create wfs layer URL
		var url_val = "";
		var layer_source_url = layer_id.split(',')[0];
		// sey url val for local en public layers
		if (layer_source_url.includes('local')) {
			// create wfs layer URL
			url_val =
				"https://geoserver.purmerend.local/geoserver/topp/ows?service=WFS&" +
				"version=1.1.0&request=GetFeature&typename=" + layer_name+ "&" +
				"&outputFormat=application/json&srsname=EPSG:28992&";
		} else{
			// create wfs layer URL
			url_val =
				"https://datalab.purmerend.nl/geoserver/topp/ows?service=WFS&" +
				"version=1.1.0&request=GetFeature&typename=" + layer_name+ "&" +
				"&outputFormat=application/json&srsname=EPSG:28992&";
		}

		// set layer select list
		set_layer_select_list(url_val, layer_name);

	}); // END Layer change

	// input data focus
	$( "#search_data_value").keyup(function() {
		$("#alert_message").hide();
	});

	// layer attribute selected
	$("#layer_attribute_list").on('change',function(){
		// search input show bij onchange
		$("#search_data_value").show();
		$("#search_value").show();
		$("#alert_message").hide();
		// hide search layer attribute
		$("#founded_object_div").hide();
		// clear input text value
		$('#search_data_value').val('');
		// set selected attribute value to search value
		var select_layer = document.getElementById("layer_attribute_list");
		// get selected values;
		attribute_name = select_layer.options[select_layer.selectedIndex].value;

		if (attribute_name == "null") {
			// search layer attribute
			$("#layer_search_menu").hide();
		}

		if (attribute_name != "null") {
			// set label text
			$("#search_value").html("Zoek op " + attribute_name);
			// set placeholder text
			$('input#search_data_value').attr('placeholder','Type een ' + attribute_name);
			// search layer attribute
			$("#layer_search_menu").show();
		}

	});

	// get x,y from polygon geom
	function get_xy(arr){
		var minX, maxX, minY, maxY;
		for (var i = 0; i < arr.length; i++)
		{
				minX = (arr[i][0] < minX || minX == null) ? arr[i][0] : minX;
				maxX = (arr[i][0] > maxX || maxX == null) ? arr[i][0] : maxX;
				minY = (arr[i][1] < minY || minY == null) ? arr[i][1] : minY;
				maxY = (arr[i][1] > maxY || maxY == null) ? arr[i][1] : maxY;
		}

		return [(minX + maxX) / 2, (minY + maxY) / 2];
	}

	// check if typed charachters are possible
	function isCharPossible(char_list, search_val){
		var isNotpossible = false;
		for (var i = 0; i < char_list.length; i++) {
			if (search_val.includes(char_list[i])) {
				isNotpossible = true;
			}
		}

		if (isNotpossible) {
			$("#loading_gif_data").hide();
			// search input hide bij more than 1000 objects result
			document.getElementById("alert_message").className = "alert alert-warning";
			$("#alert_message").show();
			$("#alert_message").html("0 resultaten gevonden.");
		} else{
			$("#loading_gif_data").show();
		}
	}

	// data filter zoek ajax
	$("#search_data_value").autocomplete({
		source: function(request, response){
			// NOT possiable charachters
			var not_pos_char =
			['(','.','/','\\','\'','\"','!','@','#','$','%','^','&','*','()',')','('];
			// check possible charachters
			isCharPossible(not_pos_char, request.term);
			// hide search layer attribute
			$("#founded_object_div").hide();
			//new RegExp( $.ui.autocomplete.escapeRegex(request.term), "i" );
			var matcher = new RegExp( $.ui.autocomplete.escapeRegex(request.term), "i" );
			// check layer location: cloud or local
			var layer_source_url = layer_id.split(',')[0];
			// set wfs service url
			var wfs_layer_url;
			// set url val for local en public layers
			if (layer_source_url.includes('local')){
				wfs_layer_url = // local layers
					"https://geoserver.purmerend.local/geoserver/topp/ows?service=WFS&";
			} else{
				wfs_layer_url = // cloud layers
					"https://datalab.purmerend.nl/geoserver/topp/ows?service=WFS&";
			}

			// dynamisch search value
			var search_cql_filter = '';
			// check inupt value
			var input_val = Number(request.term);

			// check Numeric input value
			if (!isNaN(input_val)) {
				search_cql_filter =
					"CQL_FILTER="+ attribute_name +" LIKE '"+ matcher.source +"'&";
			} else{
				search_cql_filter =
					"CQL_FILTER="+ attribute_name +" ILIKE '%25"+ matcher.source +"%25'&";
			}

			// dynamisch url links
			var url_val =
				wfs_layer_url +
				"version=1.1.0&request=GetFeature&typename="+ layer_name +"&" +
				search_cql_filter +
				"outputFormat=application/json&srsname=EPSG:28992&maxFeatures=1000";

				console.log(url_val);

			$.ajax({
			 dataType: "json",
			 url: url_val,
			 success: function (data) {

				var pop_attribute_admin = false;
				 // loading gif hide
	 			$("#loading_gif_data").hide();
				 response($.map(data.features, function(v,i){
					 // founded feature length
					 var feature_length = data.features.length;
					 // 1000 and more objects
					 if (feature_length == 1000) {
						 // search input hide bij more than 1000 objects result
						 document.getElementById("alert_message").className = "alert alert-warning";
						 $("#alert_message").show();
	 					 $("#alert_message").html("<strong>" +
	 					 	data.features.length + "</strong> objecten gevonden"+
							"<br/>" +
								"Te veel resultaten; pas uw zoekopdracht aan.");
					 }
					 // check feature length
					 if (feature_length == 0 || feature_length == 1) {
						 // founded feature length dynamich
	 					 $("#alert_message").show();
	 					 $("#alert_message").html("<strong>" +
	 					 	data.features.length + "</strong> object gevonden");
					 }

					 if (feature_length >1 && feature_length < 1000) {
						 // founded feature length dynamich
						 document.getElementById("alert_message").className =
						 	"alert alert-info";
						 $("#alert_message").show();
						 $("#alert_message").html("<strong>" +
							data.features.length + "</strong> objecten gevonden");
					 }

					 // check feature length between 1 and 1000
					 if (feature_length > 0 && feature_length <1000) {

							// get dynamich attribute name
	 					 var dots = "v.properties." + attribute_name;
	 					 var text_split = dots.split('.').join('.');
	 					 // set text value
	 					 var text = eval(text_split);

	 					 // check maching for autocomplete
	 					 if ( text && ( !request.term || matcher.test(text) ) ) {
	 						 // set label value
	 						 var label_result = "";
	 						 var json_obj = {};

							 //get layer list
					 		layerList.forEach(function(layer, t){

					 			// attributes from Admin
					 			if (layer.get('popupAttributes')) {

					 				// get the source params
					 				var source = layer.getSource();
					 				var params = source.getParams();

					 				// layer name from layer list
					 				var layersName = params.layers;
					 				// selected layer name
					 				if (layersName == layer_name) {
					 					pop_attribute_admin = true;
					 					// popup attributes list from Admin
					 					for (var i = 0; i < layer.get('popupAttributes').length; i++) {
					 						var popup_name = layer.get('popupAttributes')[i];
					 						var popup_val = v.properties[popup_name];

					 						var name_capitalized = popup_name.charAt(0).toUpperCase() +
					 							popup_name.slice(1);

											label_result += name_capitalized + " : " + popup_val + " ";
											json_obj[popup_name] = popup_val;

					 					}
					 				}
					 			}
					 		}); // END LayerList
							// check popup attirbutes from Admin
							if (!pop_attribute_admin) {
								// get attribute name and value
 	 						 $.each(v.properties, function(prop_name,prop_val){
 	 							 label_result += prop_name + ": " + prop_val + " ";
								 json_obj[prop_name] = prop_val;
 	 						 });

							}

	 						 return {
	 							// label: attribute_name + " : " + text,
	 							label: label_result,
	 							value: text,
	 							geo: v.geometry,
	 							result: json_obj
	 						 };
	 					}
					 }
				 }));
			 },
			 error: function () {
					 response([]);
			 }
	 });
		},
		select: function(event, ui){
			// Hide founded feature length dynamich
			 $("#alert_message").hide();
			// clear markers
			vectorSource.clear();
			// get geometry type
			var geom_type = ui.item.geo.type;
			var arr_multiple_pol = ui.item.geo.coordinates[0][0];
			var arr_polygon = ui.item.geo.coordinates[0];
			var arr_linestring = ui.item.geo.coordinates;
			// get coordinaten
			var coordinaat = [];
			// check geom type
			if (geom_type == "Point") { // Point selected
				coordinaat = ui.item.geo.coordinates;
			}
			if (geom_type == "MultiPolygon"){ // MultiPolygon selected
				coordinaat = get_xy(arr_multiple_pol);
			}
			if (geom_type == "Polygon") { // Polygon selected
				coordinaat = get_xy(arr_polygon);
			}
			if (geom_type == "MultiLineString") {
				coordinaat = get_xy(arr_polygon);
			}
			if (geom_type == "LineString") {
				coordinaat = get_xy(arr_linestring);
			}
			// set pin to founded object
			founded_object(coordinaat, ui, layer_name);

		} // END select
	});

	//first leeter Capital
	function jsUcfirst(string){
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

	// Set variables for initialization.
	let strt_options = {
		targetElement: document.getElementById('streetsmartApi'),
		username: smartstreet_user,
		password: smartstreet_password,
		apiKey: smartstreet_api_key,
		srs: "EPSG:28992",
		locale: 'nl',
		configurationUrl: 'https://atlas.cyclomedia.com/configuration',
		 addressSettings:
		 {
			 locale: "nl",
			 database: "Nokia"
		 }
	};
	// set marker on map
	function setMarkerOnMap(coordinates){
		// clear all selected objects
		vectorSource.clear();
		// get coordinates
		cor_x = coordinates.split(',')[0];
		cor_y = coordinates.split(',')[1];
		// create feature icon
		var iconFeature = new ol.Feature({
			geometry: new ol.geom.Point(ol.proj.transform([parseInt(cor_x),
			parseInt(cor_y)], 'EPSG:28992', 'EPSG:28992'))
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

	// StreetView API successCallback
	function successCallback() {
		//hide alert message
		$("#view_alert_message").hide();
		// create ciewer type
		var viewerType = StreetSmartApi.ViewerType.PANORAMA

		// check clicked location
		if (dynamisch_adres_coordinate != "null") {
			// create viewer center
			coordint_map_viewer = dynamisch_adres_coordinate;
			// check adres location
		} else{
			// create viewer center
			coordint_map_viewer = "125549.58, 502205.69";
		}

		// set marker on map
		setMarkerOnMap(coordint_map_viewer);
		StreetSmartApi.open(
			coordint_map_viewer,
			{
				viewerType: viewerType,
				srs: 'EPSG:28992',
			}
		).then(
		function(result)
		{
			if (result) {
				for (let i =0; i < result.length; i++) {
					if(result[i].getType() === StreetSmartApi.ViewerType.PANORAMA) window.panoramaViewer = result[i];
				}
			}
		}.bind(this)
		).catch(
			function(reason) {
				console.log('Failed to create component(s) through API: ' + reason);
				// search input hide bij more than 1000 objects result
				document.getElementById("view_alert_message").className = "alert alert-warning";
				// show alert message
				$("#view_alert_message").show();
				$("#view_alert_message").html("Geen rondkijkfoto beschikbaar op deze locatie: " + center_map_viewer);
			}
		);
	}

	// StreetView errorCallback
	function errorCallback(err) {
		console.log('Api: init: failed. Error: ', err);
		alert('Api Init Failed!');
	}

	// Street-view API Actief
	function set_street_view_on(){
		// Initalize StreetSmartApi
		StreetSmartApi.init(strt_options).then( successCallback, errorCallback);
		isStreetViewActief = true;
		$("#streetsmartApi").show();
		$('#streetsmartDiv').show();
		// specifiek for IE-11
		$(".btn_stret_sty").css('background-color', '#afc812');
	}

	// Street-view API NOT actief
	function set_street_view_off(){
		// remove Init StreetSmartApi
		isStreetViewActief = false;
		StreetSmartApi.destroy(strt_options);
		$('#streetsmartDiv').hide();
		$("#streetsmartApi").hide();
		// specifiek for IE-11
		$(".btn_stret_sty").css('background-color', '#fff');
		// clear all selected objects
		vectorSource.clear();
	}

	var click_count = 0;
	// Street-vie toggle button
	$(".btn_stret_sty").click(function(){
		click_count ++;
		console.log("clicked " + click_count);
		// street-view actief toogle
		$(".btn_stret_sty").toggleClass("street_view_actief");
		if ($(this).hasClass('street_view_actief')){
			// set Street-vie On
			set_street_view_on();
			//hide alert message
			$("#view_alert_message").hide();
		} else {
			// set Street-view Off
			set_street_view_off();
		}

	});

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

	// Zoek op data button
	$(".btn_zoek_data_style").click(function(){
		$(".btn_zoek_data_style").toggleClass("zoek_data_filter_actief");
		if ($(this).hasClass('zoek_data_filter_actief')){
			// set zoek op adres On
			$("#zoekDataFilterDiv").show();
			// specifiek for IE-11
			$(".btn_zoek_data_style").css('background-color', '#afc812');
		} else {
			// set zoek op adres Off
			$("#zoekDataFilterDiv").hide();
			// specifiek for IE-11
			$(".btn_zoek_data_style").css('background-color', '#fff');
		}

	});

	// data result
	function getKadasterList(data, result_attr_list, kad_cod){
		// data result content
		var content_feature = " ";

		// get data features
		for (var i = 0; i < data.features.length; i++) {
			if (data.features.length == 1) { // for one object
				// data result property list
				for (var j = 0; j < result_attr_list.length; j++) {

					// kad data result details
					if (data.features[i].properties[result_attr_list[j]] != null) {
						// kad data result details
						content_feature +=
							"<span class='attr_name'>" + result_attr_list[j] + ": </span>";
						content_feature +=
							"<span class='attr_value'>"+
							data.features[i].properties[result_attr_list[j]] +"</span>";
					} else{
						// kad data result details
						content_feature +=
							"<span class='attr_name'>" + result_attr_list[j] + ": - </span>";
					}

					content_feature += "</br>";
				}
			} else{
				// kad result label text
				var kad_result_label =
					data.features[i].properties['kadsleutel'] + " " +
					data.features[i].properties['kadkoletter'] + " " +
					data.features[i].properties['kadkoindex'];

				content_feature +=
					"<a class='accordion-toggle collapsed' data-toggle='collapse'" +
					"data-parent='#categorieen-accordion' href='#"+i+kad_cod+"'>";
				content_feature +=
					"<span class='attr_link'>"+kad_result_label+"</span>";
				content_feature +=
					"<span class='icon-caret icon-caret-right'></span></a>";
				content_feature += "<br/>";

				content_feature += "<div id='"+i+kad_cod+"' class='collapse'>";

				// data result property list
				for (var j = 0; j < result_attr_list.length; j++) {

					if (data.features[i].properties[result_attr_list[j]] != null) {
						// kad data result details
						content_feature +=
							"<span class='attr_name'>" + result_attr_list[j] + ": </span>";
						content_feature +=
							"<span class='attr_value'>"+
							data.features[i].properties[result_attr_list[j]] +"</span>";
					} else{
						// kad data result details
						content_feature +=
							"<span class='attr_name'>" + result_attr_list[j] + ": - </span>";
					}

					content_feature += "</br>";
				}

				content_feature += "</div>";
			}

		}

		return content_feature
	}

	function getKadasterObject(url_link){
		$.ajax({
			dataType: "json",
			url: 	url_link,
			success: function(data){

				var start_tabelregel = "<table class='table'  width='100%' cellspacing = '0'>";
				var body_regel = "<tbody>";
				var content_feature = " ";
				var einde_tabelregel = "</tbody></table>";
				var data_result = "";

				// data result attribute filter
				var result_attr_list = [
					'kadsleutel', 'kadkoletter', 'kadkoindex', 'oppervlakte', 'eukoopsom'
				]

				$("#kad_object").html(
					getKadasterList(data, result_attr_list, 'kad_obj')
				);
			} // END Success
		}); // END Ajax
	} // END function

	// get Kadaster adres
	function getKadasterAdres(url_link){
		$.ajax({
			dataType: "json",
			url: 	url_link,
			success: function(data){
				// data result attribute filter
				var result_attr_list = [
						'kadsleutel', 'kadkoletter', 'kadkoindex', 'straatnaam', 'huisnr',
						'huislt', 'postcode', 'woonplaats'
				]

				// data result push
				$("#kad_adres").html(getKadasterList(data, result_attr_list, 'kad_Ad'));

			} // END Success
		}); // END Ajax
	} // END function

	// get Kadaster rechthebbende
	function getKadasterRechthebbende(url_link){
		$.ajax({
			dataType: "json",
			url: 	url_link,
			success: function(data){

				// data result attribute filter
				var result_attr_list = [
					'kadsleutel', 'kadkoletter', 'kadkoindex', 'akrzakelijkrechtoms',
					'akrnietnatpersoondom', 'akrnatpersoondom', 'voorletters',
					'subjectnaam', 'gbageboorte', 'wstraatnaam', 'whuisnr', 'wtoev',
					'wpostcode','wwoonplaats'
				];

				// data result push
				$("#kad_rechthebbende").html(
						getKadasterList(data, result_attr_list, 'kad_recht')
				);

			} // END Success
		}); // END Ajax
	} // END functionv

	// check draw starting
	var start_drawing = false;
	// get feature from json -url insie bbox
	function get_json_url(extent){
		// get json url
		var get_feature_url = "https://datalab.purmerend.nl/geoserver/topp/ows?" +
			 "service=WFS&version=1.0.0&" +
			 "request=GetFeature&typeName=BAG_Verblijfseenheid_GEKOPPELD&" +
			 "outputFormat=application%2Fjson&" +
			 "bbox=" + extent;
		// push url
		return get_feature_url;

	}

	// get properties adress
	function get_adres_properties(data, content_popup){
		// content popup input
		var content_popup_input = '';
		// get selected features
		for (var i = 0; i < data.features.length; i++) {
			// create adress string
			var straat_naam = data.features[i].properties['straatnaam'];
			var huis_nummer = data.features[i].properties['huisnummer'];
			var huis_letter = ' ';
			var postcode = data.features[i].properties['postcode'];
			var woonplaats = data.features[i].properties['woonplaats'];
			// chaeck huisletters
			if (data.features[i].properties['huisletter'] != null) {
				huis_letter = data.features[i].properties['huisletter'];
			}

			// create adress content
			var adres_content =
				straat_naam + ' ' + huis_nummer + ' ' + huis_letter + ' ' +
				postcode + ' ' + woonplaats;

			// push adress links
			content_popup_input += "<a class='accordion-toggle collapsed'"
				"data-toggle='collapse' data-parent='#categorieen-accordion'"
				"href='#"+data.features[i].properties['verblijfseenheid_id']+"'>";

			content_popup_input += "<span class='text'>"+adres_content+"</span>";
			content_popup_input += "<span class='icon-caret icon-caret-right'></span>";
			content_popup_input += "</a>";
			content_popup_input += "<br/>";

		}
		return content_popup_input;
	}

	// get download button with json data
	function get_popup_content(data, adres_download, CSRF_TOKEN, content_popup){
		// get properties
		content_popup += get_adres_properties(data, content_popup);

		// push adres data JSON
		content_popup += "<form action='/atlas/savedataset' method='POST'>";
		content_popup += "<div class='form-group'>";
		content_popup += "<input type='hidden' name='title' value='Adressen (BAG)' >";
		content_popup += "<input type='hidden' name='json' value='"+adres_download+"' >";
		content_popup += "<input type='hidden' name='csrfmiddlewaretoken' value='"+CSRF_TOKEN+"' >";
		content_popup += "</div>";
		content_popup += "<div class='form-group'>";
		content_popup += "<button class='btn btn-primary btn-md' type='submit'>"
		content_popup += "<span class='glyphicon glyphicon-download'></span> Download</button>";
		content_popup += "</div>";
		content_popup += "</form>";

		content_popup += "</div>";

		// add pop-up info content
		$("#dataResult").html(content_popup);
		$("#popupTitle").html("Geselecteerde adressen");
		$('#dataresulmodal').modal('show');

	}

	// clear selection when drawing a new box and when clicking on the map
	dragBox.on('boxstart', function() {
	 // when starting drawing
	 start_drawing = true;
	});

	// box drawing is finished
	dragBox.on('boxend', function() {
		// get selected bbox
		var extent_bbox = dragBox.getGeometry().getExtent();
		// get json from wfs
		$.ajax({
			 url: get_json_url(extent_bbox),
			 method:'get',
			 success:function(data){
				 // pop-up content
				 var content_popup = "";
				 // json object to download
				 var adres_download = JSON.stringify(data);
				 // get popup_content
				 get_popup_content(data, adres_download, CSRF_TOKEN, content_popup);

				 } // END success

			 }); // END Ajax

	}); // END dragbox boxend

	// call smart street api
	function get_smart_street(evt){

		var cor_x = evt.coordinate[0];
		var cor_y = evt.coordinate[1];

		var totaal_coordinaat = cor_x + "," + cor_y;

		const options = {
		 viewerType: [StreetSmartApi.ViewerType.PANORAMA,
			 StreetSmartApi.ViewerType.OBLIQUE],
		 srs: 'EPSG:28992',
		 panoramaViewer: {
				 closable: true,
				 maximizable: true,
				 replace: true,
				 recordingsVisible: true,
				 navbarVisible: false,
				 timeTravelVisible : true,
				 measureTypeButtonVisible: true,
				 measureTypeButtonStart: true,
				 measureTypeButtonToggle: true,
		 },
		 obliqueViewer: {
				 closable: true,
				 maximizable: true,
				 navbarVisible: true,
				 timeTravelVisible : true,
		 }
	 };
	 // check StreetView
	 if (isStreetViewActief) {
		 if (dynamisch_adres_coordinate != "null") {
			 // call StreetSmartApi bij on.click
			 StreetSmartApi.open(dynamisch_adres_coordinate, options)
		 } else{
				// call StreetSmartApi bij on.click
				StreetSmartApi.open(totaal_coordinaat, options)
		 }
	 }
	}

	//check layer visible
	function chec_layer_viisble(layer, layer_name){
		//check layer visiblity
		if (layer.get('layerName') == layer_name){
			console.log("Layer name: "+ layer_name);
			console.log(layer.getVisible());
			// set selecter layer visible on map
			layer.setVisible(true);
			// checkbox checked on layer menu
			document.getElementById(layer.get('id')).checked = true;
		}
	}

	// set pin by select object
	function founded_object(coordint, ui, layer_name){
		var pop_attribute_from_admin = false;
		// clear all selected objects
		vectorSource.clear();
		// get coordinates
		var cor_x = coordint[0];
		var cor_y = coordint[1];
		// set dynamich coordinates
		dynamisch_adres_coordinate = cor_x + ", " + cor_y;
		// create feature icon
		var iconFeature = new ol.Feature({
			geometry: new ol.geom.Point(ol.proj.transform([parseInt(cor_x),
			parseInt(cor_y)], 'EPSG:28992', 'EPSG:28992'))
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

		// set map postion to found item
		map.getView().setCenter(ol.proj.transform(coordint,
		'EPSG:28992', 'EPSG:28992'));
		map.getView().setZoom(19);

		// create layer content
		var layer_result_content = "";

		//get layer list
		layerList.forEach(function(layer, v){
			// set layer visible
			chec_layer_viisble(layer, layer_name)
			// attributes from Admin
			if (layer.get('popupAttributes')) {

				// get the source params
				var source = layer.getSource();
				var params = source.getParams();

				// layer name from layer list
				var layersName = params.layers;
				// selected layer name
				if (layersName == layer_name) {
					pop_attribute_from_admin = true;
					// popup attributes list from Admin
					for (var i = 0; i < layer.get('popupAttributes').length; i++) {
						var popup_name = layer.get('popupAttributes')[i];
						var popup_val = ui.item.result[layer.get('popupAttributes')[i]];

						var name_capitalized = popup_name.charAt(0).toUpperCase() +
							popup_name.slice(1);

						layer_result_content += "<b>";
						layer_result_content += name_capitalized;
						layer_result_content += ": </b>";

						// check for website links
						if (popup_val != null) {
							if (popup_val.includes('http')) {
								layer_result_content += "<a target='_blank' href='"+ popup_val +"'>Meer info</a>";
							} else{
								layer_result_content += popup_val;
							}
						}
						layer_result_content += "</br>";
					}
				}
			}
		}); // END LayerList

		// check popup attributes from Admin
		if (!pop_attribute_from_admin) {
			// get object info from object
			for(var i in ui.item.result){

				var nameCapitalized = i.charAt(0).toUpperCase() + i.slice(1)
				layer_result_content += "<b>";
				layer_result_content += nameCapitalized;
				layer_result_content += ": </b>";
				// check for website links
				if (ui.item.result[i] != null) {
					if (ui.item.result[i].includes('http')) {
						layer_result_content += "<a target='_blank' href='"+
							ui.item.result[i] +"'>Meer info</a>";
					} else{
						layer_result_content += ui.item.result[i];
					}
				}
				layer_result_content += "</br>";
			}
		}

		// set layer result content
		$("#founded_object_info").html(layer_result_content);
		// show result info
		$("#founded_object_div").show();
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

	// click close button
	$("#close_viewer_btn").click(function(){
		$(".btn_stret_sty").toggleClass("street_view_actief");
		// set Street-vie Off
		set_street_view_off();
	}); // END functie

	// click close button of data
	$("#close_data_filter_btn").click(function(){
		$(".btn_zoek_data_style").toggleClass("zoek_data_filter_actief");
		$(".btn_zoek_data_style").css('background-color', '#fff');

		// set data filter Off
		$("#zoekDataFilterDiv").hide();
	});

	// check dataresult modal opening
	$('#dataresulmodal').on('hidden.bs.modal', function () {
		// clear all selected objects
		vectorSource.clear();
	});

	// click on map function
	map.on('click', function(evt) {

		// set viewer coordinates
		//clicked_map_coordinate = "127670.30027916425, 502412.9339569349";
		dynamisch_adres_coordinate = evt.coordinate[0] + ", " + evt.coordinate[1];

		// when street-view actief
		if (isStreetViewActief) {
			// selected objects pin-marker
			selected_object(evt);
		}

		// popup content
		var content_popup = "";
		// by measure hide street-view
		if (!is_interaction) {
			if (isStreetViewActief) {
				// set smart street api position
				get_smart_street(evt)
				$("#streetsmartApi").show();
				$('#streetsmartDiv').show();

			}
		}

	//get layerList
	layerList.forEach(function(layer, i){
		// if layer visible and not Basigreg not MarkerLayer not
		if(layer.getVisible() && !layer.get('isBaseLayer') &&
			layer.get('title') != "Marker Layer" && layer.get('isQueryable') == true)
			{
			// get layer URL
			var layer_url = getUrlSelected(layer, evt);

			// if url true
			if (layer_url) {

				var parser = new ol.format.GeoJSON();

				$.ajax({
					url: layer_url,
					method:'get',
					success:function(data){
						// create empty table
						var start_tabelregel = "<table class='table'  width='100%' cellspacing = '0'>";
						var header_regel = "<thead>";
						var content_header = " ";
						var body_regel = "<tbody>";
						var content_feature = " ";
						var einde_tabelregel = "</tbody></table>";

						// json object to download
						var adres_download = JSON.stringify(data);
						var input_adres = "";
						// get features length
						var features_length = data.features.length;

						data.features.map(function (v,i) {

							content_popup += "<a class='accordion-toggle collapsed' data-toggle='collapse' data-parent='#categorieen-accordion' href='#"+layer.get('filterdataId')+"'>";
							content_popup += 	"<span class='text'>"+layer.get('title')+"</span>";
							content_popup +=  "<span class='icon-caret icon-caret-right'></span></a>";
							content_popup += "<br/>";

							content_popup += "<div id='"+layer.get('filterdataId')+"' class='collapse'>";

							$.each(v.properties, function(prop_name,prop_val){

								// get popup info
								function get_popup(attr_nm, attr_val){
									var result = "";
									if (attr_nm == "meer_informatie") {
										content_popup += "<a target='_blank' href='"+prop_val+"'>Meer info</a>";
										content_popup += "<br>";

									} else if (attr_nm == "foto"){
										content_popup += "<a href='../data/images/"+layer.get('title')+"/"+attr_val+"' target='_blank'><img style='width:100%; height:250px;' src='../data/images/"+layer.get('title')+"/"+attr_val+"'/></a>";
										content_popup += "<br>";
									} else{ // the other attribute values
										content_popup += "<b>"+jsUcfirst(attr_nm)+": </b>";
										content_popup += attr_val;
										content_popup += "<br>";
									}
									return content_popup;
								}

								// check kadaster layer selected
								if (prop_name == "kadsleutel") {
									var kad_cql_filter = "&CQL_FILTER=kadsleutelg='" +prop_val+ "'";

									// create a url list for kadaster data
									// var kad_data_url_list_local = [BRK_KADOBJECT_dummie + kad_cql_filter, BRK_KADADRES_dummie + kad_cql_filter, BRK_KADSUBJECTZR_dummie + kad_cql_filter];
									var kad_data_url_list_pro = [BRK_KADOBJECT + kad_cql_filter, BRK_KADADRES + kad_cql_filter, BRK_KADSUBJECTZR + kad_cql_filter];

									// call getKadasterData function to push data
									getKadasterObject(kad_data_url_list_pro[0]);
									getKadasterAdres(kad_data_url_list_pro[1]);
									getKadasterRechthebbende(kad_data_url_list_pro[2]);

									// when measure is actief
									if(!is_interaction){
										// show Kadaster data result
										$("#kad-result-link").show();
										$("#kadaster-resultaat").show();
									}

									// change Kadaster link style
									document.getElementById("kadasterToggleDiv").className = "glyphicon glyphicon-chevron-down";

								} else{ // END if kadsleutel
									// hide Kadaster data result
									$("#kad-result-link").hide();
									$("#kadaster-resultaat").hide();
								}

									// has layer the popupAttributes properties?
									if(layer.get('popupAttributes')){

										// get feature attributes from param: popupAttributes per layer
										for (var i = 0; i < layer.get('popupAttributes').length; i++) {

											//create popup content if NOT empty
											if(prop_val != "" && prop_val != null && prop_name == layer.get('popupAttributes')[i]){

												// call get popup info function
												get_popup(prop_name, prop_val);
												// selected objects pin-marker
												selected_object(evt);

											}
										}

									} else{
										//create popup content if NOT empty
										if(prop_val != "" && prop_val != null){

											// call get popup info function
											get_popup(prop_name, prop_val);
											// selected objects pin-marker
											selected_object(evt);

										}

									}

								});

								// push adres data JSON
								content_popup += "<form action='/atlas/savedataset' method='POST'>";
								content_popup += "<div class='form-group'>";
								content_popup += "<input type='hidden' name='title' value='"+ layer.get('title') +"' >";
								content_popup += "<input type='hidden' name='json' value='"+adres_download+"' >";
								content_popup += "<input type='hidden' name='csrfmiddlewaretoken' value='"+CSRF_TOKEN+"' >";
								content_popup += "</div>";
								content_popup += "<div class='form-group'>";
								content_popup += "<button class='btn btn-primary btn-md' type='submit'>";
								content_popup += "<span class='glyphicon glyphicon-download'></span> Download</button>";
								content_popup += "</div>";
								content_popup += "</form>";

							 	content_popup += "</div>";

							 });


							// check feature length > 0
							if(features_length != 0 && !is_interaction){
								// add pop-up info content
								$("#dataResult").html(content_popup + input_adres);
								$("#popupTitle").html("Geselecteerde objecten");
								// show data result model
								$('#dataresulmodal').modal('show');

							}

						} // END success

					}); // END Ajax

				} // END if layer url

			} // END if layer visibility

		}); // END layersList forEach

	}); // END map.on.click
	// toogle Kadaster link
	$("#openKadasterInfo").click(function(){
		$("#kadaster-resultaat").toggle();
		// check Kadaster link style
		if (document.getElementById("kadasterToggleDiv").className == "glyphicon glyphicon-chevron-right") {
				document.getElementById("kadasterToggleDiv").className = "glyphicon glyphicon-chevron-down";
		} else{
			document.getElementById("kadasterToggleDiv").className = "glyphicon glyphicon-chevron-right";
		}

	}); //END click

	$(".modal-dialog").draggable({
      handle: ".modal-header"
  });

	// Street view draggable
	$("#streetsmartDiv").resizable({
		 handles: 'e, w'
	});
	// street-view draggable
	$("#streetsmartDiv").draggable();

	// zoek filter data draggable
	$("#zoekDataFilterDiv").draggable();

	// // Street wil on-draggable when street-vew IN using
	$("#streetsmartApi").on('mouseenter', function(event) {
		$("#streetsmartDiv").draggable("disable");

	}).on('mouseleave', function(){
		// Street wil on-draggable when street-vew NOT using
		$("#streetsmartDiv").draggable("enable");
	});

	// move map event
	 map.on('moveend', function(evt){
		 // create dynamish coordinate
		 coord = map.getView().getCenter();
		 dynamisch_adres_coordinate = coord[0] + ", " + coord[1];

		 console.log(dynamisch_adres_coordinate);
	 });

	// update de layers when de db changed
	map.updateSize();

} // END Init()
