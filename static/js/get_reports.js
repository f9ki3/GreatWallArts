$(document).ready(function () {
  let currentPage = 1;
  let perPage = parseInt($("#per-page").val());
  let searchQuery = "";
  let totalPages = 1;

  function fetchReports() {
    $.ajax({
      url: "/api/get-reports",
      type: "GET",
      data: {
        page: currentPage,
        limit: perPage,
        search: searchQuery,
      },
      success: function (response) {
        let tbody = $("#general_ledger_tbody");
        tbody.empty();

        if (response.reports.length === 0) {
          tbody.append(
            '<tr><td colspan="7" class="text-center">No reports found</td></tr>'
          );
        } else {
          response.reports.forEach((report) => {
            tbody.append(`
              <tr>
                <td><p>${report.report_number}</p></td>
                <td><p>${report.created_date}</p></td>
                <td><p>${report.start_date}</p></td>
                <td><p>${report.end_date}</p></td>
                <td><p>${report.type}</p></td>
                <td><p><a href="${report.Link}">View</a></p></td>
                <td class="text-end">
                  <p>
                    <button class="btn btn-sm delete-reports" data-id="${report.id}">
                      <i class="bi bi-trash"></i>
                    </button>
                  </p>
                </td>
              </tr>
            `);
          });
        }

        // Update total pages
        totalPages = response.total_pages;
        updatePaginationControls();
      },
      error: function () {
        console.error("Error fetching reports.");
      },
    });
  }

  function updatePaginationControls() {
    $("#page-info").text(`Page ${currentPage} of ${totalPages}`);
    $("#prev-page").prop("disabled", currentPage === 1);
    $("#next-page").prop("disabled", currentPage >= totalPages);
  }

  $("#search-input").on("input", function () {
    searchQuery = $(this).val();
    currentPage = 1;
    fetchReports();
  });

  $("#per-page").on("change", function () {
    perPage = parseInt($(this).val());
    currentPage = 1;
    fetchReports();
  });

  $("#prev-page").on("click", function () {
    if (currentPage > 1) {
      currentPage--;
      fetchReports();
    }
  });

  $("#next-page").on("click", function () {
    if (currentPage < totalPages) {
      currentPage++;
      fetchReports();
    }
  });

  $(document).on("click", ".delete-reports", function () {
    var accountId = $(this).data("id");
    if (confirm("Are you sure you want to delete this account?")) {
      deleteReports(accountId);
    }
  });

  // Initial load
  fetchReports();
});

// Function to delete account
function deleteReports(accountId) {
  $.ajax({
    url: `/api/reports/${accountId}`,
    type: "DELETE",
    success: function () {
      Toastify({
        text: "Deleted successfully!",
        duration: 3000,
        gravity: "top",
        position: "right",
        backgroundColor: "#db3446",
      }).showToast();

      setTimeout(() => {
        window.location.reload();
      }, 2000);
    },
    error: function () {
      alert("An error occurred while deleting the account.");
    },
  });
}
