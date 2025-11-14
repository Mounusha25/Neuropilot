import { useState, useEffect, useRef } from 'react'
import './App.css'

function App() {
  const [sessionId, setSessionId] = useState(null)
  const [messages, setMessages] = useState([])
  const [isRecording, setIsRecording] = useState(false)
  const [isProcessing, setIsProcessing] = useState(false)
  const [messageCount, setMessageCount] = useState(0)
  const [error, setError] = useState(null)
  const [feedback, setFeedback] = useState(null)
  const [quiz, setQuiz] = useState(null)
  const [pendingQuiz, setPendingQuiz] = useState(null) // Store quiz until audio finishes
  const [selectedAnswer, setSelectedAnswer] = useState(null)
  const [quizResult, setQuizResult] = useState(null)
  const [quizSubmitted, setQuizSubmitted] = useState(false) // Track if quiz was submitted
  const [overallSummary, setOverallSummary] = useState(null) // Overall feedback at end
  
  const mediaRecorderRef = useRef(null)
  const audioChunksRef = useRef([])
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const startConversation = async () => {
    setIsProcessing(true)
    setError(null)
    
    try {
      const formData = new FormData()
      formData.append('user_name', 'User')
      
      const response = await fetch('/api/audio/start', {
        method: 'POST',
        body: formData
      })
      
      const data = await response.json()
      setSessionId(data.session_id)
      setMessageCount(0)
      
      setMessages([{
        role: 'assistant',
        text: data.ai_text_response,
        timestamp: new Date()
      }])
      
      if (data.audio_response) {
        playAudio(data.audio_response)
      }
    } catch (err) {
      setError('Failed to start conversation: ' + err.message)
    } finally {
      setIsProcessing(false)
    }
  }

  const startRecording = async () => {
    if (!sessionId) {
      setError('Please start a conversation first')
      return
    }
    
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      mediaRecorderRef.current = new MediaRecorder(stream)
      audioChunksRef.current = []

      mediaRecorderRef.current.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data)
      }

      mediaRecorderRef.current.onstop = async () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/wav' })
        await sendAudio(audioBlob)
        stream.getTracks().forEach(track => track.stop())
      }

      mediaRecorderRef.current.start()
      setIsRecording(true)
      setError(null)
    } catch (err) {
      setError('Microphone access denied: ' + err.message)
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
    }
  }

  const sendAudio = async (audioBlob) => {
    setIsProcessing(true)
    
    try {
      const formData = new FormData()
      formData.append('audio', audioBlob, 'audio.wav')
      formData.append('session_id', sessionId)
      formData.append('include_feedback', 'false')  // ⚡ DISABLED to avoid Groq rate limits
      
      const response = await fetch('/api/audio/converse', {
        method: 'POST',
        body: formData
      })
      
      const data = await response.json()
      
      setMessages(prev => [...prev, 
        {
          role: 'user',
          text: data.user_text,
          timestamp: new Date()
        },
        {
          role: 'assistant',
          text: data.ai_text_response,
          timestamp: new Date()
        }
      ])
      
      setMessageCount(data.conversation_count)
      
      // Handle feedback
      if (data.feedback) {
        setFeedback(data.feedback)
      }
      
      // Handle overall summary (final message only)
      if (data.overall_summary) {
        setOverallSummary(data.overall_summary)
      }
      
      // Handle quiz - store it but don't show yet (wait for audio to finish)
      if (data.quiz) {
        setPendingQuiz(data.quiz)
        setSelectedAnswer(null)
        setQuizResult(null)
      }
      
      if (data.audio_response) {
        playAudio(data.audio_response, data.quiz) // Pass quiz to show after audio
      }
    } catch (err) {
      setError('Failed to send audio: ' + err.message)
    } finally {
      setIsProcessing(false)
    }
  }

  const playAudio = (base64Audio, quizToShowAfter = null) => {
    try {
      const audio = new Audio(`data:audio/mp3;base64,${base64Audio}`)
      
      // Show quiz AFTER audio finishes playing
      audio.onended = () => {
        if (quizToShowAfter) {
          setQuiz(quizToShowAfter)
          setPendingQuiz(null)
        }
      }
      
      audio.play()
    } catch (err) {
      console.error('Audio playback error:', err)
      // If audio fails, still show quiz if there is one
      if (quizToShowAfter) {
        setQuiz(quizToShowAfter)
        setPendingQuiz(null)
      }
    }
  }

  const submitQuiz = async () => {
    if (!quiz || selectedAnswer === null) return
    
    setQuizSubmitted(true)
    
    try {
      const formData = new FormData()
      formData.append('session_id', sessionId)
      formData.append('selected_answer_index', selectedAnswer.toString())
      
      const response = await fetch('/api/audio/verify-quiz', {
        method: 'POST',
        body: formData
      })
      
      const data = await response.json()
      console.log('Quiz result from backend:', data) // Debug log
      setQuizResult(data)
    } catch (err) {
      console.error('Quiz error:', err)
    }
  }

  const closeQuiz = () => {
    setQuiz(null)
    setSelectedAnswer(null)
    setQuizResult(null)
    setQuizSubmitted(false)
  }

  return (
    <div style={{ 
      minHeight: '100vh', 
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      display: 'flex',
      flexDirection: 'column',
      fontFamily: 'system-ui, -apple-system, sans-serif'
    }}>
      {/* Header */}
      <div style={{
        background: 'rgba(255,255,255,0.1)',
        backdropFilter: 'blur(10px)',
        padding: '20px',
        borderBottom: '1px solid rgba(255,255,255,0.2)'
      }}>
        <h1 style={{ margin: 0, color: 'white', fontSize: '2rem', textAlign: 'center' }}>
          🧠 NeuroPilot - Voice Conversation
        </h1>
        <p style={{ margin: '5px 0 0 0', color: 'rgba(255,255,255,0.8)', textAlign: 'center' }}>
          Messages: {messageCount} / 12
        </p>
      </div>

      {/* Messages Container */}
      <div style={{
        flex: 1,
        overflow: 'auto',
        padding: '20px',
        maxWidth: '800px',
        width: '100%',
        margin: '0 auto'
      }}>
        {messages.length === 0 ? (
          <div style={{
            textAlign: 'center',
            color: 'white',
            padding: '60px 20px'
          }}>
            <h2 style={{ fontSize: '2.5rem', marginBottom: '20px' }}>👋 Welcome!</h2>
            <p style={{ fontSize: '1.2rem', opacity: 0.9, marginBottom: '30px' }}>
              Click "Start New Conversation" to begin practicing with AI
            </p>
            <button
              onClick={startConversation}
              disabled={isProcessing}
              style={{
                background: 'white',
                color: '#667eea',
                border: 'none',
                padding: '15px 30px',
                fontSize: '1.1rem',
                borderRadius: '25px',
                cursor: isProcessing ? 'not-allowed' : 'pointer',
                fontWeight: 'bold',
                boxShadow: '0 4px 15px rgba(0,0,0,0.2)',
                opacity: isProcessing ? 0.6 : 1
              }}
            >
              {isProcessing ? '⏳ Starting...' : '🚀 Start New Conversation'}
            </button>
          </div>
        ) : (
          <>
            {messages.map((msg, idx) => (
              <div
                key={idx}
                style={{
                  display: 'flex',
                  justifyContent: msg.role === 'user' ? 'flex-end' : 'flex-start',
                  marginBottom: '15px'
                }}
              >
                <div style={{
                  background: msg.role === 'user' 
                    ? 'rgba(255,255,255,0.9)' 
                    : 'rgba(255,255,255,0.2)',
                  color: msg.role === 'user' ? '#333' : 'white',
                  padding: '15px 20px',
                  borderRadius: '20px',
                  maxWidth: '70%',
                  boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
                }}>
                  <div style={{ fontWeight: 'bold', marginBottom: '5px', fontSize: '0.9rem' }}>
                    {msg.role === 'user' ? '👤 You' : '🤖 AI Coach'}
                  </div>
                  <div style={{ lineHeight: '1.5' }}>{msg.text}</div>
                </div>
              </div>
            ))}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Error Display */}
      {error && (
        <div style={{
          background: 'rgba(255,0,0,0.2)',
          color: 'white',
          padding: '15px',
          margin: '0 20px',
          borderRadius: '10px',
          textAlign: 'center'
        }}>
          ⚠️ {error}
        </div>
      )}

      {/* Controls */}
      {sessionId && (
        <div style={{
          background: 'rgba(255,255,255,0.1)',
          backdropFilter: 'blur(10px)',
          padding: '20px',
          borderTop: '1px solid rgba(255,255,255,0.2)'
        }}>
          <div style={{
            maxWidth: '800px',
            margin: '0 auto',
            display: 'flex',
            gap: '15px',
            alignItems: 'center',
            justifyContent: 'center',
            flexWrap: 'wrap'
          }}>
            {!isRecording ? (
              <button
                onClick={startRecording}
                disabled={isProcessing}
                style={{
                  background: '#10b981',
                  color: 'white',
                  border: 'none',
                  padding: '20px 40px',
                  fontSize: '1.2rem',
                  borderRadius: '50px',
                  cursor: isProcessing ? 'not-allowed' : 'pointer',
                  fontWeight: 'bold',
                  boxShadow: '0 4px 15px rgba(0,0,0,0.3)',
                  opacity: isProcessing ? 0.6 : 1,
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px'
                }}
              >
                🎙️ Hold to Record
              </button>
            ) : (
              <button
                onClick={stopRecording}
                style={{
                  background: '#ef4444',
                  color: 'white',
                  border: 'none',
                  padding: '20px 40px',
                  fontSize: '1.2rem',
                  borderRadius: '50px',
                  cursor: 'pointer',
                  fontWeight: 'bold',
                  boxShadow: '0 4px 15px rgba(0,0,0,0.3)',
                  animation: 'pulse 1.5s infinite',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px'
                }}
              >
                🔴 Recording... (Click to Stop)
              </button>
            )}
            
            {isProcessing && (
              <div style={{ color: 'white', fontSize: '1.1rem' }}>
                ⏳ Processing...
              </div>
            )}
            
            <button
              onClick={startConversation}
              style={{
                background: 'rgba(255,255,255,0.2)',
                color: 'white',
                border: '2px solid white',
                padding: '12px 24px',
                fontSize: '1rem',
                borderRadius: '25px',
                cursor: 'pointer',
                fontWeight: 'bold'
              }}
            >
              🔄 New Conversation
            </button>
          </div>
        </div>
      )}

      {/* Quiz Modal */}
      {quiz && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0,0,0,0.7)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 2000,
          padding: '20px'
        }}>
          <div style={{
            background: 'white',
            borderRadius: '20px',
            padding: '30px',
            maxWidth: '600px',
            width: '100%',
            boxShadow: '0 10px 40px rgba(0,0,0,0.3)'
          }}>
            <h2 style={{ margin: '0 0 10px 0', color: '#667eea' }}>❓ Quiz Time!</h2>
            {quiz.dialogue && (
              <div style={{ 
                background: '#f3f4f6', 
                padding: '15px', 
                borderRadius: '10px', 
                marginBottom: '20px',
                fontStyle: 'italic',
                color: '#555'
              }}>
                "{quiz.dialogue}"
              </div>
            )}
            <h3 style={{ margin: '0 0 20px 0', color: '#333' }}>{quiz.question}</h3>
            
            {/* Options as radio buttons */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '20px' }}>
              {quiz.options.map((option, idx) => {
                const isSelected = selectedAnswer === idx
                const isCorrect = quizResult?.correct_answer_index === idx
                const showAsCorrect = quizSubmitted && isCorrect
                const showAsWrong = quizSubmitted && isSelected && !quizResult?.is_correct
                
                return (
                  <label
                    key={idx}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      padding: '15px',
                      borderRadius: '10px',
                      background: showAsCorrect
                        ? '#d1fae5'  // Light green for correct
                        : showAsWrong
                        ? '#fee2e2'  // Light red for wrong
                        : isSelected
                        ? '#e0e7ff'  // Light blue for selected
                        : '#f3f4f6', // Gray default
                      border: showAsCorrect
                        ? '2px solid #10b981'
                        : showAsWrong
                        ? '2px solid #ef4444'
                        : isSelected
                        ? '2px solid #667eea'
                        : '2px solid transparent',
                      cursor: quizSubmitted ? 'not-allowed' : 'pointer',
                      transition: 'all 0.3s'
                    }}
                    onClick={() => !quizSubmitted && setSelectedAnswer(idx)}
                  >
                    <input
                      type="radio"
                      name="quiz-option"
                      checked={isSelected}
                      disabled={quizSubmitted}
                      onChange={() => setSelectedAnswer(idx)}
                      style={{ marginRight: '12px', cursor: quizSubmitted ? 'not-allowed' : 'pointer' }}
                    />
                    <span style={{ flex: 1, fontWeight: (showAsCorrect || showAsWrong) ? 'bold' : 'normal' }}>
                      {String.fromCharCode(65 + idx)}. {option}
                    </span>
                    {showAsCorrect && <span style={{ color: '#10b981', fontWeight: 'bold' }}>✅ Correct</span>}
                  </label>
                )
              })}
            </div>
            
            {/* Submit or Close button */}
            {!quizSubmitted ? (
              <button
                onClick={submitQuiz}
                disabled={selectedAnswer === null}
                style={{
                  width: '100%',
                  background: selectedAnswer === null ? '#d1d5db' : '#667eea',
                  color: 'white',
                  border: 'none',
                  padding: '15px',
                  borderRadius: '10px',
                  fontSize: '1.1rem',
                  fontWeight: 'bold',
                  cursor: selectedAnswer === null ? 'not-allowed' : 'pointer',
                  transition: 'background 0.3s'
                }}
              >
                Submit Answer
              </button>
            ) : (
              <button
                onClick={closeQuiz}
                style={{
                  width: '100%',
                  background: '#667eea',
                  color: 'white',
                  border: 'none',
                  padding: '15px',
                  borderRadius: '10px',
                  fontSize: '1.1rem',
                  fontWeight: 'bold',
                  cursor: 'pointer',
                  transition: 'background 0.3s'
                }}
              >
                Close & Continue
              </button>
            )}
            
            {/* Result explanation */}
            {quizResult && (
              <div style={{
                marginTop: '20px',
                padding: '20px',
                background: quizResult.is_correct ? '#d1fae5' : '#fee2e2',
                borderRadius: '10px',
                color: '#333',
                border: quizResult.is_correct ? '2px solid #10b981' : '2px solid #ef4444'
              }}>
                <div style={{ marginBottom: '10px' }}>
                  <strong style={{ fontSize: '1.1rem' }}>
                    {quizResult.is_correct ? '🎉 Correct!' : '❌ Incorrect'}
                  </strong>
                </div>
                
                {!quizResult.is_correct && quiz.options && (
                  <div style={{ 
                    marginTop: '10px', 
                    padding: '10px', 
                    background: '#d1fae5',
                    borderRadius: '8px',
                    borderLeft: '4px solid #10b981'
                  }}>
                    <strong>✅ Correct Answer:</strong> {quiz.options[quizResult.correct_answer_index]}
                  </div>
                )}
                
                {quizResult.encouragement && (
                  <div style={{ 
                    marginTop: '15px',
                    padding: '10px',
                    background: 'rgba(255,255,255,0.5)',
                    borderRadius: '8px'
                  }}>
                    {quizResult.encouragement}
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Overall Summary Modal - Shows at end of conversation */}
      {overallSummary && (
        <div style={{
          position: 'fixed',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: 'rgba(0, 0, 0, 0.8)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          zIndex: 2000,
          padding: '20px'
        }}>
          <div style={{
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            borderRadius: '20px',
            padding: '30px',
            maxWidth: '500px',
            width: '100%',
            color: 'white',
            boxShadow: '0 20px 60px rgba(0,0,0,0.4)'
          }}>
            <h2 style={{ margin: '0 0 20px 0', textAlign: 'center', fontSize: '28px' }}>
              🎉 Session Complete!
            </h2>
            
            <div style={{ 
              background: 'rgba(255,255,255,0.2)', 
              borderRadius: '15px', 
              padding: '20px',
              marginBottom: '20px'
            }}>
              <p style={{ margin: '0 0 15px 0', fontSize: '16px', textAlign: 'center' }}>
                {overallSummary.summary}
              </p>
              
              <div style={{ 
                display: 'grid', 
                gridTemplateColumns: '1fr 1fr', 
                gap: '15px',
                marginTop: '15px'
              }}>
                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '32px', fontWeight: 'bold' }}>{overallSummary.tone}</div>
                  <div style={{ fontSize: '14px', opacity: 0.9 }}>Tone</div>
                </div>
                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '32px', fontWeight: 'bold' }}>{overallSummary.clarity}</div>
                  <div style={{ fontSize: '14px', opacity: 0.9 }}>Clarity</div>
                </div>
                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '32px', fontWeight: 'bold' }}>{overallSummary.empathy}</div>
                  <div style={{ fontSize: '14px', opacity: 0.9 }}>Empathy</div>
                </div>
                <div style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '32px', fontWeight: 'bold' }}>{overallSummary.engagement}</div>
                  <div style={{ fontSize: '14px', opacity: 0.9 }}>Engagement</div>
                </div>
              </div>
            </div>
            
            <button
              onClick={() => {
                setOverallSummary(null)
                setSessionId(null)
                setMessages([])
                setMessageCount(0)
                setFeedback(null)
              }}
              style={{
                width: '100%',
                padding: '15px',
                background: 'white',
                color: '#667eea',
                border: 'none',
                borderRadius: '12px',
                fontSize: '16px',
                fontWeight: 'bold',
                cursor: 'pointer',
                transition: 'transform 0.2s'
              }}
              onMouseOver={(e) => e.target.style.transform = 'scale(1.05)'}
              onMouseOut={(e) => e.target.style.transform = 'scale(1)'}
            >
              Start New Conversation
            </button>
          </div>
        </div>
      )}

      <style>{`
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.7; }
        }
      `}</style>
    </div>
  )
}

export default App
