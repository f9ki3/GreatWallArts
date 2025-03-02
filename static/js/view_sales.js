$(document).ready(function () {
  const urlParams = new URLSearchParams(window.location.search);
  const id = urlParams.get("id");

  $.ajax({
    url: `/api/get-sales?id=${id}`, // Fixed backticks for interpolation
    method: "GET",
    dataType: "json", // Ensures the response is parsed as JSON
    success: function (salesData) {
      console.log(salesData);
      // Populate sales table
      let salesHTML = "";
      salesData.sale.cart_items.forEach((item) => {
        salesHTML += `
             <tr>
              <td class="text-muted py-3"><p>${item.product_name}</p></td>
              <td class="text-muted py-3"><p>₱${item.regular_price}</p></td>
              <td class="text-muted py-3"><p>₱${item.sale_price}</p></td>
            </tr>

            `;
      });

      $("#sales-table-body").html(salesHTML);
      $("#earnings").text("₱ " + salesData.sale.earnings);
      $("#capital").text(
        "₱ " + (salesData.sale.total_sum - salesData.sale.earnings)
      );
      $("#total-sum").text(salesData.sale.total_sum);
      $("#timestamp").text(salesData.sale.timestamp);
    },
    error: function (xhr, status, error) {
      console.error("Error fetching sales data:", error);
    },
  });
});
