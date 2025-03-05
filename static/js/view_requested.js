$(document).ready(function () {
  const urlParams = new URLSearchParams(window.location.search);
  const referenceNumber = urlParams.get("ref");

  if (!referenceNumber) {
    console.warn("No reference number provided in URL.");
    return; // Stop execution if reference number is missing
  }

  $.ajax({
    url: `api/get-budget?reference_number=${referenceNumber}`,
    method: "GET",
    dataType: "json",
    success: function (response) {
      if (response.data && response.data.length > 0) {
        const budgetData = response.data[0]; // First item in array
        const budgetDetails = budgetData.budget_details;

        let salesHTML = "";
        budgetDetails.forEach((item) => {
          salesHTML += `
            <tr>
              <td class="text-muted py-3"><p>${item.category}</p></td>
              <td class="text-muted py-3"><p>₱${item.amount.toLocaleString()}</p></td>
              <td class="text-muted py-3"><p>${item.description}</p></td>
            </tr>`;
        });

        $("#budget-table-body").html(salesHTML);

        // Populate details using class selectors
        $(".reference-number").text(budgetData.reference_number);
        $(".requested-by").text(budgetData.requested_by);
        $(".department").text(budgetData.department);
        $(".email").text(budgetData.email);
        $(".date-of-request").text(budgetData.date_of_request);
        const statusText = budgetData.status.toLowerCase(); // Convert to lowercase for comparison
        let badgeClass = "bg-secondary"; // Default badge color (gray)

        if (statusText === "pending") {
          badgeClass = "bg-warning"; // Yellow for Pending
          $(".status-btn").removeClass("d-none");
        } else if (statusText === "approved") {
          badgeClass = "bg-success"; // Green for Approved
        } else if (statusText === "rejected") {
          badgeClass = "bg-danger"; // Red for Declined
        }

        $(".status").html(
          `<span class="badge ${badgeClass} text-white">${budgetData.status}</span>`
        );
      } else {
        console.warn("No budget data found.");
      }
    },
    error: function (xhr, status, error) {
      console.error("Error fetching budget data:", error);
    },
  });
});
$(document).ready(function () {
  const urlParams = new URLSearchParams(window.location.search);
  const referenceNumber = urlParams.get("ref");

  if (!referenceNumber) {
    console.warn("No reference number provided in URL.");
    return; // Stop execution if reference number is missing
  }

  $.ajax({
    url: `api/get-budget?reference_number=${referenceNumber}`,
    method: "GET",
    dataType: "json",
    success: function (response) {
      // console.log(response);

      if (response.data && response.data.length > 0) {
        const budgetData = response.data[0]; // First item in array
        const budgetDetails = budgetData.budget_details;

        let salesHTML = "";
        budgetDetails.forEach((item) => {
          salesHTML += `
            <tr>
              <td class="text-muted py-3"><p>${item.category}</p></td>
              <td class="text-muted py-3"><p>₱${item.amount.toLocaleString()}</p></td>
              <td class="text-muted py-3"><p>${item.description}</p></td>
            </tr>`;
        });

        $("#budget-table-body").html(salesHTML);

        // Populate details using class selectors
        $(".reference-number").text(budgetData.reference_number);
        $(".requested-by").text(budgetData.requested_by);
        $(".department").text(budgetData.department);
        $(".email").text(budgetData.email);
        $(".date-of-request").text(budgetData.date_of_request);

        // Handle status display
        const statusText = (budgetData.status || "").toLowerCase(); // Ensure lowercase comparison
        let badgeClass = "bg-danger"; // Default badge color (gray)

        if (statusText === "pending") {
          badgeClass = "bg-warning"; // Yellow for Pending
          $(".status-btn").removeClass("d-none").show(); // Show status button
        } else {
          $(".status-btn").hide(); // Hide status button for approved/rejected
          if (statusText === "approved") {
            badgeClass = "bg-success"; // Green for Approved
          } else if (statusText === "rejected") {
            badgeClass = "bg-danger"; // Red for Declined
          }
        }

        $(".status").html(
          `<span class="badge ${badgeClass} text-white">${budgetData.status}</span>`
        );
      } else {
        console.warn("No budget data found.");
      }
    },
    error: function (xhr, status, error) {
      console.error("Error fetching budget data:", error);
    },
  });
});
