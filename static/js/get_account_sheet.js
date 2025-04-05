$(document).ready(function () {
  let sortOrder = "desc";
  let currentPage = 1;
  let perPage = parseInt($("#per-page").val());
  let searchQuery = "";
  let totalPages = 1;
  let searchDate = "";
  let searchTimeout; // To store the timeout for debouncing

  // Update pagination controls
  function updatePaginationControls() {
    $("#page-info").text(`Page ${currentPage} of ${totalPages}`);

    $("#prev-page").toggleClass("disabled", currentPage === 1);
    $("#next-page").toggleClass("disabled", currentPage >= totalPages);
  }

  // Load accounts with pagination, search, and sorting by date
  function loadAccounts() {
    let apiUrl = `/api/get-accounts-balance?page=${currentPage}&per_page=${perPage}&sort=${sortOrder}&sort_by=date`;
    if (searchDate) apiUrl += `&search_date=${searchDate}`;
    if (searchQuery) apiUrl += `&search=${searchQuery}`;

    $.ajax({
      url: apiUrl,
      type: "GET",
      dataType: "json",
      success: function (response) {
        let tableBody = $("#general_ledger_tbody");
        tableBody.empty();

        if (!response.data || response.data.length === 0) {
          tableBody.append(
            '<tr><td colspan="7" class="text-center">No accounts found.</td></tr>'
          );
          totalPages = 1;
          updatePaginationControls();
          return;
        }

        totalPages = response.total_pages;
        updatePaginationControls();

        // Sort by date before rendering if the backend doesn't handle it
        let sortedData = response.data.sort((a, b) => {
          return sortOrder === "desc"
            ? new Date(b.date) - new Date(a.date)
            : new Date(a.date) - new Date(b.date);
        });

        // Render accounts
        sortedData.forEach((item) => {
          tableBody.append(`
            <tr class="account-row" data-date="${item.date}">
              <td><p class="mt-2">${item.date}</p></td>
              <td><p class="mt-2">${item.net_balance}</p></td>
              <td><p class="mt-2">${item.total_credit}</p></td>
               <td class="text-end"><p class="mt-2">${item.total_debit}</p></td>
            </tr>
          `);
        });

        // Add event listeners for click and hover
        $(".account-row").on("click", function () {
          let date = $(this).data("date");
          window.location.href = `/view_balance?date=${date}`;
        });

        $(".account-row").on("mouseenter", function () {
          $(this).css("cursor", "pointer");
        });
      },
      error: function () {
        $("#general_ledger_tbody").html(
          '<tr><td colspan="7" class="text-center text-danger">Error loading data.</td></tr>'
        );
      },
    });
  }

  // Pagination control actions
  $("#prev-page").click(function () {
    if (currentPage > 1) {
      currentPage--;
      loadAccounts();
    }
  });

  $("#next-page").click(function () {
    if (currentPage < totalPages) {
      currentPage++;
      loadAccounts();
    }
  });

  // Items per page change
  $("#per-page").change(function () {
    perPage = parseInt($(this).val());
    currentPage = 1;
    loadAccounts();
  });

  // Real-time search input functionality with debounce
  $("#search-input").on("input", function () {
    clearTimeout(searchTimeout); // Clear the previous timeout
    searchQuery = $(this).val();
    currentPage = 1;

    // Set a new timeout for the search query
    searchTimeout = setTimeout(function () {
      loadAccounts(); // Call loadAccounts after a delay
    }, 500); // 500ms delay to debounce
  });

  // Date filter search functionality
  $("#search-date").on("change", function () {
    searchDate = $(this).val(); // Get the selected date
    currentPage = 1;
    loadAccounts();
  });

  // Sorting toggle
  $("#sort-date").click(function () {
    sortOrder = sortOrder === "desc" ? "asc" : "desc";
    loadAccounts();
  });

  // Handle delete button click
  $(document).on("click", ".delete-account", function () {
    var accountId = $(this).data("id");
    if (confirm("Are you sure you want to delete this account?")) {
      deleteLedger(accountId);
    }
  });

  // Initial load
  loadAccounts();
});

// Function to delete account
function deleteLedger(accountId) {
  $.ajax({
    url: `/api/delete-accounts/${accountId}`,
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
