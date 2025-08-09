"use client"

import type React from "react"

import { useState, useRef, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Card } from "@/components/ui/card"
import { useAgentContext } from "@/contexts/agent-context"
import { useTravelContext } from "@/contexts/travel-context"
import { MessageRenderer } from "@/components/message-renderer"
import { apiService } from "@/services/api-service"
import { Send, Loader2 } from "lucide-react"
import { v4 as uuidv4 } from "uuid";

export function generateThreadId(): string {
  return uuidv4();
}



export function ChatInterface() {
  const [input, setInput] = useState("")
  const [threadId, setThreadId] = useState<string>("");

  useEffect(() => {
    if (typeof window !== "undefined") {
      let saved = localStorage.getItem("thread_id");
      if (!saved) {
        saved = generateThreadId();
        localStorage.setItem("thread_id", saved);
      }
      setThreadId(saved);
    }
  }, []);
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const { activeAgent, messages, addMessage, isLoading, setIsLoading } = useAgentContext()
  const { preferences } = useTravelContext()

  const currentMessages = messages[activeAgent]

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [currentMessages])

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage = input.trim()
    setInput("")

    // Add user message
    addMessage(activeAgent, {
      content: userMessage,
      role: "user",
      agentType: activeAgent,
    })

    setIsLoading(true)
    try {
      const response = await apiService.sendMessage({
        message: userMessage,
        agentType: activeAgent,
        travelPreferences: preferences,
        thread_id: threadId ,
      })

      addMessage(activeAgent, {
        content: response.message,
        role: "assistant",
        agentType: activeAgent,
      })
    } catch (error) {
      console.error("Error sending message:", error)
      addMessage(activeAgent, {
        content: "Sorry, I encountered an error. Please try again.",
        role: "assistant",
        agentType: activeAgent,
      })
    } finally {
      setIsLoading(false)
    }
  }

  const getAgentWelcomeMessage = () => {
    const welcomeMessages = {
      team: "Hello! I'm your Travel Team coordinator. I can help you plan your entire trip, coordinate between different services, and answer any travel-related questions. What would you like to explore today?",
      flights:
        "Hi there! I'm your Flight Expert. I specialize in finding the best flights, comparing prices, checking schedules, and helping with airline-related questions. Where are you planning to fly?",
      hotels:
        "Welcome! I'm your Hotel Specialist. I can help you find the perfect accommodation, compare prices, check amenities, and answer questions about hotels and stays. What kind of accommodation are you looking for?",
    }
    return welcomeMessages[activeAgent]
  }

  return (
    <div className="flex flex-col h-full">
      <div className="bg-white/95 backdrop-blur-sm border-b border-gray-200 p-3 md:p-4">
        <div className="flex items-center justify-between">
          <div className="ml-12 md:ml-0">
            <h2 className="text-lg md:text-xl font-semibold text-gray-900">
              {activeAgent === "team" && "Travel Team"}
              {activeAgent === "flights" && "Flight Expert"}
              {activeAgent === "hotels" && "Hotel Specialist"}
            </h2>
            <p className="text-xs md:text-sm text-gray-600 hidden sm:block">
              {activeAgent === "team" && "General travel planning and coordination"}
              {activeAgent === "flights" && "Flight bookings and airline information"}
              {activeAgent === "hotels" && "Accommodation and hotel bookings"}
            </p>
          </div>
          <div className="flex items-center space-x-2">
            <div className="h-2 w-2 bg-green-500 rounded-full"></div>
            <span className="text-xs md:text-sm text-gray-600">Online</span>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {currentMessages.length === 0 && (
          <Card className="bg-white/90 backdrop-blur-sm border-0 shadow-lg">
            <div className="p-4 md:p-6 text-center">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Welcome to{" "}
                {activeAgent === "team"
                  ? "Travel Team"
                  : activeAgent === "flights"
                    ? "Flight Expert"
                    : "Hotel Specialist"}
                !
              </h3>
              <p className="text-gray-700 mb-4 text-sm">{getAgentWelcomeMessage()}</p>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-sm">
                {activeAgent === "team" && (
                  <>
                    <Button variant="outline" size="sm" onClick={() => setInput("Help me plan a 7-day trip to Japan")}>
                      Plan a trip to Japan
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => setInput("What's the best time to visit Europe?")}
                    >
                      Best time to visit Europe
                    </Button>
                    <Button variant="outline" size="sm" onClick={() => setInput("Create an itinerary for Paris")}>
                      Create Paris itinerary
                    </Button>
                    <Button variant="outline" size="sm" onClick={() => setInput("Budget travel tips")}>
                      Budget travel tips
                    </Button>
                  </>
                )}
                {activeAgent === "flights" && (
                  <>
                    <Button variant="outline" size="sm" onClick={() => setInput("Find flights from NYC to London")}>
                      NYC to London flights
                    </Button>
                    <Button variant="outline" size="sm" onClick={() => setInput("Best time to book flights")}>
                      When to book flights
                    </Button>
                    <Button variant="outline" size="sm" onClick={() => setInput("Compare airline prices")}>
                      Compare airline prices
                    </Button>
                    <Button variant="outline" size="sm" onClick={() => setInput("Flight delay compensation")}>
                      Flight delay help
                    </Button>
                  </>
                )}
                {activeAgent === "hotels" && (
                  <>
                    <Button variant="outline" size="sm" onClick={() => setInput("Find hotels in Tokyo")}>
                      Hotels in Tokyo
                    </Button>
                    <Button variant="outline" size="sm" onClick={() => setInput("Best hotel booking sites")}>
                      Best booking sites
                    </Button>
                    <Button variant="outline" size="sm" onClick={() => setInput("Hotel amenities to look for")}>
                      Hotel amenities guide
                    </Button>
                    <Button variant="outline" size="sm" onClick={() => setInput("Luxury vs budget hotels")}>
                      Luxury vs budget
                    </Button>
                  </>
                )}
              </div>
            </div>
          </Card>
        )}

        {currentMessages.map((message) => (
          <MessageRenderer key={message.id} message={message} />
        ))}

        {isLoading && (
          <div className="flex items-center space-x-2 text-gray-500">
            <Loader2 className="h-4 w-4 animate-spin" />
            <span className="text-sm">AI is thinking...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      <div className="bg-white/95 backdrop-blur-sm border-t border-gray-200 p-3 md:p-4">
        <form onSubmit={handleSubmit} className="flex space-x-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={`Ask ${activeAgent === "team" ? "Travel Team" : activeAgent === "flights" ? "Flight Expert" : "Hotel Specialist"} anything...`}
            className="flex-1 h-12"
            disabled={isLoading}
          />
          <Button type="submit" disabled={!input.trim() || isLoading} className="h-12 px-4">
            <Send className="h-4 w-4" />
          </Button>
        </form>
        <p className="text-xs text-gray-500 mt-2 text-center">
          AI responses may contain inaccuracies. Please verify important information.
        </p>
      </div>
    </div>
  )
}
