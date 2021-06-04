jq_goToTop = null;
		//jquery
$(function() {

    function goToTop() {
		$("html, body").animate({
			scrollTop: $("#Methods").offset().top - 100
		}, 'fast');
	}
	jq_goToTop = goToTop;
})

//javascript
function displayMethod(x) {
	clearAllMethods();
	var meth = document.getElementById(x);
	meth.style.display = "";
	jq_goToTop();
}

function clearAllMethods() {
	var childs = document.getElementById("Methods").childNodes;
	for (var i = 0; i < childs.length; i++) {
		if (childs[i].tagName == "DIV") {
			childs[i].style.display = "none";
		}
	}

	var childs = document.getElementById("TableOfContents").childNodes;
	for (var i = 5; i < childs.length; i += 4) {
		if (childs[i].tagName == "UL") {
			var ulChilds = childs[i].childNodes;
			for (var j = 0; j < ulChilds.length; j++) {
				if (ulChilds[j].tagName == "LI") {
					ulChilds[j].style.fontWeight = "";
				}
			}
		}
	}
}