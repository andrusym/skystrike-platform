
import React, { useEffect, useState } from "react";
import authFetch from "../utils/authFetch";

const AdminPage = () => {
  const [users, setUsers] = useState([]);
  const [audit, setAudit] = useState([]);

  useEffect(() => {
    authFetch("/api/admin/users").then(setUsers);
    authFetch("/api/admin/audit").then(setAudit);
  }, []);

  return (
    <div>
      <h2>Users</h2>
      <pre>{JSON.stringify(users, null, 2)}</pre>
      <h2>Audit Log</h2>
      <pre>{JSON.stringify(audit, null, 2)}</pre>
    </div>
  );
};

export default AdminPage;
