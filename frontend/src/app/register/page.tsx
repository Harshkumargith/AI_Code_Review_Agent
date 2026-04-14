"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";

export default function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();

  const handleRegister = () => {
    if (!email || !password) {
      alert("Fill all fields");
      return;
    }

    localStorage.setItem(
      "user",
      JSON.stringify({ email, password })
    );

    alert("Registered successfully!");
    router.replace("/login");
  };

  return (
    <main className="min-h-screen flex items-center justify-center bg-black text-white">
      <div className="bg-white/10 p-8 rounded-xl w-96">
        <h2 className="text-2xl font-bold mb-6 text-center">Register</h2>

        <input
          type="email"
          placeholder="Email"
          className="w-full mb-3 p-2 bg-black rounded"
          onChange={(e) => setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          className="w-full mb-4 p-2 bg-black rounded"
          onChange={(e) => setPassword(e.target.value)}
        />

        <button
          onClick={handleRegister}
          className="w-full bg-green-600 py-2 rounded"
        >
          Register
        </button>
      </div>
    </main>
  );
}