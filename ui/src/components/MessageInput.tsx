import React, { useState } from 'react';

interface MessageInputProps {
  onSend: (message: string) => void;
}

const MessageInput: React.FC<MessageInputProps> = ({ onSend }) => {
  const [message, setMessage] = useState('');

  const handleSend = () => {
    if (message.trim()) {
      onSend(message);
      setMessage('');
    }
  };

  return (
    <div className="flex items-center space-x-2">
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Type a message"
        className="flex-1 border rounded px-4 py-2 shadow-sm focus:outline-none focus:ring focus:border-blue-300"
      />
      <button
        onClick={handleSend}
        className="bg-blue-600 text-black px-4 py-2 rounded shadow hover:bg-blue-700"
      >
        Send
      </button>
    </div>
  );
};

export default MessageInput;
