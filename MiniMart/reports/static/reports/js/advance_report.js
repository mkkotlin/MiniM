$(document).ready(function() {

    
    $('#category-filter').on('change', function(){
        alert($('#category-filter').val())
        $.ajax({
            url: '/reports/get_product_category/' + $('#category-filter').val() + '/',
            success: function(data) {
                // console.log(data.products);
                $('.product-list-filtered').empty();
                data.products.forEach(function(product) {
                    $('.product-list-filtered').append('<p>' + product.name + ' - ' + product.selling_price + ' - ' + product.stock + '</p>');
                });
            }
        });
    })

    $('#product-filter').on('change', function(){
        alert($('#product-filter').val())
        $.ajax({
            url: '/reports/get_product_name/' + $('#product-filter').val() + '/',
            success: function(data) {
                // console.log(data.products);
                $('.product-list-filtered').empty();
                data.products.forEach(function(product) {
                    $('.product-list-filtered').append('<p>' + product.name + ' - ' + product.selling_price + ' - ' + product.stock + '</p>');
                });
            }
        });
    })

    $('#to-date-filter').on('change', function(){
        var fromDate = $('#from-date-filter').val();
        var toDate = $('#to-date-filter').val();
        alert(fromDate + ' ' + toDate);
        $.ajax({
            url: '/reports/get_product_date/' + fromDate + '/' + toDate + '/',
            success: function(data) {
                $('.product-list-filtered').empty();
                data.products.forEach(function(product) {
                    $('.product-list-filtered').append('<p>' + product.name + ' - ' + product.selling_price + ' - ' + product.stock + ' - ' + product.created_at + '</p>');
                });
            }
        });
    })

    $('#clear-filters').on('click', function() {
        $('#category-filter').val('');
        $('#product-filter').val('');
        $('#from-date-filter').val('');
        $('#to-date-filter').val('');
        $('.product-list-filtered').empty();
         $.ajax({
        url: '/reports/get_product_all/',
        success: function(data) {
            // console.log(data.products);
            data.products.forEach(function(product) {
                $('.product-list-filtered').append('<p>' + product.name + ' - ' + product.selling_price + ' - ' + product.stock + '</p>');
            });
        }
    });
    });
   





});