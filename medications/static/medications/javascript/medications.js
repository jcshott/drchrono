
// process refill
$('.refillButton').on('click', function (evt) {
    evt.preventDefault();
    var buttonSelected = $(this).attr("id");
    var refillSelected = buttonSelected.substring(7);
    var data = {
               "csrfmiddlewaretoken": document.getElementsByName('csrfmiddlewaretoken')[0].value,
               "med_id": refillSelected,
    }

    $.post('/medications/process_refill/', data, function(response){
        console.log(response);
        if (response < 2 && $("#remaining-"+refillSelected).text() > 1) {
            $("."+refillSelected).append(
                "<button class='renewButton' id='renew-{{ med.med_id }}'> renew options for this Rx </button>"
            );
        }

        $("#remaining-"+refillSelected).text(response);
        $("#button-"+refillSelected).remove();

    });
});

// query for form to submit renewal
$('#renewModal').on('show.bs.modal', function (event) {
      var button = $(event.relatedTarget) // Button that triggered the modal
      var med_id = button.data('id') // Extract med_id info from data-id attributes
      // AJAX to get form
      $.get('/medications/process_renewal/', {"med_id": med_id}, function(result) {
          $(".modal-content").html(result);
      })
});

// process renewal
$("#renewModal").on('submit', "#renewForm", function(evt) {
    evt.preventDefault();
    var data = $('form#renewForm').serialize();
    $.post('/medications/process_renewal/', data, function (response) {
        console.log(response);
        $("#renewModal").modal('hide');
        if (response == "no email") {
            $(".alert").attr("hidden", false);
        }

    });
});

$("#renewModal").on('click', "#cancel", function () {
    console.log("cancel");
    $("#renewModal").modal('hide');
})
