"use client"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { useAgentContext, type AgentType } from "@/contexts/agent-context"
import { useTravelContext } from "@/contexts/travel-context"
import { Plane, Hotel, Users, Settings, MessageCircle, Trash2, MapPin } from "lucide-react"
import { useState } from "react"

interface SidebarProps {
  activeView: "chat" | "settings"
  setActiveView: (view: "chat" | "settings") => void
}

const agentConfig = {
  team: {
    name: "Travel Team",
    icon: Users,
    description: "General travel planning and coordination",
    color: "bg-blue-500",
  },
  flights: {
    name: "Flight Expert",
    icon: Plane,
    description: "Flight bookings and airline information",
    color: "bg-green-500",
  },
  hotels: {
    name: "Hotel Specialist",
    icon: Hotel,
    description: "Accommodation and hotel bookings",
    color: "bg-purple-500",
  },
}

export function Sidebar({ activeView, setActiveView }: SidebarProps) {
  const { activeAgent, setActiveAgent, messages, clearMessages } = useAgentContext()
  const { preferences } = useTravelContext()
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false)

  const handleAgentSwitch = (agent: AgentType) => {
    setActiveAgent(agent)
    setActiveView("chat")
  }

  return (
    <div className="md:hidden">
      {/* Mobile Menu Button */}
      <Button
        variant="default"
        className="w-full justify-start p-3 h-auto"
        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
      >
        <div className="p-2 rounded-lg bg-gray-500 mr-3">
          <MapPin className="h-4 w-4 text-white" />
        </div>
        <div className="text-left flex-1">
          <div className="font-medium text-sm">Menu</div>
        </div>
      </Button>

      {/* Mobile Menu Overlay */}
      {isMobileMenuOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
          <div className="w-80 bg-white/95 backdrop-blur-sm border-r border-gray-200 flex-col">
            {/* Header */}
            <div className="p-6 border-b border-gray-200">
              <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
                <MapPin className="h-6 w-6 text-blue-500" />
                TravelAI
              </h1>
              <p className="text-sm text-gray-600 mt-1">Your AI Travel Assistant</p>
            </div>

            {/* Travel Summary */}
            {preferences.destination && (
              <div className="p-4 border-b border-gray-200">
                <Card className="p-3 bg-blue-50/80 backdrop-blur-sm">
                  <h3 className="font-semibold text-sm text-blue-900">Current Trip</h3>
                  <p className="text-sm text-blue-700">{preferences.destination}</p>
                  <div className="flex justify-between text-xs text-blue-600 mt-1">
                    <span>{preferences.departureDate ? new Date(preferences.departureDate).toLocaleDateString() : 'No date'}</span>
                    <span>{preferences.numGuests} guests</span>
                  </div>
                </Card>
              </div>
            )}

            {/* Navigation */}
            <div className="p-4 border-b border-gray-200">
              <div className="space-y-2">
                <Button
                  variant={activeView === "chat" ? "default" : "ghost"}
                  className="w-full justify-start"
                  onClick={() => setActiveView("chat")}
                >
                  <MessageCircle className="h-4 w-4 mr-2" />
                  Chat
                </Button>
                <Button
                  variant={activeView === "settings" ? "default" : "ghost"}
                  className="w-full justify-start"
                  onClick={() => setActiveView("settings")}
                >
                  <Settings className="h-4 w-4 mr-2" />
                  Travel Settings
                </Button>
              </div>
            </div>

            {/* Agents */}
            <div className="flex-1 p-4">
              <h3 className="text-sm font-semibold text-gray-700 mb-3">AI Agents</h3>
              <div className="space-y-2">
                {Object.entries(agentConfig).map(([key, config]) => {
                  const agentKey = key as AgentType
                  const Icon = config.icon
                  const messageCount = messages[agentKey].length

                  return (
                    <div key={key} className="relative">
                      <Button
                        variant={activeAgent === agentKey ? "default" : "ghost"}
                        className="w-full justify-start p-3 h-auto"
                        onClick={() => handleAgentSwitch(agentKey)}
                      >
                        <div className={`p-2 rounded-lg ${config.color} mr-3`}>
                          <Icon className="h-4 w-4 text-white" />
                        </div>
                        <div className="text-left flex-1">
                          <div className="font-medium text-sm">{config.name}</div>
                          <div className="text-xs text-gray-500 truncate">{config.description}</div>
                        </div>
                        {messageCount > 0 && (
                          <span className="bg-blue-500 text-white text-xs rounded-full px-2 py-1 ml-2">{messageCount}</span>
                        )}
                      </Button>

                      {messageCount > 0 && activeAgent === agentKey && (
                        <Button
                          variant="ghost"
                          size="sm"
                          className="absolute top-1 right-1 h-6 w-6 p-0 opacity-0 group-hover:opacity-100 hover:bg-red-100"
                          onClick={(e) => {
                            e.stopPropagation()
                            clearMessages(agentKey)
                          }}
                        >
                          <Trash2 className="h-3 w-3 text-red-500" />
                        </Button>
                      )}
                    </div>
                  )
                })}
              </div>
            </div>

            {/* Footer */}
            <div className="p-4 border-t border-gray-200">
              <p className="text-xs text-gray-500 text-center">Powered by AI • Built with React</p>
            </div>
          </div>
        </div>
      )}
    </div>
  \
    <div className="hidden md:flex w-80 bg-white/95 backdrop-blur-sm border-r border-gray-200 flex-col">
  ;<div className="p-6 border-b border-gray-200">
    <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
      <MapPin className="h-6 w-6 text-blue-500" />
      TravelAI
    </h1>
    <p className="text-sm text-gray-600 mt-1">Your AI Travel Assistant</p>
  </div>
  preferences.destination && (
    <div className="p-4 border-b border-gray-200">
      <Card className="p-3 bg-blue-50/80 backdrop-blur-sm">
        <h3 className="font-semibold text-sm text-blue-900">Current Trip</h3>
        <p className="text-sm text-blue-700">{preferences.destination}</p>
        <div className="flex justify-between text-xs text-blue-600 mt-1">
          <span>
            {preferences.departureDate ? new Date(preferences.departureDate).toLocaleDateString() : "No date"}
          </span>
          <span>{preferences.numGuests} guests</span>
        </div>
      </Card>
    </div>
  )
  ;<div className="p-4 border-b border-gray-200">
    <div className="space-y-2">
      <Button
        variant={activeView === "chat" ? "default" : "ghost"}
        className="w-full justify-start"
        onClick={() => setActiveView("chat")}
      >
        <MessageCircle className="h-4 w-4 mr-2" />
        Chat
      </Button>
      <Button
        variant={activeView === "settings" ? "default" : "ghost"}
        className="w-full justify-start"
        onClick={() => setActiveView("settings")}
      >
        <Settings className="h-4 w-4 mr-2" />
        Travel Settings
      </Button>
    </div>
  </div>
  ;<div className="flex-1 p-4">
    <h3 className="text-sm font-semibold text-gray-700 mb-3">AI Agents</h3>
    <div className="space-y-2">
      {Object.entries(agentConfig).map(([key, config]) => {
        const agentKey = key as AgentType
        const Icon = config.icon
        const messageCount = messages[agentKey].length

        return (
          <div key={key} className="relative">
            <Button
              variant={activeAgent === agentKey ? "default" : "ghost"}
              className="w-full justify-start p-3 h-auto"
              onClick={() => handleAgentSwitch(agentKey)}
            >
              <div className={`p-2 rounded-lg ${config.color} mr-3`}>
                <Icon className="h-4 w-4 text-white" />
              </div>
              <div className="text-left flex-1">
                <div className="font-medium text-sm">{config.name}</div>
                <div className="text-xs text-gray-500 truncate">{config.description}</div>
              </div>
              {messageCount > 0 && (
                <span className="bg-blue-500 text-white text-xs rounded-full px-2 py-1 ml-2">{messageCount}</span>
              )}
            </Button>

            {messageCount > 0 && activeAgent === agentKey && (
              <Button
                variant="ghost"
                size="sm"
                className="absolute top-1 right-1 h-6 w-6 p-0 opacity-0 group-hover:opacity-100 hover:bg-red-100"
                onClick={(e) => {
                  e.stopPropagation()
                  clearMessages(agentKey)
                }}
              >
                <Trash2 className="h-3 w-3 text-red-500" />
              </Button>
            )}
          </div>
        )
      })}
    </div>
  </div>
  ;<div className="p-4 border-t border-gray-200">
    <p className="text-xs text-gray-500 text-center">Powered by AI • Built with React</p>
  </div>
  </div>
  )
}
