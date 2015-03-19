// last updated 2015-03-19 toby
// file for all of the javascript logic for crowdflower

require(['jquery-noconflict', 'bootstrap-modal', 'bootstrap-tooltip', 'bootstrap-popover', 'jquery-cookie'], function($) {
	Window.implement('$', function(el, nc) {
		return document.id(el, nc, this.document);
	});

	var $ = window.jQuery;

	$("#toggle_background").click(function(){
		$("#background_info").toggle();
	});

	$("#toggle_gene_def").click(function(){
		$("#gene_definitions").toggle();
	});

	$("#toggle_gene_var_def").click(function(){
		$("#gene_var_definitions").toggle();
	});

	$("#toggle_chemical_def").click(function(){
		$("#chemical_definitions").toggle();
	});

	$("#toggle_disease_def").click(function(){
		$("#disease_definitions").toggle();
	});
});
