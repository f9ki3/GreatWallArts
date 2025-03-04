$(document).ready(function () {
  let page = 1;
  let perPage = $("#per-page").val();
  let sortField = "reference_number";
  let sortOrder = "asc";

  function formatStatus(status) {
    switch (status.toLowerCase()) {
      case "pending":
        return '<span class="badge bg-warning text-dark">Pending</span>';
      case "approved":
        return '<span class="badge bg-success">Approved</span>';
      default:
        return '<span class="badge bg-danger">Rejected</span>';
    }
  }

  function fetchBudgetRequests() {
    let searchRef = $("#search-input").val().trim();
    let apiUrl = `/api/get-budget?page=${page}&per_page=${perPage}&sort=${sortField}&order=${sortOrder}`;

    if (searchRef) {
      apiUrl = `/api/get-budget?reference_number=${searchRef}`;
    }

    $.get(apiUrl, function (response) {
      console.log(response);
      let requests = response.data;
      let totalPages = response.total_pages || 1;
      $("#page-info").text(`Page ${page} of ${totalPages}`);

      if (requests.length === 0) {
        $("#budget-table-body").html(
          '<tr><td colspan="6" class="text-center"><p>No budget requests found</p></td></tr>'
        );
        return;
      }

      let tableRows = requests
        .map(
          (request) => `
          <tr onclick="window.location.href='/view_request?ref=${
            request.reference_number
          }'" style="cursor: pointer;">
            <td><p>${request.reference_number}</p></td>
            <td><p>${request.requested_by}</p></td>
            <td><p>${request.date_of_request}</p></td>
            <td><p>${request.department}</p></td>
            <td><p>${request.email}</p></td>
            <td><p>${formatStatus(request.status)}</p></td>
          </tr>
        `
        )
        .join("");

      $("#budget-table-body").html(tableRows);
    }).fail(function () {
      $("#budget-table-body").html(
        '<tr><td colspan="6" class="text-center"><p>No Data Results</p></td></tr>'
      );
    });
  }

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

  $("#search-input").on("keyup", function () {
    page = 1;
    fetchBudgetRequests();
  });

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

  fetchBudgetRequests();
});
