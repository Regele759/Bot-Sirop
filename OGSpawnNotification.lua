-- OG Spawn Notification Script for Roblox with Discord Integration
-- Place this in ServerScriptService

local Players = game:GetService("Players")
local Workspace = game:GetWorkspace()
local HttpService = game:GetService("HttpService")

-- Configuration
local OG_MODEL_NAME = "OG" -- Change this to your OG model name
local NOTIFICATION_DURATION = 10 -- Seconds
local DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1526981760964104262/vgalYOtRRi6094q_EoXliHAGVfXQmbbQTd34VbKM_lMpFyOPk--y7x2KBgvim1aUNt6K"
local DISCORD_CHANNEL_ID = "1526978299325321340"

-- Function to send message to Discord
local function sendDiscordNotification(username, userId, timestamp, location)
    if not DISCORD_WEBHOOK_URL or DISCORD_WEBHOOK_URL == "YOUR_WEBHOOK_URL_HERE" then
        print("WARNING: Discord webhook URL not configured!")
        return
    end
    
    local embedData = {
        embeds = {
            {
                title = "🎮 OG Spawned!",
                description = "An OG has just spawned in the game!",
                color = 16711680, -- Red color
                fields = {
                    {
                        name = "Username",
                        value = username,
                        inline = true
                    },
                    {
                        name = "User ID",
                        value = tostring(userId),
                        inline = true
                    },
                    {
                        name = "Time",
                        value = timestamp,
                        inline = false
                    },
                    {
                        name = "Location",
                        value = location,
                        inline = false
                    }
                },
                timestamp = os.date("!%Y-%m-%dT%H:%M:%SZ")
            }
        }
    }
    
    local success, response = pcall(function()
        return HttpService:PostAsync(
            DISCORD_WEBHOOK_URL,
            HttpService:JSONEncode(embedData),
            Enum.HttpContentType.ApplicationJson
        )
    end)
    
    if success then
        print("✅ Discord notification sent successfully!")
    else
        print("❌ Failed to send Discord notification: " .. tostring(response))
    end
end

-- Function to create and display spawn notification
local function notifyOGSpawn(ogModel, player)
    local userId = player.UserId
    local username = player.Name
    local timestamp = os.date("%H:%M:%S")
    
    -- Create notification message
    local message = string.format(
        "[OG SPAWNED]\n" ..
        "Username: %s\n" ..
        "User ID: %d\n" ..
        "Time: %s\n" ..
        "Location: %s",
        username,
        userId,
        timestamp,
        ogModel.Name
    )
    
    -- Broadcast to server console
    print(message)
    
    -- Send to Discord
    sendDiscordNotification(username, userId, timestamp, ogModel.Name)
end

-- Function to detect OG spawns
local function onOGSpawned(ogModel)
    -- Find the player who should receive the notification
    -- Adjust this logic based on your game mechanics
    
    local nearestPlayer = nil
    local closestDistance = math.huge
    
    for _, player in pairs(Players:GetPlayers()) do
        if player.Character then
            local distance = (player.Character.HumanoidRootPart.Position - ogModel.Position).Magnitude
            if distance < closestDistance then
                closestDistance = distance
                nearestPlayer = player
            end
        end
    end
    
    if nearestPlayer then
        notifyOGSpawn(ogModel, nearestPlayer)
    end
end

-- Function to monitor for OG spawns
local function monitorOGSpawns()
    Workspace.ChildAdded:Connect(function(child)
        if child.Name == OG_MODEL_NAME then
            onOGSpawned(child)
        end
    end)
end

-- Start monitoring when game loads
monitorOGSpawns()

-- Handle existing OGs in workspace
for _, child in pairs(Workspace:GetChildren()) do
    if child.Name == OG_MODEL_NAME then
        -- Optional: Handle any existing OGs
    end
end

print("OG Spawn Notification system initialized!")
print("Discord Channel ID: " .. DISCORD_CHANNEL_ID)
