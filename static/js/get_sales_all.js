$(document).ready(function () {
  let page = 1;
  let perPage = $("#per-page").val();
  let sortBy = "timestamp";
  let order = "desc";

  function fetchSales() {
    let searchID = $("#search-input").val().trim();
    let apiUrl = `/api/get-sales?page=${page}&per_page=${perPage}&sort_by=${sortBy}&order=${order}`;

    if (searchID) {
      apiUrl = `/api/get-sales?id=${searchID}`;
    }

    $.get(apiUrl, function (response) {
      if (searchID) {
        let sale = response.sale;
        if (!sale) {
          $("#sales-table-body").html(
            '<tr><td colspan="4" class="text-center">No data found</td></tr>'
          );
          return;
        }
        $("#sales-table-body").html(`
          <tr onclick="window.location.href='/view_sales?id=${sale.id}'" style="cursor: pointer;">
            <td><p>${sale.id}</p></td>
            <td><p>${sale.total_sum}</p></td>
            <td><p>${sale.earnings}</p></td>
            <td class="text-end"><p>${sale.timestamp}</p></td>
          </tr>
        `);
      } else {
        let sales = response.sales;
        let totalPages = response.total_pages;
        $("#page-info").text(`Page ${page} of ${totalPages}`);

        if (sales.length === 0) {
          $("#sales-table-body").html(
            '<tr><td colspan="4" class="text-center">No sales data found</td></tr>'
          );
          return;
        }

        let tableRows = sales
          .map(
            (sale) => `
          <tr onclick="window.location.href='/view_sales?id=${sale.id}'" style="cursor: pointer;">
            <td><p>${sale.id}</p></td>
            <td><p>${sale.total_sum}</p></td>
            <td><p>${sale.earnings}</p></td>
            <td class="text-end"><p>${sale.timestamp}</p></td>
          </tr>

        `
          )
          .join("");

        $("#sales-table-body").html(tableRows);
      }
    }).fail(function () {
      $("#sales-table-body").html(
        '<tr><td colspan="4" class="text-center">No Data Results</td></tr>'
      );
    });
  }

  // Initial fetch
  fetchSales();

  // Search by ID
  $("#search-input").on("keyup", function () {
    page = 1;
    fetchSales();
  });

  // Sorting
  $(".sortable").on("click", function () {
    sortBy = $(this).data("sort");
    order = order === "asc" ? "desc" : "asc";
    fetchSales();
  });

  // Pagination
  $("#prev-page").on("click", function () {
    if (page > 1) {
      page--;
      fetchSales();
    }
  });

  $("#next-page").on("click", function () {
    page++;
    fetchSales();
  });

  // Per Page Selection
  $("#per-page").on("change", function () {
    perPage = $(this).val();
    page = 1; // Reset to page 1
    fetchSales();
  });
});
