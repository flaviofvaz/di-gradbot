import React, { useState } from "react";
import { motion } from "framer-motion";

function formatTimestamp() {
  const d = new Date();
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  const time = d.toLocaleTimeString();
  return `${year}-${month}-${day} ${time}`;
}

export default function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [timestamps, setTimestamps] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { user: input }];
    setMessages(newMessages);

    setTimestamps([...timestamps, formatTimestamp()]);
    
    setInput("");
    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/chat/interact", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(newMessages)
      });

      const data = await response.json();
      setMessages([...newMessages, { bot: data.message }]); // 
      setTimestamps(prev => [...prev, formatTimestamp()]);
    } catch (error) {
      console.error("API error", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6 flex flex-col items-center">
      <div className="w-full max-w-2xl bg-white shadow-xl rounded-2xl p-4 flex flex-col gap-4">
        
        {/* Messages */}
        <div className="flex flex-col gap-3 max-h-[60vh] overflow-y-auto pr-2">
          {
            messages.map((msg, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.2 }}
                className={`p-3 rounded-2xl shadow text-sm max-w-[80%] ${
                  msg.user ? "bg-blue-100 self-end" : "bg-gray-200 self-start"
                }`}
              >
                <div className="text-sm">
                  <span className="text-xs font-semibold opacity-70">
                    {timestamps[idx]} — {msg.user ? "user" : "gradbot"}:
                  </span>{" "}
                  {msg.user || msg.bot}
                </div>
              </motion.div>
          ))}
        </div>

        {/* Input bar */}
        <div className="flex items-center gap-2 pt-2">
          <input
            className="flex-1 border border-gray-300 rounded-xl px-3 py-2"
            placeholder="Type a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <button
            className="bg-blue-600 text-white px-4 py-2 rounded-xl shadow"
            onClick={sendMessage}
            disabled={loading}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
