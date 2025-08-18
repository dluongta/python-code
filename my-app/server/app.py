from flask import Flask, request, jsonify
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from flask_cors import CORS  # Đảm bảo đã import CORS

# Khởi tạo Flask app và mô hình AI
app = Flask(__name__)

# Cho phép CORS cho tất cả các nguồn gốc
CORS(app)

# Tải mô hình và tokenizer của DialoGPT
tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")

# Khởi tạo biến lưu trữ lịch sử cuộc trò chuyện
chat_history_ids = None

def get_chat_response(text):
    """
    Generate a chatbot response using Microsoft DialoGPT.

    Args:
        text (str): The input text from the user.

    Returns:
        str: The generated response from the chatbot.
    """
    global chat_history_ids

    # encode the new user input, add the eos_token and return a tensor in Pytorch
    new_user_input_ids = tokenizer.encode(str(text) + tokenizer.eos_token, return_tensors="pt")

    # append the new user input tokens to the chat history
    if chat_history_ids is not None:
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1)
    else:
        bot_input_ids = new_user_input_ids

    # generate a response while limiting the total chat history to 1000 tokens
    chat_history_ids = model.generate(
        bot_input_ids, 
        max_length=5000,  # Giới hạn độ dài của cuộc trò chuyện (số token)
        temperature=1.0,  # Điều chỉnh độ sáng tạo của mô hình
        top_k=50,         # Sử dụng 50 từ có khả năng cao nhất
        top_p=0.95,       # Sampling theo phân phối xác suất
        pad_token_id=tokenizer.eos_token_id
    )

    # Trả về phản hồi (giải mã các token thành chuỗi văn bản)
    return tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)

@app.route("/chat", methods=["POST"])
def chat():
    # Lấy câu hỏi từ người dùng
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Lấy phản hồi từ hàm get_Chat_response
    bot_response = get_chat_response(user_input)

    # Trả về phản hồi cho người dùng
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # Bật chế độ debug và auto-reload
