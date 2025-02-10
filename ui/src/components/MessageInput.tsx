import React, { useState } from "react";

interface MessageInputProps {
  onSend: (message: string) => void;
  onTyping: (typing: boolean) => void;
}

const MessageInput: React.FC<MessageInputProps> = ({ onSend, onTyping }) => {
  const [message, setMessage] = useState("");

  const handleSend = () => {
    if (message.trim()) {
      onSend(message);
      setMessage("");
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setMessage(e.target.value);
    if (e.target.value.trim()) {
      onTyping(true);
    } else {
      onTyping(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter") {
      handleSend();
    }
  };

  return (
    <div className="flex gap-2">
      <input
        type="text"
        value={message}
        onChange={handleChange}
        onKeyDown={handleKeyDown}
        className="flex-1 p-2 border rounded-lg"
        placeholder="Type a message..."
      />
      <button
        onClick={handleSend}
        className="px-4 py-2 bg-blue-500 text-black rounded-lg hover:bg-blue-600"
      >
        Send
      </button>
    </div>
  );
};

export default MessageInput;
