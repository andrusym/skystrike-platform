// utils/authFetch.js

const authFetch = async (url, options = {}) => {
  try {
    const user = JSON.parse(localStorage.getItem("skystrikeUser"));
    const token = user?.token;

    const headers = {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...(options.headers || {}),
    };

    const response = await fetch(url, { ...options, headers });

    const contentType = response.headers.get("content-type");
    const isJson = contentType && contentType.includes("application/json");
    const responseBody = isJson ? await response.json() : await response.text();

    if (!response.ok) {
      console.error("AuthFetch Error:", response.status, responseBody);
      throw new Error(`Request failed: ${response.status} - ${JSON.stringify(responseBody)}`);
    }

    return responseBody;
  } catch (err) {
    console.error("authFetch exception:", err);
    throw err;
  }
};

export default authFetch;
