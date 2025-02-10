import React, { useState, useEffect } from "react";
import API from "../services/api";

interface SidebarProps {
  activeRoom: string;
  changeRoom: (room: string) => void;
}
interface Room {
  id: number;
  name: string;
  members: any[];
  created_at: string;
}

const Sidebar: React.FC<SidebarProps> = ({ activeRoom, changeRoom }) => {
  const [rooms, setRooms] = useState<Room[]>([]);
  const [loading, setLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newRoomName, setNewRoomName] = useState("");

  useEffect(() => {
    const fetchRooms = async () => {
      setLoading(true);

      try {
        const response = await API.get("/chat/rooms/");
        const data = await response.data;
        setRooms(Array.isArray(data) ? data : []);
      } catch (error) {
        console.error("Error fetching rooms:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchRooms();
  }, []);

  const handleCreateRoom = async () => {
    if (!newRoomName.trim()) return;

    try {
      const response = await API.post("/chat/rooms/", {
        name: newRoomName,
      });
      if (response.data) {
        const data: Room = response.data;
        setRooms((prevRooms) => [...prevRooms, data]);
        changeRoom(newRoomName);
        setIsModalOpen(false);
        setNewRoomName("");
      } else {
        console.error("Error creating room:", response.statusText);
      }
    } catch (error) {
      console.error("Error creating room:", error);
    }
  };

  return (
    <div className="bg-gray-800 text-white w-64 p-4 space-y-4 ">
      <h2 className="text-lg font-bold">Chat Rooms</h2>
      <ul className="space-y-2">
        {loading ? (
          <li>Loading...</li>
        ) : (
          rooms.map((room: Room) => (
            <li
              key={room.name}
              onClick={() => changeRoom(room.name)}
              className={`cursor-pointer p-2 rounded ${
                activeRoom === room.name ? "bg-blue-600" : "hover:bg-gray-700"
              }`}
            >
              {room.name}
            </li>
          )) || <div>No rooms available</div>
        )}
      </ul>

      <div className="flex justify-center">
        <button
          onClick={() => setIsModalOpen(true)}
          className="bg-blue-500 hover:bg-blue-700 text-black font-bold py-2 px-4 rounded"
        >
          Create Room
        </button>
      </div>

      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center">
          <div 
            className="fixed inset-0 bg-black opacity-50"
            onClick={() => setIsModalOpen(false)}
          ></div>
          <div className="bg-white p-6 rounded-lg shadow-lg w-80 z-50">
            <h3 className="text-lg font-semibold text-gray-800 mb-4">
              Create a New Room
            </h3>

            <input
              type="text"
              value={newRoomName}
              onChange={(e) => setNewRoomName(e.target.value)}
              placeholder="Enter room name"
              className="w-full p-2 border border-gray-300 rounded mb-4 text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500"
              autoFocus
            />

            <div className="flex justify-end space-x-2">
              <button
                onClick={() => setIsModalOpen(false)}
                className="px-4 py-2 text-gray-600 hover:text-gray-800 font-medium"
              >
                Cancel
              </button>
              <button
                onClick={handleCreateRoom}
                className="px-4 py-2 bg-blue-500 text-black rounded hover:bg-blue-600 font-medium"
              >
                Create
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Sidebar;
