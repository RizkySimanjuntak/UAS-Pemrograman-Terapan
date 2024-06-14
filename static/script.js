$(document).ready(function() {
    $('#searchButton').click(function() {
        var searchText = $('#searchInput').val().toLowerCase();
        
        $('#dataTable tbody tr').each(function() {
            var found = false;
            $(this).find('td').each(function() {
                if ($(this).text().toLowerCase().includes(searchText)) {
                    found = true;
                    return false; 
                }
            });
            if (found) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });

    $('#searchInput').on('input', function() {
        var searchText = $(this).val().toLowerCase();
        
        $('#dataTable tbody tr').each(function() {
            var found = false;
            $(this).find('td').each(function() {
                if ($(this).text().toLowerCase().includes(searchText)) {
                    found = true;
                    return false; 
                }
            });
            if (found) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });
});