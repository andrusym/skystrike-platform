export async function fetchDashboardData() {
  try {
    const res = await fetch(`${import.meta.env.VITE_API_BASE_URL}/dashboard`);
    if (!res.ok) throw new Error(`Server error: ${res.status}`);
    return await res.json();
  } catch (err) {
    console.error('[API] Dashboard fetch failed:', err);
    throw err;
  }
}

export default dashboard;
