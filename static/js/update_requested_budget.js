function accept_budget() {
  const reference = $(".reference-number").text();
  data = {
    reference_number: reference,
  };

  $.ajax({
    url: "/api/update-and-approve-budget",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify(data),
    success: function (response) {
      console.log(response);
      Toastify({
        text: "Appoved successfully!",
        duration: 3000,
        gravity: "top",
        position: "right",
        backgroundColor: "#4CAF50",
      }).showToast();
      setTimeout(() => {
        window.location.reload();
      }, 2000);
    },
    error: function (error) {
      console.log(error);
    },
  });
}

function reject_budget() {
  const reference = $(".reference-number").text();
  data = {
    reference_number: reference,
  };

  $.ajax({
    url: "/api/update-and-delete-budget",
    type: "POST",
    contentType: "application/json",
    data: JSON.stringify(data),
    success: function (response) {
      console.log(response);
      Toastify({
        text: "Declined successfully!",
        duration: 3000,
        gravity: "top",
        position: "right",
        backgroundColor: "#db3446",
      }).showToast();
      setTimeout(() => {
        window.location.reload();
      }, 2000);
    },
    error: function (error) {
      console.log(error);
    },
  });
}
