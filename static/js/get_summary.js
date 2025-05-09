$(document).ready(function () {
  function loadPaidInvoicesChart() {
    $.ajax({
      url: "api/get-logistics-summary",
      type: "GET",
      dataType: "json",
      success: function (response) {
        if (!response.paid_amounts || response.paid_amounts.length === 0) {
          $("#invoiceAreaChart").html(
            '<p class="text-center">No paid invoice data available.</p>'
          );
          return;
        }

        // Display the total paid, overdue, and pending
        $("#totalPaid").text(
          response.total_paid.toLocaleString(undefined, {
            minimumFractionDigits: 2,
          })
        );
        $("#totalOverdue").text(
          response.total_overdue.toLocaleString(undefined, {
            minimumFractionDigits: 2,
          })
        );
        $("#totalPending").text(
          response.total_pending.toLocaleString(undefined, {
            minimumFractionDigits: 2,
          })
        );

        // Labels for the X-axis (e.g., Invoice numbers)
        const chartLabels = Array.from(
          { length: response.paid_amounts.length },
          (_, index) => ` ${index + 1}`
        );
        const chartSeries = response.paid_amounts;

        const ctx = document
          .getElementById("invoiceAreaChart")
          .getContext("2d");

        const chart = new Chart(ctx, {
          type: "line",
          data: {
            labels: chartLabels,
            datasets: [
              {
                label: "Paid Amounts",
                data: chartSeries,
                fill: true,
                borderColor: "#00b894",
                backgroundColor: "rgba(0, 184, 148, 0.3)",
                tension: 0.4,
              },
            ],
          },
          options: {
            responsive: true,
            plugins: {
              tooltip: {
                callbacks: {
                  label: function (tooltipItem) {
                    return "₱" + tooltipItem.raw.toFixed(2);
                  },
                },
              },
              legend: {
                display: false,
              },
            },
            scales: {
              x: {
                title: {
                  display: true,
                  text: "Invoices",
                },
              },
              y: {
                title: {
                  display: true,
                  text: "Summary of Sales and Logistics",
                },
                ticks: {
                  beginAtZero: true,
                  callback: function (value) {
                    return "₱" + value.toFixed(2);
                  },
                },
              },
            },
          },
        });
      },
      error: function (xhr, status, error) {
        console.error("Error fetching paid invoice data:", error);
        $("#invoiceAreaChart").html(
          '<p class="text-danger text-center">Failed to load chart.</p>'
        );
      },
    });
  }

  loadPaidInvoicesChart();
});
