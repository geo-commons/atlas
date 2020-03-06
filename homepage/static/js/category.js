var atlasCategory = {
    init: function() {
        atlasCategory.setLayerListCat(layerList);
		atlasCategory.setLayerListContent(layerList);
    },

    setLayerListCat: function(layerList) {
		var layerContent = "";
		var uniqueLayerList = atlasCategory.getUniqueCategoryList(layerList);

		// add categorie layer Title to layermenu
		for (var i = 0; i < uniqueLayerList.length; i++) {
			layerContent += "<div class='accordion-heading'>";
            layerContent +=
                "<a class='accordion-toggle collapsed'" +
				"data-toggle='collapse' data-parent='#categorieen-accordion'" +
                "href='#"+uniqueLayerList[i]+"'>";
            layerContent += "<span class='text'>" + uniqueLayerList[i].split('_').join(' ') + "</span>"
            layerContent += "<span class='icon-caret icon-caret-right'></span></a>";
            layerContent += "</div>";
            layerContent += "<div style='padding-bottom:1px;' class='label_div2'>";
            layerContent += "<div id='" + uniqueLayerList[i] + "' class=\"collapse\" data-type=\"category\"></div>";
            layerContent += "</div>";
        }

        $("#theme-list").append(layerContent);
    },

    setLayerListContent: function(layerList) {
		$('div[data-type="category"]').each(function() {
			$(this).append(
				'<table class="table"  width="100%" cellspacing="0">' +
				'<tbody>'
			);
		});

        for (var i = 0; i < layerList.length; i++) {
            if (layerList[i].get('categorie')) {
				var moved_space = layerList[i].get('categorie').split(' ').join('_');
                $('#' + moved_space).find("tbody").append(
                    atlasCategory.setCategoryContent(layerList[i])
                );
            }
		}

		$('div[data-type="category"]').each(function() {
			$(this).append(
				'</tbody>' +
				'</table>'
			);
		});
    },

    getUniqueCategoryList: function(layerList) {
		var unique_list = [];
		for (var i = 0; i < atlasCategory.getCategoryNames(layerList).length; i++) {
			var move_space = atlasCategory.getCategoryNames(layerList)[i].split(' ').join('_');
			unique_list.push(move_space);
		}

		return unique_list;
    },

    getCategoryNames: function(array) {
		var outputArray = [];
		var count = 0;
		var start = false;

		for (j = 0; j < array.length; j++) {
				if (array[j].get('categorie')) {
					for (k = 0; k < outputArray.length; k++) {
							if ( array[j].get('categorie') == outputArray[k] ) {
									start = true;
							}
					}
					count++;
					if (count == 1 && start == false) {
							outputArray.push(array[j].get('categorie'));
					}
					start = false;
					count = 0;
				}
		}

		return outputArray.sort();
    },

	setCategoryContent: function(layer) {
		// creat dynamish layer content
		var dynamish_category_content = "";
		// Thema kaarten - check for NOT base layer and NOT marker layer and NOT PDOK layer
		if(!layer.get('isBaseLayer') && name != "Marker Layer" && !basisregistratie && !luchtfotokaart){
			var name = layer.get('title');
			var visiblity = layer.get('visible');
			var lyrID = layer.get('id');
			var lgndID = layer.get('lgnd');
			var basisregistratie = layer.get('basisreg');
			var luchtfotokaart = layer.get('isLufo');
			var sldDiv = layer.get('sldDiv');
			var infoDiv = layer.get('infoDiv');

			// get category name
			dynamish_category_content += "<tr>";
			dynamish_category_content += "<td class='eerste'>";

			if(visiblity) { //check the visibility
				dynamish_category_content += "<span class='layerName'>" + name + "</span>";
				dynamish_category_content += "<div class ='layer-switch pull-right'>";
				dynamish_category_content += "<input checked id='"+ lyrID + "' value='" + lyrID + "' type='checkbox'/><label class='label-success' for='"+ lyrID +"'></label>";
				dynamish_category_content += "</div>";
			} else {
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
}
