$(document).ready(function () {
    //strat of hide and show
    $('#add_product').click(function (e){
    $('#add_p_form').slideToggle(); //hide and show

    const text = $(this).text();
    $(this).text(text === '➕Add Items'? '➖Hide Form':'➕Add Items')
    });
    //end of hide and show

    // start of form submit
    $('#submit').click(function (e){
        e.preventDefault();


            let isValid = true;

        // Loop through all input fields inside the form
        $("#form_data :input[required]").each(function () {
        if (!$(this).val().trim()) {
            isValid = false;
            $(this).css("border", "1px solid red"); // Optional: visual cue
        } else {
            $(this).css("border", ""); // Reset if filled
        }
        });

        if (!isValid) {
        alert("Please fill in all required fields.");
        return;
        }
        
        $.ajax({
            type: 'POST',
            url: "/inventory/add/",
            data:$('#form_data').serialize(),  //direct data from form
            success: function(response){
                alert(response.success)
                $("#form_data")[0].reset(); //reset field to none
            },
            error: function(xhr){
                const err = JSON.parse(xhr.responseText);  //to read message
                alert(err.message || 'Something went wrong' + xhr.status, xhr.readyState) //to read status and cycle of ajax
            }
        })
    });
     // start of form submit
});