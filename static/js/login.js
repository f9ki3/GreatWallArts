function login() {
  let email = $("#floatingEmail").val();
  let password = $("#floatingPassword").val();
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
      $("#btn-login").prop("disabled", false);
      $("#success").show();
      $("#error").hide();
      $("#label-login").show();
      $("#label-loading").hide();
      $("#floatingEmail, #floatingPassword").removeClass("is-invalid");
      setTimeout(() => {
        window.location.href = "/";
      }, 1000);
    },
    error: function (xhr, status, error) {
      console.error(error);
      $("#btn-login").prop("disabled", false);
      $("#label-login").show();
      $("#label-loading").hide();
      $("#error").show();
      $("#success").hide();
      $("#floatingEmail, #floatingPassword").addClass("is-invalid");
    },
  });
}
