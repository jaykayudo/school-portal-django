let canvasElement = document.getElementById("cookieChart");
let config = {
  type: "bar",
  data: {
    labels: ["utilities", "salary", "debt", "employees", "students"],
    datasets: [
      {
        label: "Amount for each stats",
        data: [5, 12, 2, 19, 4],
        backgroundColor: [
          "rgb(97, 18, 4,0.3)",
          "rgba(8, 112, 63,0.3)",
          "rgba(233, 131, 124,0.3)",
          "rgba(147,47,109,0.3)",
          "rgba(92,83,136,0.3)",
        ],
        borderColor: [
          "rgba(36,32,56,,0.3,1)",
          "rgba(8, 112, 63,0.3,1)",
          "rgba(233, 131, 124,0.3,1)",
          "rgba(147,47,109,0.3,1)",
          "rgba(92,83,136,0.3,1)",
        ],
        borderWidth: 1,
      },
    ],
  },
};
let cookieChart = new Chart(canvasElement, config);
