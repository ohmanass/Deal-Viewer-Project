import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav style={styles.nav}>
      <span style={styles.brand}>🗂 Deal Viewer</span>
      <div style={styles.links}>
        <Link to="/templates" style={styles.link}>Templates</Link>
        <Link to="/deals" style={styles.link}>Deals</Link>
      </div>
    </nav>
  );
}

const styles = {
  nav: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "1rem 2rem",
    backgroundColor: "#1e1e2e",
    color: "white",
  },
  brand: {
    fontSize: "1.3rem",
    fontWeight: "bold",
  },
  links: {
    display: "flex",
    gap: "1.5rem",
  },
  link: {
    color: "#a9b1d6",
    textDecoration: "none",
    fontSize: "1rem",
  },
};