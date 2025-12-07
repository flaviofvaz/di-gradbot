import React, { useState } from 'react';
import { Upload, Trash2, Send, File, MessageSquare, X } from 'lucide-react';

export default function DocumentChatApp() {
  const [activeTab, setActiveTab] = useState('documents');
  const [documents, setDocuments] = useState([]);
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isLoadingDocs, setIsLoadingDocs] = useState(false);
  const [apiConfig, setApiConfig] = useState({
    uploadUrl: 'http://localhost:8000/documents/insert',
    deleteUrl: 'http://localhost:8000/documents/remove',
    chatUrl: 'http://localhost:8000/chat/interact',
    listUrl: 'http://localhost:8000/documents/list'
  });

  // Carregar documentos ao montar o componente
  React.useEffect(() => {
    loadDocuments();
  }, []);

  // Carregar documentos da API
  const loadDocuments = async () => {
    setIsLoadingDocs(true);
    try {
      const response = await fetch(apiConfig.listUrl, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      if (response.ok) {
        const data = await response.json();
        // Espera que a API retorne um array de documentos
        // Formato esperado: [{id, name, size, uploadedAt}, ...]
        setDocuments(data.local_documents || data);
      } else {
        console.error('Erro ao carregar documentos:', response.statusText);
      }
    } catch (error) {
      console.error('Erro na requisição de listagem:', error);
      // Modo demo: mantém documentos vazios ou usa dados mockados
      console.log('Modo demo ativo - usando dados locais');
    } finally {
      setIsLoadingDocs(false);
    }
  };

  // Adicionar documento
  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    setIsLoading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(apiConfig.uploadUrl, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();
        // Após upload bem-sucedido, recarrega a lista de documentos
        await loadDocuments();
        alert('Documento inserido com sucesso!');
      } else {
        console.error('Erro ao fazer upload:', response.statusText);
        alert('Erro ao fazer upload do documento');
      }
    } catch (error) {
      console.error('Erro na requisição:', error);
    } finally {
      setIsLoading(false);
      event.target.value = '';
    }
  };

  // Remover documento
  const handleDeleteDocument = async (docId) => {
    setIsLoading(true);
    try {
      const response = await fetch(`${apiConfig.deleteUrl}?filename=${encodeURIComponent(docId)}`, {
          method: 'POST'
      });

      if (response.ok) {
        // Após deletar, recarrega a lista de documentos
        await loadDocuments();
        alert('Documento removido com sucesso!');
      } else {
        console.error('Erro ao deletar:', response.statusText);
        alert('Erro ao remover documento');
      }
    } catch (error) {
      console.error('Erro na requisição:', error);
    } finally {
      setIsLoading(false);
    }
  };

  // Enviar mensagem
  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
    };

    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch(apiConfig.chatUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedMessages.map(m => ({ role: m.role, content: m.content }))),
      });

      if (response.ok) {
        const data = await response.json();
        const assistantMessage = {
          role: 'assistant',
          content: data.message,
          timestamp: new Date().toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' })
        };
        setMessages([...updatedMessages, assistantMessage]);
      } else {
        console.error('Erro na API:', response.statusText);
        throw new Error('Erro na API');
      }
    } catch (error) {
      console.error('Erro na requisição:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-t-2xl shadow-lg p-6 border-b">
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            GradBot
          </h1>
        </div>

        {/* Tabs */}
        <div className="bg-white shadow-lg flex border-b">
          <button
            onClick={() => setActiveTab('documents')}
            className={`flex-1 py-4 px-6 font-semibold transition-colors ${
              activeTab === 'documents'
                ? 'bg-blue-500 text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            <Upload className="inline-block mr-2" size={20} />
            Gerenciar Documentos
          </button>
          <button
            onClick={() => setActiveTab('chat')}
            className={`flex-1 py-4 px-6 font-semibold transition-colors ${
              activeTab === 'chat'
                ? 'bg-blue-500 text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            }`}
          >
            <MessageSquare className="inline-block mr-2" size={20} />
            Chat
          </button>
        </div>

        {/* Content Area */}
        <div className="bg-white rounded-b-2xl shadow-lg p-6 min-h-[600px]">
          {/* Documents Tab */}
          {activeTab === 'documents' && (
            <div>
              <div className="mb-6">
                <h2 className="text-2xl font-bold text-gray-800 mb-4">
                  Documentos Carregados ({documents.length})
                </h2>
                
                {/* Upload Area */}
                <div className="border-2 border-dashed border-gray-300 rounded-xl p-8 text-center hover:border-blue-400 transition-colors">
                  <input
                    type="file"
                    id="fileUpload"
                    className="hidden"
                    onChange={handleFileUpload}
                    accept=".pdf,.doc,.docx,.txt"
                  />
                  <label
                    htmlFor="fileUpload"
                    className="cursor-pointer flex flex-col items-center"
                  >
                    <Upload size={48} className="text-blue-500 mb-3" />
                    <span className="text-lg font-semibold text-gray-700 mb-1">
                      Clique para fazer upload
                    </span>
                    <span className="text-sm text-gray-500">
                      PDF, DOC, DOCX, TXT
                    </span>
                  </label>
                </div>
              </div>

              {/* Documents List */}
              <div className="space-y-3">
                {isLoading && (
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
                    <div className="flex items-center space-x-3">
                      <div className="animate-spin rounded-full h-5 w-5 border-2 border-blue-500 border-t-transparent"></div>
                      <p className="text-blue-700 font-medium">
                        Processando...
                      </p>
                    </div>
                  </div>
                )}
                {isLoadingDocs ? (
                  <div className="text-center py-12">
                    <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
                    <p className="text-gray-600 mt-4">Carregando documentos...</p>
                  </div>
                ) : documents.length === 0 ? (
                  <div className="text-center py-12 text-gray-400">
                    <File size={64} className="mx-auto mb-4 opacity-50" />
                    <p>Nenhum documento carregado ainda</p>
                  </div>
                ) : (
                  documents.map((fileName, index) => (
                    <div
                      key={index}
                      className="flex items-center justify-between bg-gray-50 p-4 rounded-lg hover:bg-gray-100 transition-colors"
                    >
                      <div className="flex items-center space-x-4">
                        <File size={24} className="text-blue-500" />
                        <div>
                          <p className="font-semibold text-gray-800">{fileName}</p>
                        </div>
                      </div>
                      <button
                        onClick={() => handleDeleteDocument(fileName)}
                        className="p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors"
                        disabled={isLoading}
                      >
                        <Trash2 size={20} />
                      </button>
                    </div>
                  ))
                )}
              </div>

              {/* API Configuration */}
              <div className="mt-8 pt-6 border-t">
                <div className="space-y-3">
                  </div>
                  <button
                    onClick={loadDocuments}
                    className="w-full mt-2 px-4 py-2 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
                  >
                    Reload
                  </button>
              </div>
            </div>
          )}

          {/* Chat Tab */}
          {activeTab === 'chat' && (
            <div className="flex flex-col h-[600px]">
              {/* Messages Area */}
              <div className="flex-1 overflow-y-auto mb-4 space-y-4 p-4 bg-gray-50 rounded-lg">
                {messages.length === 0 ? (
                  <div className="text-center py-12 text-gray-400">
                    <MessageSquare size={64} className="mx-auto mb-4 opacity-50" />
                    <p>Inicie uma conversa</p>
                    <p className="text-sm mt-2">
                      {documents.length} documento(s) disponível(is)
                    </p>
                  </div>
                ) : (
                  messages.map((msg, idx) => (
                    <div
                      key={idx}
                      className={`flex ${
                        msg.role === 'user' ? 'justify-end' : 'justify-start'
                      }`}
                    >
                      <div
                        className={`max-w-[70%] p-4 rounded-2xl ${
                          msg.role === 'user'
                            ? 'bg-blue-500 text-white'
                            : 'bg-white text-gray-800 shadow-md'
                        }`}
                      >
                        <p className="whitespace-pre-wrap">{msg.content}</p>
                        <p
                          className={`text-xs mt-2 ${
                            msg.role === 'user' ? 'text-blue-100' : 'text-gray-400'
                          }`}
                        >
                          {msg.timestamp}
                        </p>
                      </div>
                    </div>
                  ))
                )}
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="bg-white text-gray-800 shadow-md p-4 rounded-2xl">
                      <div className="flex space-x-2">
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Input Area */}
              <div className="flex items-end space-x-3">
                <textarea
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Digite aqui..."
                  className="flex-1 px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
                  rows="3"
                  disabled={isLoading || documents.length === 0}
                />
                <button
                  onClick={handleSendMessage}
                  disabled={isLoading || !inputMessage.trim() || documents.length === 0}
                  className="px-6 py-3 bg-blue-500 text-white rounded-xl hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors flex items-center space-x-2"
                >
                  <Send size={20} />
                  <span>Enviar</span>
                </button>
              </div>
              
              {documents.length === 0 && (
                <p className="text-sm text-red-500 mt-2 text-center">
                  Carregue pelo menos um documento para conversar
                </p>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}