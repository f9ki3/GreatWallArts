$(document).ready(function () {
  let sortOrder = "asc";
  let currentPage = 1;
  let perPage = parseInt($("#per-page").val());
  let searchQuery = "";
  let totalPages = 1;

  function updatePaginationControls() {
    $("#page-info").text(`Page ${currentPage} of ${totalPages}`);

    if (currentPage === 1) {
      $("#prev-page").addClass("disabled");
    } else {
      $("#prev-page").removeClass("disabled");
    }

    if (currentPage >= totalPages) {
      $("#next-page").addClass("disabled");
    } else {
      $("#next-page").removeClass("disabled");
    }
  }

  function loadAccounts() {
    let apiUrl = `/api/get-accounts?page=${currentPage}&per_page=${perPage}&sort=${sortOrder}`;
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
          totalPages = 1; // Reset totalPages if no data is found
          updatePaginationControls();
          return;
        }

        // Set total pages from response
        totalPages = response.total_pages;
        updatePaginationControls();

        // Render accounts
        response.data.forEach((item) => {
          tableBody.append(`
            <tr>
              <td><p class="mt-2">${item.reference}</p></td>
              <td><p class="mt-2">${item.date}</p></td>
              <td><p class="mt-2">${item.account}</p></td>
              <td><p class="mt-2">${item.credit}</p></td>
              <td><p class="mt-2">${item.debit}</p></td>
              <td><p class="mt-2">${item.description}</p></td>
              <td class="text-end">
                <button class="btn btn-sm delete-account" data-id="${item.id}">
                  <i class="bi bi-trash"></i>
                </button>
              </td>
            </tr>
          `);
        });
      },
      error: function () {
        $("#general_ledger_tbody").html(
          '<tr><td colspan="7" class="text-center text-danger">Error loading data.</td></tr>'
        );
      },
    });
  }

  // Pagination controls
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

  $("#per-page").change(function () {
    perPage = parseInt($(this).val());
    currentPage = 1;
    loadAccounts();
  });

  // Search functionality
  $("#search-input").on("input", function () {
    searchQuery = $(this).val();
    currentPage = 1;
    loadAccounts();
  });

  loadAccounts();
});
