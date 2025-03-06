function edit_account() {
  $("#change-password-div").addClass("d-none");
  $("#edit-account-div").removeClass("d-none");
  $("#fullname").prop("disabled", false);
  $("#email").prop("disabled", false);
  $("#password-div").removeClass("d-none");
  $("#save-edit-accounts").removeClass("d-none");
}

function cancel_edit_account() {
  $("#fullname").prop("disabled", true);
  $("#email").prop("disabled", true);
  $("#password-div").addClass("d-none");
  $("#save-edit-accounts").addClass("d-none");
}

function change_password() {
  cancel_edit_account();
  $("#change-password-div").removeClass("d-none");
  $("#edit-account-div").addClass("d-none");
}

function cancel_change_password() {
  $("#change-password-div").addClass("d-none");
  $("#edit-account-div").removeClass("d-none");
}

$("#show-password-account").on("change", function () {
  console.log("clicked");
  $("#edit-confirm-password, #edit-password").attr(
    "type",
    this.checked ? "text" : "password"
  );
});

function update_account() {
  const fullname = $("#fullname").val();
  const email = $("#email").val();
  const pass = $("#edit-password").val() || null;
  const c_pass = $("#edit-confirm-password").val() || null;
  const edit_id = $("#edit-id").val();
  const url = `https://admin.gwamerchandise.com/api/users/${edit_id}`;

  const data = {
    name: fullname,
    email: email,
    role: "finance",
    status: "active",
    password: pass,
    password_confirmation: c_pass,
  };

  console.log(data);

  $.ajax({
    url: url,
    type: "PUT",
    contentType: "application/json",
    data: JSON.stringify(data),
    success: function () {
      alert("Success");
    },
    error: function (error) {
      alert("error");
      console.log(error);
      $.ajax({
        url: `/session-update/${edit_id}`,
        type: "GET",
        success: function (response) {
          console.log(response);
        },
        error: function (error) {
          console.log(error);
        },
      });
    },
  });
}
