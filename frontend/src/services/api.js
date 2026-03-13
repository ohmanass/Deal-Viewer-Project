const BASE_URL = "http://localhost:8000";

// --- Templates ---

export const getTemplates = async () => {
  const res = await fetch(`${BASE_URL}/templates`);
  return res.json();
};

export const getTemplate = async (id) => {
  const res = await fetch(`${BASE_URL}/templates/${id}`);
  return res.json();
};

export const createTemplate = async (data) => {
  const res = await fetch(`${BASE_URL}/templates`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
};

export const deleteTemplate = async (id) => {
  await fetch(`${BASE_URL}/templates/${id}`, { method: "DELETE" });
};

// --- Deals ---

export const getDeals = async (filters = {}) => {
  const params = new URLSearchParams();
  if (filters.clientName) params.append("clientName", filters.clientName);
  if (filters.startDate) params.append("startDate", filters.startDate);
  if (filters.endDate) params.append("endDate", filters.endDate);
  const res = await fetch(`${BASE_URL}/deals?${params.toString()}`);
  return res.json();
};

export const getDeal = async (id) => {
  const res = await fetch(`${BASE_URL}/deals/${id}`);
  return res.json();
};

export const createDeal = async (data) => {
  const res = await fetch(`${BASE_URL}/deals`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
};

export const deleteDeal = async (id) => {
  await fetch(`${BASE_URL}/deals/${id}`, { method: "DELETE" });
};

export const viewDealWithTemplate = async (dealId, templateId) => {
  const res = await fetch(
    `${BASE_URL}/deals/${dealId}/view?templateId=${templateId}`
  );
  return res.json();
};