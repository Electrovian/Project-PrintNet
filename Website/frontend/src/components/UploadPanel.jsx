export function UploadPanel({ files, onFilesAdded }) {
  return (
    <section className="panel card upload-panel">
      <label className="dropzone">
        <input
          type="file"
          multiple
          accept=".stl,.step,.stp"
          onChange={(event) => onFilesAdded(event.target.files)}
        />
        <div className="dropzone-body">
          <div className="dropzone-title">Upload STL or STEP Files</div>
          <div className="dropzone-subtitle">Drag and drop or click to select multiple files</div>
        </div>
      </label>
      <ul className="file-list">
        {files.map((file) => (
          <li key={file.name} className="file-item">
            <span>{file.name}</span>
            <span>{Math.max(0, Number(file.size || 0))} bytes</span>
          </li>
        ))}
        {files.length === 0 ? <li className="file-item muted">No files selected</li> : null}
      </ul>
    </section>
  );
}
