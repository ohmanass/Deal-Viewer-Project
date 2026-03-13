import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { createTemplate } from "../services/api";

export default function TemplateForm() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    name: "",
    code: "",
    description: "",
    visibleFields: "",
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async () => {
    const payload = {
      name: form.name,
      code: form.code.toUpperCase().replace(/\s+/g, "_"),
      description: form.description,
      visibleFields: form.visibleFields.split(",").map((f) => f.trim()).filter(Boolean),
    };
    await createTemplate(payload);
    navigate("/templates");
  };

  return (
    <div style={styles.container}>
      <h1>New Template</h1>

      <div style={styles.form}>
        <label style={styles.label}>Name</label>
        <input
          name="name"
          value={form.name}
          onChange={handleChange}
          placeholder="Ex: Financial View"
          style={styles.input}
        />

        <label style={styles.label}>Code</label>
        <input
          name="code"
          value={form.code}
          onChange={handleChange}
          placeholder="Ex: FINANCE_VIEW"
          style={styles.input}
        />

        <label style={styles.label}>Description</label>
        <input
          name="description"
          value={form.description}
          onChange={handleChange}
          placeholder="Short description"
          style={styles.input}
        />

        <label style={styles.label}>
          Visible Fields{" "}
          <span style={styles.hint}>(comma separated, dot notation allowed)</span>
        </label>
        <textarea
          name="visibleFields"
          value={form.visibleFields}
          onChange={handleChange}
          placeholder="reference, title, clientName, financials.totalInclTax"
          style={styles.textarea}
        />

        <div style={styles.actions}>
          <button onClick={() => navigate("/templates")} style={styles.btnCancel}>
            Cancel
          </button>
          <button onClick={handleSubmit} style={styles.btnSubmit}>
            Create Template
          </button>
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: { maxWidth: "600px", margin: "0 auto" },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "1rem",
    backgroundColor: "#1e1e2e",
    padding: "2rem",
    borderRadius: "10px",
    marginTop: "1.5rem",
  },
  label: { color: "#a9b1d6", fontSize: "0.9rem", fontWeight: "bold" },
  hint: { color: "#6b7280", fontWeight: "normal" },
  input: {
    padding: "0.7rem",
    borderRadius: "6px",
    border: "1px solid #3b3b5c",
    backgroundColor: "#13131f",
    color: "white",
    fontSize: "1rem",
  },
  textarea: {
    padding: "0.7rem",
    borderRadius: "6px",
    border: "1px solid #3b3b5c",
    backgroundColor: "#13131f",
    color: "white",
    fontSize: "0.9rem",
    minHeight: "100px",
    resize: "vertical",
  },
  actions: { display: "flex", gap: "1rem", justifyContent: "flex-end" },
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