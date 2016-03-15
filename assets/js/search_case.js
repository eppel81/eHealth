$.expr[":"].contains = $.expr.createPseudo(function (arg) {
    return function (elem) {
        return $(elem).text().toUpperCase().indexOf(arg.toUpperCase()) >= 0;
    };
});


$('#id_form_search_case').on('submit', function () {
    var searchPhrase = $("#id_search_case").val();
    var allCases = $('tr.case-item');

    if (searchPhrase) {
        allCases.hide();
        var successfulCases = $("td.case-item-search:contains('" + searchPhrase + "')").parent();
        successfulCases.show();
    } else {
        allCases.show();

    }
    return false;
});

