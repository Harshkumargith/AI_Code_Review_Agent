"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const router = useRouter();


  useEffect(() => {
    if (localStorage.getItem("isLoggedIn")) {
      router.replace("/");
    }
  }, []);

  const handleLogin = () => {
    const user = JSON.parse(localStorage.getItem("user") || "{}");

    if (user.email === email && user.password === password) {
      localStorage.setItem("isLoggedIn", "true");
      router.replace("/");
    } else {
      alert("Invalid credentials");
    }
  };

  return (
    <main className="min-h-screen flex items-center justify-center bg-black text-white">
      <div className="bg-white/10 p-8 rounded-xl w-96">
        <h2 className="text-2xl font-bold mb-6 text-center">Login</h2>

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
          onClick={handleLogin}
          className="w-full bg-blue-600 py-2 rounded"
        >
          Login
        </button>

        <p className="text-sm mt-4 text-center">
          Don’t have an account?{" "}
          <span
            className="text-blue-400 cursor-pointer"
            onClick={() => router.push("/register")}
          >
            Register
          </span>
        </p>
      </div>
    </main>
  );
}