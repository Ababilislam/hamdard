$.afui.useOSThemes=false;
$.afui.useOSThemes=false;
$.afui.loadDefaultHash=true;
$.afui.autoLaunch=false;
var vNo=201222;

//check search
var search=document.location.search.toLowerCase().replace("?","");
if(search.length>0){
   $.afui.useOSThemes=true;
	if(search=="win8")
		$.os.ie=true;
	else if(search=="firefox")
		$.os.fennec="true"
	$.afui.ready(function(){
		$(document.body).get(0).className=(search);
	});
}


var  apipath =''; //for medicine search


//var  apipath ='http://127.0.0.1:8000/w02_ipi/medSearch/'

var oprtunityVal='';
localStorage.ff_present=0
localStorage.associated_call=0
localStorage.associated_call_others=0
var clickCount=0;
$(document).ready(function(){
        $.afui.launch();
		
		clickCount=0	
		localStorage.ff_present=0
		localStorage.associated_call=0
		localStorage.associated_call_others=0		
		
		if (localStorage.synced_rx=='YES'){
			$("#cid").val(localStorage.cid);
			$("#user_id").val(localStorage.user_id);
			$("#user_pass").val(localStorage.user_pass);
					
			//$.afui.loadContent("#pageHome",true,true,'right');
			$.afui.loadContent("#page_PrescriptionCapture",true,true,'right');			
				 			
		}
		
		
		
		// presscription page
		var imgList='';
		
		//imgList='<div style="width:30%; position:relative; float:left; border:1px solid #b3e4ff; border-radius:5px; height:120px; margin:1%; overflow:hidden; box-shadow:3px 3px 3px #b3e4ff;" ><img src="roxy.jpg" width="100%" style="border-radius: 5px; height:auto;" alt="&nbsp;&nbsp;&nbsp;Image &nbsp;'+100+'" id="myImage'+100+'" onClick="gotoPic('+100+')"><input name="prPhoto'+100+'" id="prPhoto'+100+'" type="hidden"/><div style="float:right; position: absolute; top:0; right: 0; width: 20px;height: 20px; "><a href="#" style="font-size:20px; text-decoration:none; color:#00a6ff;" class="icon remove" onClick="cancelPicture('+100+')" ></a></div></div>';
		
		for(i=1;i<=60;i++){					
			imgList+='<div style="width:30%; position:relative; float:left; border:1px solid #b3e4ff; border-radius:5px; height:120px; margin:1%; overflow:hidden; box-shadow:3px 3px 3px #b3e4ff;" ><img width="100%" style="border-radius: 5px; height:auto;" alt="&nbsp;&nbsp;&nbsp;Image &nbsp;'+i+'" id="myImage'+i+'" onClick="gotoPic('+i+')"><input name="prPhoto'+i+'" id="prPhoto'+i+'" type="hidden"/><div style="float:right; position: absolute; top:0; right: 0; width: 20px;height: 20px; "><a href="#" style="font-size:20px; text-decoration:none; color:#00a6ff;" class="icon remove" onClick="cancelPicture('+i+')" ></a></div></div>';//<img src="cancel.png" width="20" height="20" alt="X" id="myImage1"  onClick="cancelPicture('+i+')"></span>
		}
		
		$("#imgList").append(imgList);
		
		//single zoom in out
		var $section = $('section').first();
		$section.find('.panzoom').panzoom({
			$zoomIn: $section.find(".zoom-in"),
			$zoomOut: $section.find(".zoom-out"),
			$zoomRange: $section.find(".zoom-range"),
			$reset: $section.find(".reset")
		});
		
		
		$("#btn_search_med").show();
		$("#wait_image_med").hide();
		$("#opitemSearch").val('');
		
		$("#btn_search_doc").show();
		$("#wait_image_doc").hide();
		$("#drSearch").val('');
		
		$("#wait_image_prescription").hide();
		
				
		$("#wait_image_login").hide();
		$("#loginButton").show();
		
		getLocationInfo_ready();
		
	//===============SetPR=================
	for (j=1; j <= 60; j++){
		var picNo=parseInt(j); 
		var imageDiv="myImage"+picNo
		var imageText="prPhoto"+picNo
		var imageSource=''
				
		if (picNo==1){imageSource=localStorage.prPhoto1}
		if (picNo==2){imageSource=localStorage.prPhoto2}
		if (picNo==3){imageSource=localStorage.prPhoto3}
		if (picNo==4){imageSource=localStorage.prPhoto4}
		if (picNo==5){imageSource=localStorage.prPhoto5}
		if (picNo==6){imageSource=localStorage.prPhoto6}
		if (picNo==7){imageSource=localStorage.prPhoto7}
		if (picNo==8){imageSource=localStorage.prPhoto8}
		if (picNo==9){imageSource=localStorage.prPhoto9}
		if (picNo==10){imageSource=localStorage.prPhoto10}
		if (picNo==11){imageSource=localStorage.prPhoto11}
		if (picNo==12){imageSource=localStorage.prPhoto12}
		if (picNo==13){imageSource=localStorage.prPhoto13}
		if (picNo==14){imageSource=localStorage.prPhoto14}
		if (picNo==15){imageSource=localStorage.prPhoto15}
		if (picNo==16){imageSource=localStorage.prPhoto16}
		if (picNo==17){imageSource=localStorage.prPhoto17}
		if (picNo==18){imageSource=localStorage.prPhoto18}
		if (picNo==19){imageSource=localStorage.prPhoto19}
		if (picNo==20){imageSource=localStorage.prPhoto20}
		if (picNo==21){imageSource=localStorage.prPhoto21}
		if (picNo==22){imageSource=localStorage.prPhoto22}
		if (picNo==23){imageSource=localStorage.prPhoto23}
		if (picNo==24){imageSource=localStorage.prPhoto24}
		if (picNo==25){imageSource=localStorage.prPhoto25}
		if (picNo==26){imageSource=localStorage.prPhoto26}
		if (picNo==27){imageSource=localStorage.prPhoto27}
		if (picNo==28){imageSource=localStorage.prPhoto28}
		if (picNo==29){imageSource=localStorage.prPhoto29}
        if (picNo==30){imageSource=localStorage.prPhoto30}
        if (picNo==31){imageSource=localStorage.prPhoto31}
        if (picNo==32){imageSource=localStorage.prPhoto32}
        if (picNo==33){imageSource=localStorage.prPhoto33}
        if (picNo==34){imageSource=localStorage.prPhoto34}
        if (picNo==35){imageSource=localStorage.prPhoto35}
        if (picNo==36){imageSource=localStorage.prPhoto36}
        if (picNo==37){imageSource=localStorage.prPhoto37}
        if (picNo==38){imageSource=localStorage.prPhoto38}
        if (picNo==39){imageSource=localStorage.prPhoto39}
        if (picNo==40){imageSource=localStorage.prPhoto40}
        if (picNo==41){imageSource=localStorage.prPhoto41}
        if (picNo==42){imageSource=localStorage.prPhoto42}
        if (picNo==43){imageSource=localStorage.prPhoto43}
        if (picNo==44){imageSource=localStorage.prPhoto44}
        if (picNo==45){imageSource=localStorage.prPhoto45}
        if (picNo==46){imageSource=localStorage.prPhoto46}
        if (picNo==47){imageSource=localStorage.prPhoto47}
        if (picNo==48){imageSource=localStorage.prPhoto48}
        if (picNo==49){imageSource=localStorage.prPhoto49}
        if (picNo==50){imageSource=localStorage.prPhoto50}
        if (picNo==51){imageSource=localStorage.prPhoto51}
        if (picNo==52){imageSource=localStorage.prPhoto52}
        if (picNo==53){imageSource=localStorage.prPhoto53}
        if (picNo==54){imageSource=localStorage.prPhoto54}
        if (picNo==55){imageSource=localStorage.prPhoto55}
        if (picNo==56){imageSource=localStorage.prPhoto56}
        if (picNo==57){imageSource=localStorage.prPhoto57}
        if (picNo==58){imageSource=localStorage.prPhoto58}
        if (picNo==59){imageSource=localStorage.prPhoto59}
        if (picNo==60){imageSource=localStorage.prPhoto60} 
		                                                   
		//alert (imageSource)
		var image=document.getElementById(imageDiv);
		image.src=imageSource;
		imagePath=imageSource;
		$("#"+imageText).val(imagePath);
		
	}
		
		var ffPresentStr='<div ><div style="width:70%; float:left;"><label  >FF Present</label></div><div style="width:30%; float:left; padding-right:30px;"><input type="checkbox" id="ff_present" name="ff_present" class="toggle" onChange="ffPresent()" ><label for="ff_present" data-on="Yes" data-off="NO" ><span></span></label></div></div>';
		var associativeCallStr='<div ><div style="width:70%; float:left;"><label>Associated Call (FS)</label></div><div style="width:30%; float:left; padding-right:30px;"><input type="checkbox" id="associated_call" name="associated_call" class="toggle" onChange="associatedCall()" ><label for="associated_call" data-on="YES" data-off="NO" ><span ></span></label></div></div>'; 
		var associativeOthersCallStr='<div ><div style="width:70%; float:left;"><label>Associated Call (Others)</label></div><div style="width:30%; float:left; padding-right:30px;"><input type="checkbox" id="associated_call_others" name="associated_call_others" class="toggle" onChange="associatedCallOthers()" ><label for="associated_call_others" data-on="YES" data-off="NO" ><span ></span></label></div></div>'; 
		
		$('#ffPresentDiv').empty();
		$('#ffPresentDiv').html(ffPresentStr);
		$('#associativeCallDiv').empty();
		$('#associativeCallDiv').html(associativeCallStr);
		$('#associativeCallOthersDiv').empty();
		$('#associativeCallOthersDiv').html(associativeOthersCallStr);
		
		
		//--------------- rx type combo		
		var rxTypeCmbo='';
		var rxTypeArr=localStorage.rxTypeStr.split('||');
		var rxTypeArrLen=rxTypeArr.length;	
		rxTypeCmbo+='<select id="rx_type" onChange="rxType()" >';
		rxTypeCmbo+='<option value="">Select Rx Type</option>';
		for (i=0;i<rxTypeArrLen;i++){
			var rxTypeS=rxTypeArr[i].split('|');
			if(rxTypeS[1]==localStorage.rx_type){
				rxTypeCmbo+='<option value="'+rxTypeS[1]+'" selected >'+rxTypeS[1]+'</option>';
			}else{
				rxTypeCmbo+='<option value="'+rxTypeS[1]+'">'+rxTypeS[1]+'</option>';	
			}																											
		}
		rxTypeCmbo+='</select>'
		
		$('#rx_type_cmb').empty();	
		$('#rx_type_cmb').html(rxTypeCmbo);
		
				
		
		$("#opitemSearch").keyup(function(){
			searchMedicine()
		});
		
		$("#drSearch").keyup(function(){
			
			var searchValue=$("#drSearch").val();
			
			if(searchValue.length<3){				
				if (localStorage.doc_area!=""){
					searchDoc()
				}else{
					$('#doctorList').empty();					
					$("#error_doctorList").text("Type Minimum 3 Character.").removeClass('success').addClass('error');
				}
			}else{				
				$('#doctorList').empty();				
				$("#error_doctorList").text("").removeClass('success').removeClass('error');
				searchDoc()
			}
		});	
		
		
		var imgDegree=0;
		$("#btn_rotate").click(function (){		
			imgDegree+=90;
			$("#myImagePrescription_show").css({'transform':'rotate('+imgDegree+'deg)'});			
		});
		
		$("#btn_reset").click(function (){
			$("#myImagePrescription_show").css({'transform':'rotate(0deg)'});			
		});
		//-------------
			//vChek()
			
    });

$.afui.animateHeader(true);


/*function vChek(){
	$(".vNo").text(vNo);	
	$.ajax({
		  url: localStorage.base_url+'check_version?cid='+localStorage.cid+'&vNo='+vNo+'&uid='+localStorage.user_id,
		  success: function(resStr) {
			if (resStr!=""){
				$("#error_v").text(resStr).addClass('info');					
				//alert(resStr);
			}}})
}
*/



//-   ----- popup
function showSearchDoc() {
	
    $.afui.popup({
        title: "Select Area<hr/>",
        message: "Region<sup style='color:#F00;'>*</sup> :<div id='doc_region_cmb' ></div><div id='doc_area_cmb' ></div><div id='doc_tr_cmb' ></div><div id='doc_cat_cmb' ></div>",
        cancelText: "Cancel",
        cancelCallback: function () {},
        doneText: "Select",
        doneCallback: function () {	
			$("#drSearch").val("");		
			localStorage.docListStr="";
			localStorage.doc_region=$('#doc_region').val();
			localStorage.doc_area=$('#doc_area').val();
			localStorage.doc_territory=$('#doc_territory').val();
			localStorage.doc_category=$('#doc_category').val();
			
			if (localStorage.doc_category=='undefined'){
				localStorage.doc_category='';
			}
			
			if (localStorage.doc_area=='undefined'){
				localStorage.doc_area='';
			}			
			if (localStorage.doc_area==''){
				localStorage.doc_territory='';				
				localStorage.doc_region='';
				localStorage.doc_area='';
				localStorage.doc_territory='';
				localStorage.doc_category='';
				localStorage.searchSelect='';
				localStorage.doc_cart_list='';
			  	localStorage.docSelect='';
				
				localStorage.docStr='';
				localStorage.docListStr='';
				
				$('#searchSelect').empty();
				$("#error_doctorList").text("Required Region ,Area.").removeClass('success').addClass('error');
				searchDoc()								
			}else{			
				localStorage.searchSelect='<div  style="background-color:#e6fff9; border-bottom:1px solid #00cc99; margin:5px; border-radius:5px; padding:5px;" ><h3 ><span style="font-size:10px;">'+localStorage.doc_region+'</span></h3><h3 ><span style="font-size:10px;">'+localStorage.doc_area+'</span></h3><h3 ><span style="font-size:10px;">'+localStorage.doc_territory+'</span></h3><h3 ><span style="font-size:10px;">'+localStorage.doc_category+'</span></h3></div>'
					
				$('#searchSelect').empty();
				$('#docCart').empty();
				$('#searchSelect').append(localStorage.searchSelect);				
			}
						
			if (localStorage.searchSelect!=''){
				searchDoc()	
			}
			
        },
        cancelOnly: false		
    });
	
	//--------------- region combo
	var regionCmbo='';
	var regionArr=localStorage.regionStr.split('<rd>');
	var regionArrLen=regionArr.length;	
	regionCmbo+='<select id="doc_region" onChange="getArea()">';
	regionCmbo+='<option value="">Select Region</option>';
	for (i=0;i<regionArrLen;i++){
		var regionS=regionArr[i].split('<fd>');																																								
		regionCmbo+='<option value="'+regionS[0]+'|'+regionS[1]+'">'+regionS[1]+'</option>';																												
		}
	regionCmbo+='</select>'	
	$('#doc_region_cmb').html(regionCmbo);

	//--------------- doctor Category combo
	var docCatCmbo='';
	var docCatArr=localStorage.docCategoryStr.split('<fd>');
	var docCatArrLen=docCatArr.length;
	docCatCmbo+='<div>Category :</div>';	
	docCatCmbo+='<select id="doc_category">';
	docCatCmbo+='<option value="">ALL</option>';
	for (i=0;i<docCatArrLen;i++){																																							
		docCatCmbo+='<option value="'+docCatArr[i]+'">'+docCatArr[i]+'</option>';																												
		}
	docCatCmbo+='</select>'	
	$('#doc_cat_cmb').html(docCatCmbo);	
	
}

function getArea(){
	var doc_region=$('#doc_region').val().split('|');
	
	var areaCmbo='';
	var areaArr=localStorage.areaStr.split('<rd>');
	var areaArrLen=areaArr.length;
	areaCmbo+='<div>Area<sup style="color:#F00;">*</sup> :</div>';	
	areaCmbo+='<select id="doc_area" onChange="getTerritory()">';
	areaCmbo+='<option value="">Select Area</option>';
	for (i=0;i<areaArrLen;i++){
		var areaS=areaArr[i].split('<fd>');																																								
			if (areaS[0]==doc_region[0]){
				areaCmbo+='<option value="'+areaS[1]+'|'+areaS[2]+'">'+areaS[2]+'</option>';		
			}																													
		}
	areaCmbo+='</select>'	
	$('#doc_area_cmb').html(areaCmbo);
	$('#doc_tr_cmb').empty();	
	}

function getTerritory(){
	var doc_region=$('#doc_region').val().split('|');
	var doc_area=$('#doc_area').val().split('|');
	
	var trCmbo='';
	var trArr=localStorage.territoryStr.split('<rd>');
	var trArrLen=trArr.length;	
	trCmbo+='<div>Territory :</div>';
	trCmbo+='<select id="doc_territory" >';
	trCmbo+='<option value="">ALL</option>';
	for (i=0;i<trArrLen;i++){
		var trS=trArr[i].split('<fd>');																																								
			if (trS[0]==doc_region[0] && trS[1]==doc_area[0]){
				trCmbo+='<option value="'+trS[2]+'|'+trS[3]+'">'+trS[3]+'</option>';		
			}																													
		}
	trCmbo+='</select>'	
	$('#doc_tr_cmb').html(trCmbo);	
	}

function addNewDoc() {
	$("#error_doctorList").text("").removeClass('success').removeClass('error');
    $.afui.popup({
        title: "New Doctor <hr/>",
        message: "<div id='doc_add_region_cmb' ></div><div id='doc_add_area_cmb' ></div><div id='doc_add_tr_cmb' ></div><div>Name<sup style='color:#F00;'>*</sup>: <input type='text' id='doc_name_new' ></div><div>Address<sup style='color:#F00;'>*</sup>: <textarea col='50' rows='3' id='doc_address_new'></textarea></div>",
        cancelText: "Cancel",
        cancelCallback: function () {},
        doneText: "Save",
        doneCallback: function () {	
			var doc_new_tr=$('#doc_add_territory').val();
				
/*			if (localStorage.doc_territory=='undefined' || localStorage.doc_territory==''){
				localStorage.doc_territory=$('#doc_add_territory').val();				
			}*/
			localStorage.doc_territory=$('#doc_add_territory').val();
							
			if (localStorage.doc_territory==""){
				$("#error_doctorList").text("Required Territory for New Doctor Add.").removeClass('success').addClass('error');
			}else{
				
				var doc_name_new=$('#doc_name_new').val();
				var doc_address_new=$('#doc_address_new').val();
				
				if (doc_name_new=='' || doc_address_new==''){
					$("#error_doctorList").text("Required Name and address For New Doctor Add.").removeClass('success').addClass('error');
				}else{
										
					if (localStorage.doc_region=='undefined' || localStorage.doc_region==''){					
						localStorage.doc_region=$('#doc_add_region').val();				
					}
					
					if (localStorage.doc_area=='undefined' || localStorage.doc_area==''){
						localStorage.doc_area=$('#doc_add_area').val();						
					}
					
					if (localStorage.doc_territory=='undefined' || localStorage.doc_territory==''){
						localStorage.doc_territory=$('#doc_add_territory').val();						
					}
					
					
								
					localStorage.searchSelect='<div  style="background-color:#e6fff9; border-bottom:1px solid #00cc99; margin:5px; border-radius:5px; padding:5px;" ><h3 ><span style="font-size:10px;">'+localStorage.doc_region+'</span></h3><h3 ><span style="font-size:10px;">'+localStorage.doc_area+'</span></h3><h3 ><span style="font-size:10px;">'+localStorage.doc_territory+'</span></h3><h3 ><span style="font-size:10px;">'+localStorage.doc_category+'</span></h3></div>'
				
					$('#searchSelect').empty();
					$('#searchSelect').html(localStorage.searchSelect);
						
					
				
					var doc_tr_new=localStorage.doc_territory.split('|');				
					var docStr='0|'+doc_name_new+'|'+doc_address_new+'|'+doc_tr_new[0];				
					localStorage.docStr=docStr
					
					
					doc_cart_list='<div style="background-color:#ccedff; border-bottom:1px solid #d9d9d9; margin:5px; padding:5px; border-radius:2px;">';
					doc_cart_list+='<h2 style="border-bottom:1px solid #d9d9d9;">Doctor</h2>';
					doc_cart_list+='<h3 > '+doc_name_new+'</h3>';
					doc_cart_list+='<p style="margin:0px; font-size:11px; line-height:normal;">'+doc_address_new+'</p>';  
					doc_cart_list+='</div>';
					doc_cart_list+='<div style="clear:both;"></div><br/>';
					
					localStorage.doc_cart_list=doc_cart_list
					
					$('#docCart').empty();
					$('#docCart').html(localStorage.doc_cart_list);
					$('#docSelect').empty();
					$('#docSelect').append('<div  style="background-color:#e6fff9; border-bottom:1px solid #00cc99; margin:5px; border-radius:5px; padding:5px;" ><h3 >'+doc_name_new+'</h3><p style="margin:0px; font-size:11px; line-height:normal;" >'+doc_address_new+'</p></div>');
				}
			}
		},
        cancelOnly: false
    });
	
/*	var docRegion=localStorage.doc_region.split('|');
	var docArea=localStorage.doc_area.split('|');
	var docTr=localStorage.doc_territory.split('|');*/
	
	if (localStorage.doc_area==""){	
		var regionCmbo='';
		var regionArr=localStorage.regionStr.split('<rd>');
		var regionArrLen=regionArr.length;
		regionCmbo+='Region<sup style="color:#F00;">*</sup>:';	
		regionCmbo+='<select id="doc_add_region" onChange="getDocAddArea()">';
		regionCmbo+='<option value="">Select Region</option>';
		for (i=0;i<regionArrLen;i++){
			var regionS=regionArr[i].split('<fd>');																																								
			regionCmbo+='<option value="'+regionS[0]+'|'+regionS[1]+'">'+regionS[1]+'</option>';																												
			}
		regionCmbo+='</select>'	
		$('#doc_add_region_cmb').html(regionCmbo);
	}else{
		var doc_region=localStorage.doc_region.split('|');
		var doc_area=localStorage.doc_area.split('|');
		
		var trCmbo='';
		var trArr=localStorage.territoryStr.split('<rd>');
		var trArrLen=trArr.length;
		trCmbo+='Territory<sup style="color:#F00;">*</sup>:';	
		trCmbo+='<select id="doc_add_territory" >';
		for (i=0;i<trArrLen;i++){
			var trS=trArr[i].split('<fd>');																																								
				if (trS[0]==doc_region[0] && trS[1]==doc_area[0]){
					trCmbo+='<option value="'+trS[2]+'|'+trS[3]+'">'+trS[3]+'</option>';		
				}																													
			}
		trCmbo+='</select>'	
		$('#doc_add_tr_cmb').html(trCmbo);
		
		
		}	

}


function getDocAddArea(){
	var doc_region=$('#doc_add_region').val().split('|');
	
	var areaCmbo='';
	var areaArr=localStorage.areaStr.split('<rd>');
	var areaArrLen=areaArr.length;	 
	areaCmbo+='Area<sup style="color:#F00;">*</sup>:';
	areaCmbo+='<select id="doc_add_area" onChange="getDocAddTerritory()">';
	areaCmbo+='<option value="">Select Area</option>';
	for (i=0;i<areaArrLen;i++){
		var areaS=areaArr[i].split('<fd>');																																								
			if (areaS[0]==doc_region[0]){
				areaCmbo+='<option value="'+areaS[1]+'|'+areaS[2]+'">'+areaS[2]+'</option>';		
			}																													
		}
	areaCmbo+='</select>'	
	$('#doc_add_area_cmb').html(areaCmbo);
	$('#doc_add_tr_cmb').empty();	
	}

function getDocAddTerritory(){
	var doc_region=$('#doc_add_region').val().split('|');
	var doc_area=$('#doc_add_area').val().split('|');
	
	var trCmbo='';
	var trArr=localStorage.territoryStr.split('<rd>');
	var trArrLen=trArr.length;
	trCmbo+='Territory<sup style="color:#F00;">*</sup>:';	
	trCmbo+='<select id="doc_add_territory" >';
	for (i=0;i<trArrLen;i++){
		var trS=trArr[i].split('<fd>');																																								
			if (trS[0]==doc_region[0] && trS[1]==doc_area[0]){
				trCmbo+='<option value="'+trS[2]+'|'+trS[3]+'">'+trS[3]+'</option>';		
			}																													
		}
	trCmbo+='</select>'	
	$('#doc_add_tr_cmb').html(trCmbo);	
	}



//----------/popup



//==Reload Location
function getLocationInfo_ready() { 
	//$("#wait_image_prescription").show();	
	var options = { enableHighAccuracy: true, timeout:30000};
	navigator.geolocation.getCurrentPosition(onSuccess_ready, onError_ready, options);
}

// onSuccess Geolocationshom
function onSuccess_ready(position) {
	$("#lat").val(position.coords.latitude);
	$("#longitude").val(position.coords.longitude);
	
	localStorage.latitude=position.coords.latitude
	localStorage.longitude=position.coords.longitude	
	
		
	//$("#checkLocation").html('Location Confirmed'); 		
	
	//$("#wait_image_visit_submit").hide();
	//$("#visit_submit").show();
	//$("#visit_location").hide();
	
	//$("#checkLocation_doc").html('Location Confirmed');
		
} 
function onError_ready(error) {	
	$("#lat").val(0);
	$("#longitude").val(0);	
		
	/*$("#checkLocation").html(''); 
	$("#wait_image_visit_submit").hide();
	$("#visit_submit").show();
	$("#visit_location").hide();
		
    $("#checkLocation_doc").html('');
	$("#wait_image_visit_submit_doc").hide();*/
	alert ("Please on your GPS")
	
}




function page_home() {
	$("#error_login").text("").removeClass('success').removeClass('error');
	
	if (localStorage.synced_rx=='YES'){	
		$.afui.loadContent("#pageHome",true,true,'right');
	}else{
		$("#error_login").text("Required LogIn.").removeClass('success').addClass('error');	
	}
}

function page_login() {
	$("#error_login").text("").removeClass('success').removeClass('error');
	$("#wait_image_login").hide();		
	$("#loginButton").show();	
	$.afui.loadContent("#login",true,true,'right');
}

function clearPicture(){
	localStorage.picFlag=0;	
	/*$("#imgList").empty();
	
	var imgList="";
	for(i=1;i<=30;i++){					
		imgList+='<div style="width:30%; position:relative; float:left; border:1px solid #b3e4ff; border-radius:5px; height:120px; margin:1%; overflow:hidden; box-shadow:3px 3px 3px #b3e4ff;" ><img width="100%" style="border-radius: 5px; height:auto;" alt="&nbsp;&nbsp;&nbsp;Image &nbsp;'+i+'" id="myImage'+i+'" onClick="gotoPic('+i+');"><input name="prPhoto'+i+'" id="prPhoto'+i+'" type="hidden"/><div style="float:right; position: absolute; top:0; right: 0; width: 20px;height: 20px; "><a href="#" style="font-size:20px; text-decoration:none; color:#00a6ff;" class="icon remove" onClick="cancelPicture('+i+')" ></a></div></div>';//<img src="cancel.png" width="20" height="20" alt="X" id="myImage1"  onClick="cancelPicture('+i+')"></span>
	}
	$("#imgList").append(imgList); */

}

function gotoPic(picNo) {
	$("#error_prescription_submit").text("").removeClass('error').removeClass('success');
	$("#btn_prescription_submit").show();
	$("#wait_image_prescription").hide();
	$(".panzoom").removeClass('panzoom').addClass('panzoom');
	
	var imageDiv="myImage"+picNo
	var imageText="prPhoto"+picNo
	
	if (picNo!=localStorage.picNo){
		$('#medicineList').empty();
		$('#doctorList').empty();
		$("#docCart").empty();						
		$("#opCart").empty();
		$("#docSelect").empty();
		
		$("#medicine_1").val('');
		$("#medicine_2").val('');
		$("#medicine_3").val('');
		$("#medicine_4").val('');
		$("#medicine_5").val('');
		
		
		localStorage.opProdID_Str=''
		
	}
	localStorage.picNo=picNo
	
	var prPic=$("#"+imageText).val();
	
	var image_show = document.getElementById('myImagePrescription_show');
	image_show.src = prPic;
	$("#myImagePrescription_show").val(prPic)
	
	if (localStorage.docStr!=""){			
		  keywordLi=localStorage.docStr.split("|")		  
		  var docID=keywordLi[0].trim();
		  var docName=keywordLi[1];
		  var docAdd=keywordLi[2];
		  var docArea=keywordLi[3];
		  		  
		  doc_cart_list='<div style="background-color:#ccedff; border-bottom:1px solid #d9d9d9; margin:5px; padding:5px; border-radius:2px;">';
		  doc_cart_list+='<input type="hidden" id="doc'+docID+'" value="'+localStorage.docStr+'"/>'
		  doc_cart_list+='<h2 style="border-bottom:1px solid #d9d9d9;">Doctor</h2>';
		  doc_cart_list+='<h3 > '+docName+'</h3>';
		  doc_cart_list+='<p style="margin:0px; font-size:11px; line-height:normal;">'+docAdd+'</p>';  
		  doc_cart_list+='</div>';
		  doc_cart_list+='<div style="clear:both;"></div><br/>';
		
		  localStorage.doc_cart_list=doc_cart_list;
		  
		  localStorage.docSelect='<div  style="background-color:#e6fff9; border-bottom:1px solid #00cc99; margin:5px; border-radius:5px; padding:5px;" ><h3 >'+docName+'</h3><p style="margin:0px; font-size:11px; line-height:normal;" >'+docAdd+'</p></div>';
		  			
		 		  
		  $('#docCart').empty();
		  $('#docCart').html(localStorage.doc_cart_list);
		  $('#docSelect').empty();
		  $('#docSelect').html(localStorage.docSelect);
		  			
		}
	
		var ffPresentStr='<div ><div style="width:70%; float:left;"><label  >FF Present</label></div><div style="width:30%; float:left; padding-right:30px;"><input type="checkbox" id="ff_present" name="ff_present" class="toggle" onChange="ffPresent()" ><label for="ff_present" data-on="Yes" data-off="NO" ><span></span></label></div></div>';
		var associativeCallStr='<div ><div style="width:70%; float:left;"><label>Associated Call (FS)</label></div><div style="width:30%; float:left; padding-right:30px;"><input type="checkbox" id="associated_call" name="associated_call" class="toggle" onChange="associatedCall()" ><label for="associated_call" data-on="YES" data-off="NO" ><span ></span></label></div></div>'; 
		var associativeOthersCallStr='<div ><div style="width:70%; float:left;"><label>Associated Call (Others)</label></div><div style="width:30%; float:left; padding-right:30px;"><input type="checkbox" id="associated_call_others" name="associated_call_others" class="toggle" onChange="associatedCallOthers()" ><label for="associated_call_others" data-on="YES" data-off="NO" ><span ></span></label></div></div>'; 
		
		$('#ffPresentDiv').empty();
		$('#ffPresentDiv').html(ffPresentStr);
		$('#associativeCallDiv').empty();
		$('#associativeCallDiv').html(associativeCallStr);
		$('#associativeCallOthersDiv').empty();
		$('#associativeCallOthersDiv').html(associativeOthersCallStr);
		
		//--------------- rx type combo	
		localStorage.rx_type="";	
		var rxTypeCmbo='';
		var rxTypeArr=localStorage.rxTypeStr.split('||');
		var rxTypeArrLen=rxTypeArr.length;	
		rxTypeCmbo+='<select id="rx_type" onChange="rxType()" >';
		rxTypeCmbo+='<option value="">Select Rx Type</option>';
		for (i=0;i<rxTypeArrLen;i++){
			var rxTypeS=rxTypeArr[i].split('|');																																								
			if(rxTypeS[1]==localStorage.rx_type){
				rxTypeCmbo+='<option value="'+rxTypeS[1]+'" selected >'+rxTypeS[1]+'</option>';
			}else{
				rxTypeCmbo+='<option value="'+rxTypeS[1]+'">'+rxTypeS[1]+'</option>';	
			}																													
		}
		rxTypeCmbo+='</select>'
		
		$('#rx_type_cmb').empty();	
		$('#rx_type_cmb').html(rxTypeCmbo);
	  
		
	if (prPic!=''){		
		$.afui.loadContent("#imageSinglePage",true,true,'right');
	}else{
		$.afui.loadContent("#imageSinglePage",true,true,'right');
	}
}

function cancelPicture(i){
	var imageDiv="myImage"+i
	var imageText="prPhoto"+i
	var imageSource=''
	var image = document.getElementById(imageDiv);
	image.src = imageSource;
	imagePath = imageSource;
	$("#"+imageText).val(imagePath);
	var picNo=i+1
	if (picNo==1){localStorage.prPhoto1=''}
	if (picNo==2){localStorage.prPhoto2=''}
	if (picNo==3){localStorage.prPhoto3=''}
	if (picNo==4){localStorage.prPhoto4=''}
	if (picNo==5){localStorage.prPhoto5=''}
	if (picNo==6){localStorage.prPhoto6=''}
	if (picNo==7){localStorage.prPhoto7=''}
	if (picNo==8){localStorage.prPhoto8=''}
	if (picNo==9){localStorage.prPhoto9=''}
	if (picNo==10){localStorage.prPhoto10=''}
	if (picNo==11){localStorage.prPhoto11=''}
	if (picNo==12){localStorage.prPhoto12=''}
	if (picNo==13){localStorage.prPhoto13=''}
	if (picNo==14){localStorage.prPhoto14=''}
	if (picNo==15){localStorage.prPhoto15=''}
	if (picNo==16){localStorage.prPhoto16=''}
	if (picNo==17){localStorage.prPhoto17=''}
	if (picNo==18){localStorage.prPhoto18=''}
	if (picNo==19){localStorage.prPhoto19=''}
	if (picNo==20){localStorage.prPhoto20=''}
	if (picNo==21){localStorage.prPhoto21=''}
	if (picNo==22){localStorage.prPhoto22=''}
	if (picNo==23){localStorage.prPhoto23=''}
	if (picNo==24){localStorage.prPhoto24=''}
	if (picNo==25){localStorage.prPhoto25=''}
	if (picNo==26){localStorage.prPhoto26=''}
	if (picNo==27){localStorage.prPhoto27=''}
	if (picNo==28){localStorage.prPhoto28=''}
	if (picNo==29){localStorage.prPhoto29=''}
    if (picNo==30){localStorage.prPhoto30=''}
    if (picNo==31){localStorage.prPhoto31=''}
    if (picNo==32){localStorage.prPhoto32=''}
    if (picNo==33){localStorage.prPhoto33=''}
    if (picNo==34){localStorage.prPhoto34=''}
    if (picNo==35){localStorage.prPhoto35=''}
    if (picNo==36){localStorage.prPhoto36=''}
    if (picNo==37){localStorage.prPhoto37=''}
    if (picNo==38){localStorage.prPhoto38=''}
    if (picNo==39){localStorage.prPhoto39=''}
    if (picNo==40){localStorage.prPhoto40=''}
    if (picNo==41){localStorage.prPhoto41=''}
    if (picNo==42){localStorage.prPhoto42=''}
    if (picNo==43){localStorage.prPhoto43=''}
    if (picNo==44){localStorage.prPhoto44=''}
    if (picNo==45){localStorage.prPhoto45=''}
    if (picNo==46){localStorage.prPhoto46=''}
    if (picNo==47){localStorage.prPhoto47=''}
    if (picNo==48){localStorage.prPhoto48=''}
    if (picNo==49){localStorage.prPhoto49=''}
    if (picNo==50){localStorage.prPhoto50=''}
    if (picNo==51){localStorage.prPhoto51=''}
    if (picNo==52){localStorage.prPhoto52=''}
    if (picNo==53){localStorage.prPhoto53=''}
    if (picNo==54){localStorage.prPhoto54=''}
    if (picNo==55){localStorage.prPhoto55=''}
    if (picNo==56){localStorage.prPhoto56=''}
    if (picNo==57){localStorage.prPhoto57=''}
    if (picNo==58){localStorage.prPhoto58=''}
    if (picNo==59){localStorage.prPhoto59=''}
    if (picNo==60){localStorage.prPhoto60=''}
	
}

//------------------ doc search 
function docAdd(docid){
						
			$('#docCart').empty();
			$('#docSelect').empty();
			var docStr=$("#doc"+docid).val();
			if (docStr!=""){
			  localStorage.docStr=docStr			
			  keywordLi=localStorage.docStr.split("|")
			  var docID=keywordLi[0].trim();
			  var docName=keywordLi[1];
			  var docAdd=keywordLi[2];
			  var docArea=keywordLi[3];
			  
			  
			  doc_cart_list='<div style="background-color:#ccedff; border-bottom:1px solid #d9d9d9; margin:5px; padding:5px; border-radius:2px;">';
			  doc_cart_list+='<input type="hidden" id="doc'+docID+'" value="'+localStorage.docStr+'"/>'
			  doc_cart_list+='<h2 style="border-bottom:1px solid #d9d9d9;">Doctor</h2>';
			  doc_cart_list+='<h3 > '+docName+'</h3>';
			  doc_cart_list+='<p style="margin:0px; font-size:11px; line-height:normal;">'+docAdd+'|'+docArea+'</p>';  
			  doc_cart_list+='</div>';
			  doc_cart_list+='<div style="clear:both;"></div><br/>';
			  
			  localStorage.doc_cart_list=doc_cart_list
			  
			  localStorage.docSelect='<div  style="background-color:#e6fff9; border-bottom:1px solid #00cc99; margin:5px; border-radius:5px; padding:5px;" ><h3 >'+docName+'</h3><p style="margin:0px; font-size:11px; line-height:normal;" >'+docAdd+'</p></div>';
		  								
			  $('#docCart').empty();
			  $('#docCart').html(localStorage.doc_cart_list);
			  $('#docSelect').empty();			  		  
		      $('#docSelect').html(localStorage.docSelect);
			  			  	
			}		
		}

<!-- doctor-->
function docList(){
	$("#wait_image_doc").hide();		
	$.afui.drawer.show('#doctor_add','left','push');
	
	if (localStorage.doc_area!=""){
		searchDoc()
	}else{
		$('#docSelect').empty();
		$('#doctorList').empty();
		$("#wait_image_doc").show();
		$('#searchSelect').empty();
		$("#wait_image_doc").hide();
		$("#drSearch").val('');
		
	}
		
}

	

function searchDoc(){
	$("#error_doctorList").text("").removeClass('success').removeClass('error');
	$('#docSelect').empty();
	$('#doctorList').empty();
	$("#wait_image_doc").show();
	$('#searchSelect').empty();
	$('#docSelect').html(localStorage.docSelect);
	$('#searchSelect').html(localStorage.searchSelect);
	
	var docRegion=localStorage.doc_region.split('|');
	var docArea=localStorage.doc_area.split('|');
	var docTr=localStorage.doc_territory.split('|');
	var docCat=localStorage.doc_category;
	var searchValue = $("#drSearch").val().toUpperCase();
	
	var doc_search_url="";
	if(localStorage.docListStr!=""){
		$("#wait_image_doc").hide();
		var keywordStr=localStorage.docListStr.split("||");
		var keywordStrLen=keywordStr.length;
		  var keywordS='<br/>';
		  for (i=0;i<keywordStrLen;i++){
			  keywordLi=keywordStr[i].split("|")
			  var docID=keywordLi[0].trim();
			  var docName=keywordLi[1];
			  var docAdd=keywordLi[2];
			  var docArea=keywordLi[3];						  
			  
			  var docNameS=keywordLi[1].toUpperCase();
			  var docAddS=keywordLi[2].toUpperCase();
			  
			  if(searchValue==''){
				  keywordS+='<div  style="background-color:#ccedff; border-bottom:1px solid #d9d9d9; margin-bottom:2px; border-radius:5px; padding:10px; " onclick="docAdd(\''+docID+'\')" >';						  				  
				  keywordS+='<input type="hidden" id="doc'+docID+'" value="'+keywordStr[i]+'"/>'
				  keywordS+='<h3 >'+docName+'</h3>';
				  keywordS+='<p style="margin:0px; font-size:11px; line-height:normal; " >'+docAdd+'| <span style="background-color:#00a6ff; border-radius:5px; color:#FFF; padding:2px;">'+docArea+'</span></p>';  
				  keywordS+='</div>';
				  keywordS+='<div style="clear:both;"></div>';  
			  
			  }else{				  			  
				  if(docNameS.indexOf(searchValue)>0 || docAddS.indexOf(searchValue)>0 ){						  
					  keywordS+='<div  style="background-color:#ccedff; border-bottom:1px solid #d9d9d9; margin-bottom:2px; border-radius:5px; padding:10px; " onclick="docAdd(\''+docID+'\')" >';						  				  
					  keywordS+='<input type="hidden" id="doc'+docID+'" value="'+keywordStr[i]+'"/>'
					  keywordS+='<h3 >'+docName+'</h3>';
					  keywordS+='<p style="margin:0px; font-size:11px; line-height:normal; " >'+docAdd+'| <span style="background-color:#00a6ff; border-radius:5px; color:#FFF; padding:2px;">'+docArea+'</span></p>'; 
					  keywordS+='</div>';
					  keywordS+='<div style="clear:both;"></div>';
				  }
			  }
		  }
		 
		 if (keywordS=="<br/>"){
			 localStorage.docSelect='';		
			 localStorage.docListStr="";
			 doc_search_url=localStorage.apipath+'search_doctor?cid='+localStorage.cid+'&uid='+localStorage.user_id+'&region=&area=&tr=&category=&searchValue='+searchValue;
		 }else{	 
			$('#doctorList').empty();
			$('#doctorList').append(keywordS).trigger('create');
		 }
		
	}else{
		localStorage.docSelect='';		
		localStorage.docListStr="";
				
		if (searchValue!=""){
			if (searchValue.length<3){				
				$('#doctorList').empty();
				$("#error_doctorList").text("Type Minimum 3 Character.").removeClass('success').addClass('error');
			}else{						
				doc_search_url=localStorage.apipath+'search_doctor?cid='+localStorage.cid+'&uid='+localStorage.user_id+'&region=&area=&tr=&category=&searchValue='+searchValue;			
			}
		}else{		
			if (docArea==undefined || docArea==""){
				$("#error_doctorList").text("Select Area.").removeClass('success').addClass('error');
			}else{				
				doc_search_url=localStorage.apipath+'search_doctor?cid='+localStorage.cid+'&uid='+localStorage.user_id+'&region='+docRegion[0]+'&area='+docArea[0]+'&tr='+docTr[0]+'&category='+docCat+'&searchValue=';
			}
		}
	}
	
	if (doc_search_url!=""){
		$("#wait_image_doc").show();
			
		$.ajax({
			  url: doc_search_url,
			  success: function(resStr) {
				if (resStr!=""){
					localStorage.docListStr=resStr;
					
					var keywordStr=resStr.split("||");
					var keywordStrLen=keywordStr.length;
					  var keywordS='<br/>';
					  for (i=0;i<keywordStrLen;i++){
						  keywordLi=keywordStr[i].split("|")
						  var docID=keywordLi[0].trim();
						  var docName=keywordLi[1];
						  var docAdd=keywordLi[2];
						  var docArea=keywordLi[3];						  
												  
						  keywordS+='<div  style="background-color:#ccedff; border-bottom:1px solid #d9d9d9; margin-bottom:2px; border-radius:5px; padding:10px; " onclick="docAdd(\''+docID+'\')" >';						  				  
						  keywordS+='<input type="hidden" id="doc'+docID+'" value="'+keywordStr[i]+'"/>'
						  keywordS+='<h3 >'+docName+'</h3>';
						  keywordS+='<p style="margin:0px; font-size:11px; line-height:normal; " >'+docAdd+'| <span style="background-color:#00a6ff; border-radius:5px; color:#FFF; padding:2px;">'+docArea+'</span></p>';  
						  keywordS+='</div>';
						  keywordS+='<div style="clear:both;"></div>';	
					  }					  
					 
					$('#doctorList').empty();
					$('#doctorList').append(keywordS).trigger('create');
					
					
					//$("#btn_search_doc").show();
					$("#wait_image_doc").hide();		
				}else{					
					$("#error_doctorList").text("Dr. Not Available.").removeClass('success').addClass('error');
					$("#wait_image_doc").hide();
					
				}		
			  }		
		});
	}
	
}

function clearDoc(){
	//$('#docSelect').empty();
	$("#error_doctorList").empty();	
	$('#doctorList').empty(); 
	$("#btn_search_doc").show();
	$("#wait_image_doc").hide();	
	$("#drSearch").val('');	
	$('#docSelect').empty();
	$("#docCart").empty();
	
	localStorage.doc_region='';
	localStorage.doc_area='';
	localStorage.doc_territory='';
	localStorage.doc_category='';
	localStorage.searchSelect='';
	localStorage.doc_cart_list='';
	localStorage.docSelect='';
	
	localStorage.docStr='';
	localStorage.docListStr='';		
	
	searchDoc()
	
}

function clearSearcDoc(){
	$('#doctorList').empty();
	$("#drSearch").val('');	
	$('#docSelect').empty();
	localStorage.doc_cart_list='';
	localStorage.docSelect='';
	localStorage.docListStr='';	
	
	searchDoc()
	
	}


<!-- op product-->
function medList(){
	/*$("#medicine_new").val("");
	var medSearch=$("#opitemSearch").val();		
	
	if (medSearch!=""){
		searchMedicine()
	}else{
		$('#medicineList').empty();		
	}*/
	searchMedicine()
	
	//$.afui.drawer.show('#op_med_add','right','push');
	
		
}

function searchMedicine(){	
	//$(".error").text("").removeClass('success').removeClass('error');
	// opitemSearch
		
	//var searchValue = $("#opitemSearch").val().toUpperCase();
	
	//if(searchValue.length>0 && searchValue.length<1){
		//$("#wait_image_med").hide();
		//$('#error_medicineList').text('Type minimum 3 character').removeClass('success').addClass('error');
		//$("#btn_search_med").show();
	//}else{
		//$("#wait_image_med").show();
		//$("#btn_search_med").hide();
		
		keywordStr=localStorage.medStr.split("||");
		var keywordStrLen=keywordStr.length;
		  var keywordS='';
		  for (i=0;i<keywordStrLen;i++){
			  keywordLi=keywordStr[i].split("|")
			  var pID=keywordLi[0].trim();
			  var medName=keywordLi[1];
			  //var brandName=keywordLi[2];//.toUpperCase()
			  var brandNameS=keywordLi[1].toUpperCase();//
			  
			  //if (brandNameS.indexOf(searchValue)==1){			 
				  keywordS+='<div  style="background-color:#ccedff; border-bottom:1px solid #d9d9d9; margin-bottom:2px; border-radius:2px; padding:10px;">';						  					  
				  keywordS+='<div onclick="medClickVal2(\''+pID+'\',\''+medName+'\')"  style="float:left; width:80%; font-size:14px;"   id="medId'+pID+'">';
				  keywordS+='<span >'+medName+'</span>' 
				  keywordS+='</div>'
				  keywordS+='<div style="float:left; width:15%;">'
				  keywordS+='<input onmouseout="medClickVal(\''+pID+'\',\''+medName+'\')" id="inpId'+pID+'" type="hidden" style="width:50px; height:30px; margin:0px; padding:0px;" />'
				  keywordS+='</div>'
				  keywordS+='<div style="clear:both;"></div></div>';
			  //}
		  }
		  
		  
		$('#medicineList').empty();
		$('#medicineList').append(keywordS).trigger('create');
		
		//$("#btn_search_med").show();
		//$("#wait_image_med").hide();
		
		
		//alert(localStorage.apipath+'search_medicine?searchValue='+searchValue);
/*		$.ajax({
			  url: localStorage.apipath+'search_medicine?searchValue='+searchValue,
			  success: function(resStr) {
				if (resStr!=""){					
					keywordStr=resStr.split("||");
					  var keywordS='';
					  for (i=0;i<keywordStr.length;i++){
						  keywordLi=keywordStr[i].split("|")
						  var pID=keywordLi[0].trim();
						  var medName=keywordLi[1];
						  
						 
						  keywordS+='<div  style="background-color:#ccedff; border-bottom:1px solid #d9d9d9; margin-bottom:2px; border-radius:2px; padding:5px;">';						  					  
						  keywordS+='<div  style="float:left; width:80%;"   id="medId'+pID+'">';
						  keywordS+='<span onclick="medClickVal2(\''+pID+'\',\''+medName+'\')"  >'+medName+'</span>' 
						  keywordS+='</div>'
						  keywordS+='<div style="float:left; width:15%;">'
						  keywordS+='<input onmouseout="medClickVal(\''+pID+'\',\''+medName+'\')" id="inpId'+pID+'" type="hidden" style="width:50px; height:30px; margin:0px; padding:0px;" />'
						  keywordS+='</div>'
						  keywordS+='<div style="clear:both;"></div></div>'
					  }
					  
					  
					$('#medicineList').empty();
					$('#medicineList').append(keywordS).trigger('create');
					 
					$("#error_medicineList").text("");
					$("#btn_search_med").show();
					$("#wait_image_med").hide();
					
				}else{
					$("#error_medicineList").text("Medicine Not Not Available.").removeClass('success').addClass('error');
				}
			
			  }
			
		});*/
	//}
	
	$.afui.drawer.show('#op_med_add','right','push');
}

function clearMedicine(){
	$(".error").text("").removeClass('success').removeClass('error');	
	$('#medicineList').empty(); 
	//$("#btn_search_med").show();
	//$("#wait_image_med").hide();	
	$("#opitemSearch").val('');	
}

function removeCarItemOp(product_idGet){	
	$("#cartOp_"+product_idGet).remove();
	var repl1='';	
	iStr=localStorage.opProdID_Str.split('||');
	iLen=iStr.length
	for(i=0;i<iLen;i++){
		iStrD=iStr[i].split('|');
		if(iStrD[0]!=product_idGet){
			if (repl1==''){
				repl1=iStr[i]
			}else{
				repl1+='||'+iStr[i]
			}				
		}				
	}
	oprtunityVal = repl1;
	localStorage.opProdID_Str=repl1;
}

function removeCartNewItem(n){	
	var itemName=$("#inpId"+n).val();
	$("#cartOp_"+n).remove();
	var repl1='';	
	iStr=localStorage.opProdID_Str.split('||');
	iLen=iStr.length
	for(i=0;i<iLen;i++){
		iStrD=iStr[i].split('|');
		if(iStrD[1]!=itemName){
			if (repl1==''){
				repl1=iStr[i]
			}else{
				repl1+='||'+iStr[i]
			}				
		}				
	}
	oprtunityVal = repl1;
	localStorage.opProdID_Str=repl1;
}


/***********  medClickVal *********/

function medClickVal(pid, name){
	var inpVal = $("#inpId"+pid).val();
	
	if(inpVal!=0 && inpVal!=undefined){
		$("#medId"+pid).addClass('bgc');
		var inpVal = $("#inpId"+pid).val();
		if(inpVal==''||inpVal==undefined){
			inpVal=0;
		}
		var pConcat = pid+'|'+name+'|'+inpVal;
		
		if(oprtunityVal.indexOf(pid)==-1){
				if (oprtunityVal==''){
					oprtunityVal=pConcat
				}else{
					oprtunityVal+='||'+pConcat
				}
		}
	}
}

function medClickVal2(pid, name){
	var pConcat ="";	
	if (pid==0 && name==0 ){
		name=$("#medicine_new").val();				
		if (name!=""){
			pConcat = pid+'|'+name+'|'+1;
		}
		
	}else{
		name=name
		var inpVal = $("#inpId"+pid).val(1);
		$("#medId"+pid).addClass('bgc');
		pConcat = pid+'|'+name+'|'+1;
	}
	
	
	if (pid!=0){
		if(oprtunityVal.indexOf(pid)==-1){
			if (oprtunityVal==''){
				oprtunityVal=pConcat
			}else{
				oprtunityVal+='||'+pConcat
			}
		}
	}else{
		name=$("#medicine_new").val();				
		if (name!=""){
			if (oprtunityVal==''){
				oprtunityVal=pConcat
			}else{
				oprtunityVal+='||'+pConcat
			}
		}
		$("#medicine_new").val("");
	}
	
	createMedCart()
}

function medClick2(pid, name){
	var pConcat=""
	if (pid!=0 && name!=0){		
		$("#medId"+pid).addClass('bgc');
		//alert(localStorage.opProdID_Str);
		var inpVal = $("#inpId"+pid).val();
		if(inpVal==''||inpVal==undefined){
			inpVal=0;
		}
		pConcat = pid+'|'+name+'|'+inpVal;		
	}
	
	
	var campaign_doc_str=localStorage.opProdID_Str
	
	if (pid!=0){
		if(campaign_doc_str.indexOf(pid)==-1){
			if (campaign_doc_str==''){
				campaign_doc_str=pConcat
			}else{
				campaign_doc_str+='||'+pConcat
			}
		}
	}
	localStorage.opProdID_Str=campaign_doc_str;	
	
}



function createMedCart(){
		$('#opCart').empty();
		localStorage.opProdID_Str = oprtunityVal;
		campaign_doc_str=localStorage.opProdID_Str
		
		var campaignList = campaign_doc_str.split('||');
		var campaignListLength=campaignList.length;
		var medId='';
		var medName='';
		var medVal='';
		
		if (localStorage.opProdID_Str!=""){				
			op_cart_list='<table style="width:100%;">';
			op_cart_list+='<tr><td colspan="3" style="border-bottom:0px;"><h2 style="border-bottom:1px solid #d9d9d9;background-color:#ccedff; padding-left:5px; margin:0px;">Brand</h2></td></tr>';			
			op_cart_list+='<tr style="background-color:#99dbff; height:20px;"><td style="width:85%; padding-left:5px;">Name</td><td style="width:3px;"></td></tr>';	//<td style="width:10%; text-align:center;"></td>			
			for ( i=0; i < campaignListLength; i++){
				
				var pID=campaignList[i];
				var pIdSpilt = pID.split('|');				
				
				var medId = pIdSpilt[0];
				var medName = pIdSpilt[1];
				var medVal = pIdSpilt[2];
			
				if(medId==0){
					op_cart_list+='<tr style="background-color:#ccedff; height:20px;" id="cartOp_'+i+'"><td style="padding-left:5px;">'+medName+'<input id="inpId'+i+'" type="hidden" value="'+medName+'"/></td><td style="text-align:center;">&nbsp;<a onClick="removeCartNewItem(\''+i+'\');" style="font-size:15px; text-decoration:none; color:#cc3300" class="icon remove"></a></td></tr>';
				}else{						
					op_cart_list+='<tr style="background-color:#ccedff; height:20px;" id="cartOp_'+medId+'"><td style="padding-left:5px;">'+medName+'<input id="inpId'+medId+'" type="hidden" value="'+medVal+'"/></td><td style="text-align:center;">&nbsp;<a onClick="removeCarItemOp(\''+medId+'\');" style="font-size:15px; text-decoration:none; color:#cc3300" class="icon remove"></a></td></tr>'; //<img  src="cancel.png" width="20" height="20" alt="X" > //< td style="text-align:center;" ></td>
				}
				
			}
			
			op_cart_list+='</table>';
				
			//alert (op_cart_list)
			$('#opCart').empty();
			$('#opCart').html(op_cart_list);
		}
	
	
	}


function check_user() {	
	$("#error_login").text("").removeClass('success').removeClass('error');
	var cid=$("#cid").val().toUpperCase();
	cid=$.trim(cid);
	
	//Local
	var apipath_base_photo_dm ='http://w05.yeapps.com/hamdard/syncmobile_rx_seen_200101/dmpath?CID='+cid +'&HTTPPASS=e99business321cba'
	//var apipath_base_photo_dm ='http://a007.yeapps.com/skf/dmpath_live_new/get_path?CID='+cid +'&HTTPPASS=e99business321cba'	
    //var apipath_base_photo_dm ='http://e2.businesssolutionapps.com/welcome/dmpath_live_new_new/get_path?CID='+cid +'&HTTPPASS=e99business321cba'
	//online
	//var apipath_base_photo_dm ='http://w011.yeapps.com/dmpath/seen_rx/get_path_200101?CID='+cid +'&HTTPPASS=e99business321cba'
    //alert (apipath_base_photo_dm)	
	
	var user_id=$("#user_id").val();
	var user_pass=$("#user_pass").val();
	
	user_id=$.trim(user_id);
		
	if (user_id=="" || user_id==undefined || user_pass=="" || user_pass==undefined){
		var url = "#login";      
		$.mobile.navigate(url);
		$("#error_login").html("Required User ID and Password").removeClass('success').addClass('error');	
	}else{
			
		//alert(apipath_base_photo_dm);
		$("#loginButton").hide();
		$("#doctorButton").hide();
		$("#wait_image_login").show();
		$("#error_logintext").val(apipath_base_photo_dm);
		$.ajax(apipath_base_photo_dm,{
								// cid:localStorage.cid,rep_id:localStorage.user_id,rep_pass:localStorage.user_pass,synccode:localStorage.synccode,
			type: 'POST',
			timeout: 30000,
			error: function(xhr) {
			$("#wait_image_login").hide();
			$("#loginButton").show();
			$("#error_login").html('Network Timeout. Please check your Internet connection..').removeClass('success').addClass('error');
													},
			success:function(data, status,xhr){		
			if (status=='success'){
				localStorage.base_url='';
				//alert (data);
				var dtaStr=data.replace('<start>','').replace('<end>','')
				var resultArray = dtaStr.split('<fd>');					
					if(resultArray.length==4){
						var base_url=resultArray[0]; // base sync url 
						var photo_url=resultArray[1]; // application path http://a007.yeapps.com/ipi/
						var photo_submit_url=resultArray[2]; // image submission url
						var report_url=resultArray[3]; // report url
						localStorage.apipath =  photo_url + 'medSearch_seen_rx/';
						
						base_url = photo_url + 'syncmobile_rx_seen_200101/';
						
						//-------------
						if(base_url=='' || photo_url==''){	
							$("#wait_image_login").hide();
							$("#loginButton").show();
							//$("#doctorButton").show();
							$("#error_login").html('Base URL not available').removeClass('success').addClass('error');	
						}
						else{
							localStorage.base_url='';
							localStorage.app_url='';
							localStorage.photo_submit_url='';
							
//							--------------------------
							//alert (base_url);
							localStorage.base_url=base_url;
							localStorage.photo_url=photo_url;
							localStorage.photo_submit_url=photo_submit_url;
							localStorage.report_url=report_url;
							//alert (localStorage.base_url);
							
							localStorage.cid=cid;
							localStorage.user_id=user_id;
							localStorage.user_pass=user_pass;   		
							localStorage.synced_rx='NO';
							localStorage.picFlag=0;
							
														
							//alert (localStorage.base_url+'check_user_pharma?cid='+localStorage.cid+'&rep_id='+localStorage.user_id+'&rep_pass='+localStorage.user_pass+'&synccode='+localStorage.synccode+'&vNo='+vNo)
							$("#error_logintext").val(localStorage.base_url+'check_user_pharma?cid='+localStorage.cid+'&rep_id='+localStorage.user_id+'&rep_pass='+localStorage.user_pass+'&synccode='+localStorage.synccode+'&vNo='+vNo);
	
							$.ajax(localStorage.base_url+'check_user_pharma?cid='+localStorage.cid+'&rep_id='+localStorage.user_id+'&rep_pass='+localStorage.user_pass+'&synccode='+localStorage.synccode+'&vNo='+vNo,{
								
								type: 'POST',
								timeout: 30000,
								error: function(xhr) {								
								$("#wait_image_login").hide();
								$("#loginButton").show();
								$("#error_login").html('Network Timeout. Please check your Internet connection..').removeClass('success').addClass('error');
													},
								success:function(data, status,xhr){	
									 	var resultArray = data.replace('</START>','').replace('</END>','').split('<SYNCDATA>');	
										
										if (resultArray[0]=='FAILED'){
											$("#wait_image_login").hide();
											$("#loginButton").show();								
											$("#error_login").html(resultArray[1]).removeClass('success').addClass('error');
										}
										else if (resultArray[0]=='SUCCESS'){										
													localStorage.synccode=resultArray[1];
													localStorage.regionStr=resultArray[2];
													localStorage.areaStr=resultArray[3];
													localStorage.territoryStr=resultArray[4];
													localStorage.docCategoryStr=resultArray[5];
													localStorage.rxGpsStr=resultArray[6];
													localStorage.medStr=resultArray[7];
													localStorage.rxTypeStr=resultArray[8];
													
													localStorage.vNo=vNo;
													localStorage.synced_rx='YES';
													
													localStorage.docListStr="";
													localStorage.docStr="";
													localStorage.opProdID_Str ="";
													localStorage.doc_region='';
													localStorage.doc_area='';
													localStorage.doc_territory='';
													localStorage.searchSelect='';
													localStorage.doc_cart_list='';
													localStorage.docSelect='';
													
													$('#opCart').empty();
													$('#docCart').empty();
													$('#docSelect').empty();	
													$('#doctorList').empty();
																									
													clickCount=0;
													$(".vNo").text(localStorage.vNo);
													//$.afui.loadContent("#pageHome",true,true,'right');
													$.afui.loadContent("#page_PrescriptionCapture",true,true,'right');													

										  }//else failed
	
								}// success
							});	//Second Hit		
						}												
					}					
				}
		}
     
    });			
}		
}//Function

function page_PrescriptionCapture() {	
	//localStorage.doctor_pr=1;
//	localStorage.doctor_plan_flag=0
//	localStorage.doctor_flag=1
	//alert (localStorage.doctor_pr)
	/*localStorage.doctor_flag=1;
	localStorage.doctor_plan_flag=0;
	localStorage.doctor_pr=1;
	localStorage.tourFlag=0
	localStorage.saved_data_submit=0;*/
	clickCount=0;	
	$.afui.loadContent("#page_PrescriptionCapture",true,true,'right');
}

function page_notice() {
	$.afui.loadContent("#card",true,true,'right');
}

function ffPresent(){
	var ff_present=document.getElementById('ff_present').checked?1:0;
	localStorage.ff_present=ff_present;
	}

function associatedCall(){
	var associated_call=document.getElementById('associated_call').checked?1:0;
	localStorage.associated_call=associated_call;
	}

function associatedCallOthers(){
	var associated_call_others=document.getElementById('associated_call_others').checked?1:0;
	localStorage.associated_call_others=associated_call_others;
	}

function rxType(){
	var rx_type=$('#rx_type').val();
	localStorage.rx_type=rx_type;
	}
	
function prescription_submit(){
	$("#btn_prescription_submit").hide();
	$("#error_prescription_submit").html("").removeClass('error').removeClass('success');		
	$("#wait_image_prescription").show();
		
	if (localStorage.docStr	==undefined || localStorage.docStr	=="" ){
		$("#error_prescription_submit").text("Required Doctor.").removeClass('success').addClass('error');		
		$("#wait_image_prescription").hide();
		$("#btn_prescription_submit").show();
	}else{		
		if (localStorage.opProdID_Str==undefined || localStorage.opProdID_Str==""){
			$("#error_prescription_submit").text("Required Brand.").removeClass('success').addClass('error');		
			$("#wait_image_prescription").hide();
			$("#btn_prescription_submit").show();
		}else{
			if (localStorage.rx_type==undefined || localStorage.rx_type	=="" ){
				$("#error_prescription_submit").text("Required Rx Type.").removeClass('success').addClass('error');		
				$("#wait_image_prescription").hide();
				$("#btn_prescription_submit").show();
			}else{				
				clickCount+=1
				if(clickCount==1){
					var latitude=$("#lat").val();
					var longitude=$("#longitude").val();
					
					if (latitude==''){
						latitude=0
						}
					if (longitude==''){
						longitude=0
						}
					
					if (localStorage.rxGpsStr=="YES" && (latitude==0 && longitude==0)){	
						$("#wait_image_prescription").hide();		
						alert ("Please on your GPS")
					}else{		
						$("#btn_prescription_submit").hide();		
						
						var doctorId=localStorage.docStr.split('|')[0]	
						var doctor_name=localStorage.docStr.split('|')[1]		
						var areaId=localStorage.docStr.split('|')[3]
						
						
						
						var picNo = localStorage.picNo
						var imageDiv="myImage"+picNo
						var imageText="prPhoto"+picNo
						var prescriptionPhoto=$("#"+imageText).val();
						
						var capDateTime='';
						if (picNo==1){				
							capDateTime=localStorage.capTime1
						}else if(picNo==2){
							capDateTime=localStorage.capTime2
						}else if(picNo==3){
							capDateTime=localStorage.capTime3
						}else if(picNo==4){
							capDateTime=localStorage.capTime4
						}else if(picNo==5){
							capDateTime=localStorage.capTime5
						}else if(picNo==6){
							capDateTime=localStorage.capTime6
						}else if(picNo==7){
							capDateTime=localStorage.capTime7
						}else if(picNo==8){
							capDateTime=localStorage.capTime8
						}else if(picNo==9){
							capDateTime=localStorage.capTime9
						}else if(picNo==10){
							capDateTime=localStorage.capTime10
						}else if(picNo==11){
							capDateTime=localStorage.capTime11
						}else if(picNo==12){
							capDateTime=localStorage.capTime12
						}else if(picNo==13){
							capDateTime=localStorage.capTime13
						}else if(picNo==14){
							capDateTime=localStorage.capTime14
						}else if(picNo==15){
							capDateTime=localStorage.capTime15
						}else if(picNo==16){
							capDateTime=localStorage.capTime16
						}else if(picNo==17){
							capDateTime=localStorage.capTime17
						}else if(picNo==18){
							capDateTime=localStorage.capTime18
						}else if(picNo==19){
							capDateTime=localStorage.capTime19
						}else if(picNo==20){
							capDateTime=localStorage.capTime20
						}else if (picNo==21){
							capDateTime=localStorage.capTime21
						}else if(picNo==22){
							capDateTime=localStorage.capTime22
						}else if(picNo==23){
							capDateTime=localStorage.capTime23
						}else if(picNo==24){
							capDateTime=localStorage.capTime24
						}else if(picNo==25){
							capDateTime=localStorage.capTime25
						}else if(picNo==26){
							capDateTime=localStorage.capTime26
						}else if(picNo==27){
							capDateTime=localStorage.capTime27
						}else if(picNo==28){
							capDateTime=localStorage.capTime28
						}else if(picNo==29){
							capDateTime=localStorage.capTime29
						}else if(picNo==30){
							capDateTime=localStorage.capTime30
						}else if (picNo==31){
							capDateTime=localStorage.capTime31
						}else if(picNo==32){
							capDateTime=localStorage.capTime32
						}else if(picNo==33){
							capDateTime=localStorage.capTime33
						}else if(picNo==34){
							capDateTime=localStorage.capTime34
						}else if(picNo==35){
							capDateTime=localStorage.capTime35
						}else if(picNo==36){
							capDateTime=localStorage.capTime36
						}else if(picNo==37){
							capDateTime=localStorage.capTime37
						}else if(picNo==38){
							capDateTime=localStorage.capTime38
						}else if(picNo==39){
							capDateTime=localStorage.capTime39
						}else if(picNo==40){
							capDateTime=localStorage.capTime40
						}else if (picNo==41){
							capDateTime=localStorage.capTime41
						}else if(picNo==42){
							capDateTime=localStorage.capTime42
						}else if(picNo==43){
							capDateTime=localStorage.capTime43
						}else if(picNo==44){
							capDateTime=localStorage.capTime44
						}else if(picNo==45){
							capDateTime=localStorage.capTime45
						}else if(picNo==46){
							capDateTime=localStorage.capTime46
						}else if(picNo==47){
							capDateTime=localStorage.capTime47
						}else if(picNo==48){
							capDateTime=localStorage.capTime48
						}else if(picNo==49){
							capDateTime=localStorage.capTime49
						}else if(picNo==50){
							capDateTime=localStorage.capTime50
						}else if (picNo==51){
							capDateTime=localStorage.capTime51
						}else if(picNo==52){
							capDateTime=localStorage.capTime52
						}else if(picNo==53){
							capDateTime=localStorage.capTime53
						}else if(picNo==54){
							capDateTime=localStorage.capTime54
						}else if(picNo==55){
							capDateTime=localStorage.capTime55
						}else if(picNo==56){
							capDateTime=localStorage.capTime56
						}else if(picNo==57){
							capDateTime=localStorage.capTime57
						}else if(picNo==58){
							capDateTime=localStorage.capTime58
						}else if(picNo==59){
							capDateTime=localStorage.capTime59
						}else if(picNo==60){
							capDateTime=localStorage.capTime60	
						}
						
						if (capDateTime==undefined){capDateTime=''}
						
								
						var medicine_1="";//$("#medicine_1").val();
						var medicine_2="";//$("#medicine_2").val();
						var medicine_3="";//$("#medicine_3").val();
						var medicine_4="";//$("#medicine_4").val();
						
								
						var now = $.now();
						
						var imageName=localStorage.user_id+'_'+now.toString()+'.jpg';
								 
						//alert(localStorage.base_url+'prescription_submit?cid='+localStorage.cid+'&rep_id='+localStorage.user_id+'&rep_pass='+encodeURIComponent(localStorage.user_pass)+'&synccode='+localStorage.synccode+'&areaId='+areaId+'&doctor_id='+encodeURIComponent(doctorId)+'&doctor_name='+encodeURIComponent(doctor_name)+'&category='+localStorage.doc_category+'&latitude='+latitude+'&longitude='+longitude+'&pres_photo='+imageName+'&cap_time='+capDateTime+'&opProdID_Str='+localStorage.opProdID_Str+'&medicine_1='+medicine_1+'&medicine_2='+medicine_2+'&medicine_3='+medicine_3+'&medicine_4='+medicine_4+'&ff_present='+localStorage.ff_present+'&associated_call='+localStorage.associated_call+'&rx_type='+localStorage.rx_type)
						$("#errorShow").val(localStorage.base_url+'prescription_submit?cid='+localStorage.cid+'&rep_id='+localStorage.user_id+'&rep_pass='+encodeURIComponent(localStorage.user_pass)+'&synccode='+localStorage.synccode+'&areaId='+areaId+'&doctor_id='+encodeURIComponent(doctorId)+'&doctor_name='+encodeURIComponent(doctor_name)+'&category='+localStorage.doc_category+'&latitude='+latitude+'&longitude='+longitude+'&pres_photo='+imageName+'&cap_time='+capDateTime+'&opProdID_Str='+localStorage.opProdID_Str);
						 $.ajax(localStorage.base_url+'prescription_submit?cid='+localStorage.cid+'&rep_id='+localStorage.user_id+'&rep_pass='+encodeURIComponent(localStorage.user_pass)+'&synccode='+localStorage.synccode+'&areaId='+areaId+'&doctor_id='+encodeURIComponent(doctorId)+'&doctor_name='+encodeURIComponent(doctor_name)+'&category='+localStorage.doc_category+'&latitude='+latitude+'&longitude='+longitude+'&pres_photo='+imageName+'&cap_time='+capDateTime+'&opProdID_Str='+localStorage.opProdID_Str+'&ff_present='+localStorage.ff_present+'&associated_call='+localStorage.associated_call+'&associated_call_others='+localStorage.associated_call_others+'&rx_type='+localStorage.rx_type,{
								// cid:localStorage.cid,rep_id:localStorage.user_id,rep_pass:localStorage.user_pass,synccode:localStorage.synccode,
								type: 'POST',
								timeout: 30000,
								error: function(xhr) {							
											var resultArray = data.split('<SYNCDATA>');
											$("#error_prescription_submit").html(resultArray[1]);
											$("#wait_image_prescription").hide();
											$("#btn_prescription_submit").show();							
								},
							success:function(data, status,xhr){					
							if (status!='success'){				
								$("#error_prescription_submit").html('Network timeout. Please ensure you have active internet connection.').removeClass('success').addClass('error');
								$("#wait_image_prescription").hide();
								$("#btn_prescription_submit").show();
							}
							else{
								//alert (data)
								   var resultArray = data.split('<SYNCDATA>');	
									if (resultArray[0]=='FAILED'){						
										$("#error_prescription_submit").html(resultArray[1]);
										$("#wait_image_prescription").hide();
										$("#btn_prescription_submit").show();
									}else if (resultArray[0]=='SUCCESS'){
										
										localStorage.opProdID_Str='';
										localStorage.prProdID_Str='';
										oprtunityVal='';
										optionVal='';
										
										clickCount=0							
										uploadPhoto(prescriptionPhoto, imageName);
										
																
										imageSource=''
										var image = document.getElementById(imageDiv);
										image.src = imageSource;
										imagePath = imageSource;
										$("#"+imageText).val(imagePath);
										
										
										if (picNo==1){localStorage.prPhoto1=''}
										if (picNo==2){localStorage.prPhoto2=''}
										if (picNo==3){localStorage.prPhoto3=''}
										if (picNo==4){localStorage.prPhoto4=''}
										if (picNo==5){localStorage.prPhoto5=''}
										if (picNo==6){localStorage.prPhoto6=''}
										if (picNo==7){localStorage.prPhoto7=''}
										if (picNo==8){localStorage.prPhoto8=''}
										if (picNo==9){localStorage.prPhoto9=''}
										if (picNo==10){localStorage.prPhoto10=''}
										if (picNo==11){localStorage.prPhoto11=''}
										if (picNo==12){localStorage.prPhoto12=''}
										if (picNo==13){localStorage.prPhoto13=''}
										if (picNo==14){localStorage.prPhoto14=''}
										if (picNo==15){localStorage.prPhoto15=''}
										if (picNo==16){localStorage.prPhoto16=''}
										if (picNo==17){localStorage.prPhoto17=''}
										if (picNo==18){localStorage.prPhoto18=''}
										if (picNo==19){localStorage.prPhoto19=''}
										if (picNo==20){localStorage.prPhoto20=''}
										if (picNo==21){localStorage.prPhoto21=''}
										if (picNo==22){localStorage.prPhoto22=''}
										if (picNo==23){localStorage.prPhoto23=''}
										if (picNo==24){localStorage.prPhoto24=''}
										if (picNo==25){localStorage.prPhoto25=''}
										if (picNo==26){localStorage.prPhoto26=''}
										if (picNo==27){localStorage.prPhoto27=''}
										if (picNo==28){localStorage.prPhoto28=''}
										if (picNo==29){localStorage.prPhoto29=''}
										if (picNo==30){localStorage.prPhoto30=''}
										if (picNo==31){localStorage.prPhoto31=''}
										if (picNo==32){localStorage.prPhoto32=''}
										if (picNo==33){localStorage.prPhoto33=''}
										if (picNo==34){localStorage.prPhoto34=''}
										if (picNo==35){localStorage.prPhoto35=''}
										if (picNo==36){localStorage.prPhoto36=''}
										if (picNo==37){localStorage.prPhoto37=''}
										if (picNo==38){localStorage.prPhoto38=''}
										if (picNo==39){localStorage.prPhoto39=''}
										if (picNo==40){localStorage.prPhoto40=''}
										if (picNo==41){localStorage.prPhoto41=''}
										if (picNo==42){localStorage.prPhoto42=''}
										if (picNo==43){localStorage.prPhoto43=''}
										if (picNo==44){localStorage.prPhoto44=''}
										if (picNo==45){localStorage.prPhoto45=''}
										if (picNo==46){localStorage.prPhoto46=''}
										if (picNo==47){localStorage.prPhoto47=''}
										if (picNo==48){localStorage.prPhoto48=''}
										if (picNo==49){localStorage.prPhoto49=''}
										if (picNo==50){localStorage.prPhoto50=''}
										if (picNo==51){localStorage.prPhoto51=''}
										if (picNo==52){localStorage.prPhoto52=''}
										if (picNo==53){localStorage.prPhoto53=''}
										if (picNo==54){localStorage.prPhoto54=''}
										if (picNo==55){localStorage.prPhoto55=''}
										if (picNo==56){localStorage.prPhoto56=''}
										if (picNo==57){localStorage.prPhoto57=''}
										if (picNo==58){localStorage.prPhoto58=''}
										if (picNo==59){localStorage.prPhoto59=''}
										if (picNo==60){localStorage.prPhoto60=''}
				
				
										$("#lat").val("");
										$("#long").val("");
										$("#medicine_1").val('');
										$("#medicine_2").val('');
										$("#medicine_3").val('');
										$("#medicine_4").val('');
										$("#medicine_5").val('');
										$("#wait_image_prescription").hide();
										$("#btn_prescription_submit").hide();
										
										
										$('#medicineList').empty();
										$('#doctorList').empty();
										$("#docCart").empty();						
										$("#opCart").empty();
										$("#docSelect").empty();
				
										//--------------------------
										//$("#error_prescription_submit").text("Uploading.").addClass('success');	
										//$.afui.loadContent("#imageSinglePage",true,true,'right');
										
									}else{						
										$("#error_prescription_submit").html('Authentication error. Please register and sync to retry.').removeClass('success').addClass('error');
										$("#wait_image_prescription").hide();
										$("#btn_prescription_submit").show();
										}
								}
							}
						});		
					
						$("#wait_image_prescription").hide();
						$("#btn_prescription_submit").show();				
				//		}pic else
					}
				}
			}
		}
	}
//$.afui.loadContent("#page_confirm_visit_success",true,true,'right');
}



function uploadPhoto(imageURI, imageName) {
	$("#btn_prescription_submit").hide();
	$("#error_prescription_submit").text("Image Sync...").removeClass('error').addClass('success');
	
	var options = new FileUploadOptions();
    options.fileKey="upload";
    options.fileName=imageName;
    options.mimeType="image/jpeg";
	
    var params = {};
    params.value1 = "test";
    params.value2 = "param";
	
    options.params = params;
	options.chunkedMode = false;
	
    var ft = new FileTransfer();
     ft.upload(imageURI, encodeURI(localStorage.photo_submit_url),winPr,failPr,options);	
		
}

function winPr(r) {
	$("#error_prescription_submit").text("Submitted Succesfully.").removeClass('error').addClass('success');
	$("#myImagePrescription_show").val('')
	$("#btn_prescription_submit").hide();
}

function failPr(error) {
	$("#error_prescription_submit").text('Memory Error. Please take new picture and Submit').removeClass('success').addClass('error');
	$("#btn_prescription_submit").show();	
}


function takePicture(){
	navigator.camera.getPicture( cameraSuccess, cameraError, {
		quality: 95,
		targetWidth: 400,
       // destinationType: Camera.DestinationType.FILE_URI,
		destinationType: Camera.DestinationType.FILE_URI,correctOrientation: true ,
        correctOrientation: true,
        saveToPhotoAlbum: true
    });
}

function cameraSuccess(uri){  
	var picNo=parseInt(localStorage.picFlag)+1 
	var imageDiv="myImage"+picNo
	var imageText="prPhoto"+picNo
	localStorage.picFlag=picNo
	var image = document.getElementById(imageDiv);
	image.src = uri;
	imagePath = uri;
	
	
	var currentDate = new Date();
	var day = currentDate.getDate();if(parseInt(day)<9)	{day="0" + day};
	var month = currentDate.getMonth() + 1;if(parseInt(month)<9){month="0" +month};
	var year = currentDate.getFullYear();
	var hours = currentDate.getHours();
	var miniutes = currentDate.getMinutes();
	var seconds = currentDate.getSeconds();
	
	var currentDateTime=year+"-"+month+"-"+day+" "+hours+":"+miniutes+":"+seconds
		
	
	if (picNo==1){localStorage.prPhoto1=uri;localStorage.capTime1=currentDateTime}
	if (picNo==2){localStorage.prPhoto2=uri;localStorage.capTime2=currentDateTime}
	if (picNo==3){localStorage.prPhoto3=uri;localStorage.capTime3=currentDateTime}
	if (picNo==4){localStorage.prPhoto4=uri;localStorage.capTime4=currentDateTime}
	if (picNo==5){localStorage.prPhoto5=uri;localStorage.capTime5=currentDateTime}
	if (picNo==6){localStorage.prPhoto6=uri;localStorage.capTime6=currentDateTime}
	if (picNo==7){localStorage.prPhoto7=uri;localStorage.capTime7=currentDateTime}
	if (picNo==8){localStorage.prPhoto8=uri;localStorage.capTime8=currentDateTime}
	if (picNo==9){localStorage.prPhoto9=uri;localStorage.capTime9=currentDateTime}
	if (picNo==10){localStorage.prPhoto10=uri;localStorage.capTime10=currentDateTime}
	if (picNo==11){localStorage.prPhoto11=uri;localStorage.capTime11=currentDateTime}
	if (picNo==12){localStorage.prPhoto12=uri;localStorage.capTime12=currentDateTime}
	if (picNo==13){localStorage.prPhoto13=uri;localStorage.capTime13=currentDateTime}
	if (picNo==14){localStorage.prPhoto14=uri;localStorage.capTime14=currentDateTime}
	if (picNo==15){localStorage.prPhoto15=uri;localStorage.capTime15=currentDateTime}
	if (picNo==16){localStorage.prPhoto16=uri;localStorage.capTime16=currentDateTime}
	if (picNo==17){localStorage.prPhoto17=uri;localStorage.capTime17=currentDateTime}
	if (picNo==18){localStorage.prPhoto18=uri;localStorage.capTime18=currentDateTime}
	if (picNo==19){localStorage.prPhoto19=uri;localStorage.capTime19=currentDateTime}
	if (picNo==20){localStorage.prPhoto20=uri;localStorage.capTime20=currentDateTime}
	if (picNo==21){localStorage.prPhoto21=uri;localStorage.capTime21=currentDateTime}
	if (picNo==22){localStorage.prPhoto22=uri;localStorage.capTime22=currentDateTime}
	if (picNo==23){localStorage.prPhoto23=uri;localStorage.capTime23=currentDateTime}
	if (picNo==24){localStorage.prPhoto24=uri;localStorage.capTime24=currentDateTime}
	if (picNo==25){localStorage.prPhoto25=uri;localStorage.capTime25=currentDateTime}
	if (picNo==26){localStorage.prPhoto26=uri;localStorage.capTime26=currentDateTime}
	if (picNo==27){localStorage.prPhoto27=uri;localStorage.capTime27=currentDateTime}
	if (picNo==28){localStorage.prPhoto28=uri;localStorage.capTime28=currentDateTime}
	if (picNo==29){localStorage.prPhoto29=uri;localStorage.capTime29=currentDateTime}
    if (picNo==30){localStorage.prPhoto30=uri;localStorage.capTime30=currentDateTime}
    if (picNo==31){localStorage.prPhoto31=uri;localStorage.capTime31=currentDateTime}
    if (picNo==32){localStorage.prPhoto32=uri;localStorage.capTime32=currentDateTime}
    if (picNo==33){localStorage.prPhoto33=uri;localStorage.capTime33=currentDateTime}
    if (picNo==34){localStorage.prPhoto34=uri;localStorage.capTime34=currentDateTime}
    if (picNo==35){localStorage.prPhoto35=uri;localStorage.capTime35=currentDateTime}
    if (picNo==36){localStorage.prPhoto36=uri;localStorage.capTime36=currentDateTime}
    if (picNo==37){localStorage.prPhoto37=uri;localStorage.capTime37=currentDateTime}
    if (picNo==38){localStorage.prPhoto38=uri;localStorage.capTime38=currentDateTime}
    if (picNo==39){localStorage.prPhoto39=uri;localStorage.capTime39=currentDateTime}
    if (picNo==40){localStorage.prPhoto40=uri;localStorage.capTime40=currentDateTime}
    if (picNo==41){localStorage.prPhoto41=uri;localStorage.capTime41=currentDateTime}
    if (picNo==42){localStorage.prPhoto42=uri;localStorage.capTime42=currentDateTime}
    if (picNo==43){localStorage.prPhoto43=uri;localStorage.capTime43=currentDateTime}
    if (picNo==44){localStorage.prPhoto44=uri;localStorage.capTime44=currentDateTime}
    if (picNo==45){localStorage.prPhoto45=uri;localStorage.capTime45=currentDateTime}
    if (picNo==46){localStorage.prPhoto46=uri;localStorage.capTime46=currentDateTime}
    if (picNo==47){localStorage.prPhoto47=uri;localStorage.capTime47=currentDateTime}
    if (picNo==48){localStorage.prPhoto48=uri;localStorage.capTime48=currentDateTime}
    if (picNo==49){localStorage.prPhoto49=uri;localStorage.capTime49=currentDateTime}
    if (picNo==50){localStorage.prPhoto50=uri;localStorage.capTime50=currentDateTime}
    if (picNo==51){localStorage.prPhoto51=uri;localStorage.capTime51=currentDateTime}
    if (picNo==52){localStorage.prPhoto52=uri;localStorage.capTime52=currentDateTime}
    if (picNo==53){localStorage.prPhoto53=uri;localStorage.capTime53=currentDateTime}
    if (picNo==54){localStorage.prPhoto54=uri;localStorage.capTime54=currentDateTime}
    if (picNo==55){localStorage.prPhoto55=uri;localStorage.capTime55=currentDateTime}
    if (picNo==56){localStorage.prPhoto56=uri;localStorage.capTime56=currentDateTime}
    if (picNo==57){localStorage.prPhoto57=uri;localStorage.capTime57=currentDateTime}
    if (picNo==58){localStorage.prPhoto58=uri;localStorage.capTime58=currentDateTime}
    if (picNo==59){localStorage.prPhoto59=uri;localStorage.capTime59=currentDateTime}
    if (picNo==60){localStorage.prPhoto60=uri;localStorage.capTime60=currentDateTime}

		
	takePicture();
	
    $("#"+imageText).val(imagePath);    
}

function cameraError(message){
	var a=''
    //alert("Canceled!"); 
	
}


$('#ThumbnailTest_buttonTakePhotosNow').click(function(){
    takePicture();
});


function exit() {	
	navigator.app.exitApp();
}


//======================== report==========

function page_report(){
	$("#wait_image_daily_summary").hide();
	$("#error_summary_rpt").text("").removeClass('success').removeClass('error');
		
	$.afui.loadContent("#page_report",true,true,'right');
}

function summaryDaily(){
	$("#error_summary_rpt").text("").removeClass('success').removeClass('error');
	$('#summaryRpt').empty();
	$("#wait_image_daily_summary").show();
	
	var from_date = $("#from_date").val();	
	
	//alert(localStorage.base_url+'summary_daily?cid='+localStorage.cid+'&rep_id='+localStorage.user_id+'&rep_pass='+encodeURIComponent(localStorage.user_pass)+'&from_date='+from_date);
	$.ajax({
		  url: localStorage.base_url+'summary_daily?cid='+localStorage.cid+'&rep_id='+localStorage.user_id+'&rep_pass='+encodeURIComponent(localStorage.user_pass)+'&from_date='+from_date,
		  success: function(resStr) {
			if (resStr!=""){					
				var summaryDailyStr=resStr.split("||");
				var summaryDailyLen=summaryDailyStr.length;
				 
				 if (from_date==''){
					from_date='Today';	 
				 }
				 
				rpt_daily_list='<table style="width:100%;">';
				rpt_daily_list+='<tr><td colspan="3" style="border-bottom:0px;"><h2 style="border-bottom:1px solid #d9d9d9;background-color:#ccedff; padding-left:5px; margin:0px;">Date: &nbsp;'+from_date+'</h2></td></tr>';			
				rpt_daily_list+='<tr style="background-color:#99dbff; height:20px;"><td style="width:40%; padding-left:5px;">Territory</td><td style="width:40%; text-align:left;">Doctor Name</td><td style="width:3px; text-align:center;">Count</td></tr>';				
				var prtDailyTotal=0;
				for ( i=0; i < summaryDailyLen; i++){						
					var summaryDailyS=summaryDailyStr[i];
					var rptDailyStr = summaryDailyS.split('|');												
					
					prtDailyTotal+=parseInt(rptDailyStr[2]);
									
					rpt_daily_list+='<tr style="background-color:#ccedff; height:20px;" ><td style="padding-left:5px;">'+rptDailyStr[0]+'</td><td style="text-align:left;" >'+rptDailyStr[1]+'</td><td style="text-align:center;">'+rptDailyStr[2]+'</td></tr>';
							
				}
				rpt_daily_list+='<tr style="background-color:#99dbff; height:20px; font-weight:bold;" ><td style="padding-left:5px;"></td><td style="text-align:right;" >Total</td><td style="text-align:center;">'+prtDailyTotal+'</td></tr>'
				rpt_daily_list+='</table>';
				
				
				$('#summaryRpt').empty();
				$('#summaryRpt').html(rpt_daily_list);
				
			}else{				
				$("#error_summary_rpt").text("Data Not Available.").removeClass('success').addClass('error');
			}
			$("#wait_image_daily_summary").hide();		
		  }		
	});	
}

//======================== report==========

function getNotice(){
	$('#notice_list').empty();
	$("#wait_image_notice").show();
	//alert(localStorage.base_url+'notice_list?cid='+localStorage.cid+'&rep_id='+localStorage.user_id+'&rep_pass='+encodeURIComponent(localStorage.user_pass));
	$.ajax({
		  url: localStorage.base_url+'notice_list?cid='+localStorage.cid+'&rep_id='+localStorage.user_id+'&rep_pass='+encodeURIComponent(localStorage.user_pass),
		  success: function(resStr) {
			if (resStr!=""){					
				var noticeStr=resStr.split("||");
				var noticeLen=noticeStr.length;
				var notice_list_str='';
				for ( i=0; i < noticeLen; i++){						
					var noticeS=noticeStr[i];
					var noticeSArr = noticeS.split('|');	
					notice_list_str+='<div style="background-color:#e6fff9; border-bottom:1px solid #00cc99; margin:3px; border-radius:5px; padding:5px;">';		  
					notice_list_str+='<h2 >'+noticeSArr[0]+'</h2>';	  
					notice_list_str+='<p style="margin:0px; font-size:11px; line-height:normal;">'+noticeSArr[1]+'</p>';  
					notice_list_str+='</div>';				
				}
				
				$("#wait_image_notice").hide();
				$('#notice_list').empty();
				$('#notice_list').html(notice_list_str);							
				
			}else{	
				$("#wait_image_notice").hide();			
				$("#error_notice_list").text("Data Not Available.").removeClass('success').addClass('error');
			}
					
		  }		
	});	
}

function page_report_link(){	
	window.location.href=localStorage.report_url+'report_seen_rx_mobile/index?cid='+localStorage.cid+'&rep_id='+localStorage.user_id+'&rep_pass='+encodeURIComponent(localStorage.user_pass)
	
	}
	

function pharma_project(){
	window.open("index.html", "_self");
}