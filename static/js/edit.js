$(document).ready(function(){

$(".del-button").click(function() {
	entity = $(this).find(".entity").html();
	$("#delete-modal input[name=entity]").val(entity);
});

$(".fav-button").click(function() {
	entity = $(this).find(".entity").html();
	$("#fav-modal input[name=entity]").val(entity);
});

});