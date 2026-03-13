import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createDeal } from "../services/api";

export default function DealForm() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    reference: "",
    title: "",
    clientName: "",
    clientCode: "",
    industry: "",
    country: "",
    city: "",
    ownerName: "",
    ownerEmail: "",
    status: "NEW",
    priority: "MEDIUM",
    estimatedRevenue: "",
    estimatedMargin: "",
    currency: "EUR",
    probability: "",
    expectedCloseDate: "",
    tags: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    const payload = {
      ...form,
      estimatedRevenue: parseFloat(form.estimatedRevenue) || null,
      estimatedMargin: parseFloat(form.estimatedMargin) || null,
      probability: parseInt(form.probability) || 0,
      tags: form.tags.split(",").map((t) => t.trim()).filter(Boolean),
    };
    await createDeal(payload);
    navigate("/deals");
  };

  return (
    <div style={styles.container}>
      <h1 style={{ color: "white" }}>New Deal</h1>

      <div style={styles.form}>
        <h3 style={styles.sectionTitle}>General Information</h3>
        <div style={styles.grid}>
          <Field label="Reference *" name="reference" value={form.reference} onChange={handleChange} placeholder="DL-2026-0004" />
          <Field label="Title *" name="title" value={form.title} onChange={handleChange} placeholder="Deal title" />
          <Field label="Client Name *" name="clientName" value={form.clientName} onChange={handleChange} placeholder="ACME Corporation" />
          <Field label="Client Code" name="clientCode" value={form.clientCode} onChange={handleChange} placeholder="ACME-001" />
          <Field label="Industry" name="industry" value={form.industry} onChange={handleChange} placeholder="Technology" />
          <Field label="Country" name="country" value={form.country} onChange={handleChange} placeholder="France" />
          <Field label="City" name="city" value={form.city} onChange={handleChange} placeholder="Paris" />
          <Field label="Owner Name" name="ownerName" value={form.ownerName} onChange={handleChange} placeholder="Alice Martin" />
          <Field label="Owner Email" name="ownerEmail" value={form.ownerEmail} onChange={handleChange} placeholder="alice@company.com" />
        </div>

        <h3 style={styles.sectionTitle}>Status & Priority</h3>
        <div style={styles.grid}>
          <div style={styles.fieldWrapper}>
            <label style={styles.label}>Status</label>
            <select name="status" value={form.status} onChange={handleChange} style={styles.input}>
              <option value="NEW">NEW</option>
              <option value="QUALIFICATION">QUALIFICATION</option>
              <option value="PROPOSAL">PROPOSAL</option>
              <option value="NEGOTIATION">NEGOTIATION</option>
              <option value="CLOSED_WON">CLOSED WON</option>
              <option value="CLOSED_LOST">CLOSED LOST</option>
            </select>
          </div>
          <div style={styles.fieldWrapper}>
            <label style={styles.label}>Priority</label>
            <select name="priority" value={form.priority} onChange={handleChange} style={styles.input}>
              <option value="LOW">LOW</option>
              <option value="MEDIUM">MEDIUM</option>
              <option value="HIGH">HIGH</option>
            </select>
          </div>
        </div>

        <h3 style={styles.sectionTitle}>Financial</h3>
        <div style={styles.grid}>
          <Field label="Estimated Revenue" name="estimatedRevenue" value={form.estimatedRevenue} onChange={handleChange} placeholder="120000" type="number" />
          <Field label="Estimated Margin" name="estimatedMargin" value={form.estimatedMargin} onChange={handleChange} placeholder="35000" type="number" />
          <Field label="Currency" name="currency" value={form.currency} onChange={handleChange} placeholder="EUR" />
          <Field label="Probability (%)" name="probability" value={form.probability} onChange={handleChange} placeholder="70" type="number" />
          <Field label="Expected Close Date" name="expectedCloseDate" value={form.expectedCloseDate} onChange={handleChange} type="date" />
        </div>

        <h3 style={styles.sectionTitle}>Other</h3>
        <div style={styles.grid}>
          <Field label="Tags (comma separated)" name="tags" value={form.tags} onChange={handleChange} placeholder="crm, enterprise, france" />
        </div>

        <div style={styles.actions}>
          <button onClick={() => navigate("/deals")} style={styles.btnCancel}>
            Cancel
          </button>
          <button onClick={handleSubmit} style={styles.btnSubmit}>
            Create Deal
          </button>
        </div>
      </div>
    </div>
  );
}

function Field({ label, name, value, onChange, placeholder, type = "text" }) {
  return (
    <div style={styles.fieldWrapper}>
      <label style={styles.label}>{label}</label>
      <input
        name={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        type={type}
        style={styles.input}
      />
    </div>
  );
}

const styles = {
  container: { maxWidth: "900px", margin: "0 auto" },
  form: {
    backgroundColor: "#1e1e2e",
    padding: "2rem",
    borderRadius: "10px",
    marginTop: "1.5rem",
  },
  sectionTitle: {
    color: "#7c3aed",
    marginBottom: "1rem",
    marginTop: "1.5rem",
    fontSize: "0.9rem",
    textTransform: "uppercase",
    letterSpacing: "0.05em",
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(250px, 1fr))",
    gap: "1rem",
    marginBottom: "1rem",
  },
  fieldWrapper: {
    display: "flex",
    flexDirection: "column",
    gap: "0.3rem",
  },
  label: { color: "#a9b1d6", fontSize: "0.85rem", fontWeight: "bold" },
  input: {
    padding: "0.7rem",
    borderRadius: "6px",
    border: "1px solid #3b3b5c",
    backgroundColor: "#13131f",
    color: "white",
    fontSize: "0.95rem",
  },
  actions: {
    display: "flex",
    gap: "1rem",
    justifyContent: "flex-end",
    marginTop: "2rem",
  },
  btnCancel: {
    padding: "0.6rem 1.2rem",
    backgroundColor: "#374151",
    color: "white",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
  },
  btnSubmit: {
    padding: "0.6rem 1.2rem",
    backgroundColor: "#7c3aed",
    color: "white",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
  },
};