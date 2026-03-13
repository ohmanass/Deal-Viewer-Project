import { useEffect, useState } from "react";
import { useParams, useSearchParams, useNavigate } from "react-router-dom";
import { viewDealWithTemplate } from "../services/api";

export default function DealView() {
  const { dealId } = useParams();
  const [searchParams] = useSearchParams();
  const templateId = searchParams.get("templateId");
  const navigate = useNavigate();
  const [view, setView] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!templateId) {
      setError("No template selected. Please go back and select a template.");
      return;
    }
    fetchView();
  }, [dealId, templateId]);

  const fetchView = async () => {
    const data = await viewDealWithTemplate(dealId, templateId);
    if (data.detail) {
      setError(data.detail);
    } else {
      setView(data);
    }
  };

  if (error) {
    return (
      <div style={styles.error}>
        <p>{error}</p>
        <button onClick={() => navigate("/deals")} style={styles.btn}>
          Back to Deals
        </button>
      </div>
    );
  }

  if (!view) return <p style={{ color: "white" }}>Loading...</p>;

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <div>
          <h1 style={styles.title}>{view.templateName}</h1>
          <span style={styles.code}>{view.templateCode}</span>
        </div>
        <button onClick={() => navigate("/deals")} style={styles.btn}>
          Back to Deals
        </button>
      </div>

      {view.sections.map((section, i) => (
        <div key={i} style={styles.section}>
          <h2 style={styles.sectionTitle}>{section.name}</h2>
          <div style={styles.fieldsGrid}>
            {section.fields.map((field, j) => (
              <div key={j} style={styles.field}>
                <span style={styles.fieldLabel}>{field.label}</span>
                <span style={styles.fieldValue}>
                  {formatValue(field.value)}
                </span>
              </div>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}

function formatValue(value) {
  if (value === null || value === undefined) return "-";
  if (typeof value === "boolean") return value ? "Yes" : "No";
  if (Array.isArray(value)) return value.join(", ");
  if (typeof value === "object") return JSON.stringify(value);
  return String(value);
}

const styles = {
  container: { maxWidth: "900px", margin: "0 auto" },
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "2rem",
  },
  title: { color: "white", margin: 0 },
  code: {
    color: "#7c3aed",
    fontSize: "0.85rem",
    fontWeight: "bold",
  },
  btn: {
    padding: "0.6rem 1.2rem",
    backgroundColor: "#374151",
    color: "white",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
  },
  section: {
    backgroundColor: "#1e1e2e",
    borderRadius: "10px",
    padding: "1.5rem",
    marginBottom: "1.5rem",
  },
  sectionTitle: {
    color: "#7c3aed",
    marginBottom: "1rem",
    fontSize: "1rem",
    textTransform: "uppercase",
    letterSpacing: "0.05em",
  },
  fieldsGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(250px, 1fr))",
    gap: "1rem",
  },
  field: {
    display: "flex",
    flexDirection: "column",
    gap: "0.3rem",
  },
  fieldLabel: {
    color: "#a9b1d6",
    fontSize: "0.8rem",
    textTransform: "uppercase",
  },
  fieldValue: {
    color: "white",
    fontSize: "1rem",
    fontWeight: "500",
  },
  error: {
    color: "#ef4444",
    backgroundColor: "#1e1e2e",
    padding: "2rem",
    borderRadius: "10px",
    display: "flex",
    flexDirection: "column",
    gap: "1rem",
    alignItems: "flex-start",
  },
};