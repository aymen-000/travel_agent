import axios from "axios"
import type { AgentType, Message } from "@/contexts/agent-context"
import type { TravelPreferences } from "@/contexts/travel-context"

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
})

export interface SendMessageRequest {
  message: string
  agentType: AgentType
  travelPreferences: TravelPreferences
  thread_id : string | null
}

export interface SendMessageResponse {
  message: string
  agentType: AgentType
  sessionId?: string
  timestamp?: string
  thread_id? : string
  metadata?: {
    suggestions?: string[]
    actions?: string[]
    data?: any
  }
}

export interface AgentStatusResponse {
  status: "online" | "offline" | "busy"
  capabilities: string[]
  description: string
}

class ApiService {

  async sendMessage(request: SendMessageRequest): Promise<SendMessageResponse> {
    try {
      let endpoint = ""
      let requestData: any = {}


      switch (request.agentType) {
        case "team":
          endpoint = "/api/v1/team/search"
          requestData = {
            query: request.message,
            thread_id : request.thread_id
          }
          break
        case "flights":
          endpoint = "/api/v1/flights/search"
          requestData = {
            query: request.message,
            //origin: request.travelPreferences.destination, // You might want to extract origin separately
            //destination: request.travelPreferences.destination,
            //departure_date: request.travelPreferences.departureDate,
            //return_date: request.travelPreferences.endDate,
            //passengers: request.travelPreferences.numGuests,
            thread_id : request.thread_id 
          }
          break
        case "hotels":
          endpoint = "/api/v1/hotels/search"
          requestData = {
            query: request.message,
            //destination: request.travelPreferences.destination,
            //check_in: request.travelPreferences.departureDate,
            //check_out: request.travelPreferences.endDate,
            //guests: request.travelPreferences.numGuests,
            thread_id : request.thread_id
          }
          break
        default:
          throw new Error(`Unknown agent type: ${request.agentType}`)
      }

      const response = await apiClient.post(endpoint, requestData)

      return {
        message: response.data.response,
        agentType: request.agentType,
        sessionId: response.data.session_id,
        timestamp: response.data.timestamp,
        thread_id : response.data.thread_id , 
        metadata: response.data.metadata || {},
      }
    } catch (error) {
      console.error("API Error:", error)
      if (axios.isAxiosError(error)) {
        const errorMessage = error.response?.data?.detail || error.message
        throw new Error(`Failed to send message to ${request.agentType} agent: ${errorMessage}`)
      }
      throw new Error(`Failed to send message to ${request.agentType} agent`)
    }
  }

  async getAgentStatus(agentType: AgentType): Promise<AgentStatusResponse> {
    try {
      const response = await apiClient.get(`/api/v1/${agentType}/status`)
      return response.data
    } catch (error) {
      console.error("API Error:", error)
      return {
        status: "online", 
        capabilities: ["search", "recommend", "chat"],
        description: `${agentType} agent is ready`,
      }
    }
  }

  // Search flights using your flights router
  async searchFlights(params: {
    query?: string
    origin?: string
    destination: string
    departureDate: string
    returnDate?: string
    passengers: number
  }) {
    try {
      const response = await apiClient.post("/api/v1/flights/search", {
        query: params.query || `Find flights from ${params.origin} to ${params.destination}`,
        //origin: params.origin,
        //destination: params.destination,
        //departure_date: params.departureDate,
        //return_date: params.returnDate,
        //passengers: params.passengers,
      })
      return response.data
    } catch (error) {
      console.error("Flight search error:", error)
      throw new Error("Failed to search flights")
    }
  }

  // Search hotels using your hotels router
  async searchHotels(params: {
    query?: string
    destination: string
    checkIn: string
    checkOut: string
    guests: number
  }) {
    try {
      const response = await apiClient.post("/api/v1/hotels/search", {
        query: params.query || `Find hotels in ${params.destination}`,
        //destination: params.destination,
        //check_in: params.checkIn,
        //check_out: params.checkOut,
        //guests: params.guests,
      })
      return response.data
    } catch (error) {
      console.error("Hotel search error:", error)
      throw new Error("Failed to search hotels")
    }
  }

  async getDestinationInfo(destination: string) {
    try {
      const response = await apiClient.post("/api/v1/destinations/search", {
        query: `Tell me about ${destination}`,
        destination: destination,
      })
      return response.data
    } catch (error) {
      console.error("Destination search error:", error)
      throw new Error("Failed to get destination information")
    }
  }

  async getTravelRecommendations(preferences: TravelPreferences) {
    try {
      const query = `Plan a trip to ${preferences.destination} for ${preferences.numGuests} guests from ${preferences.departureDate} to ${preferences.endDate}`
      const response = await apiClient.post("/api/v1/team/search", {
        query: query,
        travel_preferences: preferences,
      })
      return response.data
    } catch (error) {
      console.error("Recommendations error:", error)
      throw new Error("Failed to get travel recommendations")
    }
  }

  async healthCheck() {
    try {
      const response = await apiClient.get("/")
      return {
        status: "healthy",
        message: response.data.message || "API is running",
      }
    } catch (error) {
      console.error("Health check failed:", error)
      return { status: "error", message: "Backend unavailable" }
    }
  }
}

export const apiService = new ApiService()
