import { useEffect, useState } from "react";

function App() {
  const [records, setRecords] = useState([]);

  // eslint-disable-next-line
  const localhost = "http://127.0.0.1:3000";

  useEffect(() => {
    fetch(`${localhost}/get_data`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((resp) => {
        return resp.json();
      })
      .then((resp) => {
        // save tournament data to state and format last update time
        setRecords(resp);
      })
      .catch((err) => {
        console.log("ERROR:");
        console.log(err);
      }); // eslint-disable-next-line
  }, []);

  return (
    <div className="App">
      <h1>First 500 records from sreality.cz</h1>
      {records.map((record) => {
        return (
          <div>
            <p>{record.object_type}</p>
            <p>{record.event_type}</p>
            <p>Struktura: {record.object_structure}</p>
            <p>Rozloha: {record.area}</p>
            <p>Cena: {record.price}</p>
            <img src={record.image} alt={record.image} />
          </div>
        );
      })}
    </div>
  );
}

export default App;
