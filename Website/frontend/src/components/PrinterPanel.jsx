export function PrinterPanel() {
  const rows = [
    { id: "printer-01", connector: "octoprint", endpoint: "http://127.0.0.1:5000", state: "Ready" },
    { id: "printer-02", connector: "moonraker", endpoint: "http://127.0.0.1:7125", state: "Ready" }
  ];
  return (
    <section className="panel card printer-panel">
      <div className="section-title">Printer Fleet</div>
      <table className="printer-table">
        <thead>
          <tr>
            <th>Printer</th>
            <th>Connector</th>
            <th>Endpoint</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.id}>
              <td>{row.id}</td>
              <td>{row.connector}</td>
              <td>{row.endpoint}</td>
              <td>{row.state}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
