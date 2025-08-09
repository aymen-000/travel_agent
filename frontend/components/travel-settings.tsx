"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { CalendarDays } from "lucide-react"
import { useTravelContext } from "@/contexts/travel-context"

export function TravelSettings() {
  const { preferences, updatePreferences, resetPreferences } = useTravelContext()
  const [localPreferences, setLocalPreferences] = useState(preferences)

  const handleSave = () => {
    updatePreferences(localPreferences)
  }

  const handleReset = () => {
    resetPreferences()
    setLocalPreferences({
      departureDate: "",
      endDate: "",
      destination: "",
      numGuests: 2,
    })
  }

  const updateLocalPreferences = (updates: Partial<typeof localPreferences>) => {
    setLocalPreferences((prev) => ({ ...prev, ...updates }))
  }

  return (
    <div className="flex-1 overflow-y-auto p-4 md:p-6">
      <div className="max-w-2xl mx-auto space-y-6">
        <div className="text-center mb-8">
          <h1 className="text-2xl md:text-3xl font-bold text-white mb-2">Travel Settings</h1>
          <p className="text-white/80">Set your travel preferences for personalized recommendations</p>
        </div>

        {/* Main Settings Card */}
        <Card className="bg-white/95 backdrop-blur-sm border-0 shadow-xl">
          <CardHeader className="text-center pb-4">
            <CardTitle className="flex items-center justify-center gap-2 text-xl">
              <CalendarDays className="h-5 w-5 text-blue-500" />
              Trip Details
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Destination */}
            <div>
              <Label htmlFor="destination" className="text-base font-medium">
                Where are you going?
              </Label>
              <Input
                id="destination"
                placeholder="e.g., Paris, Tokyo, New York..."
                value={localPreferences.destination}
                onChange={(e) => updateLocalPreferences({ destination: e.target.value })}
                className="mt-2 text-base h-12"
              />
            </div>

            {/* Dates */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <Label htmlFor="departureDate" className="text-base font-medium">
                  Departure Date
                </Label>
                <Input
                  id="departureDate"
                  type="date"
                  value={localPreferences.departureDate}
                  onChange={(e) => updateLocalPreferences({ departureDate: e.target.value })}
                  className="mt-2 text-base h-12"
                />
              </div>
              <div>
                <Label htmlFor="endDate" className="text-base font-medium">
                  Return Date
                </Label>
                <Input
                  id="endDate"
                  type="date"
                  value={localPreferences.endDate}
                  onChange={(e) => updateLocalPreferences({ endDate: e.target.value })}
                  className="mt-2 text-base h-12"
                />
              </div>
            </div>

            {/* Number of Guests */}
            <div>
              <Label htmlFor="numGuests" className="text-base font-medium">
                Number of Guests
              </Label>
              <div className="flex items-center mt-2 space-x-4">
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => updateLocalPreferences({ numGuests: Math.max(1, localPreferences.numGuests - 1) })}
                  className="h-12 w-12"
                >
                  -
                </Button>
                <div className="flex-1 text-center">
                  <div className="text-2xl font-bold">{localPreferences.numGuests}</div>
                  <div className="text-sm text-gray-600">guests</div>
                </div>
                <Button
                  type="button"
                  variant="outline"
                  size="sm"
                  onClick={() => updateLocalPreferences({ numGuests: Math.min(20, localPreferences.numGuests + 1) })}
                  className="h-12 w-12"
                >
                  +
                </Button>
              </div>
            </div>

            {/* Action Buttons */}
            <div className="flex flex-col sm:flex-row gap-3 pt-4">
              <Button variant="outline" onClick={handleReset} className="flex-1 h-12 bg-transparent">
                Reset
              </Button>
              <Button onClick={handleSave} className="flex-1 h-12 bg-blue-500 hover:bg-blue-600">
                Save Settings
              </Button>
            </div>
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <Card className="bg-white/90 backdrop-blur-sm border-0">
          <CardContent className="p-4">
            <h3 className="font-semibold mb-3 text-center">Quick Actions</h3>
            <div className="grid grid-cols-2 gap-2">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => updateLocalPreferences({ destination: "Paris, France" })}
                className="text-xs"
              >
                🇫🇷 Paris
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => updateLocalPreferences({ destination: "Tokyo, Japan" })}
                className="text-xs"
              >
                🇯🇵 Tokyo
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => updateLocalPreferences({ destination: "New York, USA" })}
                className="text-xs"
              >
                🇺🇸 New York
              </Button>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => updateLocalPreferences({ destination: "London, UK" })}
                className="text-xs"
              >
                🇬🇧 London
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
