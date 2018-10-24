$(function() {
    $("#companiesList").autocomplete({
    	source: "{% url 'polls:autocomplete_companyData' %}",
    });
});