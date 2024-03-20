import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [records, setRecords] = useState([]);

  // eslint-disable-next-line
  const localhost = "http://127.0.0.1:5000";

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
      <h1>Prvních 500 záznamů z portálu sreality.cz</h1>

      {records.length != 0 ? (
        records.map((record) => {
          return (
            <div className="record">
              <h2>Byt na prodej {record.object_structure}</h2>
              <div className="recordContent">
                <div className="recordText">
                  <p>Rozloha: {record.area}</p>
                  <p>Cena: {record.price}</p>
                  <p>Lokalita: {record.locality}</p>
                </div>
                <img
                  className="recordImg"
                  src={record.image}
                  alt={record.image}
                />
              </div>
            </div>
          );
        })
      ) : (
        <>
          <h3>
            Záznamy se stahují, bude to trvat cca 1-2 minuty. (max 5 minut)
          </h3>
          <h3>Pro zkrácení čekání Vám zatím zatancuje tenhle fešák.</h3>
          <div
            style={{
              display: "flex",
              justifyContent: "center",
              alignItems: "start",
              height: "100vh",
            }}
          >
            <img
              alt="monkey"
              src="./monkey.gif"
              style={{
                top: "20px",
                height: "50vh",
                margin: "50px",
                borderRadius: "20px",
              }}
            />
          </div>
        </>
      )}
    </div>
  );
}

export default App;
