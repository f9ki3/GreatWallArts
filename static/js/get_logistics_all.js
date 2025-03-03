$(document).ready(function () {
  let sortOrder = "asc"; // Default sort order
  let currentPage = 1; // Default page
  let perPage = 10; // Default results per page
  let searchInvoiceID = ""; // Search filter

  function loadInvoices() {
    let apiUrl = `api/get-logistics?page=${currentPage}&per_page=${perPage}&sort=${sortOrder}`;
    if (searchInvoiceID) {
      apiUrl += `&invoice_id=${searchInvoiceID}`;
    }

    $.ajax({
      url: apiUrl,
      type: "GET",
      dataType: "json",
      success: function (response) {
        let tableBody = $("#invoice-table-body");
        tableBody.empty(); // Clear previous data

        if (!response.data || response.data.length === 0) {
          tableBody.append(
            '<tr><td colspan="10" class="text-center">No invoices found.</td></tr>'
          );
          return;
        }

        response.data.forEach((item) => {
          const invoice = item.invoice;
          const purchaseOrder = item.purchase_order;

          let statusClass =
            invoice.status === "Pending"
              ? "bg-warning text-dark"
              : invoice.status === "Paid"
              ? "bg-success text-white"
              : "bg-danger text-white";

          let productDetails = "<ul class='m-0 p-0 list-unstyled'>";
          purchaseOrder.products.forEach((product) => {
            productDetails += `
          <li>
            <strong>${product.name}</strong> (${product.brand}) - 
            <span class="text-muted">${
              product.quantity
            } pcs @ ₱${product.sale_price.toFixed(
              2
            )} = ₱${product.total_price.toFixed(2)}</span>
          </li>
        `;
          });
          productDetails += "</ul>";

          let row = `
          <tr onclick="window.location.href='/view_logistics?id=${
            invoice.invoice_number
          }'">
            <td class="py-4"><p>${invoice.invoice_number}</p></td>
            <td class="py-4"><p>${invoice.po_id}</p></td>
            <td class="py-4"><p>${invoice.vendor_id}</p></td>
            <td class="py-4"><p>${invoice.due_date}</p></td>
            <td class="py-4"><p>₱${invoice.subtotal.toFixed(2)}</p></td>
            <td class="py-4"><p>${invoice.tax_rate}%</p></td>
            <td class="py-4"><p>₱${invoice.tax_amount.toFixed(2)}</p></td>
            <td class="py-4"><p>₱${invoice.discount_amount.toFixed(2)}</p></td>
            <td class="py-4"><p>₱${invoice.total_amount.toFixed(2)}</p></td>
            <td class="py-4"><span class="badge ${statusClass}">${
            invoice.status
          }</span></td>
          </tr>
        `;

          tableBody.append(row);
        });

        updatePagination(response.page, response.total_pages);
      },
      error: function (xhr, status, error) {
        console.error("Error fetching invoices:", error);
        $("#invoice-table-body").html(
          '<tr><td colspan="10" class="text-center text-danger">Failed to load data.</td></tr>'
        );
      },
    });
  }

  function updatePagination(current, total) {
    $("#page-info").text(`Page ${current} of ${total}`);
    $("#prev-page").prop("disabled", current === 1);
    $("#next-page").prop("disabled", current >= total);
  }

  $("#search-input").on("keypress", function (e) {
    if (e.which === 13) {
      searchInvoiceID = $(this).val().trim();
      currentPage = 1;
      loadInvoices();
    }
  });

  $(".sortable").on("click", function () {
    let sortField = $(this).data("sort");
    sortOrder = sortOrder === "asc" ? "desc" : "asc";
    loadInvoices();
  });

  $("#prev-page").click(function () {
    if (currentPage > 1) {
      currentPage--;
      loadInvoices();
    }
  });

  $("#next-page").click(function () {
    currentPage++;
    loadInvoices();
  });

  $("#per-page").change(function () {
    perPage = $(this).val();
    currentPage = 1;
    loadInvoices();
  });

  // Load invoices on page load
  loadInvoices();
});
