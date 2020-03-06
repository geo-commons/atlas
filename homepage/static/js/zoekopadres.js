
$(document).ready(function(){
	// create vector source for search marker
	vectorSource = new ol.source.Vector({});

	// zoek op adres - autocomplete JSON from Locatieserver
	$("#straatnaam").autocomplete({

		source: function (request, response) {
		    var matcher = new RegExp( $.ui.autocomplete.escapeRegex(request.term), "i" );
		    $.ajax({
				// url:"https://geodata.nationaalgeoregister.nl/locatieserver/v3/suggest?q=" + request.term + " and (gemeentecode:0439 or gemeentecode:0370)",
				url:"https://geodata.nationaalgeoregister.nl/locatieserver/v3/suggest?q=" + request.term + " and (gemeentecode:0439 or gemeentecode:0370)",
		        dataType: "json",
		        success: function (data) {
		            response($.map(data.response.docs, function(v,i){
									var text = v.weergavenaam;
		              if ( text && ( !request.term || matcher.test(text) ) ) {
										// filter op de data van gemeente Purmerend & Beemster
										///alert(text);
											return {
											 label: v.weergavenaam,
											 value: v.weergavenaam,
											 geo: v.centroide_rd,
											 adrs_id: v.id
											};

		                }
		            }));
		        }
		    });
		},
		select: function( event , ui ) {
			// check the value at locatieserver
			$.ajax({
					url:"https://geodata.nationaalgeoregister.nl/locatieserver/v3/free?q=id:" + ui.item.adrs_id,
					dataType: "json",
					success: function (data) {
						// get RD geometry
						var geometrie_rd = data.response.docs[0].centroide_rd;
						console.log(data.response.docs[0].centroide_rd);

						var coord_x = 0;
						var coord_y = 0;

						for(var i=0; i<geometrie_rd.length; i++){

								var spaceIndex = geometrie_rd.indexOf(" ");

								coord_x = geometrie_rd.substring(6, spaceIndex);
								coord_y = geometrie_rd.substring(spaceIndex, geometrie_rd.length-1);
						}

						// set position for street-view
						dynamisch_adres_coordinate = coord_x + ", " + coord_y;

						var center = [parseInt(coord_x), parseInt(coord_y)];

						var iconFeature = new ol.Feature({
							geometry: new ol.geom.Point(ol.proj.transform([parseInt(coord_x), parseInt(coord_y)], 'EPSG:28992', 'EPSG:28992'))
						});

						var iconStyle = new ol.style.Style({
						 image: new ol.style.Icon(({
							 anchor: [0.5, 46],
							 anchorXUnits: 'fraction',
							 anchorYUnits: 'pixels',
							 opacity: 0.75,
							 src: icon_png
						 }))
					 });


						iconFeature.setStyle(iconStyle);

						// add marker
						//vectorSource.addFeature(iconFeature);

						vectorLayer = new ol.layer.Vector({
					    source: vectorSource
						});
						// clear all vector layer icons
						vectorSource.clear();
						vectorSource.addFeature(iconFeature);

						map.getView().setCenter(ol.proj.transform([parseInt(coord_x), parseInt(coord_y)] , 'EPSG:28992', 'EPSG:28992'));
						map.getView().setZoom(19);

						map.addLayer(vectorLayer);
					}
			});

		}

	}); // END autocomplete
	// clear markers van zoek op adres
	$(".btn_zoek_adres_style").click(function(){
      vectorSource.clear();
  });

}); // END document.ready
