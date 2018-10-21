 
  $( function() {
    $( "#companiesList" ).autocomplete({
      source: "{% url 'polls:company_autocomplete' %}"
    });
  });
 
