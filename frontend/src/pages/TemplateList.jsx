import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { getTemplates, deleteTemplate } from "../services/api";

export default function TemplateList() {
  const [templates, setTemplates] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    fetchTemplates();
  }, []);

  const fetchTemplates = async () => {
    const data = await getTemplates();
    setTemplates(data);
  };

  const handleDelete = async (id) => {
    if (confirm("Delete this template?")) {
      await deleteTemplate(id);
      fetchTemplates();
    }
  };

  return (
    <div>
      <div style={styles.header}>
        <h1>Templates</h1>
        <button onClick={() => navigate("/templates/new")} style={styles.btn}>
          + New Template
        </button>
      </div>

      <div style={styles.grid}>
        {templates.map((t) => (
          <div key={t._id} style={styles.card}>
            <div style={styles.cardHeader}>
              <span style={styles.name}>{t.name}</span>
              <span style={t.isActive ? styles.active : styles.inactive}>
                {t.isActive ? "Active" : "Inactive"}
              </span>
            </div>
            <p style={styles.desc}>{t.description}</p>
            <p style={styles.fields}>
              {t.visibleFields.length} visible fields
            </p>
            <div style={styles.cardActions}>
              <button
                onClick={() => navigate(`/deals?templateId=${t._id}`)}
                style={styles.btnPrimary}
              >
                View Deals
              </button>
              <button
                onClick={() => handleDelete(t._id)}
                style={styles.btnDanger}
              >
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

const styles = {
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "2rem",
  },
  btn: {
    padding: "0.6rem 1.2rem",
    backgroundColor: "#7c3aed",
    color: "white",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))",
    gap: "1.5rem",
  },
  card: {
    backgroundColor: "#1e1e2e",
    borderRadius: "10px",
    padding: "1.5rem",
    color: "white",
  },
  cardHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "0.5rem",
  },
  name: { fontWeight: "bold", fontSize: "1.1rem" },
  active: {
    backgroundColor: "#22c55e",
    color: "white",
    padding: "2px 8px",
    borderRadius: "12px",
    fontSize: "0.75rem",
  },
  inactive: {
    backgroundColor: "#6b7280",
    color: "white",
    padding: "2px 8px",
    borderRadius: "12px",
    fontSize: "0.75rem",
  },
  desc: { color: "#a9b1d6", fontSize: "0.9rem", marginBottom: "0.5rem" },
  fields: { color: "#7c3aed", fontSize: "0.85rem", marginBottom: "1rem" },
  cardActions: { display: "flex", gap: "0.5rem" },
  btnPrimary: {
    flex: 1,
    padding: "0.5rem",
    backgroundColor: "#3b82f6",
    color: "white",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
  },
  btnDanger: {
    padding: "0.5rem 1rem",
    backgroundColor: "#ef4444",
    color: "white",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
  },
};