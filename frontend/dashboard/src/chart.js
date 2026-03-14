import { Bar } from "react-chartjs-2";

export default function CategoryChart({ data }) {

  const labels = Object.keys(data);
  const values = Object.values(data);

  const chartData = {
    labels: labels,
    datasets: [
      {
        label: "Category Count",
        data: values
      }
    ]
  };

  return <Bar data={chartData} />;
}