import React, { useState } from "react";
import axios from "axios";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
} from "chart.js";

import { Bar } from "react-chartjs-2";

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend
);
function App() {
  const [file, setFile] = useState(null);

  const [profile, setProfile] = useState(null);
  const [cleanReport, setCleanReport] = useState(null);
  const [insights, setInsights] = useState(null);

  const [cleanConfig, setCleanConfig] = useState({
    remove_duplicates: true,
    missing_strategy: "mean",
    normalize_text: true
  });

  const uploadFile = async () => {

  const formData = new FormData();
  formData.append("file", file);

  const res = await axios.post(
    "http://127.0.0.1:8000/upload",
    formData
  );

  setProfile(res.data);
};
const runCleaning = async () => {

  const res = await axios.post(
    "http://127.0.0.1:8000/clean",
    cleanConfig
  );

  setCleanReport(res.data);
};
const generateInsights = async () => {

  const res = await axios.get(
    "http://127.0.0.1:8000/insights"
  );

  setInsights(res.data);
};
let categoryChartData = null;

if (insights && insights.top_categories) {

  const firstCategory = Object.keys(insights.top_categories)[0];

  const labels = Object.keys(insights.top_categories[firstCategory]);
  const values = Object.values(insights.top_categories[firstCategory]);

  categoryChartData = {
    labels: labels,
    datasets: [
      {
        label: firstCategory,
        data: values
      }
    ]
  };
}

  return (
    <div>

      <h2>AutoInsight Dashboard</h2>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <button onClick={uploadFile}>
        Upload
      </button>

      {profile && (
  <div>
    <h3>Dataset Overview</h3>

    <p>Rows: {profile.rows}</p>
    <p>Columns: {profile.columns}</p>
    <p>Missing values: {profile.missing_values}</p>
    <p>Duplicate rows: {profile.duplicate_rows}</p>

  </div>
)}

{profile && (

  <div>

    <h3>Cleaning Configuration</h3>

    <label>
      Remove duplicates
      <input
        type="checkbox"
        checked={cleanConfig.remove_duplicates}
        onChange={(e) =>
          setCleanConfig({
            ...cleanConfig,
            remove_duplicates: e.target.checked
          })
        }
      />
    </label>

    <br />

    <label>Missing value strategy</label>

    <select
      value={cleanConfig.missing_strategy}
      onChange={(e) =>
        setCleanConfig({
          ...cleanConfig,
          missing_strategy: e.target.value
        })
      }
    >
      <option value="mean">Mean</option>
      <option value="median">Median</option>
    </select>

  </div>

)}
  <button onClick={runCleaning}>
Run Cleaning
</button>
{cleanReport && (

  <div>

    <h3>Cleaning Report</h3>

    <p>Rows before: {cleanReport.rows_before}</p>
    <p>Rows after: {cleanReport.rows_after}</p>

  </div>

)}
<button onClick={generateInsights}>
Generate Insights
</button>
{insights && (

  <div>

    <h3>Insights</h3>

    <pre>
      {JSON.stringify(insights, null, 2)}
    </pre>

  </div>

)}
  {categoryChartData && (

  <div style={{ width: "600px" }}>

    <h3>Category Distribution</h3>

    <Bar data={categoryChartData} />

  </div>

)}

    </div>
    
  );
}

export default App;