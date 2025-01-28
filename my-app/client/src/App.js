import React, { useState } from "react";
import axios from "axios";
import './App.css'; // Đảm bảo rằng bạn đã tạo và áp dụng file CSS này

function App() {
  const [message, setMessage] = useState("");
  const [response, setResponse] = useState("");
  const [isLoading, setIsLoading] = useState(false);  // Thêm trạng thái loading
  const [error, setError] = useState(null);  // Thêm trạng thái lỗi

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);  // Khi bắt đầu gửi yêu cầu, đặt trạng thái loading là true
    setError(null);  // Reset lỗi trước khi gửi yêu cầu

    try {
      // Gửi yêu cầu POST đến Flask backend
      const res = await axios.post("http://localhost:5000/chat", {
        message: message,
      });
      setResponse(res.data.response);  // Lưu phản hồi vào trạng thái
    } catch (error) {
      console.error("Error during API call:", error);
      setError("Có lỗi xảy ra. Vui lòng thử lại.");  // Hiển thị thông báo lỗi nếu có
    } finally {
      setIsLoading(false);  // Sau khi hoàn thành yêu cầu (thành công hoặc thất bại), đặt loading là false
    }
  };

  return (
    <div className="app-container">
      <div className="chat-box">
        <h1>Chatbot</h1>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Nhập câu hỏi của bạn..."
            className="input-field"
          />
          <button type="submit" className="submit-button" disabled={isLoading}>
            {isLoading ? "Đang gửi..." : "Gửi"} {/* Hiển thị trạng thái khi gửi yêu cầu */}
          </button>
        </form>

        {/* Hiển thị thông báo lỗi nếu có */}
        {error && <p className="error-message">{error}</p>}

        {/* Hiển thị phản hồi từ chatbot */}
        <div className="response-container">
          <p className="response">{response}</p>
        </div>
      </div>
    </div>
  );
}

export default App;
