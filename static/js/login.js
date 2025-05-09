function login() {
  let email = $("#floatingEmail").val().trim(); // Trim spaces
  let password = $("#floatingPassword").val().trim(); // Trim spaces

  // Hide the login label and show loading state
  $("#label-login").hide();
  $("#label-loading").show();
  $("#btn-login").prop("disabled", true);

  // Ensure both fields are filled
  if (!email || !password) {
    alert("Please enter both email and password.");
    $("#label-login").show();
    $("#label-loading").hide();
    $("#btn-login").prop("disabled", false);
    return;
  }

  // Basic client-side validation (optional - server validation is a must)
  const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
  if (!emailPattern.test(email)) {
    alert("Please enter a valid email address.");
    $("#label-login").show();
    $("#label-loading").hide();
    $("#btn-login").prop("disabled", false);
    return;
  }

  $.ajax({
    url: "/api/login",
    type: "POST",
    contentType: "application/json",
    dataType: "json", // Fix: Ensure this is correctly capitalized
    data: JSON.stringify({
      email: email,
      password: password,
    }),
    success: function (response) {
      console.log(response);
      // Handle success
      if (response.success) {
        $("#btn-login").prop("disabled", false);
        $("#success").show();
        $("#error").hide();
        $("#label-login").show();
        $("#label-loading").hide();
        $("#floatingEmail, #floatingPassword").removeClass("is-invalid");
        setTimeout(() => {
          window.location.href = "/";
        }, 1000);
      } else {
        // Handle unexpected responses securely
        showError("Login failed. Please try again.");
      }
    },
    error: function (xhr, status, error) {
      console.error(error);
      // Handle error securely, don't expose too much info
      showError("An error occurred. Please try again later.");
    },
  });

  // Helper function to show error
  function showError(message) {
    $("#btn-login").prop("disabled", false);
    $("#label-login").show();
    $("#label-loading").hide();
    $("#error").text(message).show();
    $("#success").hide();
    $("#floatingEmail, #floatingPassword").addClass("is-invalid");
  }
}
