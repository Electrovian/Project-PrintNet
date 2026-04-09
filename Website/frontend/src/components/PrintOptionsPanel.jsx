const SUPPORTS = ["On (Default)", "Off", "Only Build Plate"];
const PLA_COLORS = [
  { label: "Black", hex: "#050505" },
  { label: "Gray", hex: "#8E949C" },
  { label: "Green", hex: "#32C287" },
  { label: "White", hex: "#F4F4F4" },
  { label: "Pink", hex: "#E46BD4" },
  { label: "Yellow", hex: "#F7CC0A" },
  { label: "Red", hex: "#FF2E2E" },
  { label: "Purple", hex: "#9E2CE0" },
  { label: "Cyan", hex: "#28BCE9" },
  { label: "Gold", hex: "#E0C109" },
  { label: "Silver", hex: "#AEAFB3" },
  { label: "Onyx", hex: "#0D0D0D" },
  { label: "Orange", hex: "#F68406" }
];

function normalizeSelectedColors(options) {
  if (Array.isArray(options?.colors)) {
    const filtered = options.colors.map((item) => String(item || "").trim()).filter(Boolean);
    if (filtered.length > 0) {
      return filtered;
    }
  }
  const fallback = String(options?.color || "").trim();
  return fallback ? [fallback] : ["Black"];
}

export function PrintOptionsPanel({ options, onOptionChange, onSend }) {
  const selectedColors = normalizeSelectedColors(options);

  function toggleColor(label) {
    const text = String(label || "").trim();
    if (!text) {
      return;
    }
    const exists = selectedColors.includes(text);
    const next = exists ? selectedColors.filter((item) => item !== text) : [...selectedColors, text];
    const safeNext = next.length > 0 ? next : ["Black"];
    onOptionChange("colors", safeNext);
    onOptionChange("color", safeNext[0]);
    onOptionChange("material", "PLA");
  }

  return (
    <section className="panel card options-panel">
      <div className="section-title">Material and Print Options</div>
      <div className="field-grid two-col">
        <label className="field-block">
          <span>Material</span>
          <div className="material-lock" aria-label="Material locked to PLA">
            PLA
          </div>
        </label>
        <div className="field-block">
          <span>PLA Filaments (multi-select)</span>
          <div className="color-swatch-row" role="listbox" aria-label="PLA color selection" aria-multiselectable="true">
            {PLA_COLORS.map((item) => {
              const isSelected = selectedColors.includes(item.label);
              const className = isSelected ? "color-swatch is-selected" : "color-swatch";
              return (
                <button
                  key={item.label}
                  type="button"
                  className={className}
                  style={{ backgroundColor: item.hex }}
                  onClick={() => toggleColor(item.label)}
                  aria-label={item.label}
                  aria-pressed={isSelected}
                  title={item.label}
                />
              );
            })}
          </div>
          <div className="muted selected-colors-line">Selected: {selectedColors.join(", ")}</div>
        </div>
      </div>
      <label className="field-block">
        <span>Project Notes</span>
        <textarea
          value={options.projectNotes}
          placeholder="Add special instructions for this print..."
          onChange={(event) => onOptionChange("projectNotes", event.target.value)}
        />
      </label>
      <div className="slider-group">
        <label className="field-block">
          <span>Infill Density ({options.infillDensityPct}%)</span>
          <input
            type="range"
            min={0}
            max={100}
            value={options.infillDensityPct}
            onChange={(event) => onOptionChange("infillDensityPct", Number(event.target.value))}
          />
        </label>
        <label className="field-block">
          <span>Layer Height ({Number(options.layerHeightMm).toFixed(2)} mm)</span>
          <input
            type="range"
            min={0.08}
            max={0.32}
            step={0.02}
            value={options.layerHeightMm}
            onChange={(event) => onOptionChange("layerHeightMm", Number(event.target.value))}
          />
        </label>
      </div>
      <div className="field-grid two-col">
        <label className="field-block">
          <span>Support Structures</span>
          <select value={options.supports} onChange={(event) => onOptionChange("supports", event.target.value)}>
            {SUPPORTS.map((item) => (
              <option key={item} value={item}>
                {item}
              </option>
            ))}
          </select>
        </label>
        <label className="field-block">
          <span>Printer ID (optional)</span>
          <input
            type="text"
            value={options.printerId}
            placeholder="printer-01"
            onChange={(event) => onOptionChange("printerId", event.target.value)}
          />
          <div className="muted">Leave blank to hand off the uploaded model in the desktop app queue.</div>
        </label>
      </div>
      <button type="button" className="primary-button" onClick={onSend}>
        Send to Printer Queue
      </button>
    </section>
  );
}
