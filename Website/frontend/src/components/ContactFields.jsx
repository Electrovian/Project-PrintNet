export function ContactFields({ contact, onFieldChange }) {
  return (
    <section className="panel card contact-panel">
      <div className="field-grid">
        <label className="field-block">
          <span>Name</span>
          <input
            type="text"
            value={contact.name}
            placeholder="Name"
            onChange={(event) => onFieldChange("name", event.target.value)}
          />
        </label>
        <label className="field-block">
          <span>Email</span>
          <input
            type="email"
            value={contact.email}
            placeholder="Email"
            onChange={(event) => onFieldChange("email", event.target.value)}
          />
        </label>
        <label className="field-block">
          <span>Phone</span>
          <input
            type="tel"
            value={contact.phone}
            placeholder="Phone"
            onChange={(event) => onFieldChange("phone", event.target.value)}
          />
        </label>
      </div>
    </section>
  );
}
