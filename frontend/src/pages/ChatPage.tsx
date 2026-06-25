import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { documentService, chatService } from "../services/api";
import { PageHeader } from "../components/shared/PageHeader";
import { Card, CardContent } from "../components/ui/card";
import { Button } from "../components/ui/button";
import { Input } from "../components/ui/input";
import { Send, Bot, User, Loader2 } from "lucide-react";
import type { ChatMessage } from "../types";

export function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [selectedDocId, setSelectedDocId] = useState<string>("");

  const { data: documents } = useQuery({
    queryKey: ['documents'],
    queryFn: documentService.getDocuments
  });

  const indexedDocs = documents?.filter(d => d.indexed) || [];

  const handleSend = async () => {
    if (!input.trim() || !selectedDocId) return;

    const userMessage: ChatMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput("");
    setIsTyping(true);

    try {
      const response = await chatService.ragChat(selectedDocId, userMessage.content);
      const aiMessage: ChatMessage = { role: 'assistant', content: response.data.answer };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Sorry, I encountered an error while processing your request.' }]);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-10rem)]">
      <PageHeader 
        title="RAG Chat" 
        description="Ask questions directly to your indexed documents."
      />

      <div className="mb-4">
        <select 
          className="flex h-10 w-[300px] rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          value={selectedDocId}
          onChange={(e) => setSelectedDocId(e.target.value)}
        >
          <option value="" disabled>Select an indexed document</option>
          {indexedDocs.map(doc => (
            <option key={doc.id} value={doc.id}>{doc.filename}</option>
          ))}
        </select>
      </div>

      <Card className="flex-1 flex flex-col overflow-hidden">
        <CardContent className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 ? (
            <div className="flex h-full items-center justify-center text-muted-foreground">
              Select a document and ask a question to begin.
            </div>
          ) : (
            messages.map((msg, idx) => (
              <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`flex max-w-[80%] items-start space-x-3 rounded-lg p-4 ${msg.role === 'user' ? 'bg-primary text-primary-foreground' : 'bg-secondary'}`}>
                  {msg.role === 'assistant' ? <Bot className="h-5 w-5 mt-1" /> : <User className="h-5 w-5 mt-1" />}
                  <div className="text-sm">{msg.content}</div>
                </div>
              </div>
            ))
          )}
          {isTyping && (
             <div className="flex justify-start">
               <div className="flex items-center space-x-2 rounded-lg bg-secondary p-4">
                 <Loader2 className="h-4 w-4 animate-spin" />
                 <span className="text-sm">AI is thinking...</span>
               </div>
             </div>
          )}
        </CardContent>
        <div className="p-4 border-t bg-card">
          <form 
            onSubmit={(e) => { e.preventDefault(); handleSend(); }}
            className="flex items-center space-x-2"
          >
            <Input 
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={selectedDocId ? "Ask a question..." : "Select a document first"}
              disabled={!selectedDocId || isTyping}
            />
            <Button type="submit" disabled={!selectedDocId || isTyping || !input.trim()}>
              <Send className="h-4 w-4" />
            </Button>
          </form>
        </div>
      </Card>
    </div>
  );
}
