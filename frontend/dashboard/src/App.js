import React, { useState } from "react";
import axios from "axios";

function App() {

  const [file, setFile] = useState(null);
  const [data, setData] = useState(null);

  const uploadFile = async () => {

    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post(
      "http://127.0.0.1:8000/upload",
      formData
    );
    console.log(res.data)
    setData(res.data);
  };

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

      {data && (
        <div>

          <h3>Dataset Summary</h3>

          <p>Rows: {data.rows}</p>
          <p>Columns: {data.columns}</p>
          <p>Missing: {data.missing_values}</p>
        </div>
        
      )}

    </div>
    
  );
}

export default App;