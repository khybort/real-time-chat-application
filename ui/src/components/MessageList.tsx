import React, { useEffect, useRef } from "react";

interface Message {
  sender: string;
  message: string;
}

interface MessageListProps {
  messages: Message[];
  currentUser: string;
  typingUsers: string[];
}

const MessageList: React.FC<MessageListProps> = ({
  messages,
  currentUser,
  typingUsers,
}) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, typingUsers]);

  const otherTypingUsers = typingUsers.filter(
    (sender) => sender !== currentUser,
  );

  const formatTypingText = (users: string[]) => {
    if (users.length === 0) return "";
    if (users.length === 1) return `${users[0]} is typing...`;
    if (users.length === 2) return `${users[0]} and ${users[1]} are typing...`;
    const lastUser = users[users.length - 1];
    const otherUsers = users.slice(0, -1);
    return `${otherUsers.join(", ")} and ${lastUser} are typing...`;
  };

  return (
    <div className="flex flex-col gap-2 overflow-y-auto h-full relative">
      <div className="flex-1">
        {messages.map((message, index) => (
        <div
            key={index}
            className={`flex ${message.sender === currentUser ? "justify-end" : "justify-start"} mb-2`}
          >
            <div
              className={`max-w-[80%] rounded-lg p-2 ${message.sender === currentUser ? "bg-blue-500 text-white" : "bg-gray-200"}`}
            >
              <div className="font-medium text-sm">{message.sender}</div>
              <div>{message.message}</div>
            </div>
          </div>
        ))}
      </div>
      {otherTypingUsers.length > 0 && (
        <div className="sticky bottom-0 left-0 w-full p-2">
          <div className="flex justify-start">
            <div className="max-w-[80%] rounded-lg p-2 bg-gray-200 text-sm text-gray-600">
              <div>{formatTypingText(otherTypingUsers)}</div>
            </div>
          </div>
        </div>
      )}
      <div ref={messagesEndRef} />
    </div>
  );
};

export default MessageList;
