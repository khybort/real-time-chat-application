import React from "react";

interface MessageBubbleProps {
  message: string;
  username: string;
  isOwnMessage: boolean;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({
  message,
  username,
  isOwnMessage,
}) => {
  return (
    <div
      className={`flex ${isOwnMessage ? "justify-end" : "justify-start"} mb-4`}
    >
      <div
        className={`max-w-xs px-4 py-2 rounded-lg shadow-md ${
          isOwnMessage
            ? "bg-blue-600 text-white self-end"
            : "bg-gray-300 text-black self-start"
        }`}
      >
        <p className="text-sm font-semibold">{username}</p>
        <p className="mt-1 text-sm">{message}</p>
      </div>
    </div>
  );
};

export default MessageBubble;
