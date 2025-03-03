$(document).ready(function () {
  const urlParams = new URLSearchParams(window.location.search);
  const id = urlParams.get("id");

  $.ajax({
    url: `/api/get-logistics?invoice_id=${encodeURIComponent(id)}`,
    method: "GET",
    dataType: "json",
    success: function (response) {
      if (response.data.length > 0) {
        const invoiceData = response.data[0].invoice;
        const poData = response.data[0].purchase_order;
        const products = poData.products;

        // Update Invoice Details
        $(".invoice-number").text(invoiceData.invoice_number);
        $(".po-id").text(invoiceData.po_id);
        $(".vendor-id").text(invoiceData.vendor_id);
        $(".supplier").text(poData.supplier);
        $(".shipment-date").text(poData.shipment_date);
        $(".created-at").text(invoiceData.created_at);
        $(".due-date").text(invoiceData.due_date);
        $(".delivery-date").text(poData.delivery_date);
        $(".order-date").text(poData.order_date);
        $(".status").text(invoiceData.status);

        // Update Status Badge
        $(".status")
          .removeClass("bg-warning bg-success bg-danger")
          .addClass(
            invoiceData.status === "Paid"
              ? "bg-success text-light"
              : invoiceData.status === "Pending"
              ? "bg-warning"
              : "bg-danger text-light"
          );

        // Populate Products Table
        let productRows = "";
        products.forEach((product) => {
          productRows += `
            <tr>
              <td><p>${product.brand}</p></td>
              <td><p>${product.name}</p></td>
              <td><p>${product.quantity}</p></td>
              <td><p>₱${product.regular_price.toFixed(2)}</p></td>
              <td><p>₱${product.sale_price.toFixed(2)}</p></td>
              <td><p>₱${product.total_price.toFixed(2)}</p></td>
            </tr>
          `;
        });
        $("tbody.product-list").html(productRows);

        // Update Summary Table
        $(".subtotal").text(`₱${invoiceData.subtotal.toFixed(2)}`);
        $(".tax-rate").text(`${invoiceData.tax_rate}%`);
        $(".tax-amount").text(`₱${invoiceData.tax_amount.toFixed(2)}`);
        $(".discount").text(`₱${invoiceData.discount_amount.toFixed(2)}`);
        $(".total-amount").text(`₱${invoiceData.total_amount.toFixed(2)}`);
      }
    },
    error: function (xhr, status, error) {
      console.error("Error fetching logistics data:", error);
    },
  });
});
