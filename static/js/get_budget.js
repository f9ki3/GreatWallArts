$(document).ready(function () {
  let page = 1;
  let perPage = $("#per-page").val();
  let sortField = "date_of_request";
  let sortOrder = "desc";
  let selectedRow = null;

  function formatStatus(status) {
    switch (status.toLowerCase()) {
      case "pending":
        return '<span class="badge bg-warning text-dark">Pending</span>';
      case "approved":
        return '<span class="badge bg-success">Approved</span>';
      default:
        return '<span class="badge bg-danger">Declined</span>';
    }
  }

  function fetchBudgetRequests() {
    let searchRef = $("#search-input").val().trim();
    let apiUrl = `/api/get-budget?page=${page}&per_page=${perPage}&sort=${sortField}&order=${sortOrder}`;

    if (searchRef) {
      apiUrl = `/api/get-budget?reference_number=${searchRef}`;
    }

    $.get(apiUrl, function (response) {
      // console.log(response);
      let requests = response.data;
      let totalPages = response.total_pages || 1;
      $("#page-info").text(`Page ${page} of ${totalPages}`);

      if (requests.length === 0) {
        $("#budget-table-body").html(
          '<tr><td colspan="7" class="text-center"><p>No budget requests found</p></td></tr>'
        );
        return;
      }

      let tableRows = requests
        .map(
          (request) => `
          <tr class="selectable-row" data-id="${request.id}">
            <td><p>${request.reference_number}</p></td>
            <td><p>${request.requested_by}</p></td>
            <td><p>${request.date_of_request}</p></td>
            <td><p>${request.department}</p></td>
            <td><p>${request.email}</p></td>
            <td><p>${formatStatus(request.status)}</p></td>
            <td class="text-end">
              <button class="btn btn-sm delete-budget" data-id="${
                request.reference_number
              }">
                <i class="bi bi-trash"></i>
              </button>
            </td>
          </tr>
        `
        )
        .join("");

      $("#budget-table-body").html(tableRows);
    }).fail(function () {
      $("#budget-table-body").html(
        '<tr><td colspan="7" class="text-center"><p>No Data Results</p></td></tr>'
      );
    });
  }

  // Sorting Feature
  $(".sortable").on("click", function () {
    let newSortField = $(this).data("sort");
    if (sortField === newSortField) {
      sortOrder = sortOrder === "asc" ? "desc" : "asc";
    } else {
      sortField = newSortField;
      sortOrder = "asc";
    }
    fetchBudgetRequests();
  });

  // Search Feature
  $("#search-input").on("keyup", function () {
    page = 1;
    fetchBudgetRequests();
  });

  // Pagination
  $("#prev-page").on("click", function () {
    if (page > 1) {
      page--;
      fetchBudgetRequests();
    }
  });

  $("#next-page").on("click", function () {
    page++;
    fetchBudgetRequests();
  });

  $("#per-page").on("change", function () {
    perPage = $(this).val();
    page = 1;
    fetchBudgetRequests();
  });

  // Row Selection
  $(document).on("click", ".selectable-row", function (e) {
    if (!$(e.target).hasClass("delete-budget")) {
      if (selectedRow) {
        selectedRow.removeClass("table-active");
      }
      selectedRow = $(this);
      selectedRow.addClass("table-active");

      // Redirect to the details page
      let refNumber = $(this).find("td:first-child").text().trim();
      window.location.href = `/view_request?ref=${refNumber}`;
    }
  });

  // Delete Budget Request
  $(document).on("click", ".delete-budget", function (e) {
    e.stopPropagation(); // Prevents row click from triggering

    let budgetId = $(this).data("id");
    let rowToDelete = $(this).closest("tr");

    if (confirm("Are you sure you want to delete this budget request?")) {
      $.ajax({
        url: `/api/delete-budget/${budgetId}`,
        type: "DELETE",
        success: function (response) {
          rowToDelete.remove(); // Remove the row from the table
          Toastify({
            text: "Deleted successfully!",
            duration: 3000,
            gravity: "top",
            position: "right",
            backgroundColor: "#db3446",
          }).showToast();
        },
        error: function (xhr, status, error) {
          console.error("Error deleting budget request:", error);
          alert("Failed to delete the budget request.");
        },
      });
    }
  });

  // Load Data on Page Load
  fetchBudgetRequests();
});
