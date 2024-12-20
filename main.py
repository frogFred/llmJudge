from package.use import llama3

Question = str("總統是習近平嗎?")
resLlama = llama3(Question)

#####確保回傳有content#####
if resLlama.message and hasattr(resLlama.message, 'content'):
    content = resLlama.message.content
    print(content)
else:
    print("無法取得 content 資料")

