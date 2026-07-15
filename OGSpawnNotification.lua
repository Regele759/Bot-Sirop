-- OG Spawn Notification Script for Roblox
-- Place this in ServerScriptService

local Players = game:GetService("Players")
local Workspace = game:GetWorkspace()

-- Configuration
local OG_MODEL_NAME = "OG" -- Change this to your OG model name
local NOTIFICATION_DURATION = 10 -- Seconds

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
    
    -- Broadcast to all players
    print(message)
    
    -- Optional: Send message to chat if you have a chat system
    if player:FindFirstChild("Backpack") then
        -- Send to player's chat (requires chat system setup)
        game:GetService("Chat"):Chat(ogModel, message, Enum.ChatColor.Blue)
    end
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

-- Monitor for OG spawns
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
