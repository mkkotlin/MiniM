$(document).ready(function() {

    function renderProductList(products) {
        let gridContent = '<div class="inventory-grid">';
        products.forEach(function(product) {
            const formattedDate = new Date(product.created_at).toLocaleDateString('en-US', {
                year: 'numeric', month: 'long', day: 'numeric'
            });
            const formattedTime = new Date(product.created_at).toLocaleTimeString('en-US', {
                hour: '2-digit', minute: '2-digit', hour12: true, timeZone: 'UTC'
            });

            gridContent += `
                <div class="inventory-card">
                    <div class="top-row">
                        <span class="item-name">${product.name}</span>
                        <span class="category">${product.category}</span>
                    </div>
                    <div class="stock-row">
                        <strong>Stock:</strong> ${product.stock}
                    </div>
                    <div class="price-row">
                        <span><strong>Cost:</strong> ₹${product.cost_price}</span>
                        <span><strong>Sell Price:</strong> ₹${product.selling_price}</span>
                    </div>
                    <div class="date-row">
                        <span>${formattedDate} &bull; ${formattedTime}</span>
                    </div>
                </div>
            `;
        });
        gridContent += '</div>';
        $('.product-list-filtered').html(gridContent);
    }

    $('#category-filter').on('change', function() {
        const val = $(this).val();
        $.ajax({
            url: '/reports/get_product_category/' + val + '/',
            success: function(data) {
                renderProductList(data.products);
            }
        });
    });

    $('#product-filter').on('change', function() {
        const val = $(this).val();
        $.ajax({
            url: '/reports/get_product_name/' + val + '/',
            success: function(data) {
                renderProductList(data.products);
            }
        });
    });

    $('#to-date-filter').on('change', function() {
        const fromDate = $('#from-date-filter').val();
        const toDate = $('#to-date-filter').val();
        $.ajax({
            url: '/reports/get_product_date/' + fromDate + '/' + toDate + '/',
            success: function(data) {
                renderProductList(data.products);
            }
        });
    });

    $('#clear-filters').on('click', function() {
        $('#category-filter').val('');
        $('#product-filter').val('');
        $('#from-date-filter').val('');
        $('#to-date-filter').val('');
        $.ajax({
            url: '/reports/get_product_all/',
            success: function(data) {
                renderProductList(data.products);
            }
        });
    });

});