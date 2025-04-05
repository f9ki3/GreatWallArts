function clearOtherField(current, other) {
  document.getElementById(other).value = ""; // Clear the other field
}

document.addEventListener("DOMContentLoaded", function () {
  const account = document.getElementById("account");
  const account_name = document.getElementById("account_name");
  const credit = document.getElementById("credit");
  const debit = document.getElementById("debit");
  const description = document.getElementById("description");
  const addAccountBtn = document.getElementById("add_account_ledge");

  function toggleButtonState() {
    const isCreditFilled = credit.value.trim() !== "";
    const isDebitFilled = debit.value.trim() !== "";
    const isAccountFilled = account.value.trim() !== "";
    const isAccountNameFilled = account_name.value.trim() !== "";
    const isDescriptionFilled = description.value.trim() !== "";

    // Ensure only one of Credit or Debit has a value
    if (
      isCreditFilled !== isDebitFilled &&
      isAccountFilled &&
      isAccountNameFilled &&
      isDescriptionFilled
    ) {
      addAccountBtn.removeAttribute("disabled");
    } else {
      addAccountBtn.setAttribute("disabled", "true");
    }
  }

  // Listen for input changes
  [account, account_name, credit, debit, description].forEach((field) => {
    field.addEventListener("input", toggleButtonState);
  });

  // Listen for changes in Credit and Debit fields to clear the other
  credit.addEventListener("input", function () {
    if (credit.value.trim() !== "") {
      clearOtherField(credit, "debit"); // Clear Debit if Credit is filled
    }
  });

  debit.addEventListener("input", function () {
    if (debit.value.trim() !== "") {
      clearOtherField(debit, "credit"); // Clear Credit if Debit is filled
    }
  });
});
