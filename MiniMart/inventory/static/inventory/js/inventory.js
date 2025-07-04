$(document).ready(function () {
    // --- Hide and Show Form ---
    $('#add_product').click(function (e){
        $('#add_p_form').slideToggle();
        const text = $(this).text();
        $(this).text(text === '➕Add Items'? '➖Hide Form':'➕Add Items')
    });

    // --- Form Submit ---
    $('#submit').click(function (e){
        e.preventDefault();
        let isValid = true;
        $("#form_data :input[required]").each(function () {
            if (!$(this).val().trim()) {
                isValid = false;
                $(this).css("border", "1px solid red");
            } else {
                $(this).css("border", "");
            }
        });
        if (!isValid) {
            alert("Please fill in all required fields.");
            return;
        }
        $.ajax({
            type: 'POST',
            url: "/inventory/add/",
            data:$('#form_data').serialize(),
            success: function(response){
                alert(response.success)
                $('.add_update').prepend(response.row_html)
                $("#form_data")[0].reset();
            },
            error: function(xhr){
                const err = JSON.parse(xhr.responseText);
                alert(err.message || 'Something went wrong' + xhr.status, xhr.readyState)
            }
        })
    });

    // --- Delete Button ---
    $(document).on('click','.delete-btn',function(e){
        e.preventDefault();
        const pId = $(this).data('id')
        if (!confirm('Are you sure you want to delete this item?')) {
            return;
        }
        $.ajax({
            type: 'POST',
            url: `/inventory/delete/${pId}/`,
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {
                alert(response.success || 'Item deleted successfully');
                $(`#delete-${pId}`).closest('tr').remove();
            },
            error: function(xhr) {
                const err = JSON.parse(xhr.responseText);
                alert(err.message || 'Failed to delete item');
            }
        });
    });

    // --- Edit Button ---
    $(document).on('click', '.edit-btn', function(e){
        e.preventDefault();
        let id = $(this).data('id');
        let row = $(this).closest('tr');
        let name = row.find('.name').text();
        let category = row.find('.category').text();
        let stock = row.find('.stock').text();
        let cost_price = row.find('.cost_price').text();
        let selling_price = row.find('.selling_price').text();
        row.find('.name').html(`<input type="text" class="form-control" value="${name}" id="id_name">`);
        row.find('.category').html(`<input type="text" class="form-control" value="${category}" id="id_category">`);
        row.find('.stock').html(`<input type="number" class="form-control" value="${stock}" id="id_stock">`);
        row.find('.cost_price').html(`<input type="number" class="form-control" value="${cost_price}" id="id_cost_price">`);
        row.find('.selling_price').html(`<input type="number" class="form-control" value="${selling_price}" id="id_selling_price">`);
        row.find('.action').html(`<button class="save-btn" data-id="${id}">Save</button> <button class="cancel-btn" data-id="${id}">Cancel</button>`);
    });

    // --- Save Button ---
    $(document).on('click', '.save-btn', function(e){
        e.preventDefault();
        let id = $(this).data('id');
        let row = $(this).closest('tr');
        let name = row.find('#id_name').val();
        let category = row.find('#id_category').val();
        let stock = row.find('#id_stock').val();
        let cost_price = row.find('#id_cost_price').val();
        let selling_price = row.find('#id_selling_price').val();
        $.ajax({
            type: 'POST',
            url: `/inventory/update/${id}/`,
            headers: {
                'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            data: {
                name: name,
                category: category,
                stock: stock,
                cost_price: cost_price,
                selling_price: selling_price
            },
            success: function(response) {
                alert(response.success || 'Item updated successfully');
                row.find('.name').text(name);
                row.find('.category').text(category);
                row.find('.stock').text(stock);
                row.find('.cost_price').text(parseFloat(cost_price).toFixed(2));
                row.find('.selling_price').text(parseFloat(selling_price).toFixed(2));
                row.find('.action').html(`<button class="edit-btn" id="edit-${id}" data-id="${id}">Edit</button> <button class="delete-btn" id="delete-${id}" data-id="${id}">Delete</button>`);
            },
            error: function(xhr) {
                const err = JSON.parse(xhr.responseText);
                alert(err.message || 'Failed to update item');
            }
        });
    });

});

// multi form or dynamic form
$(document).ready(function () {
  // Show form
  $('#show-multi-form').click(function () {
    $('#multi-form-container').slideToggle();
  });

  // Add new form
  $('#add-more').click(function () {
    const form = `
      <div class="product-form">
        <input type="text" name="name" placeholder="Name" required>
        <input type="text" name="category" placeholder="Category" required>
        <input type="number" name="stock" placeholder="Stock" required>
        <input type="number" name="cost_price" placeholder="Cost Price" required>
        <input type="number" name="selling_price" placeholder="Selling Price" required>
        <button class="remove-form">Remove</button>
      </div>`;
    $('#form-wrapper').append(form);
  });

  // Remove form
  $(document).on('click', '.remove-form', function (e) {
    e.preventDefault();
    $(this).closest('.product-form').remove();
  });

  // Save all forms
  $('#save-multiple').click(function () {
    const products = [];

    $('.product-form').each(function () {
      const name = $(this).find('input[name="name"]').val();
      const category = $(this).find('input[name="category"]').val();
      const stock = $(this).find('input[name="stock"]').val();
      const cost = $(this).find('input[name="cost_price"]').val();
      const selling = $(this).find('input[name="selling_price"]').val();

      products.push({ name, category, stock: parseInt(stock), cost_price: parseFloat(cost), selling_price: parseFloat(selling) });
    });

    $.ajax({
      url: '/inventory/multi_add/',
      method: 'POST',
      headers: {
        'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
      },
      contentType: 'application/json',
      data: JSON.stringify({ products }),
      success: function (response) {
        alert(response.success || "Products added successfully!");
        location.reload();
      },
      error: function (xhr) {
        const err = xhr.responseJSON || {};
        alert(err.message || "Error adding products.");
      }
    });
  });
});
