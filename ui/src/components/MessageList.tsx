import React from 'react';
import MessageBubble from './MessageBubble';

interface Message {
  sender: string;
  content: string;
}

interface MessageListProps {
  messages: Message[];
  currentUser: string;
}

const MessageList: React.FC<MessageListProps> = ({ messages, currentUser }) => {
  return (
    <div className="flex flex-col space-y-2">
      {messages.map((msg, index) => (
        <div
          key={index}
          className={`flex ${msg.sender === currentUser ? 'justify-end' : 'justify-start'}`}
        >
          <MessageBubble
            message={msg.content}
            username={msg.sender}
            isOwnMessage={msg.sender === currentUser}
          />
        </div>
      ))}
    </div>
  );
};

export default MessageList;