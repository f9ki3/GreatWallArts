function clearOtherField(current, other) {
  document.getElementById(other).value = ""; // Clear the other field
}
document.addEventListener("DOMContentLoaded", function () {
  const account = document.getElementById("account");
  const credit = document.getElementById("credit");
  const debit = document.getElementById("debit");
  const description = document.getElementById("description");
  const addAccountBtn = document.getElementById("add_account_ledge");

  function toggleButtonState() {
    const isCreditFilled = credit.value.trim() !== "";
    const isDebitFilled = debit.value.trim() !== "";
    const isAccountFilled = account.value.trim() !== "";
    const isDescriptionFilled = description.value.trim() !== "";

    // Ensure only one of Credit or Debit has a value
    if (
      isCreditFilled !== isDebitFilled &&
      isAccountFilled &&
      isDescriptionFilled
    ) {
      addAccountBtn.removeAttribute("disabled");
    } else {
      addAccountBtn.setAttribute("disabled", "true");
    }
  }

  // Listen for input changes
  [account, credit, debit, description].forEach((field) => {
    field.addEventListener("input", toggleButtonState);
  });
});
