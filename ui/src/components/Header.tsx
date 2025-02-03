import React, { useState } from "react";
import avatar from "../../src/assets/abc.png";

const Header: React.FC = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const userData = localStorage.getItem("user");
  const parsedUserData = userData ? JSON.parse(userData) : {};
  const user = {
    username: parsedUserData.username || "Guest",
    avatarUrl: avatar,
  };

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const handleLogout = () => {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    localStorage.removeItem("user");
    window.location.href = "/login";
  };

  return (
    <header className="bg-gray-600 text-white py-4 px-6 shadow-md flex items-center justify-between">
      <h1 className="text-xl font-bold ">Real Time Chat App</h1>

      <div className="relative">
        <button onClick={toggleMenu} className="flex items-center space-x-2">
          <img
            src={user.avatarUrl}
            alt="Avatar"
            className="w-8 h-8 rounded-full"
          />
          <span className="text-black">{user.username}</span>
        </button>

        {isMenuOpen && (
          <div className="absolute right-0 mt-2 bg-white text-black rounded-md shadow-md w-48 py-2">
            <button
              onClick={handleLogout}
              className="block w-full text-left px-4 py-2 hover:bg-gray-100"
            >
              Logout
            </button>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;
