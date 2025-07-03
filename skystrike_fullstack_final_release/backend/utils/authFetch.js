const authFetch = (url, options = {}) => {
  const storedUser = JSON.parse(localStorage.getItem("skystrikeUser"));
  const token = storedUser?.token;

  // Rewrite login route if necessary
  const fullUrl = url === "/api/login" ? "/api/auth/login" : url;

  return fetch(fullUrl, {
    method: options.method || "GET",
    ...options,
    headers: {
      ...options.headers,
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  });
};

export default authFetch;
