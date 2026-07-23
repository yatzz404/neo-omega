@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'response': '⚠️ Invalid request'}), 400

        user_message = data['message'].strip()
        if not user_message:
            return jsonify({'response': '⚠️ Message cannot be empty'}), 400

        # === RESPONSE SEDERHANA ===
        msg = user_message.lower()
        
        if 'help' in msg or 'bantuan' in msg:
            response = """📋 **Menu NEO-OMEGA by YATZZ:**
• `halo` - Sapaan
• `nama kamu` - Nama AI
• `waktu` - Jam sekarang
• `tanggal` - Tanggal sekarang
• `2+2` - Hitung matematika
• `help` - Menu ini"""
        
        elif 'nama' in msg or 'siapa' in msg:
            response = "🤖 Saya **NEO-OMEGA** by **YATZZ**!"
        
        elif 'halo' in msg or 'hai' in msg or 'hey' in msg:
            response = "Halo juga! Ada yang bisa dibantu? 👋"
        
        elif 'waktu' in msg or 'jam' in msg:
            from datetime import datetime
            response = f"🕐 Sekarang: {datetime.now().strftime('%H:%M:%S')}"
        
        elif 'tanggal' in msg or 'date' in msg:
            from datetime import datetime
            response = f"📅 Tanggal: {datetime.now().strftime('%d %B %Y')}"
        
        elif any(op in msg for op in ['+', '-', '*', '/']):
            try:
                # Hanya angka dan operator
                import re
                if re.match(r'^[\d+\-*/.() ]+$', msg):
                    result = eval(msg)
                    response = f"📝 Hasil: **{result}**"
                else:
                    response = "⚠️ Hanya operasi matematika dasar"
            except:
                response = "⚠️ Gagal menghitung"
        
        else:
            response = f"📝 Pesan: '{user_message}'\n\nKetik **help** untuk menu lengkap!"
        
        return jsonify({'response': response})
    
    except Exception as e:
        print(f"Error: {e}")  # Ini akan muncul di logs
        return jsonify({'response': f'⚠️ Error: {str(e)}'}), 500
