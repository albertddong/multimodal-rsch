/* Sidebar Component */
import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPlus, faTimes } from '@fortawesome/free-solid-svg-icons'; // Import FontAwesome plus and times icon

const Sidebar = ({ chatHistory, currentChatIndex, handleChatSelect, handleNewChat, handleDeleteChat }) => {
  return (
    <div className="sidebar">
      <h2>Chat History</h2>
      <button onClick={handleNewChat} className="new-chat-button">
        <FontAwesomeIcon icon={faPlus} style={{ color: 'white', marginRight: '5px' }} />
        New Chat
      </button>
      <ul>
        {chatHistory.map((chat, index) => (
          <li key={index} className={`chat-item ${currentChatIndex === index ? 'selected' : ''}`}>
            <div className="chat-summary" onClick={() => handleChatSelect(chat, index)}>
              {chat.summary}
            </div>
            <button className="delete-button" onClick={(e) => {
              e.stopPropagation(); // Prevent click from selecting chat
              handleDeleteChat(index);
            }}>
              <FontAwesomeIcon icon={faTimes} />
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Sidebar;