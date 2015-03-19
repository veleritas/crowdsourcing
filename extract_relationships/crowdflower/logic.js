// last updated 2015-03-19 toby
// file for all of the javascript logic for crowdflower

require(['jquery-noconflict', 'bootstrap-modal', 'bootstrap-tooltip', 'bootstrap-popover', 'jquery-cookie'], function($) {
	Window.implement('$', function(el, nc) {
		return document.id(el, nc, this.document);
	});

	var $ = window.jQuery;

	$("#toggle_background").click(function(){
		$("#background_info").toggle();
		if ($("#background_info").is(":visible"))
			$("#toggle_background").html("Hide background information");
		else
			$("#toggle_background").html("Show background information");
	});

	$("#toggle_gene_def").click(function(){
		$("#gene_definitions").toggle();
		if ($("#gene_definitions").is(":visible"))
			$("#toggle_gene_def").html("Hide gene or protein definition");
		else
			$("#toggle_gene_def").html("Show gene or protein definition");
	});

	$("#toggle_gene_var_def").click(function(){
		$("#gene_var_definitions").toggle();
		if ($("#gene_var_definitions").is(":visible"))
			$("#toggle_gene_var_def").html("Hide gene variant definition");
		else
			$("#toggle_gene_var_def").html("Show gene variant definition");
	});

	$("#toggle_chemical_def").click(function(){
		$("#chemical_definitions").toggle();
		if ($("#chemical_definitions").is(":visible"))
			$("#toggle_chemical_def").html("Hide drug definition");
		else
			$("#toggle_chemical_def").html("Show drug definition");
	});

	$("#toggle_disease_def").click(function(){
		$("#disease_definitions").toggle();
		if ($("#disease_definitions").is(":visible"))
			$("#toggle_disease_def").html("Hide disease definition");
		else
			$("#toggle_disease_def").html("Show disease definition");
	});
});
