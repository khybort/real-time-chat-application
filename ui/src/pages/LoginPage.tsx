import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../services/api";
import { useChatStore } from "../store/chatStore";

const LoginPage: React.FC = () => {
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const setUser = useChatStore((state) => state.setUser);
  const navigate = useNavigate();

  const handleLogin = async () => {
    if (!username.trim() || !password.trim()) {
      alert("Please fill in both fields.");
      return;
    }

    try {
      const response = await API.post("/auth/login/", { username, password });
      const { access, refresh, user } = response.data;
      localStorage.setItem("access", access);
      localStorage.setItem("refresh", refresh);
      localStorage.setItem("user", JSON.stringify(user));
      setUser(username);
      navigate("/chat");
    } catch (error) {
      alert("Invalid username or password.");
    }
  };

  return (
    <div className="flex items-center justify-center w-screen h-screen bg-gray-100">
      <div className="bg-white w-full max-w-4xl p-12 shadow-xl rounded-lg">
        <h1 className="text-4xl font-bold text-center mb-6 text-gray-800">
          Welcome Back!
        </h1>
        <p className="text-center text-gray-500 mb-8">
          Please login to access your account
        </p>
        <div className="space-y-6">
          <input
            type="text"
            placeholder="Enter your username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full p-4 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <input
            type="password"
            placeholder="Enter your password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full p-4 border rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
        <button
          onClick={handleLogin}
          className="mt-6 w-full bg-blue-500 text-black py-4 rounded-md hover:bg-blue-600 transition duration-200"
        >
          Login
        </button>
        <div className="mt-4 text-center">
          <span className="text-gray-600">Don't have an account?</span>{" "}
          <button
            onClick={() => navigate("/register")}
            className="text-blue-500 hover:underline"
          >
            Register
          </button>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;
