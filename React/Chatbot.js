import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faPaperPlane, faPaperclip, faTimes } from '@fortawesome/free-solid-svg-icons';
import Sidebar from './Sidebar';
import './Chatbot.css';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [file, setFile] = useState(null);
  const [chatHistory, setChatHistory] = useState([]);
  const [currentChatIndex, setCurrentChatIndex] = useState(null);
  const fileInputRef = useRef(null);
  const textareaRef = useRef(null);

  useEffect(() => {
    const initialChat = [{ id: 1, summary: 'Chat 1', messages: [] }];
    setChatHistory(initialChat);
    setCurrentChatIndex(0);
    setMessages(initialChat[0].messages);
  }, []);

  const saveCurrentChatMessages = () => {
    if (currentChatIndex !== null && chatHistory[currentChatIndex]) {
      const updatedChatHistory = [...chatHistory];
      updatedChatHistory[currentChatIndex].messages = messages;
      setChatHistory(updatedChatHistory);
    }
  };

  const handleChatSelect = (chat, index) => {
    saveCurrentChatMessages();
    setMessages(chat.messages);
    setCurrentChatIndex(index);
  };

  const handleNewChat = () => {
    saveCurrentChatMessages();
    const newChat = {
      id: chatHistory.length + 1,
      summary: `Chat ${chatHistory.length + 1}`,
      messages: []
    };
    setChatHistory([...chatHistory, newChat]);
    setMessages([]);
    setCurrentChatIndex(chatHistory.length);
  };

  const handleDeleteChat = (index) => {
    saveCurrentChatMessages();
    const updatedChatHistory = chatHistory.filter((_, i) => i !== index);
  
    if (updatedChatHistory.length === 0) {
      setMessages([]);
      setCurrentChatIndex(null);
    } else if (index === currentChatIndex) {
      // If the current chat is being deleted, select the first remaining chat
      if (index === chatHistory.length-1) {
        setCurrentChatIndex(index-1);
        setMessages(updatedChatHistory[index-1].messages);
      }
      else {
        setCurrentChatIndex(index);
        setMessages(updatedChatHistory[index].messages);
      }
    } else if (index < currentChatIndex) {
      // If a chat before the current chat is deleted, adjust the current chat index
      setCurrentChatIndex(currentChatIndex - 1);
    }
  
    setChatHistory(updatedChatHistory);
  };

  const sendMessage = async () => {
    if (input.trim() || file) {
      if (currentChatIndex === null) {
        handleNewChat();
      }
  
      const fileUrl = file ? URL.createObjectURL(file) : null;
      const fileType = file ? file.type.split('/')[0] : null;
      const newMessage = { text: input, sender: 'user', file: fileUrl, fileType, fileName: file ? file.name : null };
      setMessages([...messages, newMessage]);
  
      // Placeholder bot response
      const placeholderMessage = { text: '...', sender: 'bot', placeholder: true };
      setMessages((prevMessages) => [...prevMessages, placeholderMessage]);
  
      try {
        const formData = new FormData();
        formData.append('message', input);
        if (file) formData.append('file', file);
  
        const response = await axios.post('YOUR_CHATBOT_API_URL', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
  
        // Replace placeholder message with actual response
        setMessages((prevMessages) => {
          const updatedMessages = [...prevMessages];
          const placeholderIndex = updatedMessages.findIndex(msg => msg.placeholder);
          if (placeholderIndex !== -1) {
            updatedMessages[placeholderIndex] = { text: response.data.message, sender: 'bot' };
          }
          return updatedMessages;
        });
      } catch (error) {
        console.error('Error sending message:', error);
      }
  
      setInput('');
      setFile(null);
      resizeTextarea();
    }
  };
  

  const handleInputChange = (e) => {
    setInput(e.target.value);
    resizeTextarea();
  };

  const handleFileInputChange = () => {
    const selectedFile = fileInputRef.current.files[0];
    setFile(selectedFile);
  };

  const handleFileClear = () => {
    setFile(null);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const resizeTextarea = () => {
    const textarea = textareaRef.current;
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
  };

  useEffect(() => {
    const messagesContainer = document.querySelector('.messages');
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }, [messages]);

  return (
    <div className="chatbot-container">
      <Sidebar 
        chatHistory={chatHistory} 
        currentChatIndex={currentChatIndex}
        handleChatSelect={handleChatSelect} 
        handleNewChat={handleNewChat} 
        handleDeleteChat={handleDeleteChat}
      />
      <div className="chatbot">
        <div className="messages">
          {messages.map((message, index) => (
            <div key={index} className={`message ${message.sender}`}>
              <div>{message.text}</div>
              {message.file && message.fileType === 'image' && (
                <img src={message.file} alt="uploaded" style={{ maxWidth: '100%', maxHeight: '200px', marginTop: '10px' }} />
              )}
              {message.file && message.fileType === 'audio' && (
                <audio controls style={{ marginTop: '10px' }}>
                  <source src={message.file} type={file?.type} />
                  Your browser does not support the audio element.
                </audio>
              )}
              {message.file && message.fileType === 'video' && (
                <video controls style={{ maxWidth: '100%', maxHeight: '200px', marginTop: '10px' }}>
                  <source src={message.file} type={file?.type} />
                  Your browser does not support the video element.
                </video>
              )}
              {message.file && !['image', 'audio', 'video'].includes(message.fileType) && (
                <div style={{ marginTop: '10px' }}><a href={message.file} target="_blank" rel="noopener noreferrer">View file</a></div>
              )}
            </div>
          ))}
        </div>
        {file && (
          <div className="file-attachment">
            <FontAwesomeIcon icon={faPaperclip} className="file-icon" />
            <span>{file.name}</span>
            <button onClick={handleFileClear} className="clear-button">
              <FontAwesomeIcon icon={faTimes} />
            </button>
          </div>
        )}
        <div className="input-bar">
          <label className="file-input-label">
            <FontAwesomeIcon icon={faPaperclip} className="file-input-icon" />
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileInputChange}
              style={{ display: 'none' }}
            />
          </label>
          <textarea
            ref={textareaRef}
            value={input}
            onChange={handleInputChange}
            onKeyPress={handleKeyPress}
            placeholder="Type a message..."
            rows={1}
            style={{ overflow: 'hidden', resize: 'none', flex: 1 }}
          />
          <button onClick={sendMessage} className="send-button">
            <FontAwesomeIcon icon={faPaperPlane} />
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chatbot;
