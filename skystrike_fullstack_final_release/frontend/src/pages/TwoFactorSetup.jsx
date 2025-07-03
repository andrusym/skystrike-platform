import React, { useEffect, useState } from "react";
import authFetch from "../utils/authFetch";

const TwoFactorSetup = () => {
  const [qr, setQr] = useState(null);
  const [code, setCode] = useState("");
  const [verified, setVerified] = useState(false);

  useEffect(() => {
    authFetch("/api/user/2fa/setup").then((res) => res.json()).then((data) => {
      setQr(data.qr);
    });
  }, []);

  const handleVerify = () => {
    authFetch("/api/user/2fa/verify", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ token: code })
    }).then(() => setVerified(true));
  };

  return (
    <div className="p-4 max-w-lg mx-auto">
      <h1 className="text-xl font-bold mb-4">2FA Setup</h1>
      {qr && <img src={qr} alt="QR Code" className="mb-4" />}
      <input className="border p-2 w-full mb-2" value={code} onChange={(e) => setCode(e.target.value)} placeholder="Enter 6-digit code" />
      <button onClick={handleVerify} className="bg-blue-600 text-white px-4 py-2 rounded">Verify</button>
      {verified && <div className="text-green-600 mt-2">✅ 2FA Enabled!</div>}
    </div>
  );
};

export default TwoFactorSetup;