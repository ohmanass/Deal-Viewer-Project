import { useEffect, useState } from "react";
import { useNavigate, useSearchParams } from "react-router-dom";
import { getDeals, getTemplates, deleteDeal } from "../services/api";

export default function DealList() {
  const [deals, setDeals] = useState([]);
  const [templates, setTemplates] = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState("");
  const [filters, setFilters] = useState({
    clientName: "",
    startDate: "",
    endDate: "",
  });
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();

  useEffect(() => {
    fetchTemplates();
    const templateId = searchParams.get("templateId");
    if (templateId) setSelectedTemplate(templateId);
  }, []);

  useEffect(() => {
    fetchDeals();
  }, [filters]);

  const fetchTemplates = async () => {
    const data = await getTemplates();
    setTemplates(data);
  };

  const fetchDeals = async () => {
    const data = await getDeals(filters);
    setDeals(data);
  };

  const handleFilterChange = (e) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
  };

  const handleDelete = async (id) => {
    if (confirm("Delete this deal?")) {
      await deleteDeal(id);
      fetchDeals();
    }
  };

  const handleViewDeal = (dealId) => {
    if (!selectedTemplate) {
      alert("Please select a template before viewing a deal.");
      return;
    }
    navigate(`/deals/${dealId}/view?templateId=${selectedTemplate}`);
  };

  return (
    <div>
      <div style={styles.header}>
        <h1>Deals</h1>
        <button onClick={() => navigate("/deals/new")} style={styles.btn}>
          + New Deal
        </button>
      </div>

      {/* Template selector - obligatoire */}
      <div style={styles.templateSelector}>
        <label style={styles.label}>Select a template to view deals</label>
        <select
          value={selectedTemplate}
          onChange={(e) => setSelectedTemplate(e.target.value)}
          style={styles.select}
        >
          <option value="">-- Choose a template --</option>
          {templates.map((t) => (
            <option key={t._id} value={t._id}>
              {t.name}
            </option>
          ))}
        </select>
        {!selectedTemplate && (
          <span style={styles.warning}>
            You must select a template to view a deal.
          </span>
        )}
      </div>

      {/* Filters */}
      <div style={styles.filters}>
        <input
          name="clientName"
          value={filters.clientName}
          onChange={handleFilterChange}
          placeholder="Filter by client name"
          style={styles.input}
        />
        <input
          name="startDate"
          type="date"
          value={filters.startDate}
          onChange={handleFilterChange}
          style={styles.input}
        />
        <input
          name="endDate"
          type="date"
          value={filters.endDate}
          onChange={handleFilterChange}
          style={styles.input}
        />
      </div>

      {/* Deals list */}
      <div style={styles.grid}>
        {deals.map((deal) => (
          <div key={deal._id} style={styles.card}>
            <div style={styles.cardHeader}>
              <span style={styles.ref}>{deal.reference}</span>
              <span style={styles.status}>{deal.status}</span>
            </div>
            <h3 style={styles.title}>{deal.title}</h3>
            <p style={styles.client}>{deal.clientName}</p>
            <p style={styles.revenue}>
              {deal.estimatedRevenue?.toLocaleString()} {deal.currency}
            </p>
            <div style={styles.cardActions}>
              <button
                onClick={() => handleViewDeal(deal._id)}
                style={styles.btnPrimary}
              >
                View
              </button>
              <button
                onClick={() => handleDelete(deal._id)}
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
    marginBottom: "1.5rem",
  },
  btn: {
    padding: "0.6rem 1.2rem",
    backgroundColor: "#7c3aed",
    color: "white",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
  },
  templateSelector: {
    backgroundColor: "#1e1e2e",
    padding: "1.5rem",
    borderRadius: "10px",
    marginBottom: "1.5rem",
    display: "flex",
    flexDirection: "column",
    gap: "0.5rem",
  },
  label: { color: "#a9b1d6", fontWeight: "bold" },
  select: {
    padding: "0.7rem",
    borderRadius: "6px",
    border: "1px solid #3b3b5c",
    backgroundColor: "#13131f",
    color: "white",
    fontSize: "1rem",
    maxWidth: "400px",
  },
  warning: {
    color: "#f59e0b",
    fontSize: "0.85rem",
  },
  filters: {
    display: "flex",
    gap: "1rem",
    marginBottom: "1.5rem",
    flexWrap: "wrap",
  },
  input: {
    padding: "0.7rem",
    borderRadius: "6px",
    border: "1px solid #3b3b5c",
    backgroundColor: "#1e1e2e",
    color: "white",
    fontSize: "0.95rem",
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
    marginBottom: "0.5rem",
  },
  ref: { color: "#7c3aed", fontSize: "0.85rem", fontWeight: "bold" },
  status: {
    backgroundColor: "#3b82f6",
    color: "white",
    padding: "2px 8px",
    borderRadius: "12px",
    fontSize: "0.75rem",
  },
  title: { margin: "0 0 0.3rem", fontSize: "1rem" },
  client: { color: "#a9b1d6", fontSize: "0.9rem", margin: "0 0 0.3rem" },
  revenue: { color: "#22c55e", fontSize: "0.9rem", marginBottom: "1rem" },
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