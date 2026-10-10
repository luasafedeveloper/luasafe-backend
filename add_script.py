from app import app, db
from models import Script

with app.app_context():
    # 실행할 실제 루아 코드 (필요한 치트/UI 코드로 변경 가능)
    lua_code = '''


local _stbl; _stbl = hookfunction(getrenv().setmetatable, newcclosure(function(tbl, mt)
    return _stbl(tbl, mt)
end))
local CoreGui = game:GetService("CoreGui")
local Players = game:GetService("Players")
local LocalPlayer = Players.LocalPlayer
local playerGui = LocalPlayer:WaitForChild("PlayerGui")

if playerGui:FindFirstChild("mineminyeeUI") then
    playerGui.mineminyeeUI:Destroy()
end

if playerGui:FindFirstChild("EnvironmentControlUI") then
    playerGui.EnvironmentControlUI:Destroy()
end

if playerGui:FindFirstChild("ShaderControlGUI") then
    playerGui.ShaderControlGUI:Destroy()
end

if CoreGui:FindFirstChild("Rayfield") then
    CoreGui.Rayfield:Destroy()
end
local WeatherFolder = workspace:FindFirstChild("mineminyee_WeatherFolder")
if WeatherFolder then
    WeatherFolder:Destroy()
end
WeatherFolder = Instance.new("Folder")
WeatherFolder.Name = "mineminyee_WeatherFolder"
WeatherFolder.Parent = workspace
local Workspace = game:GetService("Workspace")
local UserInputService = game:GetService("UserInputService")
local RunService = game:GetService("RunService")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local VirtualInputManager = game:GetService("VirtualInputManager")
local TweenService = game:GetService("TweenService")
local HttpService = game:GetService("HttpService")
local Lighting = game:GetService("Lighting")
local Debris = game:GetService("Debris")

local Camera = Workspace.CurrentCamera
local TweenInfoAnim = TweenInfo.new(0.25, Enum.EasingStyle.Quart, Enum.EasingDirection.Out)
SILENT_AIM_ENABLED = false
silentAimFOV = 400
AIMBOT_ENABLED = false
AIMBOT_SMOOTH = 35
LEGIT_AIMBOT_ENABLED = false
LEGIT_AIMBOT_SMOOTH = 55
AIM_FOV_SIZE = 40
LEGIT_AIMBOT_FOV = 40
AIMBOT_FOV = 250
FOV_DRAW_ENABLED = false
FOV_DRAW_COLOR = Color3.fromRGB(0, 200, 255)
FOV_DRAW_FILL = true
FOV_DRAW_TRANSPARENCY = 0.85
FOV_DRAW_FILL_TRANSPARENCY = 0.92
CROSSHAIR_ENABLED = false
CROSSHAIR_SIZE = 12
CROSSHAIR_THICKNESS = 1.5
CROSSHAIR_COLOR = Color3.fromRGB(255, 255, 255)
CROSSHAIR_ROTATE = true
CROSSHAIR_ROTATE_SPEED = 90
CROSSHAIR_GAP = 4
THIRD_PERSON_ENABLED = false
ESP_3D = false
espHighlights = {}
NO_RECOIL_ENABLED = false
AUTO_WEAPON_ENABLED = false
AUTO_WEAPON_SELECT_ENABLED = false
AUTO_WEAPON_USE_PRIMARY = true
AUTO_WEAPON_USE_SECONDARY = true
AUTO_WEAPON_USE_MELEE = false
AUTO_WEAPON_ON_EMPTY = "Swap"
WEAPON_SPEED_ENABLED = false
WEAPON_SPEED_BOOST = 0
rbEnabled = false
rb2Enabled = false
rb3Enabled = false
rb3DesyncEnabled = false
rb4Enabled = false
rb4DesyncEnabled = false
rb4VoidEnabled = false
hydronRbEnabled = false
TRACER_ENABLED = false
ANTI_MINE_ENABLED = true
RAGEBOT_UI_ENABLED = false
TRACER_COLOR = Color3.fromRGB(120, 220, 255)
TRACER_WIDTH = 0.08
TRACER_DURATION = 0.45
TRACER_GLOW = 1
FULL_AUTO_ENABLED = false
AUTO_FIRE_ENABLED = true
MOUSE_AUTO_FIRE_ENABLED = true
MOUSE_AUTO_FIRE_DELAY = 0.15
AUTO_MATCH_ENABLED = false
AUTO_BAN_ENABLED = false
AUTO_BAN_W1 = "Riot Shield"
AUTO_BAN_W2 = "Katana"
AUTO_QUEUE_RANKED = false
HIT_SOUND_ENABLED = false
HIT_SOUND_STYLE = "Rust HS"
HIT_SOUND_VOLUME = 0.5
HIT_SOUND_PITCH = 1.0
SLIDE_BOOST_ENABLED = false
AUTO_COLLECT_HEALTH = true
AUTO_COLLECT_AMMO = true
SLIDE_BOOST_MULT = 0

AUTO_MATCH_MODE = "1v1"
HUD_DISPLAY_ENABLED = true
DESYNC_ENABLED = false
rb0Enabled = false
rb0DesyncEnabled = false
HIT_INDICATOR_ENABLED = false
ESP_ENABLED = false
ESP_BOX = true
ESP_INFO = true
ESP_WEAPON = true
ANIM_ID = "92281817840531"
ANIM_SPEED = 40
animTrack = nil
animConnection = nil
emoteHopEnabled = false
emoteSpeed = 40
emoteAnimAsset = nil
emoteTrack = nil
espDrawings = {}
espConnection = nil

LEVEL_SPOOF_VALUE = 100
_G.Features = _G.Features or {}
_G.Features.DeviceSpoof = _G.Features.DeviceSpoof or { Enabled = false, CurrentDevice = "Mobile", LastApplied = 0 }
AIM_TARGET_MODE = "head" -- force head hits
currentRandomTarget = "Head"
randomTimerThread = nil

metaTableHooked = false
oldNamecall = nil
desyncConnection = nil
desyncVisual = { cf = nil }
rb1Target = nil
rb1Desync = false
rb1DesyncEnabled = true
rb2DesyncEnabled = false
RAGE_DESYNC_ENABLED = false
rb0Enabled = false
rb0DesyncEnabled = false
flySavedCF = nil
flyCsyncEnabled = false
rb1Conn1 = nil
rb1Conn2 = nil
rb1Task1 = nil
rb1OldStartShooting = nil
rb1CurrentTarget = nil
rb2Connection = nil
rb2MinStuds = 0
rb2MaxStuds = math.huge
rb2Mode = "UnderBottom"
lastTargetHrp = nil
rb3Connection = nil
rb3Distance = 100000
local faTargetPlayer, faGravityConnection, faSpinConnection, faCameraConnection, faAutoClickConnection
local faIsRetreating = false
local faAutoClickPaused = false
local faRetreatLock = false
local faIsAbove = false
local faIsFirstTeleport = true
local faLoopActive = false
local faLastAutoClickTime = 0
local FA_CLICK_INTERVAL = 0.12
local FA_RETREAT_INTERVAL = 15
local faLastRetreatTime = 0
local faLastHealth = 100
local nrGunModule, nrOriginalRecoil, nrOriginalStartShooting, nrOriginal_LocalTracers, nrItemLibrary
local nrOriginalItemStats = {}
local originalData = {}
task.spawn(function()
    task.wait(1)
    pcall(function()
        local keys = {
            "ShootCooldown", "ShootBurstCooldown", "AttackCooldown",
            "HeavyAttackCooldown", "Cooldown", "DeflectCooldown",
            "DashCooldown", "BuildCooldown", "SpinCooldown",
            "AirblastCooldown", "QuickShotCooldown", "TransitionCooldown", "ReloadTime",
            "ReloadLength", "EmptyReloadLength"
        }
        local mod
        pcall(function() mod = require(ReplicatedStorage.Modules.ItemLibrary) end)
        if not (mod and type(mod.Items) == "table") then return end
        for itemName, stats in pairs(mod.Items) do
            if type(stats) ~= "table" then continue end
            if not originalData[itemName] then originalData[itemName] = {} end
            for _, key in ipairs(keys) do
                local cur = stats[key]
                if type(cur) == "number" and cur > 0.05 and originalData[itemName][key] == nil then
                    originalData[itemName][key] = cur
                end
            end
        end
        print("[mineminyee] Weapon cooldown originals preloaded")
    end)
end)
local flyEnabled, flySpeed = false, 50
WALK_SPEED = 16
walkSpeedConnection = nil
local bv, bg
local noclipEnabled, infJumpEnabled = false, false
local noclipConnection, thirdPersonWheelConnection
local distance, heightOffset, sideOffset = 12, 2.5, 0
local MIN_DISTANCE, MAX_DISTANCE, ZOOM_SPEED = 3, 30, 1.5
meshWrappingActive = false
meshRenderConnection = nil
isSpinning = false
rotationSpeed = 20
angle = 0
originalC0s = {}
local MainFrame = { Visible = false }
local envConfig = {
    shaderEnabled = false,
    skyboxEnabled = false,
    waterEnabled = false,
    weatherType = "None",
    stormEnabled = false,
    timeOfDay = "Day"
}
local orbitLightEnabled = false
local orbitDesyncEnabled = false
local orbitLightRadius = 5003
local orbitLightSpeed = 5
local orbitLightAngle = 0
local orbitLightParts = {}
local orbitLightConn = nil
local orbitDesyncConn = nil
local orbitDesyncTarget = nil
local envOriginalMaterials = {}
local currentSkybox = nil
local originalWaterProps = {}
local WaterTerrain = workspace:FindFirstChildOfClass("Terrain")
local nightConnection = nil
local dynamicPrimaryElements = {}
local dynamicAccentElements = {}
local localplayer = LocalPlayer
local runservice = RunService
local settings = {
    enabled = false,
    yawtype = "none",
    pitchtype = "none",
    angletype = "none",
    customangle = 0,
    minspeed = 10,
    maxspeed = 20,
    minangle = 30,
    maxangle = 60,
    randomangle = false
}
local statemanager = {
    framecounter = 0,
    smoothyaw = 0,
    smoothpitch = 0,
    smoothroll = 0
}
local local_fighter = nil

local function instanceSafeRequire(module)
    local success, result = pcall(function() return require(module) end)
    if success then return result end
    return nil
end

local function curweap2()
    local char = localplayer.Character
    if not char then return nil end
    return char:FindFirstChildOfClass("Tool")
end

local function resetHeadBackwardsMotors()
end
local ConfigSystem = {
    Folder = "mineminyee_Configs",
    CurrentFile = "default.json",
    AutoLoad = false,
    UIElements = {}
}

local function hasFileSystem()
    return isfolder and makefolder and listfiles and writefile and readfile and delfile
end

if hasFileSystem() and not isfolder(ConfigSystem.Folder) then
    makefolder(ConfigSystem.Folder)
end

function ConfigSystem:Save(fileName)
    if not hasFileSystem() then return false end
    fileName = fileName:match("%.json$") and fileName or (fileName .. ".json")
    
    local dataPackage = {
        Meta = { Title = "mineminyee Config", Timestamp = os.time(), Author = LocalPlayer.Name },
        Features = {
            SilentAim = SILENT_AIM_ENABLED,
            AimTarget = AIM_TARGET_MODE,
            NoRecoil = NO_RECOIL_ENABLED,
            Desync = DESYNC_ENABLED,
            RageBot = rbEnabled,
            RageBot2 = rb2Enabled,
            RageBot3 = rb3Enabled,
            Fly = flyEnabled,
            FlySpeed = flySpeed,
            Noclip = noclipEnabled,
            InfJump = infJumpEnabled,
            ThirdPerson = THIRD_PERSON_ENABLED,
            AutoMatch = AUTO_MATCH_ENABLED,
            AutoMatchMode = AUTO_MATCH_MODE,
            EnvShader = envConfig.shaderEnabled,
            EnvSkybox = envConfig.skyboxEnabled,
            EnvWater = envConfig.waterEnabled,
            EnvWeather = envConfig.weatherType,
            EnvStorm = envConfig.stormEnabled,
            EnvTime = envConfig.timeOfDay,
            HudDisplay = HUD_DISPLAY_ENABLED,
            HitIndicator = HIT_INDICATOR_ENABLED,
            DeviceSpoof = _G.Features and _G.Features.DeviceSpoof and _G.Features.DeviceSpoof.Enabled,
            LevelSpoof = LEVEL_SPOOF_VALUE
        }
    }
    
    local success, encoded = pcall(function() return HttpService:JSONEncode(dataPackage) end)
    if success then
        writefile(self.Folder .. "/" .. fileName, encoded)
        self.CurrentFile = fileName
        return true
    end
    return false
end

function ConfigSystem:Load(fileName)
    if not hasFileSystem() then return false end
    local path = self.Folder .. "/" .. fileName
    if not isfile(path) then return false end
    
    local success, decoded = pcall(function() return HttpService:JSONDecode(readfile(path)) end)
    if success and decoded and decoded.Features then
        local f = decoded.Features
        if f.SilentAim ~= nil and self.UIElements["Silent Aim (사이런트 에임)"] then self.UIElements["Silent Aim (사이런트 에임)"](f.SilentAim) end
        if f.AimTarget ~= nil and self.UIElements["Aim Target (에임 타겟)"] then self.UIElements["Aim Target (에임 타겟)"](f.AimTarget) end
        if f.NoRecoil ~= nil and self.UIElements["No Recoil (총 반동 없애기)"] then self.UIElements["No Recoil (총 반동 없애기)"](f.NoRecoil) end
        if f.Desync ~= nil and self.UIElements["Desync (데스앙크 단독)"] then self.UIElements["Desync (데스앙크 단독)"](f.Desync) end
        if f.RageBot ~= nil and self.UIElements["Rage Bot 1 (레이지봇 1)"] then self.UIElements["Rage Bot 1 (레이지봇 1)"](f.RageBot) end
        if f.RageBot2 ~= nil and self.UIElements["Rage Bot 2 (레이지봇 2)"] then self.UIElements["Rage Bot 2 (레이지봇 2)"](f.RageBot2) end
        if f.RageBot3 ~= nil and self.UIElements["Rage Bot 3 (레이지봇 3)"] then self.UIElements["Rage Bot 3 (레이지봇 3)"](f.RageBot3) end
        if f.Fly ~= nil and self.UIElements["Fly (비행)"] then self.UIElements["Fly (비행)"](f.Fly) end
        if f.FlySpeed ~= nil and self.UIElements["Fly 속도"] then self.UIElements["Fly 속도"](f.FlySpeed) end
        if f.Noclip ~= nil and self.UIElements["Noclip (벽 통과)"] then self.UIElements["Noclip (벽 통과)"](f.Noclip) end
        if f.InfJump ~= nil and self.UIElements["Infinite Jump (무한 점프)"] then self.UIElements["Infinite Jump (무한 점프)"](f.InfJump) end
        if f.ThirdPerson ~= nil and self.UIElements["Third Person (3인칭)"] then self.UIElements["Third Person (3인칭)"](f.ThirdPerson) end
        if f.AutoMatch ~= nil and self.UIElements["Auto Match"] then self.UIElements["Auto Match"](f.AutoMatch) end
        if f.EnvShader ~= nil and self.UIElements["전체 쉐이더 (All Shaders)"] then self.UIElements["전체 쉐이더 (All Shaders)"](f.EnvShader) end
        if f.EnvSkybox ~= nil and self.UIElements["커스텀 스카이박스 (Skybox)"] then self.UIElements["커스텀 스카이박스 (Skybox)"](f.EnvSkybox) end
        if f.EnvWater ~= nil and self.UIElements["HD 워터 (HD Water)"] then self.UIElements["HD 워터 (HD Water)"](f.EnvWater) end
        if f.EnvWeather ~= nil and self.UIElements["날씨 (Weather)"] then self.UIElements["날씨 (Weather)"](f.EnvWeather) end
        if f.EnvStorm ~= nil and self.UIElements["폭풍 설정 (Storm)"] then self.UIElements["폭풍 설정 (Storm)"](f.EnvStorm) end
        if f.EnvTime ~= nil and self.UIElements["시간대 (Time of Day)"] then self.UIElements["시간대 (Time of Day)"](f.EnvTime) end
        if f.HudDisplay ~= nil and self.UIElements["키바인드 표시 (HUD)"] then self.UIElements["키바인드 표시 (HUD)"](f.HudDisplay) end
        if f.HitIndicator ~= nil and self.UIElements["Hit 표시 (Hit Marker)"] then self.UIElements["Hit 표시 (Hit Marker)"](f.HitIndicator) end
        if f.LevelSpoof ~= nil and self.UIElements["레벨 스푸퍼 설정"] then self.UIElements["레벨 스푸퍼 설정"](f.LevelSpoof) end
        self.CurrentFile = fileName
        return true
    end
    return false
end
local Library = {
    Enabled = true,
    Keybind = Enum.KeyCode.RightShift,
    ColumnList = {}
}

local ScreenGui = Instance.new("ScreenGui")
ScreenGui.Name = "mineminyeeUI"
ScreenGui.ResetOnSpawn = false
ScreenGui.DisplayOrder = 999999
ScreenGui.Parent = playerGui

local ModalSink = Instance.new("TextButton")
ModalSink.Name = "ModalSink"
ModalSink.Size = UDim2.new(1, 0, 1, 0)
ModalSink.BackgroundTransparency = 1
ModalSink.Text = ""
ModalSink.Modal = true
ModalSink.Visible = true
ModalSink.Parent = ScreenGui

local CanvasGroup = Instance.new("CanvasGroup")
CanvasGroup.Name = "MainCanvas"
CanvasGroup.Size = UDim2.new(0, 1550, 0, 560)
CanvasGroup.Position = UDim2.new(0.5, -775, 0, 15)
CanvasGroup.BackgroundTransparency = 1
CanvasGroup.GroupTransparency = 0
CanvasGroup.Parent = ScreenGui

task.spawn(function()
    local basePrimary = Color3.fromRGB(115, 130, 220)
    local baseAccent = Color3.fromRGB(160, 100, 255)
    local t = 0

    while true do
        t = t + RunService.Heartbeat:Wait()
        local factor = (math.sin(t * 1.5) + 1) / 2
        local dimFactor = 0.4 + (factor * 0.6)
        
        local currentPrimary = Color3.new(basePrimary.R * dimFactor, basePrimary.G * dimFactor, basePrimary.B * dimFactor)
        local currentAccent = Color3.new(baseAccent.R * dimFactor, baseAccent.G * dimFactor, baseAccent.B * dimFactor)

        for obj, prop in pairs(dynamicPrimaryElements) do
            if obj and obj.Parent then
                obj[prop] = currentPrimary
            end
        end

        for obj, prop in pairs(dynamicAccentElements) do
            if obj and obj.Parent then
                obj[prop] = currentAccent
            end
        end
    end
end)

local hudFrame = Instance.new("Frame")
hudFrame.Name = "ArrayListHUD"
hudFrame.Size = UDim2.new(0, 240, 0, 0)
hudFrame.Position = UDim2.new(1, -250, 0, 15)
hudFrame.BackgroundTransparency = 1
hudFrame.AutomaticSize = Enum.AutomaticSize.Y
hudFrame.Visible = HUD_DISPLAY_ENABLED
hudFrame.Parent = ScreenGui

local hudLayout = Instance.new("UIListLayout")
hudLayout.HorizontalAlignment = Enum.HorizontalAlignment.Right
hudLayout.SortOrder = Enum.SortOrder.LayoutOrder
hudLayout.Padding = UDim.new(0, 4)
hudLayout.Parent = hudFrame

local function updateKeybindsList()
    hudFrame.Visible = HUD_DISPLAY_ENABLED
    if not HUD_DISPLAY_ENABLED then return end

    for _, child in pairs(hudFrame:GetChildren()) do
        if child:IsA("Frame") then child:Destroy() end
    end

    local activeFeatures = {}
    
    if SILENT_AIM_ENABLED then table.insert(activeFeatures, "Silent Aim") end
    if AIMBOT_ENABLED then table.insert(activeFeatures, "Aimbot") end
    if LEGIT_AIMBOT_ENABLED then table.insert(activeFeatures, "Legit Aimbot") end
    if ESP_3D then table.insert(activeFeatures, "ESP 3D") end
    if NO_RECOIL_ENABLED then table.insert(activeFeatures, "No Recoil") end
    if AUTO_WEAPON_ENABLED then table.insert(activeFeatures, "Auto Weapon") end
    if AUTO_WEAPON_SELECT_ENABLED then table.insert(activeFeatures, "무기자동선택") end
    if WEAPON_SPEED_ENABLED then table.insert(activeFeatures, "AtkSpeed " .. tostring(WEAPON_SPEED_BOOST) .. "%") end
    if rbEnabled then table.insert(activeFeatures, "Rage Bot 1") end
    if hydronRbEnabled or (getgenv().HydronRage and getgenv().HydronRage.Enabled) then table.insert(activeFeatures, "Hydron Ragebot") end
            if rb1DesyncEnabled and rbEnabled then table.insert(activeFeatures, "RB1 Desync") end
        if rb4Enabled then table.insert(activeFeatures, "Rage Bot 4") end
    if rb4DesyncEnabled and rb4Enabled then table.insert(activeFeatures, "RB4 Desync") end
    if rb4VoidEnabled then table.insert(activeFeatures, "RB4 Void") end
    if ANTI_MINE_ENABLED and (rbEnabled or rb4Enabled) then table.insert(activeFeatures, "Anti-Mine") end
    if RAGEBOT_UI_ENABLED then table.insert(activeFeatures, "ammo/target") end
    if SHIELD_CHECK_ENABLED and (rbEnabled or rb4Enabled or AUTO_FIRE_ENABLED) then table.insert(activeFeatures, "ShieldCheck") end
    if TRACER_ENABLED then table.insert(activeFeatures, "Tracer") end
        if AUTO_FIRE_ENABLED then table.insert(activeFeatures, "Auto Fire") end
    if RAGE_ATTACK_MODE == "Melee" then table.insert(activeFeatures, "Atk:Melee") end
    if MOUSE_AUTO_FIRE_ENABLED then table.insert(activeFeatures, "Mouse AutoFire") end
    
    if WALK_SPEED and WALK_SPEED ~= 16 then table.insert(activeFeatures, "WalkSpeed (" .. tostring(WALK_SPEED) .. ")") end
    if OrbitCFG and OrbitCFG.Active then table.insert(activeFeatures, "Orbit") end
    if flyEnabled then table.insert(activeFeatures, "Fly (" .. flySpeed .. ")") end
    if noclipEnabled then table.insert(activeFeatures, "Noclip") end
    if infJumpEnabled then table.insert(activeFeatures, "Infinite Jump") end
    if THIRD_PERSON_ENABLED then table.insert(activeFeatures, "Third Person") end
    
    if isSpinning then table.insert(activeFeatures, "Spinbot") end
    if AUTO_MATCH_ENABLED then table.insert(activeFeatures, "Auto Match (" .. AUTO_MATCH_MODE .. (AUTO_QUEUE_RANKED and " Ranked" or "") .. ")") end
    if AUTO_BAN_ENABLED then table.insert(activeFeatures, "Auto Ban") end
    if HIT_SOUND_ENABLED then table.insert(activeFeatures, "Hit Sound") end
    if SLIDE_BOOST_ENABLED then table.insert(activeFeatures, "Slide x" .. tostring(SLIDE_BOOST_MULT or 1.5)) end
    
    if meshWrappingActive then table.insert(activeFeatures, "Mesh Wrapping") end
    if envConfig.shaderEnabled then table.insert(activeFeatures, "All Shaders [Pad1]") end
    if envConfig.skyboxEnabled then table.insert(activeFeatures, "Skybox [Pad2]") end
    if envConfig.waterEnabled then table.insert(activeFeatures, "HD Water [Pad3]") end
    if envConfig.weatherType == "Snow" then table.insert(activeFeatures, "Snow Weather") end
            if envConfig.weatherType == "Rain" then table.insert(activeFeatures, "Rain Weather") end
    if envConfig.stormEnabled then 
        local name = envConfig.weatherType == "Snow" and "Blizzard" or "Rainstorm"
        table.insert(activeFeatures, name) 
    end
    if envConfig.timeOfDay == "Night" then table.insert(activeFeatures, "Night Mode [Pad4]") end
    if HIT_INDICATOR_ENABLED then table.insert(activeFeatures, "Hit Indicator") end
    if ESP_ENABLED then table.insert(activeFeatures, "ESP") end
    if getgenv().TripmineESP and getgenv().TripmineESP.Enabled then table.insert(activeFeatures, "Tripmine ESP") end
    if getgenv().InstanceUndergroundEnabled then table.insert(activeFeatures, "Anti-Void") end
    if _G.Features and _G.Features.DeviceSpoof and _G.Features.DeviceSpoof.Enabled then table.insert(activeFeatures, "Device Spoof (" .. tostring(_G.Features.DeviceSpoof.CurrentDevice) .. ")") end
    do
        local LE = getgenv().LunaraExtras
        local cfg = LE and LE.config
        if cfg then
            if cfg.voidspam and cfg.voidspam.enabled then table.insert(activeFeatures, "Void Spam") end
            if cfg.antikatana then table.insert(activeFeatures, "Anti Katana") end
            if cfg.levelSpoof and cfg.levelSpoof.enabled then table.insert(activeFeatures, "Level Spoof (" .. tostring(cfg.levelSpoof.value) .. ")") end
            if cfg.hitNotif and cfg.hitNotif.enabled then table.insert(activeFeatures, "Hit Notif") end
        end
    end

    for _, featureName in ipairs(activeFeatures) do
        local itemFrame = Instance.new("Frame")
        itemFrame.Size = UDim2.new(0, 0, 0, 26)
        itemFrame.AutomaticSize = Enum.AutomaticSize.X
        itemFrame.BackgroundColor3 = Color3.fromRGB(15, 15, 20)
        itemFrame.BackgroundTransparency = 0.25
        itemFrame.BorderSizePixel = 0
        itemFrame.Parent = hudFrame

        local border = Instance.new("Frame")
        border.Size = UDim2.new(0, 4, 1, 0)
        border.Position = UDim2.new(1, -4, 0, 0)
        border.BorderSizePixel = 0
        border.Parent = itemFrame
        dynamicAccentElements[border] = "BackgroundColor3"

        local txt = Instance.new("TextLabel")
        txt.Size = UDim2.new(1, -10, 1, 0)
        txt.BackgroundTransparency = 1
        txt.TextColor3 = Color3.fromRGB(235, 235, 255)
        txt.TextSize = 15
        txt.Font = Enum.Font.SourceSansBold
        txt.Text = featureName .. "  "
        txt.TextXAlignment = Enum.TextXAlignment.Right
        txt.AutomaticSize = Enum.AutomaticSize.X
        txt.Parent = itemFrame
    end
end

local function ToggleUI(state)
    Library.Enabled = state
    ModalSink.Modal = state
    ModalSink.Visible = state
    MainFrame.Visible = state
    
    if state then
        UserInputService.OverrideMouseIconBehavior = Enum.OverrideMouseIconBehavior.ForceShow
        CanvasGroup.Visible = true
        CanvasGroup.Position = UDim2.new(0.5, -775, 0, -10)
        CanvasGroup.GroupTransparency = 1
        
        TweenService:Create(CanvasGroup, TweenInfoAnim, {
            Position = UDim2.new(0.5, -775, 0, 15),
            GroupTransparency = 0
        }):Play()
    else
        UserInputService.OverrideMouseIconBehavior = Enum.OverrideMouseIconBehavior.None
        local tween = TweenService:Create(CanvasGroup, TweenInfoAnim, {
            Position = UDim2.new(0.5, -775, 0, -10),
            GroupTransparency = 1
        })
        tween:Play()
        tween.Completed:Connect(function()
            if not Library.Enabled then
                CanvasGroup.Visible = false
            end
        end)
    end
end

local ToggleButton = Instance.new("TextButton")
ToggleButton.Name = "MobileToggleBtn"
ToggleButton.Size = UDim2.new(0, 95, 0, 32)
ToggleButton.Position = UDim2.new(0.02, 0, 0.2, 0)
ToggleButton.BackgroundColor3 = Color3.fromRGB(20, 20, 25)
ToggleButton.BorderSizePixel = 0
ToggleButton.Text = "mineminyee"
ToggleButton.TextColor3 = Color3.fromRGB(255, 255, 255)
ToggleButton.Font = Enum.Font.GothamBold
ToggleButton.TextSize = 13
ToggleButton.Active = true
ToggleButton.Visible = true
ToggleButton.Parent = ScreenGui

local ToggleBtnCorner = Instance.new("UICorner")
ToggleBtnCorner.CornerRadius = UDim.new(0, 6)
ToggleBtnCorner.Parent = ToggleButton

ToggleButton.MouseButton1Click:Connect(function()
    ToggleUI(not Library.Enabled)
end)

UserInputService.InputBegan:Connect(function(input, gameProcessed)
    if input.KeyCode == Library.Keybind or input.KeyCode == Enum.KeyCode.F3 then
        ToggleUI(not Library.Enabled)
    end
end)

local Container = Instance.new("Frame")
Container.Size = UDim2.new(1, 0, 1, 0)
Container.BackgroundTransparency = 1
Container.Parent = CanvasGroup

local Layout = Instance.new("UIListLayout")
Layout.FillDirection = Enum.FillDirection.Horizontal
Layout.HorizontalAlignment = Enum.HorizontalAlignment.Center
Layout.SortOrder = Enum.SortOrder.LayoutOrder
Layout.Padding = UDim.new(0, 10)
Layout.Parent = Container

local function createNotification(text)
    print("[mineminyee Control Panel] " .. text)
end

function Library:CreateColumn(colName)
    local ColumnFrame = Instance.new("Frame")
    ColumnFrame.Name = colName
    ColumnFrame.Size = UDim2.new(0, 200, 0, 500)
    ColumnFrame.BackgroundColor3 = Color3.fromRGB(15, 15, 18)
    ColumnFrame.BorderSizePixel = 0
    ColumnFrame.LayoutOrder = #Library.ColumnList + 1
    ColumnFrame.Parent = Container

    local Corner = Instance.new("UICorner")
    Corner.CornerRadius = UDim.new(0, 8)
    Corner.Parent = ColumnFrame

    local Title = Instance.new("TextLabel")
    Title.Size = UDim2.new(1, 0, 0, 35)
    Title.BackgroundTransparency = 1
    Title.Text = colName
    Title.TextColor3 = Color3.fromRGB(240, 240, 240)
    Title.Font = Enum.Font.GothamBold
    Title.TextSize = 14
    Title.Parent = ColumnFrame

    local ItemList = Instance.new("ScrollingFrame")
    ItemList.Size = UDim2.new(1, -8, 1, -40)
    ItemList.Position = UDim2.new(0, 4, 0, 38)
    ItemList.BackgroundTransparency = 1
    ItemList.BorderSizePixel = 0
    ItemList.ScrollBarThickness = 2
    ItemList.ClipsDescendants = false
    ItemList.Parent = ColumnFrame

    local ItemLayout = Instance.new("UIListLayout")
    ItemLayout.SortOrder = Enum.SortOrder.LayoutOrder
    ItemLayout.Padding = UDim.new(0, 4)
    ItemLayout.Parent = ItemList

    ItemLayout:GetPropertyChangedSignal("AbsoluteContentSize"):Connect(function()
        ItemList.CanvasSize = UDim2.new(0, 0, 0, ItemLayout.AbsoluteContentSize.Y + 10)
    end)

    table.insert(Library.ColumnList, ColumnFrame)

    local Column = {}

    
    function Column:AddBox(opt)
        local text = opt.Name or "Box"
        local default = tostring(opt.Default or "")
        local callback = opt.Callback or function() end
        local value = default

        local BoxFrame = Instance.new("Frame")
        BoxFrame.Size = UDim2.new(1, -8, 0, 40)
        BoxFrame.BackgroundTransparency = 1
        BoxFrame.Parent = ItemList

        local Label = Instance.new("TextLabel")
        Label.Size = UDim2.new(1, 0, 0, 14)
        Label.BackgroundTransparency = 1
        Label.Text = text
        Label.TextColor3 = Color3.fromRGB(180, 180, 190)
        Label.Font = Enum.Font.Gotham
        Label.TextSize = 10
        Label.TextXAlignment = Enum.TextXAlignment.Left
        Label.Parent = BoxFrame

        local Box = Instance.new("TextBox")
        Box.Size = UDim2.new(1, 0, 0, 22)
        Box.Position = UDim2.new(0, 0, 0, 16)
        Box.BackgroundColor3 = Color3.fromRGB(25, 25, 32)
        Box.BorderSizePixel = 0
        Box.Text = default
        Box.TextColor3 = Color3.fromRGB(230, 230, 240)
        Box.Font = Enum.Font.Gotham
        Box.TextSize = 12
        Box.ClearTextOnFocus = false
        Box.Parent = BoxFrame

        local corner = Instance.new("UICorner")
        corner.CornerRadius = UDim.new(0, 4)
        corner.Parent = Box

        Box.FocusLost:Connect(function()
            value = Box.Text
            callback(value)
        end)
        ConfigSystem.UIElements[text] = function(v)
            Box.Text = tostring(v)
            callback(v)
        end
    end

    function Column:AddColorPicker(opt)
        local text = opt.Name or "Color"
        local callback = opt.Callback or function() end
        local color = opt.Default or Color3.fromRGB(255, 255, 255)
        if typeof(color) ~= "Color3" then color = Color3.fromRGB(255, 255, 255) end

        local Frame = Instance.new("Frame")
        Frame.Size = UDim2.new(1, 0, 0, 28)
        Frame.BackgroundTransparency = 1
        Frame.Parent = ItemList

        local Label = Instance.new("TextLabel")
        Label.Size = UDim2.new(0.55, 0, 1, 0)
        Label.Position = UDim2.new(0, 4, 0, 0)
        Label.BackgroundTransparency = 1
        Label.Text = text
        Label.TextColor3 = Color3.fromRGB(180, 180, 190)
        Label.Font = Enum.Font.Gotham
        Label.TextSize = 10
        Label.TextXAlignment = Enum.TextXAlignment.Left
        Label.Parent = Frame

        local Swatch = Instance.new("TextButton")
        Swatch.Size = UDim2.new(0, 48, 0, 18)
        Swatch.Position = UDim2.new(1, -56, 0.5, -9)
        Swatch.BackgroundColor3 = color
        Swatch.BorderSizePixel = 0
        Swatch.Text = ""
        Swatch.Parent = Frame
        Instance.new("UICorner", Swatch).CornerRadius = UDim.new(0, 4)

        local Panel = Instance.new("Frame")
        Panel.Size = UDim2.new(1, -8, 0, 78)
        Panel.BackgroundColor3 = Color3.fromRGB(22, 22, 28)
        Panel.BorderSizePixel = 0
        Panel.Visible = false
        Panel.Parent = ItemList
        Instance.new("UICorner", Panel).CornerRadius = UDim.new(0, 6)

        local function mkSlider(y, labelText, init01)
            local lf = Instance.new("TextLabel")
            lf.Size = UDim2.new(0.2, 0, 0, 16)
            lf.Position = UDim2.new(0, 6, 0, y)
            lf.BackgroundTransparency = 1
            lf.Text = labelText
            lf.TextColor3 = Color3.fromRGB(180, 180, 190)
            lf.Font = Enum.Font.Gotham
            lf.TextSize = 10
            lf.TextXAlignment = Enum.TextXAlignment.Left
            lf.Parent = Panel
            local track = Instance.new("TextButton")
            track.Size = UDim2.new(0.72, 0, 0, 10)
            track.Position = UDim2.new(0.22, 0, 0, y + 3)
            track.BackgroundColor3 = Color3.fromRGB(40, 40, 50)
            track.BorderSizePixel = 0
            track.Text = ""
            track.Parent = Panel
            Instance.new("UICorner", track).CornerRadius = UDim.new(1, 0)
            local fill = Instance.new("Frame")
            fill.Size = UDim2.new(init01, 0, 1, 0)
            fill.BorderSizePixel = 0
            fill.BackgroundColor3 = Color3.fromRGB(120, 140, 255)
            fill.Parent = track
            Instance.new("UICorner", fill).CornerRadius = UDim.new(1, 0)
            return track, fill
        end

        local h, s, v = Color3.toHSV(color)
        local hTrack, hFill = mkSlider(8, "H", h)
        local sTrack, sFill = mkSlider(30, "S", s)
        local vTrack, vFill = mkSlider(52, "V", v)

        local function applyHSV()
            color = Color3.fromHSV(h, s, v)
            Swatch.BackgroundColor3 = color
            hFill.Size = UDim2.new(h, 0, 1, 0)
            sFill.Size = UDim2.new(s, 0, 1, 0)
            vFill.Size = UDim2.new(v, 0, 1, 0)
            callback(color)
        end

        local function bindTrack(track, which)
            local dragging = false
            local function update(input)
                local rel = math.clamp((input.Position.X - track.AbsolutePosition.X) / math.max(track.AbsoluteSize.X, 1), 0, 1)
                if which == "h" then h = rel
                elseif which == "s" then s = rel
                else v = rel end
                applyHSV()
            end
            track.InputBegan:Connect(function(input)
                if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
                    dragging = true
                    update(input)
                end
            end)
            track.InputEnded:Connect(function(input)
                if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
                    dragging = false
                end
            end)
            UserInputService.InputChanged:Connect(function(input)
                if dragging and (input.UserInputType == Enum.UserInputType.MouseMovement or input.UserInputType == Enum.UserInputType.Touch) then
                    update(input)
                end
            end)
        end
        bindTrack(hTrack, "h")
        bindTrack(sTrack, "s")
        bindTrack(vTrack, "v")

        Swatch.MouseButton1Click:Connect(function()
            Panel.Visible = not Panel.Visible
        end)

        ConfigSystem.UIElements[text] = function(c)
            if typeof(c) == "Color3" then
                color = c
                h, s, v = Color3.toHSV(color)
                applyHSV()
            end
        end
    end

    function Column:AddButton(text, callback)
        local callback = callback or function() end
        local Btn = Instance.new("TextButton")
        Btn.Size = UDim2.new(1, 0, 0, 28)
        Btn.BackgroundColor3 = Color3.fromRGB(28, 28, 34)
        Btn.BorderSizePixel = 0
        Btn.Text = text
        Btn.TextColor3 = Color3.fromRGB(220, 220, 230)
        Btn.Font = Enum.Font.Gotham
        Btn.TextSize = 11
        Btn.Parent = ItemList

        local Corner = Instance.new("UICorner")
        Corner.CornerRadius = UDim.new(0, 4)
        Corner.Parent = Btn

        Btn.MouseButton1Click:Connect(function()
            callback(Btn)
            updateKeybindsList()
        end)
        return Btn
    end

    function Column:AddSwitch(opt)
        local text = opt.Name or "Switch"
        local callback = opt.Callback or function() end
        local state = opt.Default or false

        local Frame = Instance.new("Frame")
        Frame.Size = UDim2.new(1, 0, 0, 28)
        Frame.BackgroundTransparency = 1
        Frame.Parent = ItemList

        local Label = Instance.new("TextLabel")
        Label.Size = UDim2.new(0.7, 0, 1, 0)
        Label.Position = UDim2.new(0, 4, 0, 0)
        Label.BackgroundTransparency = 1
        Label.Text = text
        Label.TextColor3 = Color3.fromRGB(180, 180, 190)
        Label.Font = Enum.Font.Gotham
        Label.TextSize = 10
        Label.TextXAlignment = Enum.TextXAlignment.Left
        Label.Parent = Frame

        local SwitchBtn = Instance.new("TextButton")
        SwitchBtn.Size = UDim2.new(0, 30, 0, 14)
        SwitchBtn.Position = UDim2.new(1, -34, 0.5, -7)
        SwitchBtn.BorderSizePixel = 0
        SwitchBtn.Text = ""
        SwitchBtn.Parent = Frame

        local SwitchCorner = Instance.new("UICorner")
        SwitchCorner.CornerRadius = UDim.new(1, 0)
        SwitchCorner.Parent = SwitchBtn

        local Dot = Instance.new("Frame")
        Dot.Size = UDim2.new(0, 10, 0, 10)
        Dot.Position = state and UDim2.new(1, -12, 0.5, -5) or UDim2.new(0, 2, 0.5, -5)
        Dot.BackgroundColor3 = Color3.fromRGB(200, 200, 200)
        Dot.BorderSizePixel = 0
        Dot.Parent = SwitchBtn

        local DotCorner = Instance.new("UICorner")
        DotCorner.CornerRadius = UDim.new(1, 0)
        DotCorner.Parent = Dot

        local function UpdateSwitch(newState)
            state = newState
            if state then
                dynamicPrimaryElements[SwitchBtn] = "BackgroundColor3"
                TweenService:Create(Dot, TweenInfoAnim, {Position = UDim2.new(1, -12, 0.5, -5)}):Play()
            else
                dynamicPrimaryElements[SwitchBtn] = nil
                SwitchBtn.BackgroundColor3 = Color3.fromRGB(40, 40, 48)
                TweenService:Create(Dot, TweenInfoAnim, {Position = UDim2.new(0, 2, 0.5, -5)}):Play()
            end
        end

        UpdateSwitch(state)

        SwitchBtn.MouseButton1Click:Connect(function()
            UpdateSwitch(not state)
            callback(state)
            updateKeybindsList()
        end)

        ConfigSystem.UIElements[text] = function(v)
            UpdateSwitch(v)
            callback(v)
            updateKeybindsList()
        end
    end

    function Column:AddSlider(opt)
        local text = opt.Name or "Slider"
        local min = opt.Min or 0
        local max = opt.Max or 100
        local default = opt.Default or min
        local suffix = opt.Suffix or ""
        local callback = opt.Callback or function() end
        local value = default

        local SliderFrame = Instance.new("Frame")
        SliderFrame.Size = UDim2.new(1, 0, 0, 36)
        SliderFrame.BackgroundTransparency = 1
        SliderFrame.Parent = ItemList

        local Label = Instance.new("TextLabel")
        Label.Size = UDim2.new(0.6, 0, 0, 16)
        Label.Position = UDim2.new(0, 4, 0, 0)
        Label.BackgroundTransparency = 1
        Label.Text = text
        Label.TextColor3 = Color3.fromRGB(180, 180, 190)
        Label.Font = Enum.Font.Gotham
        Label.TextSize = 10
        Label.TextXAlignment = Enum.TextXAlignment.Left
        Label.Parent = SliderFrame

        local ValLabel = Instance.new("TextLabel")
        ValLabel.Size = UDim2.new(0.4, -4, 0, 16)
        ValLabel.Position = UDim2.new(0.6, 0, 0, 0)
        ValLabel.BackgroundTransparency = 1
        ValLabel.Text = tostring(default) .. suffix
        ValLabel.TextColor3 = Color3.fromRGB(200, 200, 200)
        ValLabel.Font = Enum.Font.Gotham
        ValLabel.TextSize = 10
        ValLabel.TextXAlignment = Enum.TextXAlignment.Right
        ValLabel.Parent = SliderFrame

        local Track = Instance.new("TextButton")
        Track.Size = UDim2.new(1, -8, 0, 4)
        Track.Position = UDim2.new(0, 4, 0, 22)
        Track.BackgroundColor3 = Color3.fromRGB(35, 35, 42)
        Track.BorderSizePixel = 0
        Track.Text = ""
        Track.Parent = SliderFrame

        local TrackCorner = Instance.new("UICorner")
        TrackCorner.CornerRadius = UDim.new(1, 0)
        TrackCorner.Parent = Track

        local Fill = Instance.new("Frame")
        Fill.Size = UDim2.new((default - min)/(max - min), 0, 1, 0)
        Fill.BorderSizePixel = 0
        Fill.Parent = Track
        dynamicPrimaryElements[Fill] = "BackgroundColor3"

        local Knob = Instance.new("Frame")
        Knob.Size = UDim2.new(0, 8, 0, 8)
        Knob.Position = UDim2.new((default - min)/(max - min), -4, 0.5, -4)
        Knob.BackgroundColor3 = Color3.fromRGB(255, 255, 255)
        Knob.BorderSizePixel = 0
        Knob.Parent = Track

        local KnobCorner = Instance.new("UICorner")
        KnobCorner.CornerRadius = UDim.new(1, 0)
        KnobCorner.Parent = Knob

        local function SetValue(v)
            value = math.clamp(v, min, max)
            local pos = (value - min) / (max - min)
            ValLabel.Text = tostring(value) .. suffix
            Fill.Size = UDim2.new(pos, 0, 1, 0)
            Knob.Position = UDim2.new(pos, -4, 0.5, -4)
            callback(value)
            updateKeybindsList()
        end

        local dragging = false
        local function UpdateSlider(input)
            local pos = math.clamp((input.Position.X - Track.AbsolutePosition.X) / Track.AbsoluteSize.X, 0, 1)
            SetValue(math.floor(min + ((max - min) * pos)))
        end

        Track.InputBegan:Connect(function(input)
            if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then
                dragging = true
                UpdateSlider(input)
            end
        end)
        UserInputService.InputEnded:Connect(function(input)
            if input.UserInputType == Enum.UserInputType.MouseButton1 or input.UserInputType == Enum.UserInputType.Touch then dragging = false end
        end)
        UserInputService.InputChanged:Connect(function(input)
            if dragging and (input.UserInputType == Enum.UserInputType.MouseMovement or input.UserInputType == Enum.UserInputType.Touch) then UpdateSlider(input) end
        end)

        ConfigSystem.UIElements[text] = SetValue
    end

    function Column:AddDropdown(opt)
        local text = opt.Name or "Dropdown"
        local options = opt.Options or {}
        local default = opt.Default or options[1]
        local callback = opt.Callback or function() end

        local DropFrame = Instance.new("Frame")
        DropFrame.Size = UDim2.new(1, 0, 0, 44)
        DropFrame.BackgroundTransparency = 1
        DropFrame.ClipsDescendants = false
        DropFrame.ZIndex = 10
        DropFrame.Parent = ItemList

        local Label = Instance.new("TextLabel")
        Label.Size = UDim2.new(1, -4, 0, 16)
        Label.Position = UDim2.new(0, 4, 0, 0)
        Label.BackgroundTransparency = 1
        Label.Text = text
        Label.TextColor3 = Color3.fromRGB(180, 180, 190)
        Label.Font = Enum.Font.Gotham
        Label.TextSize = 10
        Label.TextXAlignment = Enum.TextXAlignment.Left
        Label.Parent = DropFrame

        local DropBtn = Instance.new("TextButton")
        DropBtn.Size = UDim2.new(1, -8, 0, 22)
        DropBtn.Position = UDim2.new(0, 4, 0, 18)
        DropBtn.BackgroundColor3 = Color3.fromRGB(28, 28, 34)
        DropBtn.BorderSizePixel = 0
        DropBtn.Text = " " .. tostring(default) .. "  ▼"
        DropBtn.TextColor3 = Color3.fromRGB(220, 220, 230)
        DropBtn.Font = Enum.Font.Gotham
        DropBtn.TextSize = 10
        DropBtn.TextXAlignment = Enum.TextXAlignment.Left
        DropBtn.AutoButtonColor = true
        DropBtn.ZIndex = 11
        DropBtn.Parent = DropFrame

        Instance.new("UICorner", DropBtn).CornerRadius = UDim.new(0, 4)

        local maxH = math.min(math.max(#options, 1) * 26, 220)
        -- Overlay on ScreenGui so nothing clips the list
        local OptionList = Instance.new("ScrollingFrame")
        OptionList.Name = "DropdownOverlay"
        OptionList.Size = UDim2.new(0, 180, 0, maxH)
        OptionList.BackgroundColor3 = Color3.fromRGB(22, 22, 28)
        OptionList.BorderSizePixel = 0
        OptionList.Visible = false
        OptionList.ZIndex = 500
        OptionList.ScrollBarThickness = 5
        OptionList.ScrollingDirection = Enum.ScrollingDirection.Y
        OptionList.CanvasSize = UDim2.new(0, 0, 0, #options * 26)
        OptionList.ClipsDescendants = true
        OptionList.Active = true
        OptionList.Parent = ScreenGui

        Instance.new("UICorner", OptionList).CornerRadius = UDim.new(0, 4)
        local ListLayout = Instance.new("UIListLayout")
        ListLayout.SortOrder = Enum.SortOrder.LayoutOrder
        ListLayout.Parent = OptionList

        local isOpen = false
        local function placeOverlay()
            local abs = DropBtn.AbsolutePosition
            local sz = DropBtn.AbsoluteSize
            OptionList.Position = UDim2.new(0, abs.X, 0, abs.Y + sz.Y + 2)
            OptionList.Size = UDim2.new(0, math.max(sz.X, 160), 0, maxH)
        end

        local function closeDropdown()
            isOpen = false
            OptionList.Visible = false
        end

        local function openDropdown()
            isOpen = true
            placeOverlay()
            OptionList.Visible = true
        end

        local function toggleDropdown()
            if isOpen then closeDropdown() else openDropdown() end
        end

        for _, item in ipairs(options) do
            local ItemBtn = Instance.new("TextButton")
            ItemBtn.Size = UDim2.new(1, 0, 0, 26)
            ItemBtn.BackgroundColor3 = Color3.fromRGB(28, 28, 34)
            ItemBtn.BorderSizePixel = 0
            ItemBtn.Text = "  " .. tostring(item)
            ItemBtn.TextColor3 = Color3.fromRGB(220, 220, 230)
            ItemBtn.Font = Enum.Font.Gotham
            ItemBtn.TextSize = 11
            ItemBtn.TextXAlignment = Enum.TextXAlignment.Left
            ItemBtn.AutoButtonColor = true
            ItemBtn.Active = true
            ItemBtn.ZIndex = 501
            ItemBtn.Parent = OptionList

            local function selectItem()
                DropBtn.Text = " " .. tostring(item) .. "  ▼"
                closeDropdown()
                pcall(callback, {item})
                pcall(updateKeybindsList)
            end
            ItemBtn.MouseButton1Click:Connect(selectItem)
            ItemBtn.Activated:Connect(selectItem)
        end

        DropBtn.MouseButton1Click:Connect(function()
            toggleDropdown()
        end)

        -- close when clicking elsewhere
        UserInputService.InputBegan:Connect(function(input, gp)
            if not isOpen then return end
            if input.UserInputType == Enum.UserInputType.MouseButton1
                or input.UserInputType == Enum.UserInputType.Touch then
                task.defer(function()
                    if not isOpen then return end
                    local pos = input.Position
                    local ap = OptionList.AbsolutePosition
                    local as = OptionList.AbsoluteSize
                    local bp = DropBtn.AbsolutePosition
                    local bs = DropBtn.AbsoluteSize
                    local inList = pos.X >= ap.X and pos.X <= ap.X + as.X and pos.Y >= ap.Y and pos.Y <= ap.Y + as.Y
                    local inBtn = pos.X >= bp.X and pos.X <= bp.X + bs.X and pos.Y >= bp.Y and pos.Y <= bp.Y + bs.Y
                    if not inList and not inBtn then
                        closeDropdown()
                    end
                end)
            end
        end)

        ConfigSystem.UIElements[text] = function(val)
            DropBtn.Text = " " .. tostring(val) .. "  ▼"
            callback({val})
            updateKeybindsList()
        end
    end

    return Column
end
local function isPlayerPart(part)
    for _, player in pairs(Players:GetPlayers()) do
        if player.Character and part:IsDescendantOf(player.Character) then
            return true
        end
    end
    return false
end

local function applyGlassReflection()
    for _, part in pairs(workspace:GetDescendants()) do
        if part:IsA("BasePart") and not isPlayerPart(part) then
            if not envOriginalMaterials[part] then
                envOriginalMaterials[part] = {
                    Material = part.Material,
                    Reflectance = part.Reflectance,
                    Transparency = part.Transparency
                }
            end
            part.Material = Enum.Material.Glass
            part.Reflectance = 0.5
            if part.Transparency < 0.1 then
                part.Transparency = 0.25
            end
        end
    end
end

local function restoreMaterials()
    for part, data in pairs(envOriginalMaterials) do
        if part and part.Parent then
            part.Material = data.Material
            part.Reflectance = data.Reflectance
            part.Transparency = data.Transparency
        end
    end
    envOriginalMaterials = {}
end
local SkyPresets = {
    ["Dark Sky"] = {
        SkyboxUp = "rbxassetid://570555929",
        SkyboxRt = "rbxassetid://570555882",
        SkyboxDn = "rbxassetid://570555964",
        SkyboxFt = "rbxassetid://570555800",
        SkyboxLf = "rbxassetid://570555840",
        SkyboxBk = "rbxassetid://570555736",
    },
    ["Vaporwave"] = {
        SkyboxUp = "rbxassetid://1417494643",
        SkyboxRt = "rbxassetid://1417494499",
        SkyboxLf = "rbxassetid://1417494402",
        SkyboxFt = "rbxassetid://1417494253",
        SkyboxBk = "rbxassetid://1417494030",
        SkyboxDn = "rbxassetid://1417494146",
    },
    ["Lake Sky"] = {
        SkyboxRt = "rbxassetid://6823531746",
        SkyboxUp = "rbxassetid://6823528533",
        SunTextureId = "rbxassetid://5392574622",
        SkyboxDn = "rbxassetid://6823525702",
        SkyboxFt = "rbxassetid://6823482923",
        SkyboxLf = "rbxassetid://6823530023",
        SkyboxBk = "rbxassetid://6823523318",
    },
    ["Black Mesa"] = {
        SkyboxUp = "rbxassetid://9569598752",
        SkyboxRt = "rbxassetid://9569601267",
        SkyboxDn = "rbxassetid://9569613307",
        SkyboxFt = "rbxassetid://9569611418",
        SkyboxLf = "rbxassetid://9569608166",
        SkyboxBk = "rbxassetid://9569742122",
    },
}
envConfig.skyPreset = envConfig.skyPreset or "Dark Sky"

local function applySkyPreset(name)
    name = tostring(name or "Dark Sky")
    local preset = SkyPresets[name] or SkyPresets["Dark Sky"]
    envConfig.skyPreset = name
    local LightingSvc = game:GetService("Lighting")
    local sky = LightingSvc:FindFirstChild("CustomSkybox")
    if not sky then
        sky = Instance.new("Sky")
        sky.Name = "CustomSkybox"
        sky.Parent = LightingSvc
    end
    pcall(function()
        sky.SkyboxUp = ""
        sky.SkyboxRt = ""
        sky.SkyboxDn = ""
        sky.SkyboxFt = ""
        sky.SkyboxLf = ""
        sky.SkyboxBk = ""
        sky.SunTextureId = ""
    end)
    for prop, val in pairs(preset) do
        pcall(function() sky[prop] = val end)
    end
    pcall(function()
        for _, c in ipairs(LightingSvc:GetChildren()) do
            if c:IsA("Sky") and c ~= sky then
                c:Destroy()
            end
        end
    end)
    currentSkybox = sky
    envConfig.skyboxEnabled = true
end

local function toggleSkybox()
    local LightingSvc = game:GetService("Lighting")
    if envConfig.skyboxEnabled then
        applySkyPreset(envConfig.skyPreset or "Dark Sky")
        createNotification("Skybox ON: " .. tostring(envConfig.skyPreset or "Dark Sky"))
    else
        pcall(function()
            local sky = LightingSvc:FindFirstChild("CustomSkybox")
            if sky then sky:Destroy() end
            for _, c in ipairs(LightingSvc:GetChildren()) do
                if c:IsA("Sky") then c:Destroy() end
            end
        end)
        currentSkybox = nil
        createNotification("Skybox OFF")
    end
    updateKeybindsList()
end

local function toggleWater()
    if WaterTerrain then
        if envConfig.waterEnabled then
            originalWaterProps = {
                WaveSize = WaterTerrain.WaterWaveSize,
                WaveSpeed = WaterTerrain.WaterWaveSpeed,
                Transparency = WaterTerrain.WaterTransparency,
                Color = WaterTerrain.WaterColor
            }
            WaterTerrain.WaterWaveSize = 0.15
            WaterTerrain.WaterWaveSpeed = 12
            WaterTerrain.WaterTransparency = 0.8
            WaterTerrain.WaterColor = Color3.fromRGB(60, 150, 200)
        else
            if originalWaterProps.WaveSize then
                WaterTerrain.WaterWaveSize = originalWaterProps.WaveSize
                WaterTerrain.WaterWaveSpeed = originalWaterProps.WaveSpeed
                WaterTerrain.WaterTransparency = originalWaterProps.Transparency
                WaterTerrain.WaterColor = originalWaterProps.Color
            end
        end
    end
    updateKeybindsList()
end
local modernShaderBlur = Instance.new("BlurEffect")
modernShaderBlur.Size = 6
modernShaderBlur.Name = "ModernShaderBlur"

local modernShaderCC = Instance.new("ColorCorrectionEffect")
modernShaderCC.Saturation = -0.4
modernShaderCC.Name = "ModernShaderCC"

local modernSnowPart = Instance.new("Part")
modernSnowPart.Size = Vector3.new(200, 1, 200)
modernSnowPart.Transparency = 1
modernSnowPart.Anchored = true
modernSnowPart.CanCollide = false
modernSnowPart.CanQuery = false
modernSnowPart.Name = "ModernShaderSnow"

local modernSnowParticle = Instance.new("ParticleEmitter")
modernSnowParticle.EmissionDirection = Enum.NormalId.Bottom
modernSnowParticle.Rate = 20000
modernSnowParticle.Lifetime = NumberRange.new(3.5, 3.5)
modernSnowParticle.Speed = NumberRange.new(50, 50)
modernSnowParticle.Texture = "rbxassetid://92367298778210"
modernSnowParticle.Size = NumberSequence.new({
    NumberSequenceKeypoint.new(0, 0.3),
    NumberSequenceKeypoint.new(1, 0.4)
})
modernSnowParticle.SpreadAngle = Vector2.new(70, 70)
modernSnowParticle.Parent = modernSnowPart
pcall(function()
    modernSnowParticle:Clone().Parent = modernSnowPart
    modernSnowParticle:Clone().Parent = modernSnowPart
end)

local modernShaderCache = {}
local modernSnowConn = nil
local modernShaderHour = 12

local function DisableModernShader()
    if type(modernShaderCache) == "table" and #modernShaderCache > 0 then
        pcall(function()
            Lighting.Ambient = modernShaderCache[1]
            Lighting.Brightness = modernShaderCache[2]
            Lighting.ColorShift_Bottom = modernShaderCache[3]
            Lighting.ColorShift_Top = modernShaderCache[4]
            Lighting.EnvironmentDiffuseScale = modernShaderCache[5]
            Lighting.EnvironmentSpecularScale = modernShaderCache[6]
            Lighting.GlobalShadows = modernShaderCache[7]
            Lighting.OutdoorAmbient = modernShaderCache[8]
            Lighting.ShadowSoftness = modernShaderCache[9]
            Lighting.TimeOfDay = modernShaderCache[10]
        end)
    end
    modernShaderBlur.Parent = nil
    modernShaderCC.Parent = nil
    modernSnowPart.Parent = nil
    if modernSnowConn then
        pcall(function() modernSnowConn:Disconnect() end)
        modernSnowConn = nil
    end
end

local function EnableModernShader()
    modernShaderCache = {
        Lighting.Ambient,
        Lighting.Brightness,
        Lighting.ColorShift_Bottom,
        Lighting.ColorShift_Top,
        Lighting.EnvironmentDiffuseScale,
        Lighting.EnvironmentSpecularScale,
        Lighting.GlobalShadows,
        Lighting.OutdoorAmbient,
        Lighting.ShadowSoftness,
        Lighting.TimeOfDay
    }
    Lighting.Ambient = Color3.fromRGB(94, 99, 188)
    Lighting.Brightness = 4
    Lighting.ColorShift_Bottom = Color3.fromRGB(0, 0, 0)
    Lighting.ColorShift_Top = Color3.fromRGB(0, 0, 0)
    Lighting.EnvironmentDiffuseScale = 1
    Lighting.EnvironmentSpecularScale = 1
    Lighting.GlobalShadows = true
    Lighting.OutdoorAmbient = Color3.fromRGB(0, 0, 0)
    Lighting.ShadowSoftness = 3
    local h = math.clamp(math.floor(tonumber(modernShaderHour) or 12), 0, 24)
    Lighting.TimeOfDay = string.format("%02d:30:00", h % 24)

    modernShaderBlur.Parent = Lighting
    modernShaderCC.Parent = Lighting
    modernSnowPart.Parent = workspace

    if modernSnowConn then pcall(function() modernSnowConn:Disconnect() end) end
    modernSnowConn = RunService.RenderStepped:Connect(function()
        local char = LocalPlayer.Character
        if char and char:FindFirstChild("HumanoidRootPart") then
            modernSnowPart.Position = char.HumanoidRootPart.Position + Vector3.new(0, 90, 0)
        end
    end)
end

local function updateLightingSettings()
    if envConfig.shaderEnabled then
        EnableModernShader()
    else
        DisableModernShader()
    end
    if envConfig.timeOfDay == "Night" then
        modernShaderHour = 0
    elseif envConfig.timeOfDay == "Day" and (modernShaderHour == 0 or modernShaderHour == 24) then
        modernShaderHour = 12
    end
    if envConfig.shaderEnabled then
        local h = math.clamp(math.floor(tonumber(modernShaderHour) or 12), 0, 24)
        Lighting.TimeOfDay = string.format("%02d:00:00", h % 24)
    end
    updateKeybindsList()
end

UserInputService.InputBegan:Connect(function(input, gameProcessed)
    if gameProcessed then return end
    
    if input.KeyCode == Enum.KeyCode.KeypadOne then
        envConfig.shaderEnabled = not envConfig.shaderEnabled
        updateLightingSettings()
    elseif input.KeyCode == Enum.KeyCode.KeypadTwo then
        envConfig.skyboxEnabled = not envConfig.skyboxEnabled
        toggleSkybox()
    elseif input.KeyCode == Enum.KeyCode.KeypadThree then
        envConfig.waterEnabled = not envConfig.waterEnabled
        toggleWater()
    elseif input.KeyCode == Enum.KeyCode.KeypadFour then
        envConfig.timeOfDay = (envConfig.timeOfDay == "Day") and "Night" or "Day"
        updateLightingSettings()
    end
end)

RunService.Heartbeat:Connect(function()
    if envConfig.weatherType == "None" then
        if WeatherFolder and #WeatherFolder:GetChildren() > 0 then
            WeatherFolder:ClearAllChildren()
        end
        return
    end

    local isRain = (envConfig.weatherType == "Rain")
    local isStorm = envConfig.stormEnabled
    local spawnRate = isRain and (isStorm and 15 or 4) or (isStorm and 14 or 7)

    for _ = 1, spawnRate do
        local part = Instance.new("Part")
        part.Anchored = false
        part.CanCollide = false
        part.CanQuery = false
        
        local fallVelocity = Vector3.zero

        if isRain then
            part.Shape = Enum.PartType.Block
            part.Material = Enum.Material.ForceField
            part.Color = Color3.fromRGB(200, 230, 255)
            
            local length = isStorm and 6.0 or 3.0
            part.Size = Vector3.new(0.12, length, 0.12)
            part.Transparency = 0.2

            local speedY = isStorm and -250 or -120
            local slightWindX = math.random(-5, 5)
            local slightWindZ = math.random(-5, 5)
            fallVelocity = Vector3.new(slightWindX, speedY, slightWindZ)
        else
            part.Size = Vector3.new(0.05, 0.05, 0.05)
            part.Transparency = 1
            part.Material = Enum.Material.SmoothPlastic
            part.CanTouch = false
            part.Massless = true
            part.CastShadow = false

            local px = isStorm and math.random(5, 11) or math.random(3, 8)
            local bill = Instance.new("BillboardGui")
            bill.Name = "Snow2D"
            bill.Size = UDim2.fromOffset(px, px)
            bill.AlwaysOnTop = false
            bill.LightInfluence = 0
            bill.MaxDistance = 280
            bill.Parent = part

            local flake = Instance.new("Frame")
            flake.Size = UDim2.fromScale(1, 1)
            flake.BackgroundColor3 = Color3.fromRGB(255, 255, 255)
            flake.BackgroundTransparency = isStorm and 0.05 or 0.18
            flake.BorderSizePixel = 0
            flake.Parent = bill
            local c = Instance.new("UICorner")
            c.CornerRadius = UDim.new(1, 0)
            c.Parent = flake

            if isStorm then
                fallVelocity = Vector3.new(math.random(-70, -20), math.random(-35, -18), math.random(-70, -20))
            else
                fallVelocity = Vector3.new(math.random(-12, 12), math.random(-22, -10), math.random(-12, 12))
            end
        end

        local spawnHeight = isRain and 90 or 55
        local spread = isRain and 120 or 95
        local spawnPos = Camera.CFrame.Position + Vector3.new(math.random(-spread, spread), spawnHeight, math.random(-spread, spread))
        part.CFrame = CFrame.new(spawnPos)
        part.Parent = WeatherFolder

        local bv = Instance.new("BodyVelocity")
        bv.MaxForce = Vector3.new(1e5, 1e5, 1e5)
        bv.Velocity = fallVelocity
        bv.Parent = part

        Debris:AddItem(part, isRain and 2 or 3.5)
    end
end)
local OrbitCFG = {
    Studs = 5003,
    Speed = 5,
    MaxDistance = math.huge,
    Active = false,
}

local OrbitParts = {}
setmetatable(OrbitParts, {
    __index = function(_, key)
        local char = LocalPlayer.Character
        if not char then return nil end
        if key == "root" then return char:FindFirstChild("HumanoidRootPart") end
        if key == "head" then return char:FindFirstChild("Head") end
        return nil
    end
})

local OrbitBot = {
    Target = nil,
    Desync = false,
    Conn1 = nil,
    Conn2 = nil,
    Conn3 = nil,
    Angle = 0,
    CurrentTarget = nil,
}
getgenv().OrbitBot = OrbitBot

function OrbitBot:StopDesync()
    self.Desync = false
    self.CurrentTarget = nil
    self.SafeCF = nil
    if self.Conn2 then
        pcall(function() self.Conn2:Disconnect() end)
        self.Conn2 = nil
    end
    pcall(function() RunService:UnbindFromRenderStep("OrbitRestore") end)
end

function OrbitBot:isTargetAlive(target)
    if not target then return false end
    local char = target.Character
    if not char then return false end
    local hum = char:FindFirstChildOfClass("Humanoid")
    local root = char:FindFirstChild("HumanoidRootPart")
    return hum and root and hum.Health > 0
end

function OrbitBot:restoreSafePosition()
    local myRoot = OrbitParts.root
    if not myRoot or not self.SafeCF then return end
    pcall(function() RunService:UnbindFromRenderStep("OrbitRestore") end)
    pcall(function()
        myRoot.CFrame = self.SafeCF
        -- do not zero velocity hard — walkspeed keeps working
    end)
end

function OrbitBot:FindTarget()
    local myChar = LocalPlayer.Character
    if not myChar then return nil end
    local myRoot = myChar:FindFirstChild("HumanoidRootPart")
    if not myRoot then return nil end
    local closest, closestDist = nil, math.huge
    for _, player in pairs(Players:GetPlayers()) do
        if player == LocalPlayer then continue end
        local sameTeam = false
        pcall(function()
            local a = LocalPlayer:GetAttribute("TeamID")
            local b = player:GetAttribute("TeamID")
            if a ~= nil and b ~= nil and a == b then sameTeam = true end
        end)
        if sameTeam then continue end
        local char = player.Character
        if not char then continue end
        local root = char:FindFirstChild("HumanoidRootPart")
        local head = char:FindFirstChild("Head")
        local hum = char:FindFirstChildWhichIsA("Humanoid")
        if not (root and head and hum and hum.Health > 0) then continue end
        local dist = (myRoot.Position - root.Position).Magnitude
        if dist > (OrbitCFG.MaxDistance or math.huge) then continue end
        if dist < closestDist then
            closestDist = dist
            closest = player
        end
    end
    return closest
end

function OrbitBot:Setup()
    if self.Conn1 then pcall(function() self.Conn1:Disconnect() end) end
    if self.Conn2 then pcall(function() self.Conn2:Disconnect() end) end
    if self.Conn3 then pcall(function() self.Conn3:Disconnect() end) end
    self.Conn2 = nil
    self.SafeCF = nil
    self.Desync = false
    self.LastTarget = nil

    self.Conn1 = RunService.Heartbeat:Connect(function()
        if not OrbitCFG.Active then return end
        self.Target = self:FindTarget()
    end)

    self.Conn3 = RunService.Heartbeat:Connect(function(dt)
        if not OrbitCFG.Active then
            self.SafeCF = nil
            self.LastTarget = nil
            return
        end
        local myRoot = OrbitParts.root
        if not myRoot then return end

        local target = self.Target
        if not self:isTargetAlive(target) then
            if self.LastTarget or self.CurrentTarget then
                self:restoreSafePosition()
            end
            self.CurrentTarget = nil
            self.LastTarget = nil
            return
        end

        if getgenv().IsTargetNearTripmine and getgenv().IsTargetNearTripmine(target) then
            self:restoreSafePosition()
            return
        end

        local targetRoot = target.Character:FindFirstChild("HumanoidRootPart")
        if not targetRoot then
            self:restoreSafePosition()
            return
        end

        self.LastTarget = target
        self.CurrentTarget = target

        local spd = tonumber(OrbitCFG.Speed) or 5
        local studs = tonumber(OrbitCFG.Studs) or 5003
        self.Angle = (self.Angle or 0) + (dt * spd)
        local desiredCFrame = targetRoot.CFrame + Vector3.new(math.cos(self.Angle) * studs, 0, math.sin(self.Angle) * studs)

        -- Orbit always runs with desync from the moment it is enabled
        orbitDesyncEnabled = true
        self.Desync = true

        local origCF = myRoot.CFrame
        local origLV = myRoot.AssemblyLinearVelocity
        local origAV = myRoot.AssemblyAngularVelocity
        local py = origCF.Position.Y
        if py > -50 and py < 2500 then
            self.SafeCF = origCF
        end

        -- RB1-style: orbit TP then same-frame restore (can walk, no freeze lock)
        myRoot.CFrame = desiredCFrame
        RunService:BindToRenderStep("OrbitRestore", Enum.RenderPriority.Camera.Value - 1, function()
            if myRoot and myRoot.Parent then
                myRoot.CFrame = origCF
                pcall(function()
                    myRoot.AssemblyLinearVelocity = origLV
                    myRoot.AssemblyAngularVelocity = origAV
                end)
                pcall(function()
                    local hum = LocalPlayer.Character and LocalPlayer.Character:FindFirstChildOfClass("Humanoid")
                    if hum and WALK_SPEED then hum.WalkSpeed = WALK_SPEED end
                end)
            end
            pcall(function() RunService:UnbindFromRenderStep("OrbitRestore") end)
        end)
    end)
end

function OrbitBot:Init()
    self:Setup()
end

pcall(function() OrbitBot:Init() end)
function clearOrbitLights() end
function getNearestEnemyPlayerForOrbit()
    return OrbitBot:FindTarget()
end
function ensureOrbitLights() end
function stopOrbitDesync()
    orbitDesyncEnabled = false
    pcall(function() OrbitBot:StopDesync() end)
end
function startOrbitDesync()
    orbitDesyncEnabled = true
end
function stopOrbitLight()
    orbitLightEnabled = false
    OrbitCFG.Active = false
    pcall(function()
        if OrbitBot then
            OrbitBot:restoreSafePosition()
            OrbitBot:StopDesync()
        end
    end)
end
function startOrbitLight()
    orbitLightEnabled = true
    orbitDesyncEnabled = true
    OrbitCFG.Active = true
    OrbitCFG.Studs = tonumber(orbitLightRadius) or OrbitCFG.Studs or 5003
    OrbitCFG.Speed = tonumber(orbitLightSpeed) or OrbitCFG.Speed or 5
    pcall(function()
        if OrbitBot then
            OrbitBot.SafeCF = nil
            OrbitBot.Desync = true
            OrbitBot.Angle = 0
            OrbitBot:Setup()
        end
    end)
end
orbitLightRadius = orbitLightRadius or 5003
orbitLightSpeed = orbitLightSpeed or 5
local silentAimOldStartShooting = nil
local silentAimHooked = false
local silentAimFOV = 400
function saIsEnemy(plr)
    if not plr or plr == LocalPlayer then return false end
    local a = LocalPlayer:GetAttribute("TeamID")
    local b = plr:GetAttribute("TeamID")
    if a ~= nil and b ~= nil and a == b then
        return false
    end
    local ok, same = pcall(function()
        return LocalPlayer.Team ~= nil and plr.Team ~= nil and LocalPlayer.Team == plr.Team
    end)
    if ok and same then return false end
    return true
end
function isEnemy(plr)
    return saIsEnemy(plr)
end
function isTargetImmune(playerOrChar)
    if not SHIELD_CHECK_ENABLED then return false end
    local char = playerOrChar
    if typeof(playerOrChar) == "Instance" and playerOrChar:IsA("Player") then
        char = playerOrChar.Character
    end
    if not char then return true end
    if char:FindFirstChildOfClass("ForceField") then return true end
    local hrp = char:FindFirstChild("HumanoidRootPart")
    if hrp and hrp:FindFirstChild("Attachment") then return true end
    local a = char:GetAttribute("Immune") or char:GetAttribute("Invincible") or char:GetAttribute("IsImmune")
        or char:GetAttribute("Shielded") or char:GetAttribute("HasShield")
    if a == true or a == 1 or a == "true" then return true end
    local hum = char:FindFirstChildOfClass("Humanoid")
    if hum then
        local ha = hum:GetAttribute("Immune") or hum:GetAttribute("Invincible") or hum:GetAttribute("IsImmune")
        if ha == true or ha == 1 then return true end
    end
    for _, key in ipairs({"Reflecting", "IsReflecting", "BulletReflect", "Reflect", "Deflecting", "Parrying"}) do
        local v = char:GetAttribute(key)
        if v == true or v == 1 or v == "true" then return true end
        if hum then
            local hv = hum:GetAttribute(key)
            if hv == true or hv == 1 then return true end
        end
    end
    return false
end
getgenv().IsTargetImmune = isTargetImmune
getgenv().IsImmuneTarget = isTargetImmune
function isLocalReloading()
    local block = false
    pcall(function()
        local fc
        pcall(function()
            fc = require(LocalPlayer.PlayerScripts.Controllers.FighterController)
        end)
        local lf = fc and fc.LocalFighter
        local item = lf and lf.EquippedItem
        if not item then
            block = true
            return
        end

        local now = tick()
        local cooldown = rawget(item, "_reload_cooldown")
        if type(cooldown) == "number" and now < cooldown then
            block = true
            return
        end
        local noAmmoCooldown = rawget(item, "_shoot_cooldown_no_ammo")
        if type(noAmmoCooldown) == "number" and now < noAmmoCooldown then
            block = true
            return
        end
        local isRel = rawget(item, "Reloading") or rawget(item, "IsReloading")
        if isRel == true then
            block = true
            return
        end
        local info = rawget(item, "Info")
        if type(info) == "table" then
            if info.Reloading == true or info.IsReloading == true then
                block = true
                return
            end
        end
        local ammo = nil
        local data = rawget(item, "Data")
        if type(data) == "table" then
            ammo = rawget(data, "Ammo") or rawget(data, "CurrentAmmo") or rawget(data, "MagazineAmmo")
        end
        if type(ammo) ~= "number" then
            pcall(function()
                if type(item.Get) == "function" then
                    ammo = item:Get("Ammo") or item:Get("CurrentAmmo") or item:Get("MagazineAmmo")
                end
            end)
        end
        if type(ammo) ~= "number" and type(info) == "table" then
            ammo = info.Ammo or info.CurrentAmmo
        end
        if type(ammo) ~= "number" then
            ammo = rawget(item, "Ammo") or rawget(item, "CurrentAmmo")
        end
        local itemTypeName = nil
        pcall(function()
            if type(item.Get) == "function" then
                itemTypeName = item:Get("Type") or item:Get("ItemType") or item:Get("Category")
            end
            itemTypeName = itemTypeName or rawget(item, "Type") or rawget(item, "ItemType")
            if type(info) == "table" then
                itemTypeName = itemTypeName or info.Type or info.ItemType or info.Category
            end
            if type(data) == "table" then
                itemTypeName = itemTypeName or data.Type or data.ItemType
            end
        end)
        local nameStr = tostring(itemTypeName or item.Name or ""):lower()
        local isGun = (nameStr == "gun" or nameStr:find("gun") or nameStr:find("rifle")
            or nameStr:find("pistol") or nameStr:find("shotgun") or nameStr:find("smg")
            or nameStr:find("sniper") or nameStr:find("primary") or nameStr:find("secondary"))
        if type(ammo) == "number" then
            if ammo <= 0 then
                block = true
                return
            end
        elseif isGun then
        end
    end)
    return block
end
getgenv().IsLocalReloading = isLocalReloading

-- practice / shooting range: IsInShootingRange == true -> ragebot OFF
local LocalFightState = {
    IsInShootingRange = false,
    IsInDuel = false,
    Seeded = false,
    LastPoll = 0,
}

local function refreshLocalFightState()
    local now = tick()
    if now - (LocalFightState.LastPoll or 0) < 0.12 then
        return LocalFightState
    end
    LocalFightState.LastPoll = now
    pcall(function()
        local fc = require(LocalPlayer.PlayerScripts.Controllers.FighterController)
        local lf = fc and fc.LocalFighter
        if not lf then return end
        local inRange, inDuel = false, false
        if type(lf.Get) == "function" then
            pcall(function()
                inRange = lf:Get("IsInShootingRange") == true
                inDuel = lf:Get("IsInDuel") == true
            end)
        end
        local data = rawget(lf, "Data")
        if type(data) == "table" then
            if rawget(data, "IsInShootingRange") == true then inRange = true end
            if rawget(data, "IsInDuel") == true then inDuel = true end
        end
        local entity = rawget(lf, "Entity")
        if type(entity) == "table" and type(rawget(entity, "Data")) == "table" then
            if rawget(entity.Data, "IsInShootingRange") == true then inRange = true end
            if rawget(entity.Data, "IsInDuel") == true then inDuel = true end
        end
        LocalFightState.IsInShootingRange = inRange == true
        LocalFightState.IsInDuel = inDuel == true
        LocalFightState.Seeded = true
    end)
    return LocalFightState
end

function isLocalInShootingRange()
    refreshLocalFightState()
    return LocalFightState.IsInShootingRange == true
end

getgenv().IsLocalInShootingRange = isLocalInShootingRange
getgenv().LocalFightState = LocalFightState

function shouldBlockRageActions()
    if isLocalReloading() then return true end
    -- 사격장/연습장에서는 레이지봇 작동 안 함
    if isLocalInShootingRange() then return true end
    return false
end
getgenv().ShouldBlockRageActions = shouldBlockRageActions
local function resolve_animation_asset(asset_id)
    local ok, objs = pcall(function()
        if game.GetObjects then return game:GetObjects(asset_id) end
        return nil
    end)
    if ok and objs and #objs > 0 then
        for i = 1, #objs do
            if objs[i]:IsA("Animation") then
                return objs[i].AnimationId
            end
        end
    end
    return asset_id
end

task.spawn(function()
    local id = "rbxassetid://92281817840531"
    id = resolve_animation_asset(id)
    emoteAnimAsset = Instance.new("Animation")
    emoteAnimAsset.AnimationId = id
end)

function play_emote(char)
    if not emoteHopEnabled then return false end
    char = char or LocalPlayer.Character
    if not char or not emoteAnimAsset then return false end
    local hum = char:FindFirstChildWhichIsA("Humanoid")
    if not hum then return false end
    pcall(function()
        if emoteTrack then emoteTrack:Stop() emoteTrack = nil end
        if animTrack then animTrack:Stop() animTrack = nil end
    end)
    local animator = hum:FindFirstChildOfClass("Animator") or hum
    local ok, track = pcall(function() return animator:LoadAnimation(emoteAnimAsset) end)
    if ok and track then
        emoteTrack = track
        animTrack = track
        track.Priority = Enum.AnimationPriority.Action4
        track:Play()
        track:AdjustSpeed(tonumber(emoteSpeed) or 40)
        track.Stopped:Connect(function()
            if emoteHopEnabled and LocalPlayer.Character == char then
                play_emote(char)
            end
        end)
        return true
    end
    return false
end

function stop_emote()
    pcall(function()
        if emoteTrack then emoteTrack:Stop() emoteTrack = nil end
        if animTrack then animTrack:Stop() animTrack = nil end
    end)
end
function playAnimById(id)
    return play_emote(LocalPlayer.Character)
end
function stopAnimPlay()
    stop_emote()
end
LocalPlayer.CharacterAdded:Connect(function(char)
    task.wait(0.5)
    if emoteHopEnabled then
        play_emote(char)
    end
end)
local KATANA_BYPASS = {
    Slingshot = true, Bow = true, Exogun = true, Spray = true,
    Flamethrower = true, ["Grenade Launcher"] = true, RPG = true,
    Crossbow = true, Daggers = true,
}

function isLocalWeaponKatanaBypass()
    local ok, name = pcall(function()
        local char = LocalPlayer.Character
        local tool = char and char:FindFirstChildOfClass("Tool")
        return tool and tool.Name
    end)
    if ok and name and KATANA_BYPASS[name] then return true end
    return false
end

function isItemKatanaDeflecting(item)
    if not item then return false end
    local ok, name = pcall(function() return item.Name end)
    if not ok or name ~= "Katana" then return false end
    local now = tick()
    local attackCooldown = rawget(item, "_attack_cooldown")
    local deflectCooldown = rawget(item, "_deflect_cooldown")
    local deflectHash = rawget(item, "_deflect_hash")
    return type(attackCooldown) == "number" and attackCooldown > now
        and type(deflectCooldown) == "number" and deflectCooldown > now
        and type(deflectHash) == "number" and deflectHash % 2 == 1
end

function shouldIgnoreKatanaTarget(player)
    if not player then return false end
    if isLocalWeaponKatanaBypass() then return false end
    local fn = getgenv().InstanceIsKatanaDeflecting
    if type(fn) == "function" then
        local ok, r = pcall(fn, player)
        if ok and r then return true end
    end
    local char = player.Character
    if char then
        local tool = char:FindFirstChild("Katana") or char:FindFirstChildOfClass("Tool")
        if tool and isItemKatanaDeflecting(tool) then return true end
        pcall(function()
            local cf = player:FindFirstChild("ClientFighter")
        end)
    end
    return false
end
getgenv().ShouldIgnoreKatanaTarget = shouldIgnoreKatanaTarget

function getAimTargetPart(character)
    if not character then return nil end
    -- always prefer head hitboxes for max damage / sniper hitreg
    local head = character:FindFirstChild("HitboxHead")
        or character:FindFirstChild("HitboxHeadSmall")
        or character:FindFirstChild("Head")
    local mode = tostring(AIM_TARGET_MODE or "head"):lower()
    if mode == "body" or mode == "torso" then
        return character:FindFirstChild("UpperTorso")
            or character:FindFirstChild("Torso")
            or character:FindFirstChild("HitboxBody")
            or character:FindFirstChild("HumanoidRootPart")
            or head
    end
    -- head / default / random -> head only
    return head or character:FindFirstChild("HumanoidRootPart")
end

if not randomTimerThread then
    randomTimerThread = task.spawn(function()
        while true do
            currentRandomTarget = (math.random(1, 2) == 1) and "Head" or "HumanoidRootPart"
            task.wait(5)
        end
    end)
end

local function isVisibleTarget(targetPart)
    if not targetPart or not targetPart.Parent then return false end
    local myChar = LocalPlayer.Character
    local origin = Camera and Camera.CFrame.Position
    if not origin then return false end
    local targetPos = targetPart.Position
    local dir = targetPos - origin
    local dist = dir.Magnitude
    if dist < 0.5 then return true end
    if dist > 2000 then return false end
    local params = RaycastParams.new()
    params.FilterType = Enum.RaycastFilterType.Exclude
    local filter = {}
    if myChar then table.insert(filter, myChar) end
    params.FilterDescendantsInstances = filter
    params.IgnoreWater = true
    local result = Workspace:Raycast(origin, dir.Unit * (dist + 1), params)
    if not result then return true end
    local hit = result.Instance
    if not hit then return true end
    local model = targetPart:FindFirstAncestorOfClass("Model") or targetPart.Parent
    if model and hit:IsDescendantOf(model) then return true end
    return false
end

local function isAimableModel(model)
    if not model or not model:IsA("Model") then return false end
    if model == LocalPlayer.Character then return false end
    local hum = model:FindFirstChildOfClass("Humanoid")
    if not hum or hum.Health <= 0 then return false end
    local root = model:FindFirstChild("HumanoidRootPart") or model:FindFirstChild("Head")
    if not root then return false end
    return true
end

local function collectSilentAimCandidates()
    local list = {}
    for _, player in ipairs(Players:GetPlayers()) do
        if player ~= LocalPlayer and saIsEnemy(player) and player.Character then
            local skip = false
            pcall(function()
                local fn = getgenv().InstanceIsKatanaDeflecting or shouldIgnoreKatanaTarget
                if fn and fn(player) then skip = true end
            end)
            if not skip then
                local part = getAimTargetPart(player.Character)
                if part then
                    table.insert(list, { part = part, model = player.Character, player = player })
                end
            end
        end
    end
    local function scanContainer(container)
        if not container then return end
        for _, model in ipairs(container:GetChildren()) do
            if model:IsA("Model") then
                local n = model.Name
                if n == "Dummy" or n == "DPS Dummy" or n == "Target" or n:find("Dummy") or n:find("Target") then
                    if isAimableModel(model) and not Players:GetPlayerFromCharacter(model) then
                        local part = getAimTargetPart(model) or model:FindFirstChild("Head") or model:FindFirstChild("HumanoidRootPart")
                        if part then
                            table.insert(list, { part = part, model = model, player = nil })
                        end
                    end
                end
            end
        end
    end
    scanContainer(Workspace)
    pcall(function()
        local map = Workspace:FindFirstChild("Map")
        scanContainer(map)
        if map then
            for _, folder in ipairs(map:GetChildren()) do
                if folder:IsA("Folder") or folder:IsA("Model") then
                    scanContainer(folder)
                end
            end
        end
    end)
    return list
end

function getSilentAimTarget()
    if not SILENT_AIM_ENABLED and not AIMBOT_ENABLED and not LEGIT_AIMBOT_ENABLED then return nil, nil end
    local best = silentAimFOV or 400
    if AIMBOT_ENABLED and tonumber(AIMBOT_FOV) then
        best = math.max(best, tonumber(AIMBOT_FOV) or best)
    end
    if getAimFovRadiusPx then
        best = math.max(best, getAimFovRadiusPx() or best)
    end
    local screenCenter = Vector2.new(Camera.ViewportSize.X / 2, Camera.ViewportSize.Y / 2)
    local closestRef, closestPart = nil, nil
    for _, entry in ipairs(collectSilentAimCandidates()) do
        local model = entry.model or (entry.player and entry.player.Character)
        if not model then continue end
        local hum = model:FindFirstChildOfClass("Humanoid")
        if not hum or hum.Health <= 0 then continue end
        local part = getAimTargetPart(model) or entry.part
        if part and isVisibleTarget(part) then
            local screenPos, onScreen = Camera:WorldToViewportPoint(part.Position)
            if onScreen and screenPos.Z > 0 then
                local dist = (Vector2.new(screenPos.X, screenPos.Y) - screenCenter).Magnitude
                if dist < best then
                    best = dist
                    closestPart = part
                    closestRef = entry.player or entry.model
                end
            end
        end
    end
    return closestRef, closestPart
end

local silentAimOldStartShooting = silentAimOldStartShooting
local silentAimHooked = false
local silentAimFOV = silentAimFOV or 400

function setupSilentAimHook()
    if silentAimHooked then return end
    pcall(function()
        local GunModule = require(LocalPlayer.PlayerScripts.Modules.ItemTypes.Gun)
        if not GunModule or type(GunModule.StartShooting) ~= "function" then return end
        if silentAimOldStartShooting then
            pcall(function() GunModule.StartShooting = silentAimOldStartShooting end)
        end
        local original = GunModule.StartShooting
        silentAimOldStartShooting = original
        GunModule.StartShooting = function(self, ...)
            local didPrime, cam, origCF = false, nil, nil
            if SILENT_AIM_ENABLED then
                local ref, part = getSilentAimTarget()
        if ref and not aimbotTargetStillValid(ref) then
            ref, part = nil, nil
        end
                if ref then
                    local model = nil
                    if typeof(ref) == "Instance" then
                        if ref:IsA("Player") then
                            model = ref.Character
                        elseif ref:IsA("Model") then
                            model = ref
                        end
                    end
                    if model then
                        part = getAimTargetPart(model) or part
                    end
                end
                if part and part.Parent then
                    cam = Workspace.CurrentCamera
                    if cam then
                        origCF = cam.CFrame
                        cam.CFrame = CFrame.lookAt(cam.CFrame.Position, part.Position)
                        didPrime = true
                        pcall(function()
                            if triggerHitMarker then triggerHitMarker() end
                        end)
                    end
                end
            end
            local results = table.pack(pcall(original, self, ...))
            if didPrime and cam and origCF and Workspace.CurrentCamera == cam then
                cam.CFrame = origCF
            end
            if not results[1] then
                return nil
            end
            return table.unpack(results, 2, results.n)
        end
        getgenv().__mineminyee_silent_wrap = GunModule.StartShooting
        silentAimHooked = true
        print("[mineminyee] Silent Aim (Myhack/Kicia camera-snap) hooked")
    end)
end

task.spawn(function()
    for _ = 1, 25 do
        setupSilentAimHook()
        if silentAimHooked then break end
        task.wait(0.8)
    end
    while true do
        task.wait(2)
        pcall(function()
            if not SILENT_AIM_ENABLED then return end
            local GunModule = require(LocalPlayer.PlayerScripts.Modules.ItemTypes.Gun)
            if GunModule and getgenv().__mineminyee_silent_wrap ~= GunModule.StartShooting then
                silentAimHooked = false
                getgenv().__mineminyee_silent_wrap = nil
                setupSilentAimHook()
            end
        end)
    end
end)

-- Bullet Track (Myhack: GunModule._Tracers)
local bulletTrackHooked = false
function setupBulletTrack()
    if bulletTrackHooked then return end
    pcall(function()
        local GunModule = require(LocalPlayer.PlayerScripts.Modules.ItemTypes.Gun)
        if not GunModule then return end
        local oldTracers = GunModule._Tracers
        if type(oldTracers) ~= "function" then return end
        GunModule._Tracers = function(self, data, ...)
            local ok, res = pcall(oldTracers, self, data, ...)
            if not TRACER_ENABLED then
                if ok then return res end
                return
            end
            pcall(function()
                local rays = data and (data.RaycastResults or data.rays or {}) or {}
                if type(rays) ~= "table" or #rays == 0 then return end
                local muzzle = nil
                pcall(function()
                    if self.ViewModel and self.ViewModel.GetMuzzlePosition then
                        muzzle = self.ViewModel:GetMuzzlePosition()
                    end
                end)
                if not muzzle then muzzle = Camera.CFrame.Position end
                local col = TRACER_COLOR or Color3.fromRGB(255, 255, 255)
                local dur = tonumber(TRACER_DURATION) or 0.6
                for _, ray in ipairs(rays) do
                    local startPos = ray.StartPosition or muzzle
                    local endPos = ray.Position or ray.EndPosition
                    if not startPos or not endPos then continue end
                    local distance = (endPos - startPos).Magnitude
                    if distance < 0.5 then continue end
                    local part = Instance.new("Part")
                    part.Anchored = true
                    part.CanCollide = false
                    part.CanQuery = false
                    part.CanTouch = false
                    part.Transparency = 0.25
                    part.Color = col
                    part.Material = Enum.Material.Neon
                    part.Size = Vector3.new(0.04, 0.04, distance)
                    part.CFrame = CFrame.new(startPos, endPos) * CFrame.new(0, 0, -distance / 2)
                    part.Parent = workspace
                    task.delay(dur, function() pcall(function() part:Destroy() end) end)
                end
            end)
            if ok then return res end
        end
        bulletTrackHooked = true
        print("[mineminyee] Bullet Track hooked (_Tracers)")
    end)
end
task.spawn(function()
    for _ = 1, 20 do
        setupBulletTrack()
        if bulletTrackHooked then break end
        task.wait(1)
    end
end)

local aimbotConn = nil
local aimbotCameraController = nil
function resolveAimbotCameraController()
    if aimbotCameraController and type(aimbotCameraController.SetRotation) == "function" then
        return aimbotCameraController
    end
    pcall(function()
        local ctrls = LocalPlayer.PlayerScripts:FindFirstChild("Controllers")
        local mod = ctrls and ctrls:FindFirstChild("CameraController")
        if mod then
            aimbotCameraController = require(mod)
        end
    end)
    return aimbotCameraController
end
AIMBOT_KEY = AIMBOT_KEY or nil
AIMBOT_KEY_LISTENING = false
aimbotLockedRef = nil
aimbotKeyHeld = false

function aimbotTargetStillValid(ref)
    if not ref then return false end
    local model = nil
    if typeof(ref) == "Instance" and ref:IsA("Player") then
        model = ref.Character
        if not model then return false end
        local hum = model:FindFirstChildOfClass("Humanoid")
        if not hum or hum.Health <= 0 then return false end
        if shouldIgnoreKatanaTarget and shouldIgnoreKatanaTarget(ref) then return false end
    elseif typeof(ref) == "Instance" and ref:IsA("Model") then
        model = ref
        local hum = model:FindFirstChildOfClass("Humanoid")
        if not hum or hum.Health <= 0 then return false end
        if not model.Parent then return false end
    else
        return false
    end
    local part = getAimTargetPart(model) or model:FindFirstChild("Head") or model:FindFirstChild("HumanoidRootPart")
    if not part then return false end
    local cam = Workspace.CurrentCamera or Camera
    if cam and isVisibleTarget and not isVisibleTarget(part) then return false end
    if cam and saHasLOS and not saHasLOS(cam.CFrame.Position, part.Position, model) then return false end
    return true
end

function resolveAimbotPart(ref)
    if not ref then return nil end
    if typeof(ref) == "Instance" and ref:IsA("Player") then
        local char = ref.Character
        return char and getAimTargetPart(char) or nil
    end
    if typeof(ref) == "Instance" and ref:IsA("Model") then
        return getAimTargetPart(ref) or ref:FindFirstChild("Head") or ref:FindFirstChild("HumanoidRootPart")
    end
    return nil
end

function stopAimbot()
    AIMBOT_ENABLED = false
    aimbotKeyHeld = false
    aimbotLockedRef = nil
    if aimbotConn then pcall(function() aimbotConn:Disconnect() end) aimbotConn = nil end
end

function startAimbot()
    if aimbotConn then pcall(function() aimbotConn:Disconnect() end) aimbotConn = nil end
    AIMBOT_ENABLED = true
    aimbotConn = RunService.RenderStepped:Connect(function(deltaTime)
        if not AIMBOT_ENABLED then return end

        local ref, part
        if AIMBOT_KEY then
            local held = (isSharedAimKeyHeld and isSharedAimKeyHeld()) or aimbotKeyHeld
            if not held then
                aimbotLockedRef = nil
                return
            end
            if aimbotTargetStillValid(aimbotLockedRef) then
                ref = aimbotLockedRef
                part = resolveAimbotPart(ref)
            else
                ref, part = getSilentAimTarget()
                if ref then aimbotLockedRef = ref end
            end
        else
            ref, part = getSilentAimTarget()
        end

        if not part or not part.Parent then return end
        if typeof(ref) == "Instance" and ref:IsA("Player") and shouldIgnoreKatanaTarget(ref) then return end

        local cam = Workspace.CurrentCamera
        if not cam then return end
        local worldPosition = part.Position
        pcall(function()
            local model = (typeof(ref) == "Instance" and ref:IsA("Player") and ref.Character)
                or (typeof(ref) == "Instance" and ref:IsA("Model") and ref)
            if model and not saHasLOS(cam.CFrame.Position, worldPosition, model) then
                aimbotLockedRef = nil
                worldPosition = nil
            end
        end)
        if not worldPosition then return end

        local sm = tonumber(AIMBOT_SMOOTH) or 35
        if sm <= 1 then sm = sm * 100 end
        sm = math.clamp(sm, 1, 100)
        local hardSnap = sm >= 99.5

        local cameraController = resolveAimbotCameraController()
        if cameraController and type(cameraController.SetRotation) == "function" then
            local currentRotation = rawget(cameraController, "Rotation")
            if typeof(currentRotation) == "Vector2" then
                local pitch, yaw = CFrame.lookAt(cam.CFrame.Position, worldPosition):ToOrientation()
                if hardSnap then
                    pcall(function()
                        cameraController:SetRotation(Vector2.new(pitch, yaw))
                    end)
                else
                    local aimSpeed = 2 + (sm * 0.85)
                    local frameDelta = math.clamp(type(deltaTime) == "number" and deltaTime or (1 / 60), 0, 0.1)
                    local blendAlpha = math.clamp(1 - math.exp(-frameDelta * aimSpeed), 0, 1)
                    pcall(function()
                        cameraController:SetRotation(Vector2.new(
                            currentRotation.X + (pitch - currentRotation.X) * blendAlpha,
                            currentRotation.Y + ((yaw - currentRotation.Y + math.pi) % (2 * math.pi) - math.pi) * blendAlpha
                        ))
                    end)
                end
                return
            end
        end
        if hardSnap then
            cam.CFrame = CFrame.lookAt(cam.CFrame.Position, worldPosition)
        else
            local smooth = math.clamp(sm / 100, 0.05, 1)
            cam.CFrame = cam.CFrame:Lerp(CFrame.lookAt(cam.CFrame.Position, worldPosition), smooth)
        end
    end)
end
legitAimbotConn = nil
legitAimNoise = { t = 0 }
fovDrawConn = nil
fovCircle, fovFill = nil, nil
crossLines = nil

function parseColorInput(str, fallback)
    fallback = fallback or Color3.fromRGB(255, 255, 255)
    if type(str) ~= "string" then return fallback end
    str = str:gsub("%s+", "")
    local hex = str:match("^#?(%x%x%x%x%x%x)$")
    if hex then
        local r = tonumber(hex:sub(1, 2), 16)
        local g = tonumber(hex:sub(3, 4), 16)
        local b = tonumber(hex:sub(5, 6), 16)
        return Color3.fromRGB(r, g, b)
    end
    local r, g, b = str:match("^(%d+),(%d+),(%d+)$")
    if r then
        return Color3.fromRGB(
            math.clamp(tonumber(r) or 255, 0, 255),
            math.clamp(tonumber(g) or 255, 0, 255),
            math.clamp(tonumber(b) or 255, 0, 255)
        )
    end
    return fallback
end

function getAimFovRadiusPx()
    local cam = Workspace.CurrentCamera
    if not cam then return 200 end
    local vs = cam.ViewportSize
    local halfDiag = (Vector2.new(vs.X, vs.Y).Magnitude) * 0.5
    local pct = math.clamp(tonumber(AIM_FOV_SIZE) or tonumber(LEGIT_AIMBOT_FOV) or 40, 1, 100)
    AIM_FOV_SIZE = pct
    LEGIT_AIMBOT_FOV = pct
    if pct >= 99.5 then
        return halfDiag + 50
    end
    return math.max(8, halfDiag * (pct / 100))
end

function destroyFovDrawings()
    pcall(function() if fovCircle then fovCircle:Remove() end end)
    pcall(function() if fovFill then fovFill:Remove() end end)
    fovCircle, fovFill = nil, nil
    if crossLines then
        for _, l in ipairs(crossLines) do
            pcall(function() l:Remove() end)
        end
    end
    crossLines = nil
end

function ensureFovDrawings()
    if not (FOV_DRAW_ENABLED or CROSSHAIR_ENABLED) then
        destroyFovDrawings()
        return
    end
    if FOV_DRAW_ENABLED then
        if not fovCircle then
            local ok, c = pcall(function()
                local d = Drawing.new("Circle")
                d.Filled = false
                d.Thickness = 1.5
                d.NumSides = 64
                d.Visible = true
                return d
            end)
            if ok then fovCircle = c end
        end
        if FOV_DRAW_FILL and not fovFill then
            local ok, c = pcall(function()
                local d = Drawing.new("Circle")
                d.Filled = true
                d.NumSides = 64
                d.Visible = true
                return d
            end)
            if ok then fovFill = c end
        elseif not FOV_DRAW_FILL and fovFill then
            pcall(function() fovFill:Remove() end)
            fovFill = nil
        end
    else
        pcall(function() if fovCircle then fovCircle:Remove() end end)
        pcall(function() if fovFill then fovFill:Remove() end end)
        fovCircle, fovFill = nil, nil
    end
    if CROSSHAIR_ENABLED then
        if not crossLines then
            crossLines = {}
            for i = 1, 4 do
                local ok, l = pcall(function()
                    local d = Drawing.new("Line")
                    d.Thickness = tonumber(CROSSHAIR_THICKNESS) or 1.5
                    d.Visible = true
                    return d
                end)
                if ok then crossLines[i] = l end
            end
        end
    else
        if crossLines then
            for _, l in ipairs(crossLines) do pcall(function() l:Remove() end) end
            crossLines = nil
        end
    end
end

function updateFovVisuals(dt)
    local cam = Workspace.CurrentCamera
    if not cam then return end
    local vs = cam.ViewportSize
    local cx, cy = vs.X * 0.5, vs.Y * 0.5
    local radius = getAimFovRadiusPx()
    local col = FOV_DRAW_COLOR or Color3.fromRGB(0, 200, 255)

    ensureFovDrawings()

    if FOV_DRAW_ENABLED and fovCircle then
        fovCircle.Position = Vector2.new(cx, cy)
        fovCircle.Radius = radius
        fovCircle.Color = col
        fovCircle.Transparency = math.clamp(tonumber(FOV_DRAW_TRANSPARENCY) or 0.85, 0, 1)
        fovCircle.Visible = true
        if fovFill then
            fovFill.Position = Vector2.new(cx, cy)
            fovFill.Radius = radius
            fovFill.Color = col
            fovFill.Transparency = math.clamp(tonumber(FOV_DRAW_FILL_TRANSPARENCY) or 0.92, 0, 1)
            fovFill.Visible = FOV_DRAW_FILL and true or false
        end
    end

    if CROSSHAIR_ENABLED and crossLines then
        local size = math.clamp(tonumber(CROSSHAIR_SIZE) or 12, 2, 200)
        local gap = math.clamp(tonumber(CROSSHAIR_GAP) or 4, 0, 40)
        local thick = math.clamp(tonumber(CROSSHAIR_THICKNESS) or 1.5, 0.5, 6)
        local ccol = CROSSHAIR_COLOR or Color3.fromRGB(255, 255, 255)
        local ang = 0
        if CROSSHAIR_ROTATE then
            crosshairAngle = (crosshairAngle or 0) + (tonumber(CROSSHAIR_ROTATE_SPEED) or 90) * (dt or 0.016) * (math.pi / 180)
            ang = crosshairAngle
        end
        local dirs = {
            Vector2.new(math.cos(ang), math.sin(ang)),
            Vector2.new(math.cos(ang + math.pi / 2), math.sin(ang + math.pi / 2)),
            Vector2.new(math.cos(ang + math.pi), math.sin(ang + math.pi)),
            Vector2.new(math.cos(ang + 3 * math.pi / 2), math.sin(ang + 3 * math.pi / 2)),
        }
        local center = Vector2.new(cx, cy)
        for i = 1, 4 do
            local l = crossLines[i]
            if l then
                local d = dirs[i]
                l.From = center + d * gap
                l.To = center + d * (gap + size)
                l.Color = ccol
                l.Thickness = thick
                l.Visible = true
            end
        end
    end
end

function startFovDrawLoop()
    if fovDrawConn then return end
    fovDrawConn = RunService.RenderStepped:Connect(function(dt)
        if not FOV_DRAW_ENABLED and not CROSSHAIR_ENABLED then
            destroyFovDrawings()
            return
        end
        pcall(updateFovVisuals, dt)
    end)
end

function stopFovDrawLoopIfIdle()
    if FOV_DRAW_ENABLED or CROSSHAIR_ENABLED then
        startFovDrawLoop()
        return
    end
    if fovDrawConn then
        pcall(function() fovDrawConn:Disconnect() end)
        fovDrawConn = nil
    end
    destroyFovDrawings()
end

getgenv().startFovDrawLoop = startFovDrawLoop
getgenv().stopFovDrawLoopIfIdle = stopFovDrawLoopIfIdle
getgenv().getAimFovRadiusPx = getAimFovRadiusPx

function stopLegitAimbot()
    LEGIT_AIMBOT_ENABLED = false
    if legitAimbotConn then
        pcall(function() legitAimbotConn:Disconnect() end)
        legitAimbotConn = nil
    end
end

function startLegitAimbot()
    if legitAimbotConn then
        pcall(function() legitAimbotConn:Disconnect() end)
        legitAimbotConn = nil
    end
    LEGIT_AIMBOT_ENABLED = true
    legitAimbotConn = RunService.RenderStepped:Connect(function(deltaTime)
        if not LEGIT_AIMBOT_ENABLED then return end
        if not isSharedAimKeyHeld() then return end
        if AIMBOT_ENABLED and AIMBOT_KEY and isSharedAimKeyHeld() then
        end

        local ref, part = getSilentAimTarget()
        if not part or not part.Parent then return end
        if typeof(ref) == "Instance" and ref:IsA("Player") then
            if shouldIgnoreKatanaTarget and shouldIgnoreKatanaTarget(ref) then return end
        end

        local cam = Workspace.CurrentCamera
        if not cam then return end
        local origin = cam.CFrame.Position
        local worldPosition = part.Position

        local screen, onScreen = cam:WorldToViewportPoint(worldPosition)
        if not onScreen or screen.Z < 0 then return end
        local center = cam.ViewportSize * 0.5
        local dist2d = (Vector2.new(screen.X, screen.Y) - Vector2.new(center.X, center.Y)).Magnitude
        local radius = getAimFovRadiusPx()
        if dist2d > radius then return end

        local dt = math.clamp(type(deltaTime) == "number" and deltaTime or (1 / 60), 0, 0.05)
        legitAimNoise.t = (legitAimNoise.t or 0) + dt
        local t = legitAimNoise.t
        worldPosition = worldPosition + Vector3.new(
            math.sin(t * 2.4) * 0.006,
            math.cos(t * 1.9) * 0.005,
            0
        )
        local sm = math.clamp(tonumber(LEGIT_AIMBOT_SMOOTH) or 55, 1, 100)
        local aimSpeed = 3.5 + (sm / 100) * 18
        local blendAlpha = math.clamp(1 - math.exp(-dt * aimSpeed), 0.04, 0.72)

        local cameraController = resolveAimbotCameraController and resolveAimbotCameraController() or nil
        if cameraController and type(cameraController.SetRotation) == "function" then
            local currentRotation = rawget(cameraController, "Rotation")
            if typeof(currentRotation) == "Vector2" then
                local pitch, yaw = CFrame.lookAt(origin, worldPosition):ToOrientation()
                pcall(function()
                    cameraController:SetRotation(Vector2.new(
                        currentRotation.X + (pitch - currentRotation.X) * blendAlpha,
                        currentRotation.Y + ((yaw - currentRotation.Y + math.pi) % (2 * math.pi) - math.pi) * blendAlpha
                    ))
                end)
                return
            end
        end
        cam.CFrame = cam.CFrame:Lerp(CFrame.lookAt(origin, worldPosition), blendAlpha)
    end)
end

getgenv().startLegitAimbot = startLegitAimbot
getgenv().stopLegitAimbot = stopLegitAimbot
function formatAimbotKey(bind)
    if bind == nil then return "없음 (자동)" end
    if typeof(bind) == "EnumItem" then
        if bind.EnumType == Enum.KeyCode then
            return "키:" .. bind.Name
        end
        if bind.EnumType == Enum.UserInputType then
            local map = {
                [Enum.UserInputType.MouseButton1] = "마우스 좌클릭",
                [Enum.UserInputType.MouseButton2] = "마우스 우클릭",
                [Enum.UserInputType.MouseButton3] = "마우스 휠클릭",
            }
            return map[bind] or ("마우스:" .. bind.Name)
        end
        return tostring(bind.Name)
    end
    return tostring(bind)
end
getgenv().formatAimbotKey = formatAimbotKey

function updateAimbotKeyButton()
    local b = getgenv().AimbotKeyBindBtn
    if b and b.Parent then
        b.Text = "Aimbot 키: " .. formatAimbotKey(AIMBOT_KEY)
    end
end
getgenv().updateAimbotKeyButton = updateAimbotKeyButton

function isAimbotBindMatch(input)
    if AIMBOT_KEY == nil then return false end
    if typeof(AIMBOT_KEY) == "EnumItem" then
        if AIMBOT_KEY.EnumType == Enum.KeyCode then
            return input.KeyCode == AIMBOT_KEY
        end
        if AIMBOT_KEY.EnumType == Enum.UserInputType then
            return input.UserInputType == AIMBOT_KEY
        end
    end
    return false
end

UserInputService.InputBegan:Connect(function(input, gp)
    if AIMBOT_KEY_LISTENING then
        if input.UserInputType == Enum.UserInputType.Keyboard then
            AIMBOT_KEY = input.KeyCode
            AIMBOT_KEY_LISTENING = false
            updateAimbotKeyButton()
            pcall(createNotification, "Aimbot 키 설정: " .. formatAimbotKey(AIMBOT_KEY))
            return
        end
        if input.UserInputType == Enum.UserInputType.MouseButton1
            or input.UserInputType == Enum.UserInputType.MouseButton2
            or input.UserInputType == Enum.UserInputType.MouseButton3 then
            AIMBOT_KEY = input.UserInputType
            AIMBOT_KEY_LISTENING = false
            updateAimbotKeyButton()
            pcall(createNotification, "Aimbot 키 설정: " .. formatAimbotKey(AIMBOT_KEY))
            return
        end
        return
    end
    if not AIMBOT_KEY then return end
    if not (AIMBOT_ENABLED or LEGIT_AIMBOT_ENABLED) then return end
    if isAimbotBindMatch(input) then
        aimbotKeyHeld = true
    end
end)
UserInputService.InputEnded:Connect(function(input)
    if AIMBOT_KEY and isAimbotBindMatch(input) then
        aimbotKeyHeld = false
        aimbotLockedRef = nil
    end
end)

function isSharedAimKeyHeld()
    if not AIMBOT_KEY then return true end
    if typeof(AIMBOT_KEY) ~= "EnumItem" then return aimbotKeyHeld and true or false end
    if AIMBOT_KEY.EnumType == Enum.KeyCode then
        local ok, down = pcall(function() return UserInputService:IsKeyDown(AIMBOT_KEY) end)
        return ok and down or aimbotKeyHeld
    end
    if AIMBOT_KEY.EnumType == Enum.UserInputType then
        local ok, down = pcall(function()
            return UserInputService:IsMouseButtonPressed(AIMBOT_KEY)
        end)
        return ok and down or aimbotKeyHeld
    end
    return aimbotKeyHeld and true or false
end
getgenv().isSharedAimKeyHeld = isSharedAimKeyHeld
rb3OrbitAngle = 0
rb3SavedCF = nil

function getClosestEnemyRB3_Lunara()
    local myChar = LocalPlayer.Character
    local myRoot = myChar and myChar:FindFirstChild("HumanoidRootPart")
    if not myRoot then return nil end
    local closest, best = nil, math.huge
    for _, plr in ipairs(Players:GetPlayers()) do
        if plr == LocalPlayer then continue end
        local enemy = true
        pcall(function()
            if type(isEnemy) == "function" then
                enemy = isEnemy(plr)
            else
                local a, b = LocalPlayer:GetAttribute("TeamID"), plr:GetAttribute("TeamID")
                if a ~= nil and b ~= nil and a == b then enemy = false end
            end
        end)
        if not enemy then continue end
        local char = plr.Character
        if not char then continue end
        local hum = char:FindFirstChildOfClass("Humanoid")
        local root = char:FindFirstChild("HumanoidRootPart")
        if not hum or not root or hum.Health <= 0 then continue end
        local d = (root.Position - myRoot.Position).Magnitude
        if d < best then
            best = d
            closest = plr
        end
    end
    return closest
end

function rb3TryShoot(targetChar, shootPos)
    pcall(function()
        local RS = game:GetService("ReplicatedStorage")
        local enums, utility, fc
        pcall(function() enums = require(RS.Modules.EnumLibrary) end)
        pcall(function() utility = require(RS.Modules.Utility) end)
        pcall(function() fc = require(LocalPlayer.PlayerScripts.Controllers.FighterController) end)
        local lf = fc and fc.LocalFighter
        if not lf or not lf.EquippedItem then return end
        local equipped = lf.EquippedItem
        local oid = equipped:Get("ObjectID")
        if not oid or not utility or not enums then return end
        local hitPart = targetChar:FindFirstChild("Head") or targetChar:FindFirstChild("HumanoidRootPart")
        if not hitPart then return end
        local targetPos = hitPart.Position
        local origin = shootPos
        if typeof(origin) ~= "Vector3" then
            origin = targetPos + Vector3.new(0, 1.2, 0)
        end
        local aimCF = CFrame.new(origin, targetPos)
        local data = {
            [utf8.char(1)] = {
                [utf8.char(0)] = utility:EncodeCFrame(aimCF),
                [utf8.char(1)] = utility:EncodeCFrame(aimCF),
                [utf8.char(2)] = hitPart,
                [utf8.char(3)] = utility:EncodeCFrame(CFrame.new(0.43, 0.25, 0.42)),
            },
        }
        local useItem = RS.Remotes.Replication.Fighter.UseItem
        local mode = tostring(RAGE_ATTACK_MODE or "Gun")
        local enumName = (mode == "Melee" or mode == "Knife" or mode == "칼") and "StartAiming" or "StartShooting"
        local ev = enums:ToEnum(enumName)
        if ev then useItem:FireServer(oid, ev, data, nil) end
    end)
end

local CharacterParts = {}
setmetatable(CharacterParts, {
    __index = function(_, key)
        local char = LocalPlayer.Character
        if not char then return nil end
        if key == "root" then return char:FindFirstChild("HumanoidRootPart") end
        if key == "head" then return char:FindFirstChild("Head") end
        return nil
    end
})

local DesyncEngine = {
    active = false,
    conn = nil,
    task1 = nil,
    currentTarget = nil,
    tag = nil,
}

function DesyncStop()
    DesyncEngine.active = false
    DesyncEngine.currentTarget = nil
    if DesyncEngine.conn then
        DesyncEngine.conn:Disconnect()
        DesyncEngine.conn = nil
    end
    if DesyncEngine.task1 then
        pcall(task.cancel, DesyncEngine.task1)
        DesyncEngine.task1 = nil
    end
    pcall(function() RunService:UnbindFromRenderStep("Restore") end)
    pcall(function() RunService:UnbindFromRenderStep("Restore_RB1") end)
    pcall(function() RunService:UnbindFromRenderStep("Restore_RB3") end)
    pcall(function() RunService:UnbindFromRenderStep("Restore_RB4") end)
    pcall(function() RunService:UnbindFromRenderStep("Restore_Standalone_Desync") end)
end

function DesyncStart(target, tag)
    if shouldBlockRageActions and shouldBlockRageActions() then return end
    if getgenv().IsTargetNearTripmine and getgenv().IsTargetNearTripmine(target) then return end
    if getgenv().IsTargetImmune and getgenv().IsTargetImmune(target) then return end
    if not target then return end
    if DesyncEngine.conn then DesyncEngine.conn:Disconnect() end
    DesyncEngine.active = true
    DesyncEngine.currentTarget = target
    DesyncEngine.tag = tag

    DesyncEngine.conn = RunService.Heartbeat:Connect(function()
        if not DesyncEngine.active then return end
        if getgenv().IsTargetNearTripmine and getgenv().IsTargetNearTripmine(DesyncEngine.currentTarget) then return end
    if getgenv().IsTargetImmune and getgenv().IsTargetImmune(DesyncEngine.currentTarget) then return end
        local myRoot = CharacterParts.root
        if not myRoot then return end
        local tchar = target.Character or (typeof(target) == "Instance" and target:IsA("Model") and target)
        local targetRoot = tchar and tchar:FindFirstChild("HumanoidRootPart")
        if not targetRoot and target.Character then
            targetRoot = target.Character:FindFirstChild("HumanoidRootPart")
        end
        if not targetRoot then
            DesyncStop()
            return
        end
        local originalCFrame = myRoot.CFrame
        local originalVelocity = myRoot.AssemblyLinearVelocity
        local originalRotVelocity = myRoot.AssemblyAngularVelocity
        do local sa = (isSpinning and spinbotAngle) or 0; myRoot.CFrame = targetRoot.CFrame * CFrame.new(0, -5, 0) * CFrame.Angles(0, sa, 0) end
        pcall(function()
            RunService:BindToRenderStep("Restore", 101, function()
                if myRoot and myRoot.Parent then
                    myRoot.CFrame = originalCFrame
                    pcall(function()
                        myRoot.AssemblyLinearVelocity = originalVelocity
                        myRoot.AssemblyAngularVelocity = originalRotVelocity
                    end)
                end
                pcall(function() RunService:UnbindFromRenderStep("Restore") end)
            end)
        end)
    end)
end

function DesyncPulse(target, tag)
    if DesyncEngine.task1 then
        pcall(task.cancel, DesyncEngine.task1)
        DesyncEngine.task1 = nil
    end
    if not DesyncEngine.active or DesyncEngine.currentTarget ~= target then
        DesyncStart(target, tag)
    end
    DesyncEngine.task1 = task.delay(0.15, function()
        DesyncStop()
    end)
end

getgenv().DesyncEngine = DesyncEngine
getgenv().DesyncStart = DesyncStart
getgenv().DesyncStop = DesyncStop
getgenv().DesyncPulse = DesyncPulse

RAGE_LOCK_TIMEOUT = 6
rb1LockStarted = 0

function isRageLockedTargetValid(target)
    if not target then return false end
    local player, char
    if typeof(target) == "Instance" and target:IsA("Player") then
        player = target
        char = player.Character
    elseif typeof(target) == "Instance" and target:IsA("Model") then
        char = target
        player = Players:GetPlayerFromCharacter(char)
    else
        return false
    end
    if not char or not char.Parent then return false end
    local hum = char:FindFirstChildOfClass("Humanoid")
    local root = char:FindFirstChild("HumanoidRootPart") or char:FindFirstChild("Head")
    if not hum or not root or hum.Health <= 0 then return false end
    if player then
        if player == LocalPlayer then return false end
        local skipTeam = false
        pcall(function()
            local a, b = player:GetAttribute("TeamID"), LocalPlayer:GetAttribute("TeamID")
            if a ~= nil and b ~= nil and a == b then skipTeam = true end
        end)
        if skipTeam then return false end
        if getgenv().IsTargetNearTripmine and getgenv().IsTargetNearTripmine(player) then return false end
        if getgenv().IsTargetImmune and getgenv().IsTargetImmune(player) then return false end
        if shouldIgnoreKatanaTarget and shouldIgnoreKatanaTarget(player) then return false end
    else
        if getgenv().IsTargetNearTripmine and getgenv().IsTargetNearTripmine(char) then return false end
        if getgenv().IsTargetImmune and getgenv().IsTargetImmune(char) then return false end
    end
    return true
end

function rb1FindTarget()
    if shouldBlockRageActions and shouldBlockRageActions() then return nil end
    local myChar = LocalPlayer.Character
    if not myChar then return nil end
    local myRoot = myChar:FindFirstChild("HumanoidRootPart")
    if not myRoot then return nil end
    local closest, closestDist = nil, math.huge
    local MAX_DISTANCE = math.huge
    for _, player in pairs(Players:GetPlayers()) do
        if player == LocalPlayer then continue end
        local skipTeam = false
        pcall(function()
            local a, b = player:GetAttribute("TeamID"), LocalPlayer:GetAttribute("TeamID")
            if a ~= nil and a == b then skipTeam = true end
        end)
        if skipTeam then continue end
        if getgenv().IsTargetNearTripmine and getgenv().IsTargetNearTripmine(player) then continue end
            if getgenv().IsTargetImmune and getgenv().IsTargetImmune(player) then continue end
        if shouldIgnoreKatanaTarget and shouldIgnoreKatanaTarget(player) then continue end
        local char = player.Character
        if not char then continue end
        local root = char:FindFirstChild("HumanoidRootPart")
        local head = char:FindFirstChild("Head")
        local hum = char:FindFirstChildWhichIsA("Humanoid")
        if not (root and head and hum and hum.Health > 0) then continue end
        local dist = (myRoot.Position - root.Position).Magnitude
        if dist > MAX_DISTANCE then continue end
        if dist < closestDist then
            closestDist = dist
            closest = player
        end
    end
    return closest
end

function rb1StopDesync()
    rb1Desync = false
    rb1CurrentTarget = nil
    if rb1Conn2 then
        rb1Conn2:Disconnect()
        rb1Conn2 = nil
    end
    pcall(function() RunService:UnbindFromRenderStep("Restore") end)
end
function rb1StartDesync(target)
    if getgenv().IsTargetNearTripmine and getgenv().IsTargetNearTripmine(target) then return end
    if getgenv().IsTargetImmune and getgenv().IsTargetImmune(target) then return end
    if rb1Conn2 then rb1Conn2:Disconnect() end
    rb1Desync = true
    rb1CurrentTarget = target
    rb1Conn2 = RunService.Heartbeat:Connect(function()
        if not rb1Desync then return end
        if getgenv().IsTargetNearTripmine and getgenv().IsTargetNearTripmine(rb1CurrentTarget) then return end
    if getgenv().IsTargetImmune and getgenv().IsTargetImmune(rb1CurrentTarget) then return end
        local myRoot = LocalPlayer.Character and LocalPlayer.Character:FindFirstChild("HumanoidRootPart")
        if not myRoot then return end
        local targetRoot = target and target.Character and target.Character:FindFirstChild("HumanoidRootPart")
        if not targetRoot then
            rb1StopDesync()
            return
        end
        local originalCFrame = myRoot.CFrame
        local originalVelocity = myRoot.AssemblyLinearVelocity
        local originalRotVelocity = myRoot.AssemblyAngularVelocity
        pcall(function()
            originalVelocity = myRoot.Velocity or originalVelocity
            originalRotVelocity = myRoot.RotVelocity or originalRotVelocity
        end)
        do local sa = (isSpinning and spinbotAngle) or 0; myRoot.CFrame = targetRoot.CFrame * CFrame.new(0, -5, 0) * CFrame.Angles(0, sa, 0) end
        pcall(function()
            RunService:BindToRenderStep("Restore", 101, function()
                if myRoot and myRoot.Parent then
                    myRoot.CFrame = originalCFrame
                    pcall(function() myRoot.Velocity = originalVelocity end)
                    pcall(function() myRoot.RotVelocity = originalRotVelocity end)
                    pcall(function()
                        myRoot.AssemblyLinearVelocity = originalVelocity
                        myRoot.AssemblyAngularVelocity = originalRotVelocity
                    end)
                end
                pcall(function() RunService:UnbindFromRenderStep("Restore") end)
            end)
        end)
    end)
end

function startRageBot()
    pcall(function()
        if rb1Conn1 then rb1Conn1:Disconnect() end
        if rb1Conn2 then rb1Conn2:Disconnect() end
        if rb1Task1 then task.cancel(rb1Task1) end
    end)
    rb1Conn1, rb1Conn2, rb1Task1 = nil, nil, nil
    rbEnabled = true
    rb1Target = nil

    rb1Conn1 = RunService.Heartbeat:Connect(function()
        if not rbEnabled then
            rb1Target = nil
            if getgenv().RAGEBOT_ACTIVE_TARGET and not rb4Enabled then
                getgenv().RAGEBOT_ACTIVE_TARGET = nil
            end
            return
        end
        -- lock until dead; if same target >6s still alive, switch to another first
        local now = tick()
        local keep = isRageLockedTargetValid(rb1Target)
        if keep then
            if (rb1LockStarted or 0) <= 0 then
                rb1LockStarted = now
            elseif (now - rb1LockStarted) >= (RAGE_LOCK_TIMEOUT or 6) then
                local stuck = rb1Target
                local nextT = nil
                -- find another enemy, skip the stuck one
                local myChar = LocalPlayer.Character
                local myRoot = myChar and myChar:FindFirstChild("HumanoidRootPart")
                if myRoot then
                    local best, bestD = nil, math.huge
                    for _, player in pairs(Players:GetPlayers()) do
                        if player == LocalPlayer or player == stuck then continue end
                        if not isRageLockedTargetValid(player) then continue end
                        local root = player.Character and player.Character:FindFirstChild("HumanoidRootPart")
                        if not root then continue end
                        local d = (myRoot.Position - root.Position).Magnitude
                        if d < bestD then bestD, best = d, player end
                    end
                    nextT = best
                end
                if nextT then
                    rb1Target = nextT
                    rb1LockStarted = now
                else
                    -- no other target: keep current, reset timer so we retry switch later
                    rb1LockStarted = now
                end
            end
        else
            rb1Target = rb1FindTarget()
            rb1LockStarted = rb1Target and now or 0
        end
        if rb1Target then
            getgenv().RAGEBOT_ACTIVE_TARGET = rb1Target
        elseif not rb4Enabled then
            getgenv().RAGEBOT_ACTIVE_TARGET = nil
        end
    end)

    pcall(function()
        local PlayerScripts = LocalPlayer:WaitForChild("PlayerScripts", 8)
        local GunModule = require(PlayerScripts:WaitForChild("Modules"):WaitForChild("ItemTypes"):WaitForChild("Gun"))
        local UtilityModule = require(ReplicatedStorage:WaitForChild("Modules"):WaitForChild("Utility"))

        if rb1OldStartShooting then
            pcall(function() GunModule.StartShooting = rb1OldStartShooting end)
        end
        local originalStartShooting = GunModule.StartShooting
        rb1OldStartShooting = originalStartShooting

        GunModule.StartShooting = function(item, ...)
            local results = { originalStartShooting(item, ...) }

            if not item.ClientFighter or not item.ClientFighter.IsLocalPlayer then
                return unpack(results)
            end

            local data = results[3]
            if not data or typeof(data) ~= "table" then
                return unpack(results)
            end

            results[4] = true
            local target = rb1Target

            if not rbEnabled or not target or not target.Character then
                return unpack(results)
            end
            local doDesync = (rb1DesyncEnabled == true)
            if doDesync then
                if not rb1Desync or rb1CurrentTarget ~= target then
                    rb1StartDesync(target)
                    task.wait(0.01)
                end
            end

            if rb1Task1 then
                task.cancel(rb1Task1)
                rb1Task1 = nil
            end

            local head = target.Character:FindFirstChild("Head")
            if not head then return unpack(results) end

            local headPos = head.Position
            local headCFrame = head.CFrame
            local belowPos = headPos - Vector3.new(0, 5, 0)
            local lookCFrame = CFrame.lookAt(belowPos, headPos)
            local randomOffset = headCFrame:ToObjectSpace(CFrame.new(headPos + Vector3.new(math.random(), math.random(), math.random())))

            data[utf8.char(0)] = UtilityModule:EncodeCFrame(CFrame.new(belowPos, headPos) * CFrame.Angles(lookCFrame:ToOrientation()))
            data[utf8.char(1)] = UtilityModule:EncodeCFrame(CFrame.new(headPos) * CFrame.Angles(lookCFrame:ToOrientation()))
            data[utf8.char(2)] = head
            data[utf8.char(3)] = UtilityModule:EncodeCFrame(randomOffset)

            if doDesync then
                rb1Task1 = task.delay(0.15, function()
                    rb1StopDesync()
                end)
            end

            return unpack(results)
        end
    end)

    createNotification("Rage Bot 1 Ready (main.lua)")
end

function stopRageBot()
    rbEnabled = false
    rb1Target = nil
    rb1Desync = false
    rb1CurrentTarget = nil
    if rb1Conn1 then
        pcall(function() rb1Conn1:Disconnect() end)
        rb1Conn1 = nil
    end
    if rb1Conn2 then
        pcall(function() rb1Conn2:Disconnect() end)
        rb1Conn2 = nil
    end
    if rb1Task1 then
        pcall(task.cancel, rb1Task1)
        rb1Task1 = nil
    end
    pcall(function() RunService:UnbindFromRenderStep("Restore") end)
    pcall(function() RunService:UnbindFromRenderStep("Restore_RB1") end)
    pcall(function()
        if DesyncEngine and DesyncEngine.tag == "rb1" then DesyncStop() end
    end)
    pcall(function()
        local ps = LocalPlayer:FindFirstChild("PlayerScripts")
        if ps and rb1OldStartShooting then
            local GunModule = require(ps.Modules.ItemTypes.Gun)
            GunModule.StartShooting = rb1OldStartShooting
        end
    end)
    pcall(function()
        if rb1OldStartShooting then
            local GunModule = require(LocalPlayer.PlayerScripts.Modules.ItemTypes.Gun)
            if GunModule.StartShooting ~= rb1OldStartShooting then
                GunModule.StartShooting = rb1OldStartShooting
            end
        end
    end)
end

function startRageBot2()
    rb2Enabled = false
    createNotification("Rage Bot 2 제거됨")
end

function stopRageBot2()
    rb2Enabled = false
end

function getClosestEnemyRB3()
    local char = LocalPlayer.Character
    local hrp = char and char:FindFirstChild("HumanoidRootPart")
    if not hrp then return nil end

    local closestEnemy, shortestDistance = nil, math.huge
    for _, player in ipairs(Players:GetPlayers()) do
        if isAliveEnemy(player) and player.Character then
            if shouldIgnoreKatanaTarget and shouldIgnoreKatanaTarget(player) then continue end
            if getgenv().IsTargetNearTripmine and getgenv().IsTargetNearTripmine(player) then continue end
            if getgenv().IsTargetImmune and getgenv().IsTargetImmune(player) then continue end
            local enemyHrp = player.Character:FindFirstChild("HumanoidRootPart")
            if enemyHrp then
                local dist = (hrp.Position - enemyHrp.Position).Magnitude
                if dist < shortestDistance then
                    shortestDistance = dist
                    closestEnemy = player
                end
            end
        end
    end
    return closestEnemy
end
rb3OrbitAngle = 0
rb3SavedCF = nil

function getClosestEnemyRB3_Lunara()
    local myChar = LocalPlayer.Character
    local myRoot = myChar and myChar:FindFirstChild("HumanoidRootPart")
    if not myRoot then return nil end
    local closest, best = nil, math.huge
    for _, plr in ipairs(Players:GetPlayers()) do
        if plr == LocalPlayer then continue end
        local enemy = true
        pcall(function()
            if type(isEnemy) == "function" then
                enemy = isEnemy(plr)
            else
                local a, b = LocalPlayer:GetAttribute("TeamID"), plr:GetAttribute("TeamID")
                if a ~= nil and b ~= nil and a == b then enemy = false end
            end
        end)
        if not enemy then continue end
        local char = plr.Character
        if not char then continue end
        local hum = char:FindFirstChildOfClass("Humanoid")
        local root = char:FindFirstChild("HumanoidRootPart")
        if not hum or not root or hum.Health <= 0 then continue end
        local d = (root.Position - myRoot.Position).Magnitude
        if d < best then
            best = d
            closest = plr
        end
    end
    return closest
end

function rb3TryShoot(targetChar, shootPos)
    pcall(function()
        local RS = game:GetService("ReplicatedStorage")
        local enums, utility, fc
        pcall(function() enums = require(RS.Modules.EnumLibrary) end)
        pcall(function() utility = require(RS.Modules.Utility) end)
        pcall(function() fc = require(LocalPlayer.PlayerScripts.Controllers.FighterController) end)
        local lf = fc and fc.LocalFighter
        if not lf or not lf.EquippedItem then return end
        local equipped = lf.EquippedItem
        local oid = equipped:Get("ObjectID")
        if not oid or not utility or not enums then return end
        local hitPart = targetChar:FindFirstChild("Head") or targetChar:FindFirstChild("HumanoidRootPart")
        if not hitPart then return end
        local targetPos = hitPart.Position
        local origin = shootPos
        if typeof(origin) ~= "Vector3" then
            origin = targetPos + Vector3.new(0, 1.2, 0)
        end
        local aimCF = CFrame.new(origin, targetPos)
        local data = {
            [utf8.char(1)] = {
                [utf8.char(0)] = utility:EncodeCFrame(aimCF),
                [utf8.char(1)] = utility:EncodeCFrame(aimCF),
                [utf8.char(2)] = hitPart,
                [utf8.char(3)] = utility:EncodeCFrame(CFrame.new(0.43, 0.25, 0.42)),
            },
        }
        local useItem = RS.Remotes.Replication.Fighter.UseItem
        local mode = tostring(RAGE_ATTACK_MODE or "Gun")
        local enumName = (mode == "Melee" or mode == "Knife" or mode == "칼") and "StartAiming" or "StartShooting"
        local ev = enums:ToEnum(enumName)
        if ev then useItem:FireServer(oid, ev, data, nil) end
    end)
end

function startRageBot3()
    rb3Enabled = false
    createNotification("Rage Bot 3 제거됨")
end

function stopRageBot3()
    rb3Enabled = false
end

function faFindClosestPlayer()
    if not FULL_AUTO_ENABLED then return nil end
    local character = LocalPlayer.Character
    if not character or not character:FindFirstChild("HumanoidRootPart") then return nil end
    local myPos = character.HumanoidRootPart.Position
    local closestPlayer, shortestDistance = nil, math.huge
    for _, player in pairs(Players:GetPlayers()) do
        if player ~= LocalPlayer and player.Character and isEnemy(player) then
            if shouldIgnoreKatanaTarget and shouldIgnoreKatanaTarget(player) then continue end
            if getgenv().IsTargetNearTripmine and getgenv().IsTargetNearTripmine(player) then continue end
            if getgenv().IsTargetImmune and getgenv().IsTargetImmune(player) then continue end
            local theirRoot = player.Character:FindFirstChild("HumanoidRootPart")
            if theirRoot then
                local distance = (myPos - theirRoot.Position).Magnitude
                if distance < shortestDistance then
                    shortestDistance = distance
                    closestPlayer = player
                end
            end
        end
    end
    return closestPlayer
end

function faPressR()
    if not FULL_AUTO_ENABLED then return end
    VirtualInputManager:SendKeyEvent(true, Enum.KeyCode.R, false, game)
    task.wait(0.05)
    VirtualInputManager:SendKeyEvent(false, Enum.KeyCode.R, false, game)
end

function faDisableGravity()
    if faGravityConnection then faGravityConnection:Disconnect() end
    faGravityConnection = RunService.RenderStepped:Connect(function()
        if not FULL_AUTO_ENABLED then 
            if faGravityConnection then faGravityConnection:Disconnect() faGravityConnection = nil end
            return 
        end
        local character = LocalPlayer.Character
        if character then
            local root = character:FindFirstChild("HumanoidRootPart")
            if root and not root:FindFirstChild("FA_NoGravity") then
                local bodyVelocity = Instance.new("BodyVelocity")
                bodyVelocity.Name = "FA_NoGravity"
                bodyVelocity.MaxForce = Vector3.new(0, math.huge, 0)
                bodyVelocity.Velocity = Vector3.zero
                bodyVelocity.Parent = root
            end
        end
    end)
end

function faStartSpinning()
    if faSpinConnection then faSpinConnection:Disconnect() end
    faSpinConnection = RunService.RenderStepped:Connect(function()
        if not FULL_AUTO_ENABLED or faIsRetreating then return end
        local character = LocalPlayer.Character
        if character and character:FindFirstChild("HumanoidRootPart") then
            local root = character.HumanoidRootPart
            root.CFrame = root.CFrame * CFrame.Angles(math.rad(math.random(-30, 30)), math.rad(math.random(0, 360)), math.rad(math.random(-30, 30)))
        end
    end)
end

function faStartCameraLock()
    if faCameraConnection then faCameraConnection:Disconnect() end
    faCameraConnection = RunService.RenderStepped:Connect(function()
        if not FULL_AUTO_ENABLED then 
            Camera.CameraType = Enum.CameraType.Custom
            if faCameraConnection then faCameraConnection:Disconnect() faCameraConnection = nil end
            return 
        end
        if faIsRetreating then return end
        local character = LocalPlayer.Character
        local myRoot = character and character:FindFirstChild("HumanoidRootPart")
        if faTargetPlayer and faTargetPlayer.Character and myRoot then
            local targetPart = getAimTargetPart(faTargetPlayer.Character)
            if targetPart then
                Camera.CameraType = Enum.CameraType.Scriptable
                Camera.CFrame = CFrame.new(myRoot.Position + Vector3.new(0, 5, 0), targetPart.Position)
            end
        end
    end)
end

function faIsTargetInRange()
    if not FULL_AUTO_ENABLED or not faTargetPlayer or not faTargetPlayer.Character then return false end
    local character = LocalPlayer.Character
    local myRoot = character and character:FindFirstChild("HumanoidRootPart")
    local targetRoot = faTargetPlayer.Character:FindFirstChild("HumanoidRootPart")
    if not myRoot or not targetRoot then return false end
    return true
end

function faStartAutoClick()
    if faAutoClickConnection then faAutoClickConnection:Disconnect() end
    faAutoClickConnection = RunService.RenderStepped:Connect(function()
        if not FULL_AUTO_ENABLED or faAutoClickPaused or faIsRetreating or MainFrame.Visible or not faIsTargetInRange() then return end
        local cur = tick()
        if cur - faLastAutoClickTime >= FA_CLICK_INTERVAL then
            faLastAutoClickTime = cur
            pcall(function() 
                pcall(mouse1click)
                VirtualInputManager:SendMouseButtonEvent(0, 0, 0, true, game, 0)
                VirtualInputManager:SendMouseButtonEvent(0, 0, 0, false, game, 0)
            end)
        end
    end)
end

local function faPerformRetreat(targetRoot)
    if not FULL_AUTO_ENABLED or faRetreatLock then return end
    faRetreatLock, faIsRetreating, faAutoClickPaused = true, true, true
    local character = LocalPlayer.Character
    local root = character and character:FindFirstChild("HumanoidRootPart")
    if not root or not targetRoot then
        faIsRetreating, faAutoClickPaused, faRetreatLock = false, false, false
        return
    end
    Camera.CameraType = Enum.CameraType.Custom
    root.CFrame = CFrame.new(targetRoot.Position + Vector3.new(0, 10000, 0))
    task.wait(0.2)
    faPressR()
    task.wait(2)
    faAutoClickPaused, faIsRetreating, faRetreatLock, faIsAbove = false, false, false, false
    faLastRetreatTime = tick()
end

local function faMainLoop()
    faLoopActive = true
    while FULL_AUTO_ENABLED do
        task.wait(0.1)
        if not FULL_AUTO_ENABLED then break end
        if not faTargetPlayer or not faTargetPlayer.Character then
            faTargetPlayer = faFindClosestPlayer()
            if not faTargetPlayer then task.wait(0.5) continue end
        end
        local character = LocalPlayer.Character
        local root = character and character:FindFirstChild("HumanoidRootPart")
        local humanoid = character and character:FindFirstChild("Humanoid")
        if not character or not humanoid or not root then task.wait(0.5) continue end
        
        local targetChar = faTargetPlayer.Character
        local targetRoot = targetChar and targetChar:FindFirstChild("HumanoidRootPart")
        if not targetRoot then faTargetPlayer = nil task.wait(0.5) continue end
        
        if not faRetreatLock then
            if humanoid.Health < faLastHealth and faLastHealth > 0 then
                faPerformRetreat(targetRoot)
            elseif not faIsRetreating and (tick() - faLastRetreatTime >= FA_RETREAT_INTERVAL) then
                faPerformRetreat(targetRoot)
            elseif not faIsAbove and not faIsRetreating then
                root.CFrame = CFrame.new(targetRoot.Position + Vector3.new(0, 10000, 0))
                task.wait(math.random(10, 20) / 10)
                faIsAbove = true
            elseif not faIsRetreating then
                root.CFrame = CFrame.new(targetRoot.Position + Vector3.new(0, 15, 0))
                if faIsFirstTeleport then task.wait(2) faIsFirstTeleport = false end
                faLastHealth = humanoid.Health
            end
        end
    end
    faLoopActive = false
end
local mouseAutoFireConn = nil
local mouseAutoLastClick = 0

local function stopMouseAutoFire()
    MOUSE_AUTO_FIRE_ENABLED = true
    if mouseAutoFireConn then
        pcall(function() mouseAutoFireConn:Disconnect() end)
        mouseAutoFireConn = nil
    end
end

local function getPlayerUnderMouse()
    local mouse = LocalPlayer:GetMouse()
    if not mouse then return nil end
    local target = mouse.Target
    if not target then return nil end
    local model = target:FindFirstAncestorOfClass("Model")
    if not model then return nil end
    local plr = Players:GetPlayerFromCharacter(model)
    if not plr or plr == LocalPlayer then return nil end
    local hum = model:FindFirstChildOfClass("Humanoid")
    if not hum or hum.Health <= 0 then return nil end
    local same = false
    pcall(function()
        local a, b = LocalPlayer:GetAttribute("TeamID"), plr:GetAttribute("TeamID")
        if a and b and a == b then same = true end
    end)
    if same then return nil end
    return plr
end

local function mouseAutoClickOnce()
    pcall(function()
        local mouse = LocalPlayer:GetMouse()
        local x = mouse and mouse.X or 0
        local y = mouse and mouse.Y or 0
        VirtualInputManager:SendMouseButtonEvent(x, y, 0, true, game, 0)
        VirtualInputManager:SendMouseButtonEvent(x, y, 0, false, game, 0)
    end)
end

local function startMouseAutoFire()
    stopMouseAutoFire()
    MOUSE_AUTO_FIRE_ENABLED = true
    mouseAutoLastClick = 0
    mouseAutoFireConn = RunService.Heartbeat:Connect(function()
        if not MOUSE_AUTO_FIRE_ENABLED then return end
        local delay = tonumber(MOUSE_AUTO_FIRE_DELAY) or 0.15
        if rbEnabled or rb4Enabled then
            delay = 0
        end
        if delay < 0 then delay = 0 end
        local now = tick()
        if now - mouseAutoLastClick < delay then return end
        local ok, plr = pcall(getPlayerUnderMouse)
        if ok and plr then
            mouseAutoLastClick = now
            mouseAutoClickOnce()
        end
    end)
end

local function startFullAuto()
    FULL_AUTO_ENABLED = false
    return
end

local function stopFullAuto()
    FULL_AUTO_ENABLED = false
    if faGravityConnection then faGravityConnection:Disconnect() faGravityConnection = nil end
    if faSpinConnection then faSpinConnection:Disconnect() faSpinConnection = nil end
    if faCameraConnection then faCameraConnection:Disconnect() faCameraConnection = nil end
    if faAutoClickConnection then faAutoClickConnection:Disconnect() faAutoClickConnection = nil end
    
    local character = LocalPlayer.Character
    if character and character:FindFirstChild("HumanoidRootPart") then
        local noGrav = character.HumanoidRootPart:FindFirstChild("FA_NoGravity")
        if noGrav then noGrav:Destroy() end
    end
    
    Camera.CameraType = Enum.CameraType.Custom
    faIsRetreating = false
    faAutoClickPaused = false
    faRetreatLock = false
    faTargetPlayer = nil
end
NO_RECOIL_STRENGTH = NO_RECOIL_STRENGTH or 100

local function initNoRecoilModules()
    pcall(function()
        local PlayerScripts = LocalPlayer:WaitForChild("PlayerScripts", 5)
        if not PlayerScripts then return end
        for _, module in pairs(PlayerScripts:GetDescendants()) do
            if module:IsA("ModuleScript") and module.Name == "Gun" then
                nrGunModule = require(module)
                break
            end
        end
        if not nrGunModule then
            pcall(function()
                nrGunModule = require(PlayerScripts.Modules.ItemTypes.Gun)
            end)
        end
        if nrGunModule and type(nrGunModule._Recoil) == "function" and not nrOriginalRecoil then
            nrOriginalRecoil = nrGunModule._Recoil
        end
        local ItemLibraryModule = ReplicatedStorage:FindFirstChild("Modules")
        ItemLibraryModule = ItemLibraryModule and ItemLibraryModule:FindFirstChild("ItemLibrary")
        if ItemLibraryModule then
            local ok, lib = pcall(require, ItemLibraryModule)
            if ok then nrItemLibrary = lib end
        end
    end)
end

local function enableNoRecoil()
    if not nrGunModule then
        initNoRecoilModules()
    end
    if not nrGunModule then
        createNotification("NoRecoil: Gun module not found")
        return
    end
    pcall(function()
        if not nrOriginalRecoil and type(nrGunModule._Recoil) == "function" then
            nrOriginalRecoil = nrGunModule._Recoil
        end
        local originalRecoil = nrOriginalRecoil
        if type(originalRecoil) ~= "function" then return end
        nrGunModule._Recoil = function(self, multiplier)
            if not NO_RECOIL_ENABLED then
                return originalRecoil(self, multiplier)
            end
            if type(multiplier) ~= "number" then
                return originalRecoil(self, multiplier)
            end
            local reduction = math.clamp(tonumber(NO_RECOIL_STRENGTH) or 100, 0, 100)
            local reducedMultiplier = multiplier * (1 - (reduction / 100))
            if reducedMultiplier <= 0.001 then
                return
            end
            return originalRecoil(self, reducedMultiplier)
        end
        if nrItemLibrary and type(nrItemLibrary.Items) == "table" then
            for weaponName, weaponData in pairs(nrItemLibrary.Items) do
                if type(weaponData) == "table" then
                    if not nrOriginalItemStats[weaponName] then
                        nrOriginalItemStats[weaponName] = {
                            ShootRecoil = weaponData.ShootRecoil,
                            AimSpreadMultiplier = weaponData.AimSpreadMultiplier,
                        }
                    end
                    if NO_RECOIL_STRENGTH >= 99 then
                        weaponData.ShootRecoil = 0
                        weaponData.AimSpreadMultiplier = 0
                    end
                end
            end
        end
    end)
    createNotification("No Recoil ON (" .. tostring(NO_RECOIL_STRENGTH or 100) .. "%)")
end

local function disableNoRecoil()
    pcall(function()
        if nrGunModule and nrOriginalRecoil then
            nrGunModule._Recoil = nrOriginalRecoil
        end
        if nrItemLibrary and nrItemLibrary.Items and nrOriginalItemStats then
            for weaponName, origStats in pairs(nrOriginalItemStats) do
                local wd = nrItemLibrary.Items[weaponName]
                if wd and origStats then
                    if origStats.ShootRecoil ~= nil then wd.ShootRecoil = origStats.ShootRecoil end
                    if origStats.AimSpreadMultiplier ~= nil then wd.AimSpreadMultiplier = origStats.AimSpreadMultiplier end
                end
            end
        end
    end)
    createNotification("No Recoil OFF")
end

local function ensureCharacterCollision()
    if flyEnabled or noclipEnabled then return end
    local char = LocalPlayer.Character
    if not char then return end
    for _, p in ipairs(char:GetDescendants()) do
        if p:IsA("BasePart") and p.Name ~= "HumanoidRootPart" then
            p.CanCollide = true
        end
    end
end

local function stopFlying()
    flyEnabled = false
    flySavedCF = nil
    getgenv().InstanceFlySavedCF = nil
    local char = LocalPlayer.Character
    local hum = char and char:FindFirstChildOfClass("Humanoid")
    if hum then pcall(function() hum.PlatformStand = false end) end
    if bv then pcall(function() bv:Destroy() end) bv = nil end
    if bg then pcall(function() bg:Destroy() end) bg = nil end
end

local function applyWalkSpeed(val)
    local n = tonumber(val)
    if type(val) == "table" then n = tonumber(val[1] or val.Value) end
    if not n then n = 16 end
    WALK_SPEED = math.clamp(n, 1, 500)
    forceWalkSpeed()
end

function forceWalkSpeed()
    local char = LocalPlayer.Character
    if not char then return end
    local hum = char:FindFirstChildOfClass("Humanoid")
    if not hum then return end
    local spd = tonumber(WALK_SPEED) or 16
    pcall(function()
        if math.abs((hum.WalkSpeed or 0) - spd) > 0.01 then
            hum.WalkSpeed = spd
        end
    end)
end

local function startWalkSpeedLoop()
    if walkSpeedConnection then
        pcall(function() walkSpeedConnection:Disconnect() end)
        walkSpeedConnection = nil
    end
    pcall(function() RunService:UnbindFromRenderStep("ms_walkspeed") end)
    walkSpeedConnection = RunService.Heartbeat:Connect(forceWalkSpeed)
    pcall(function()
        RunService:BindToRenderStep("ms_walkspeed", Enum.RenderPriority.Last.Value, forceWalkSpeed)
    end)
    pcall(function()
        local char = LocalPlayer.Character
        local hum = char and char:FindFirstChildOfClass("Humanoid")
        if hum and not hum:GetAttribute("_wsHooked") then
            hum:SetAttribute("_wsHooked", true)
            hum:GetPropertyChangedSignal("WalkSpeed"):Connect(function()
                if hum.WalkSpeed ~= WALK_SPEED then
                    hum.WalkSpeed = WALK_SPEED
                end
            end)
        end
    end)
    forceWalkSpeed()
end

LocalPlayer.CharacterAdded:Connect(function(char)
    task.spawn(function()
        local hum = char:WaitForChild("Humanoid", 8)
        if not hum then return end
        pcall(function()
            hum:GetPropertyChangedSignal("WalkSpeed"):Connect(function()
                if hum.WalkSpeed ~= WALK_SPEED then
                    hum.WalkSpeed = WALK_SPEED
                end
            end)
        end)
        for _ = 1, 30 do
            pcall(function() hum.WalkSpeed = WALK_SPEED end)
            task.wait(0.05)
        end
        startWalkSpeedLoop()
    end)
end)

local function startFlying()
    stopFlying()
    flyEnabled = true
    flySavedCF = nil

    task.spawn(function()
        while flyEnabled do
            local char = LocalPlayer.Character
            local hrp = char and char:FindFirstChild("HumanoidRootPart")
            local hum = char and char:FindFirstChildOfClass("Humanoid")
            if hrp and hum and hum.Health > 0 then
                pcall(function() hum.PlatformStand = true end)
                local cam = Camera.CFrame
                local dir = Vector3.zero
                if UserInputService:IsKeyDown(Enum.KeyCode.W) then dir = dir + cam.LookVector end
                if UserInputService:IsKeyDown(Enum.KeyCode.S) then dir = dir - cam.LookVector end
                if UserInputService:IsKeyDown(Enum.KeyCode.A) then dir = dir - cam.RightVector end
                if UserInputService:IsKeyDown(Enum.KeyCode.D) then dir = dir + cam.RightVector end
                if UserInputService:IsKeyDown(Enum.KeyCode.Space) then dir = dir + Vector3.new(0, 1, 0) end
                if UserInputService:IsKeyDown(Enum.KeyCode.LeftControl) or UserInputService:IsKeyDown(Enum.KeyCode.LeftShift) then
                    dir = dir - Vector3.new(0, 1, 0)
                end
                local md = hum.MoveDirection
                if dir.Magnitude < 0.05 and md.Magnitude > 0.05 then
                    dir = Vector3.new(md.X, 0, md.Z)
                end
                local spd = flySpeed or 50
                local dt = RunService.Heartbeat:Wait()
                local base = hrp.CFrame
                if dir.Magnitude > 0 then
                    local nextPos = base.Position + dir.Unit * spd * dt
                    hrp.CFrame = CFrame.new(nextPos, nextPos + Vector3.new(cam.LookVector.X, 0, cam.LookVector.Z))
                else
                    hrp.CFrame = CFrame.new(base.Position, base.Position + Vector3.new(cam.LookVector.X, 0, cam.LookVector.Z))
                end
                flySavedCF = hrp.CFrame
                getgenv().InstanceFlySavedCF = flySavedCF
                hrp.AssemblyLinearVelocity = Vector3.zero
                hrp.AssemblyAngularVelocity = Vector3.zero
            else
                RunService.Heartbeat:Wait()
            end
        end
        local char = LocalPlayer.Character
        local hum = char and char:FindFirstChildOfClass("Humanoid")
        if hum then pcall(function() hum.PlatformStand = false end) end
    end)
end

local function toggleNoclip(state)
    noclipEnabled = state
    if noclipConnection then noclipConnection:Disconnect() noclipConnection = nil end
    if state then
        noclipConnection = RunService.Stepped:Connect(function()
            local character = LocalPlayer.Character
            if character and noclipEnabled then
                for _, part in pairs(character:GetDescendants()) do
                    if part:IsA("BasePart") then part.CanCollide = false end
                end
            end
        end)
    end
end

UserInputService.JumpRequest:Connect(function()
    if infJumpEnabled then
        local character = LocalPlayer.Character
        local humanoid = character and character:FindFirstChildOfClass("Humanoid")
        if humanoid then humanoid:ChangeState(Enum.HumanoidStateType.Jumping) end
    end
end)
task.defer(function()
    local function setHalmuThirdPerson(on)
        pcall(function()
            local cc = require(LocalPlayer.PlayerScripts.Controllers.CameraController)
            if not cc or not cc.CameraState then return end
            local states = cc.CameraState.States
            if on then
                if states.ThirdPersonMirrored then
                    cc.CameraState:_SetPOVState(states.ThirdPersonMirrored)
                elseif type(cc.SetThirdPersonOverride) == "function" then
                    cc:SetThirdPersonOverride(true)
                end
            else
                local fp = states.FirstPerson or states.FirstPersonMirrored or states.Default
                if fp then
                    cc.CameraState:_SetPOVState(fp)
                elseif type(cc.SetThirdPersonOverride) == "function" then
                    cc:SetThirdPersonOverride(false)
                end
            end
        end)
    end

    local function enableThirdPerson()
        THIRD_PERSON_ENABLED = true
        setHalmuThirdPerson(true)
        task.spawn(function()
            for _ = 1, 8 do
                if not THIRD_PERSON_ENABLED then break end
                setHalmuThirdPerson(true)
                task.wait(0.25)
            end
        end)
        pcall(createNotification, "Third Person ON")
    end

    local function disableThirdPerson()
        THIRD_PERSON_ENABLED = false
        setHalmuThirdPerson(false)
        pcall(createNotification, "Third Person OFF")
    end

    getgenv().enableThirdPerson = enableThirdPerson
    getgenv().disableThirdPerson = disableThirdPerson
    getgenv().updateThirdPersonCamera = function()
        if THIRD_PERSON_ENABLED then setHalmuThirdPerson(true) end
    end
    pcall(function()
        LocalPlayer.CharacterAdded:Connect(function()
            task.wait(0.6)
            if THIRD_PERSON_ENABLED then
                setHalmuThirdPerson(true)
                task.spawn(function()
                    for _ = 1, 10 do
                        if not THIRD_PERSON_ENABLED then break end
                        setHalmuThirdPerson(true)
                        task.wait(0.3)
                    end
                end)
            end
        end)
    end)
end)
function enableThirdPerson(...)
    local f = getgenv().enableThirdPerson
    if f then return f(...) end
    THIRD_PERSON_ENABLED = true
end
function disableThirdPerson(...)
    local f = getgenv().disableThirdPerson
    if f then return f(...) end
    THIRD_PERSON_ENABLED = false
end
local autoWeaponItemCache = {}
local function safeClone(t)
    if type(t) ~= "table" then return t end
    if table.clone then return table.clone(t) end
    local n = {}
    for k, v in pairs(t) do n[k] = v end
    return n
end

local function getEquippedClientItem()
    local ok, item = pcall(function()
        local fc = require(LocalPlayer.PlayerScripts.Controllers.FighterController)
        local lf = fc and fc.LocalFighter
        return lf and lf.EquippedItem or nil
    end)
    return ok and item or nil
end

local function storeItemInfoSnapshot(item)
    if not item then return end
    local info = item.Info
    if type(info) ~= "table" then return end
    local function goodNum(v)
        return type(v) == "number" and v > 0.05
    end
    local sc = rawget(info, "ShootCooldown")
    local sbc = rawget(info, "ShootBurstCooldown")
    local qsc = rawget(info, "QuickShotCooldown")
    local existing = autoWeaponItemCache[item]
    if existing then
        if goodNum(sc) and not goodNum(existing.ShootCooldown) then existing.ShootCooldown = sc end
        if goodNum(sbc) and not goodNum(existing.ShootBurstCooldown) then existing.ShootBurstCooldown = sbc end
        if goodNum(qsc) and not goodNum(existing.QuickShotCooldown) then existing.QuickShotCooldown = qsc end
        return
    end
    local isp = rawget(info, "InputSpammingEnabled")
    autoWeaponItemCache[item] = {
        Info = info,
        HasInputSpamming = isp ~= nil,
        InputSpamming = type(isp) == "table" and safeClone(isp) or isp,
        ShootCooldown = goodNum(sc) and sc or nil,
        ShootBurstCooldown = goodNum(sbc) and sbc or nil,
        QuickShotCooldown = goodNum(qsc) and qsc or nil,
    }
end

local function applyAutomaticWeapon(item)
    if not item then return end
    storeItemInfoSnapshot(item)
    local snap = autoWeaponItemCache[item]
    local info = snap and snap.Info
    if type(info) ~= "table" then return end
    if AUTO_WEAPON_ENABLED then
        local base = snap.InputSpamming
        local tbl
        if type(base) == "table" then
            tbl = safeClone(base)
        else
            tbl = {}
        end
        tbl.StartShooting = 0
        tbl.StartReloading = 0
        rawset(info, "InputSpammingEnabled", tbl)
    else
        if snap.HasInputSpamming then
            rawset(info, "InputSpammingEnabled", type(snap.InputSpamming) == "table" and safeClone(snap.InputSpamming) or snap.InputSpamming)
        else
            rawset(info, "InputSpammingEnabled", nil)
        end
    end
end

local function weaponSpeedScale()
    if not WEAPON_SPEED_ENABLED then return 1 end
    local boost = math.clamp(tonumber(WEAPON_SPEED_BOOST) or 0, 0, 100)
    if boost <= 0 then return 1 end
    return 1 / (1 + (boost / 100))
end

local function applyWeaponSpeed(item)
    if not item then return end
    storeItemInfoSnapshot(item)
    local snap = autoWeaponItemCache[item]
    local info = snap and snap.Info
    if type(info) ~= "table" then return end
    local scale = weaponSpeedScale()
    if WEAPON_SPEED_ENABLED and scale < 0.999 then
        if type(snap.ShootCooldown) == "number" then
            rawset(info, "ShootCooldown", math.max(0.001, snap.ShootCooldown * scale))
        end
        if type(snap.ShootBurstCooldown) == "number" then
            rawset(info, "ShootBurstCooldown", math.max(0.001, snap.ShootBurstCooldown * scale))
        end
        if type(snap.QuickShotCooldown) == "number" then
            rawset(info, "QuickShotCooldown", math.max(0.001, snap.QuickShotCooldown * scale))
        end
    else
        if type(snap.ShootCooldown) == "number" then rawset(info, "ShootCooldown", snap.ShootCooldown) end
        if type(snap.ShootBurstCooldown) == "number" then rawset(info, "ShootBurstCooldown", snap.ShootBurstCooldown) end
        if type(snap.QuickShotCooldown) == "number" then rawset(info, "QuickShotCooldown", snap.QuickShotCooldown) end
    end
end

local function refreshWeaponMods()
    local item = getEquippedClientItem()
    if not item then return end
    applyAutomaticWeapon(item)
    applyWeaponSpeed(item)
end

local autoWeaponSelectLast = 0

local function forceEquipPreferredWeapon(force)
    if not AUTO_WEAPON_SELECT_ENABLED and not force then return end
    if not AUTO_WEAPON_SELECT_ENABLED then return end
    pcall(function()
        local fc = require(LocalPlayer.PlayerScripts.Controllers.FighterController)
        local lf = fc and fc.LocalFighter
        if not lf or type(lf.Items) ~= "table" then return end
        local function ammoOf(item)
            if not item then return nil end
            local data = rawget(item, "Data")
            if type(data) == "table" then
                local a = rawget(data, "Ammo")
                if type(a) == "number" then return a end
            end
            local ok, a = pcall(function()
                if type(item.Get) == "function" then
                    return item:Get("Ammo") or item:Get("CurrentAmmo")
                end
            end)
            if ok and type(a) == "number" then return a end
            return nil
        end
        local function typeOf(item)
            local t = nil
            pcall(function()
                if type(item.Get) == "function" then t = item:Get("Type") or item:Get("ItemType") end
                t = t or rawget(item, "Type") or (item.Info and item.Info.Type)
            end)
            return tostring(t or ""):lower()
        end
        local function slotAllowed(idx, item)
            local t = typeOf(item)
            if idx == 1 or t:find("primary") then return AUTO_WEAPON_USE_PRIMARY end
            if idx == 2 or t:find("secondary") then return AUTO_WEAPON_USE_SECONDARY end
            if idx == 3 or t:find("melee") or t:find("knife") then return AUTO_WEAPON_USE_MELEE end
            if t:find("gun") then return AUTO_WEAPON_USE_PRIMARY or AUTO_WEAPON_USE_SECONDARY end
            return AUTO_WEAPON_USE_PRIMARY
        end
        -- prefer: primary with ammo > secondary with ammo > melee
        local candidates = {}
        for idx, item in pairs(lf.Items) do
            if type(idx) == "number" and item and slotAllowed(idx, item) then
                local ammo = ammoOf(item)
                local t = typeOf(item)
                local isMelee = t:find("melee") or t:find("knife")
                local score = idx
                if isMelee then score = score + 100 end
                if type(ammo) == "number" and ammo <= 0 and not isMelee then
                    score = score + 1000
                end
                candidates[#candidates+1] = { idx = idx, score = score, item = item }
            end
        end
        table.sort(candidates, function(a, b) return a.score < b.score end)
        if candidates[1] and type(lf.EquipItem) == "function" then
            pcall(function() lf:EquipItem(candidates[1].idx) end)
        end
    end)
end
getgenv().ForceEquipPreferredWeapon = forceEquipPreferredWeapon

local function tryAutoWeaponSelect()
    if not AUTO_WEAPON_SELECT_ENABLED then return end
    local now = tick()
    if now - autoWeaponSelectLast < 0.2 then return end
    autoWeaponSelectLast = now
    pcall(function()
        local fc = require(LocalPlayer.PlayerScripts.Controllers.FighterController)
        local lf = fc and fc.LocalFighter
        if not lf then return end
        local equipped = lf.EquippedItem
        local need = false
        if not equipped then
            need = true
        else
            local data = rawget(equipped, "Data")
            local ammo = data and rawget(data, "Ammo")
            if type(ammo) ~= "number" then
                pcall(function()
                    if type(equipped.Get) == "function" then
                        ammo = equipped:Get("Ammo") or equipped:Get("CurrentAmmo")
                    end
                end)
            end
            if type(ammo) == "number" and ammo <= 0 then
                need = true
            end
        end
        if need then
            forceEquipPreferredWeapon(true)
        end
    end)
end

-- match start / respawn: auto equip preferred weapon
task.spawn(function()
    local lastStatus = nil
    while true do
        task.wait(0.5)
        if not AUTO_WEAPON_SELECT_ENABLED then continue end
        local status = nil
        pcall(function() status = workspace:GetAttribute("MatchmadeStatus") end)
        if status == "Started" and lastStatus ~= "Started" then
            task.delay(0.8, function()
                forceEquipPreferredWeapon(true)
            end)
            task.delay(2.0, function()
                forceEquipPreferredWeapon(true)
            end)
        end
        lastStatus = status
    end
end)
pcall(function()
    LocalPlayer.CharacterAdded:Connect(function()
        if not AUTO_WEAPON_SELECT_ENABLED then return end
        task.delay(1.0, function() forceEquipPreferredWeapon(true) end)
        task.delay(2.5, function() forceEquipPreferredWeapon(true) end)
    end)
end)

RunService.Heartbeat:Connect(function()
    pcall(refreshWeaponMods)
    pcall(tryAutoWeaponSelect)
end)
task.defer(function()
    local function applyMeshWrapping()
        local VM = workspace:FindFirstChild("ViewModels")
        local FP = VM and VM:FindFirstChild("FirstPerson")
        if not FP then return false end
        for _, o in ipairs(FP:GetDescendants()) do
            if o:IsA("BasePart") then
                o.Material = Enum.Material.ForceField
                o.Color = Color3.new(0, 0, 0)
                for _, f in ipairs({
                    Enum.NormalId.Top, Enum.NormalId.Bottom,
                    Enum.NormalId.Left, Enum.NormalId.Right,
                    Enum.NormalId.Front, Enum.NormalId.Back
                }) do
                    local texName = "FixedTexture_" .. tostring(f.Name)
                    local t = o:FindFirstChild(texName)
                    if not t then
                        t = Instance.new("Texture")
                        t.Name = texName
                        t.Parent = o
                    end
                    t.Texture = "rbxassetid://135989547473439"
                    t.Face = f
                    t.Color3 = Color3.new(0, 0, 0)
                    t.StudsPerTileU = 0.1
                    t.StudsPerTileV = 0.1
                end
            end
        end
        return true
    end
    getgenv().applyMeshWrapping = applyMeshWrapping
end)

function applyMeshWrapping(...)
    local f = getgenv().applyMeshWrapping
    if type(f) == "function" then return f(...) end
    return false
end
local spinbotMotors = {}
local spinbotTwists = {}
local spinbotAngle = 0
local spinbotLastTwist = 0
local spinbotTwistInterval = 2
local spinbotCharConn = nil

function resetJoints()
    for motor, originalC0 in pairs(originalC0s) do
        if motor and motor.Parent then
            pcall(function() motor.C0 = originalC0 end)
        end
    end
    table.clear(originalC0s)
    table.clear(spinbotTwists)
end

local function spinbotCacheMotors(character)
    table.clear(spinbotMotors)
    table.clear(spinbotTwists)
    if not character then return end
    for _, desc in ipairs(character:GetDescendants()) do
        if desc:IsA("Motor6D") then
            spinbotMotors[#spinbotMotors + 1] = desc
            if not originalC0s[desc] then
                originalC0s[desc] = desc.C0
            end
        end
    end
end

local function spinbotRandomTwists()
    for i = 1, #spinbotMotors do
        local m = spinbotMotors[i]
        if m and m.Parent then
            if not originalC0s[m] then originalC0s[m] = m.C0 end
            local rx = math.rad(math.random(-170, 170))
            local ry = math.rad(math.random(-170, 170))
            local rz = math.rad(math.random(-170, 170))
            spinbotTwists[m] = CFrame.Angles(rx, ry, rz)
        end
    end
end

local function spinbotApplyTwists()
    for m, off in pairs(spinbotTwists) do
        if m and m.Parent and originalC0s[m] then
            pcall(function() m.C0 = originalC0s[m] * off end)
        end
    end
end

function setSpinbot(on)
    isSpinning = on and true or false
    if not isSpinning then
        resetJoints()
        local char = LocalPlayer.Character
        local hum = char and char:FindFirstChildOfClass("Humanoid")
        if hum then pcall(function() hum.AutoRotate = true end) end
        return
    end
    local char = LocalPlayer.Character
    if char then
        spinbotCacheMotors(char)
        spinbotRandomTwists()
        spinbotLastTwist = tick()
        local hum = char:FindFirstChildOfClass("Humanoid")
        if hum then pcall(function() hum.AutoRotate = false end) end
    end
end
getgenv().SetSpinbot = setSpinbot
pcall(function()
    LocalPlayer.CharacterAdded:Connect(function(char)
        task.wait(0.4)
        if isSpinning then
            spinbotCacheMotors(char)
            spinbotRandomTwists()
            spinbotLastTwist = tick()
            local hum = char:FindFirstChildOfClass("Humanoid")
            if hum then pcall(function() hum.AutoRotate = false end) end
        end
    end)
end)
RunService.Heartbeat:Connect(function(dt)
    if not isSpinning then return end
    local character = LocalPlayer.Character
    if not character then return end
    local hrp = character:FindFirstChild("HumanoidRootPart")
    if not hrp then return end
    local spd = tonumber(rotationSpeed) or 20
    spinbotAngle = spinbotAngle + math.rad(spd * 36 * dt)
    local desyncOn = false
    pcall(function()
        desyncOn = DesyncEngine and DesyncEngine.active
    end)
    if not desyncOn then
        local pos = hrp.Position
        pcall(function()
            hrp.CFrame = CFrame.new(pos) * CFrame.Angles(0, spinbotAngle, 0)
        end)
    end
    local now = tick()
    if (now - spinbotLastTwist) >= spinbotTwistInterval then
        spinbotLastTwist = now
        if #spinbotMotors == 0 then spinbotCacheMotors(character) end
        spinbotRandomTwists()
    end
    spinbotApplyTwists()
end)
task.defer(function()
    local function attemptJoinMatch()
        if not AUTO_MATCH_ENABLED then return end
        pcall(function()
            local args = { AUTO_MATCH_MODE }
            local remotes = ReplicatedStorage:FindFirstChild("Remotes")
            if not remotes then return end
            local mm = remotes:FindFirstChild("Matchmaking")
            if not mm then return end
            local jq = mm:FindFirstChild("JoinQueue")
            if jq then
                jq:InvokeServer(unpack(args))
            end
        end)
    end
    getgenv().attemptJoinMatch = attemptJoinMatch
    task.spawn(function()
        while task.wait(1) do
            if AUTO_MATCH_ENABLED then
                pcall(attemptJoinMatch)
            end
        end
    end)
end)
function attemptJoinMatch(...)
    local f = getgenv().attemptJoinMatch
    if type(f) == "function" then return f(...) end
end
task.defer(function()
    local underground_enabled = false
    local underground_oldpos = nil
    getgenv().InstanceUndergroundEnabled = false

    local camera_controller = nil
    pcall(function()
        local ctrls = LocalPlayer.PlayerScripts:FindFirstChild("Controllers")
        if ctrls then
            camera_controller = instanceSafeRequire(ctrls:FindFirstChild("CameraController"))
        end
    end)

    local function getFloorBelowPosition(pos)
        local rayDirection = Vector3.new(0, -500, 0)
        local raycastParams = RaycastParams.new()
        raycastParams.FilterType = Enum.RaycastFilterType.Exclude
        local lf = local_fighter
        if lf and lf.Entity and lf.Entity.RootPart then
            raycastParams.FilterDescendantsInstances = { lf.Entity.RootPart.Parent }
        elseif LocalPlayer.Character then
            raycastParams.FilterDescendantsInstances = { LocalPlayer.Character }
        end
        local result = workspace:Raycast(pos, rayDirection, raycastParams)
        if result then
            return CFrame.new(Vector3.new(pos.X, result.Position.Y - 2, pos.Z))
        end
        return nil
    end
    getgenv()._getFloorBelowPosition = getFloorBelowPosition

    if camera_controller and camera_controller.Update then
        local old_underground_camera_controller = camera_controller.Update
        camera_controller.Update = function(...)
            local arguments = { ... }
            if underground_enabled and local_fighter and local_fighter.Entity and local_fighter.Entity.RootPart and underground_oldpos then
                local_fighter.Entity.RootPart.CFrame = underground_oldpos
            end
            return old_underground_camera_controller(table.unpack(arguments))
        end
    end

    RunService.Heartbeat:Connect(function()
        if getgenv().InstanceConfigLoading then return end
        if not underground_enabled then
            underground_oldpos = nil
            return
        end
        local curweap = nil
        pcall(function() curweap = curweap2() end)
        if not curweap then
            underground_oldpos = nil
            return
        end
        if local_fighter and local_fighter.Entity and local_fighter.Entity.RootPart then
            underground_oldpos = local_fighter.Entity.RootPart.CFrame
            local currentPos = local_fighter.Entity.RootPart.Position
            local floorCFrame = getFloorBelowPosition(currentPos)
            if floorCFrame then
                local_fighter.Entity.RootPart.CFrame = floorCFrame
            end
        end
    end)

    local function flushAntiAimMovementState()
        pcall(function()
            if local_fighter and local_fighter.Entity and local_fighter.Entity.RootPart and underground_oldpos then
            end
        end)
    end
    getgenv().flushAntiAimMovementState = flushAntiAimMovementState
    local function updantiaim()
        if not settings then return end
        settings.enabled = settings.enabled or false
        pcall(function()
            if Toggles and Toggles.AntiAimUnderground then
                underground_enabled = Toggles.AntiAimUnderground.Value == true
                getgenv().InstanceUndergroundEnabled = underground_enabled
                if not underground_enabled then underground_oldpos = nil end
            end
        end)
        pcall(function()
            if Options and Options.AntiAimYaw then
                settings.yawtype = Options.AntiAimYaw.Value or "none"
            end
            if Options and Options.AntiAimPitch then
                settings.pitchtype = Options.AntiAimPitch.Value or "none"
            end
            if Options and Options.AntiAimAngle then
                settings.angletype = Options.AntiAimAngle.Value or "none"
            end
        end)
        if not settings.enabled or (settings.yawtype == "none" and settings.pitchtype == "none" and settings.angletype == "none") then
            flushAntiAimMovementState()
            underground_oldpos = nil
        end
    end
    getgenv().updantiaim = updantiaim

    pcall(function()
        LocalPlayer.CharacterAdded:Connect(function()
            task.defer(flushAntiAimMovementState)
        end)
    end)

    getgenv().InstanceSetUnderground = function(val)
        underground_enabled = val and true or false
        getgenv().InstanceUndergroundEnabled = underground_enabled
        if not underground_enabled then
            underground_oldpos = nil
        end
    end
    getgenv()._underground_oldpos_ref = function()
        return underground_oldpos
    end
    getgenv()._underground_oldpos_set = function(cf)
        underground_oldpos = cf
    end
end)
getgenv().InstanceSetUnderground = getgenv().InstanceSetUnderground or function(val)
    getgenv().InstanceUndergroundEnabled = val and true or false
end
do
    local ORIGINAL_FALLEN = nil
    local safeCF = nil

    local function applyFallenHeight(enabled)
        pcall(function()
            if enabled then
                if ORIGINAL_FALLEN == nil then
                    ORIGINAL_FALLEN = workspace.FallenPartsDestroyHeight
                end
                workspace.FallenPartsDestroyHeight = 0 / 0
            else
                if ORIGINAL_FALLEN ~= nil then
                    workspace.FallenPartsDestroyHeight = ORIGINAL_FALLEN
                else
                    workspace.FallenPartsDestroyHeight = -500
                end
            end
        end)
    end
    task.spawn(function()
        local was = false
        while true do
            local on = getgenv().InstanceUndergroundEnabled == true
            if on ~= was then
                applyFallenHeight(on)
                was = on
            elseif on then
                pcall(function()
                    local h = workspace.FallenPartsDestroyHeight
                    if h == h then
                        workspace.FallenPartsDestroyHeight = 0 / 0
                    end
                end)
            end
            task.wait(0.5)
        end
    end)

    pcall(function()
        RunService:UnbindFromRenderStep("AntiVoid_Guard")
        RunService:BindToRenderStep("AntiVoid_Guard", Enum.RenderPriority.Character.Value, function()
            if not getgenv().InstanceUndergroundEnabled then return end
            local char = LocalPlayer.Character
            if not char then return end
            local hrp = char:FindFirstChild("HumanoidRootPart")
            local hum = char:FindFirstChildOfClass("Humanoid")
            if not hrp or not hum or hum.Health <= 0 then return end

            local y = hrp.Position.Y
            if y > 2 and hum.FloorMaterial ~= Enum.Material.Air then
                safeCF = hrp.CFrame
                if getgenv()._underground_oldpos_set then
                    getgenv()._underground_oldpos_set(safeCF)
                end
            elseif y > 8 then
                safeCF = hrp.CFrame
                if getgenv()._underground_oldpos_set then
                    getgenv()._underground_oldpos_set(safeCF)
                end
            end

            local killY = -20
            pcall(function()
                local fh = workspace.FallenPartsDestroyHeight
                if fh == fh then
                    killY = math.max(killY, fh + 8)
                end
            end)
            if y < killY then
                local ref = (getgenv()._underground_oldpos_ref and getgenv()._underground_oldpos_ref()) or safeCF
                local sx, sy, sz
                if ref then
                    sx = ref.Position.X
                    sy = math.max(ref.Position.Y, 12)
                    sz = ref.Position.Z
                else
                    sx, sy, sz = hrp.Position.X, 25, hrp.Position.Z
                end
                pcall(function()
                    hrp.CFrame = CFrame.new(sx, sy, sz)
                    hrp.AssemblyLinearVelocity = Vector3.zero
                    hrp.AssemblyAngularVelocity = Vector3.zero
                end)
                pcall(function()
                    local st = hum:GetState()
                    if st == Enum.HumanoidStateType.Freefall
                        or st == Enum.HumanoidStateType.FallingDown
                        or st == Enum.HumanoidStateType.Physics then
                        hum:ChangeState(Enum.HumanoidStateType.GettingUp)
                    end
                end)
                if hum.Health > 0 and hum.Health < hum.MaxHealth * 0.2 then
                    pcall(function()
                        hum.Health = math.max(hum.Health, hum.MaxHealth * 0.35)
                    end)
                end
            end
        end)
    end)
    local prevSet = getgenv().InstanceSetUnderground
    getgenv().InstanceSetUnderground = function(val)
        if type(prevSet) == "function" then pcall(prevSet, val) end
        getgenv().InstanceUndergroundEnabled = val and true or false
        applyFallenHeight(getgenv().InstanceUndergroundEnabled)
    end
end

runservice.Heartbeat:Connect(function() local f = getgenv().updantiaim if f then pcall(f) end end)
task.defer(function()
    _G.Features = _G.Features or {}
    _G.Features.DeviceSpoof = _G.Features.DeviceSpoof or {
        Enabled = false,
        CurrentDevice = "Console",
        LastApplied = 0
    }
    _G.Features.SlideBoost = _G.Features.SlideBoost or {
        Enabled = false,
        Speed = 300
    }

    local devicecfgs = {
        ["Mobile"] = { Display = "Mobile", Code = "Touch" },
        ["Console"] = { Display = "Console", Code = "Gamepad" },
        ["VR"] = { Display = "VR", Code = "VR" },
        ["PC"] = { Display = "PC", Code = "MouseKeyboard" }
    }

    local function applydevice()
        _G.Features = _G.Features or {}
        _G.Features.DeviceSpoof = _G.Features.DeviceSpoof or { Enabled = false, CurrentDevice = "Mobile", LastApplied = 0 }
        if not _G.Features.DeviceSpoof.Enabled then return end
        local device = _G.Features.DeviceSpoof.CurrentDevice or "Mobile"
        local devicecfg = devicecfgs[device]
        if not devicecfg then return end
        _G.Features.DeviceSpoof.LastApplied = tick()
        pcall(function()
            local path = ReplicatedStorage:FindFirstChild("Remotes")
            path = path and path:FindFirstChild("Replication")
            path = path and path:FindFirstChild("Fighter")
            local sc = path and path:FindFirstChild("SetControls")
            if sc then
                sc:FireServer(devicecfg.Code)
            end
        end)
        -- 속성/입력 타입도 맞춤
        pcall(function()
            LocalPlayer:SetAttribute("Platform", devicecfg.Display)
            LocalPlayer:SetAttribute("Device", devicecfg.Display)
            LocalPlayer:SetAttribute("InputType", devicecfg.Code)
        end)
    end
    getgenv().applydevice = applydevice

    -- Device Spoof 지속 적용
    task.spawn(function()
        while true do
            pcall(function()
                if _G.Features and _G.Features.DeviceSpoof and _G.Features.DeviceSpoof.Enabled then
                    applydevice()
                end
            end)
            task.wait(2)
        end
    end)

    task.spawn(function()
        local RS = game:GetService("RunService")
        local LP = game:GetService("Players").LocalPlayer
        local mech
        while true do
            local ok, result = pcall(function()
                return require(LP.PlayerScripts.Controllers.MechanicsController)
            end)
            if ok then mech = result break end
            task.wait(1)
        end
        local connection = RS.RenderStepped:Connect(function()
            if _G.Features and _G.Features.SlideBoost and _G.Features.SlideBoost.Enabled and mech and mech.IsSliding then
                local success = pcall(function()
                    mech._sliding_velocity.Velocity = mech._sliding_velocity.Velocity.Unit * _G.Features.SlideBoost.Speed
                end)
                if not success then
                    local newOk, newMech = pcall(function()
                        return require(LP.PlayerScripts.Controllers.MechanicsController)
                    end)
                    if newOk then mech = newMech end
                end
            end
        end)
        game:GetService("Players").PlayerRemoving:Connect(function(player)
            if player == LP then pcall(function() connection:Disconnect() end) end
        end)
    end)

    LocalPlayer.CharacterAdded:Connect(function()
        task.wait(1)
        if _G.Features.DeviceSpoof.Enabled then
            task.wait(0.5)
            applydevice()
        end
    end)

    task.spawn(function()
        game:GetService("ReplicatedStorage"):WaitForChild("Remotes", 10)
        task.wait(2)
        if _G.Features.DeviceSpoof.Enabled then
            applydevice()
        end
    end)
end)
function applydevice()
    local f = getgenv().applydevice
    if type(f) == "function" then return f() end
end

function buildHubUI()
CombatCol = Library:CreateColumn("전투유틸")

CombatCol:AddSwitch({
    Name = "Silent Aim (사이런트 에임)",
    Default = false,
    Callback = function(Value)
        SILENT_AIM_ENABLED = Value and true or false
        if not SILENT_AIM_ENABLED then
        end
        createNotification(Value and "Silent Aim ON" or "Silent Aim OFF")
        updateKeybindsList()
    end
})

CombatCol:AddSwitch({
    Name = "Aimbot (에임봇)",
    Default = false,
    Callback = function(Value)
        AIMBOT_ENABLED = Value and true or false
        if AIMBOT_ENABLED then startAimbot() else stopAimbot() end
        createNotification(AIMBOT_ENABLED and "Aimbot ON" or "Aimbot OFF")
        updateKeybindsList()
    end
})
getgenv().AimbotKeyBindBtn = CombatCol:AddButton("Aimbot 키: 없음 (자동)", function(btn)
    AIMBOT_KEY_LISTENING = true
    if btn then btn.Text = "Aimbot 키: 입력 대기중..." end
    createNotification("키보드 또는 마우스 버튼을 누르세요")
end)
CombatCol:AddButton("Aimbot 키 리셋 (가까운 적 자동)", function()
    AIMBOT_KEY = nil
    AIMBOT_KEY_LISTENING = false
    aimbotLockedRef = nil
    aimbotKeyHeld = false
    if getgenv().updateAimbotKeyButton then getgenv().updateAimbotKeyButton() end
    createNotification("Aimbot 키 해제 → 화면 가까운 적 자동 조준")
end)

CombatCol:AddSwitch({
    Name = "Legit Aimbot (레짓 에임봇)",
    Default = false,
    Callback = function(Value)
        LEGIT_AIMBOT_ENABLED = Value and true or false
        if LEGIT_AIMBOT_ENABLED then
            pcall(startLegitAimbot)
            createNotification("Legit ON (키 = Aimbot 키 공유)")
        else
            pcall(stopLegitAimbot)
            createNotification("Legit Aimbot OFF")
        end
        updateKeybindsList()
    end
})
CombatCol:AddSlider({
    Name = "Legit 에임 속도",
    Min = 1, Max = 100, Default = 55, Suffix = "%",
    Callback = function(Value)
        LEGIT_AIMBOT_SMOOTH = math.clamp(tonumber(Value) or 55, 1, 100)
    end
})
CombatCol:AddSlider({
    Name = "Aimbot Speed (에임 속도)",
    Min = 5,
    Max = 100,
    Default = 35,
    Suffix = "",
    Callback = function(Value)
        AIMBOT_SMOOTH = math.clamp(tonumber(Value) or 35, 5, 100)
    end
})

CombatCol:AddDropdown({
    Name = "Aim Target (에임 타겟)",
    Options = {"Head", "Body", "Random"},
    Default = "Head",
    Callback = function(Options)
        local v = Options
        if type(Options) == "table" then
            v = Options[1] or Options.Value or Options.Selected or "Head"
        end
        AIM_TARGET_MODE = tostring(v or "Head"):lower()
        createNotification("에임 타겟: " .. tostring(v))
    end
})

CombatCol:AddSwitch({
    Name = "No Recoil (반동 없애기)",
    Default = false,
    Callback = function(Value)
        NO_RECOIL_ENABLED = Value and true or false
        if NO_RECOIL_ENABLED then
            pcall(enableNoRecoil)
        else
            pcall(disableNoRecoil)
        end
        createNotification(NO_RECOIL_ENABLED and "No Recoil ON" or "No Recoil OFF")
        updateKeybindsList()
    end
})
CombatCol:AddSlider({
    Name = "No Recoil Strength (%)",
    Min = 0, Max = 100, Default = 100, Suffix = "%",
    Callback = function(Value)
        NO_RECOIL_STRENGTH = math.clamp(tonumber(Value) or 100, 0, 100)
        if NO_RECOIL_ENABLED then pcall(enableNoRecoil) end
    end
})

CombatCol:AddSwitch({
    Name = "Automatic Weapon (단발→연사)",
    Default = false,
    Callback = function(Value)
        AUTO_WEAPON_ENABLED = Value and true or false
        pcall(refreshWeaponMods)
        createNotification(AUTO_WEAPON_ENABLED and "Automatic Weapon ON" or "Automatic Weapon OFF")
        updateKeybindsList()
    end
})

CombatCol:AddSwitch({
    Name = "Weapon Attack Speed (공격속도)",
    Default = false,
    Callback = function(Value)
        WEAPON_SPEED_ENABLED = Value and true or false
        pcall(refreshWeaponMods)
        createNotification(WEAPON_SPEED_ENABLED and "Attack Speed ON" or "Attack Speed OFF")
        updateKeybindsList()
    end
})

CombatCol:AddSlider({
    Name = "Attack Speed Boost (%)",
    Min = 0, Max = 100, Default = 0, Suffix = "%",
    Callback = function(Value)
        WEAPON_SPEED_BOOST = math.clamp(tonumber(Value) or 0, 0, 100)
        pcall(refreshWeaponMods)
    end
})

CombatCol:AddSlider({
    Name = "총기 연사속도 증가율 (%)",
    Min = 0, Max = 100, Default = 0, Suffix = "%",
    Callback = function(Value)
        Value = math.clamp(math.floor(tonumber(Value) or 0), 0, 100)
        local weaponDataCache = nil
        local modulesFolder = ReplicatedStorage:FindFirstChild("Modules")
        if modulesFolder then
            for _, name in ipairs({"ItemLibrary", "WeaponStats", "Items", "WeaponData", "Weapons"}) do
                local found = modulesFolder:FindFirstChild(name)
                if found then
                    local ok, mod = pcall(require, found)
                    if ok and type(mod) == "table" and type(mod.Items) == "table" then
                        weaponDataCache = mod
                        break
                    end
                end
            end
        end
        if not weaponDataCache then
            pcall(function()
                local mod = require(ReplicatedStorage.Modules.ItemLibrary)
                if type(mod) == "table" and type(mod.Items) == "table" then
                    weaponDataCache = mod
                end
            end)
        end
        if not (weaponDataCache and weaponDataCache.Items) then
            createNotification("무기 데이터를 찾을 수 없습니다")
            return
        end
        local keys = {
            "ShootCooldown", "ShootBurstCooldown", "AttackCooldown",
            "HeavyAttackCooldown", "Cooldown", "DeflectCooldown",
            "DashCooldown", "BuildCooldown", "SpinCooldown",
            "AirblastCooldown", "QuickShotCooldown", "TransitionCooldown", "ReloadTime",
            "ReloadLength", "EmptyReloadLength"
        }
        for itemName, stats in pairs(weaponDataCache.Items) do
            if type(stats) ~= "table" then continue end
            if not originalData[itemName] then
                originalData[itemName] = {}
            end
            for _, key in ipairs(keys) do
                local cur = stats[key]
                if type(cur) ~= "number" then continue end
                local prev = originalData[itemName][key]
                if prev == nil and cur > 0.05 then
                    originalData[itemName][key] = cur
                elseif type(prev) == "number" and prev <= 0.05 and cur > 0.05 then
                    originalData[itemName][key] = cur
                end
            end
        end
        local multiplier = (100 - Value) / 100
        local patched = 0
        for itemName, stats in pairs(weaponDataCache.Items) do
            if type(stats) ~= "table" or not originalData[itemName] then continue end
            for _, key in ipairs(keys) do
                local originalVal = originalData[itemName][key]
                if type(originalVal) == "number" then
                    if Value <= 0 then
                        stats[key] = originalVal
                    elseif Value >= 100 then
                        stats[key] = (key == "ReloadTime" or tostring(key):find("Reload")) and 0.01 or 0.00001
                    else
                        stats[key] = math.max(originalVal * multiplier, 0.00001)
                    end
                    patched = patched + 1
                end
            end
        end
        pcall(function()
            local fc = require(LocalPlayer.PlayerScripts.Controllers.FighterController)
            local item = fc and fc.LocalFighter and fc.LocalFighter.EquippedItem
            local info = item and item.Info
            if type(info) ~= "table" then return end
            local n = item.Name
            local od = n and originalData[n]
            for _, key in ipairs({"ShootCooldown", "ShootBurstCooldown", "QuickShotCooldown", "AttackCooldown", "Cooldown", "ReloadTime", "ReloadLength"}) do
                local base = od and od[key]
                if type(base) == "number" then
                    if Value <= 0 then
                        info[key] = base
                    elseif Value >= 100 then
                        info[key] = 0.00001
                    else
                        info[key] = math.max(base * multiplier, 0.00001)
                    end
                end
            end
            if autoWeaponItemCache then
                table.clear(autoWeaponItemCache)
            end
        end)
        createNotification("연사 " .. Value .. "% 적용 (무기 재장착 권장) [" .. patched .. "]")
    end
})

CombatCol:AddSwitch({
    Name = "Device Spoofer (기기 스푸퍼)",
    Default = false,
    Callback = function(Value)
        if not _G.Features then _G.Features = {} end
        if not _G.Features.DeviceSpoof then _G.Features.DeviceSpoof = { Enabled = false, CurrentDevice = "Mobile" } end
        _G.Features.DeviceSpoof.Enabled = Value
        if Value and applydevice then pcall(applydevice) end
        createNotification(Value and "Device Spoof ON" or "Device Spoof OFF")
        updateKeybindsList()
    end
})

CombatCol:AddDropdown({
    Name = "Device 종류",
    Options = {"Mobile", "Console", "VR", "PC"},
    Default = "Mobile",
    Callback = function(Options)
        local val = type(Options) == "table" and Options[1] or Options
        if not _G.Features then _G.Features = {} end
        if not _G.Features.DeviceSpoof then _G.Features.DeviceSpoof = {} end
        _G.Features.DeviceSpoof.CurrentDevice = val
        if _G.Features.DeviceSpoof.Enabled and applydevice then pcall(applydevice) end
        createNotification("Device: " .. tostring(val))
    end
})

CombatCol:AddSwitch({
    Name = "Level Spoof (레벨 스푸퍼)",
    Default = false,
    Callback = function(Value)
        local LE = getgenv().LunaraExtras
        if LE and LE.setLevelSpoof then LE.setLevelSpoof(Value, nil) end
        createNotification(Value and "Level Spoof ON" or "Level Spoof OFF")
        updateKeybindsList()
    end
})

CombatCol:AddSlider({
    Name = "Level 값",
    Min = 1, Max = 9999, Default = 9999, Suffix = " Lv",
    Callback = function(Value)
        local LE = getgenv().LunaraExtras
        if LE and LE.setLevelSpoof then
            local on = LE.config and LE.config.levelSpoof and LE.config.levelSpoof.enabled
            LE.setLevelSpoof(on, Value)
        end
    end
})

CombatCol:AddSwitch({
    Name = "Win Streak Spoof (연승 스푸퍼)",
    Default = false,
    Callback = function(Value)
        local LE = getgenv().LunaraExtras
        if LE and LE.setWinStreakSpoof then LE.setWinStreakSpoof(Value, nil) end
        createNotification(Value and "Win Streak Spoof ON" or "Win Streak Spoof OFF")
        updateKeybindsList()
    end
})

CombatCol:AddSlider({
    Name = "연승 값",
    Min = 1, Max = 9999, Default = 9999, Suffix = " 연승",
    Callback = function(Value)
        local LE = getgenv().LunaraExtras
        if LE and LE.setWinStreakSpoof then
            local on = LE.config and LE.config.winStreakSpoof and LE.config.winStreakSpoof.enabled
            LE.setWinStreakSpoof(on, Value)
        end
    end
})

CombatCol:AddSwitch({
    Name = "Bullet Track (총알 궤적)",
    Default = false,
    Callback = function(Value)
        TRACER_ENABLED = Value
        local R = getgenv().RageBot4
        if R and R.setTracer then R.setTracer(Value) end
        createNotification(Value and "Tracer ON" or "Tracer OFF")
        updateKeybindsList()
    end
})

CombatCol:AddSwitch({
    Name = "Anti Katana (안티 카타나)",
    Default = true,
    Callback = function(Value)
        local LE = getgenv().LunaraExtras
        local R = getgenv().RageBot4
        if LE and LE.setAntiKatana then LE.setAntiKatana(Value) end
        if R and R.setAntiKatana then R.setAntiKatana(Value) end
        if getgenv().AntiKatana then getgenv().AntiKatana.Enabled = Value end
        createNotification(Value and "Anti Katana ON" or "Anti Katana OFF")
        updateKeybindsList()
    end
})

CombatCol:AddSwitch({
    Name = "Hit Notification (히트 알림)",
    Default = false,
    Callback = function(Value)
        local M = getgenv().MiscExtras
        local LE = getgenv().LunaraExtras
        if M and M.setHitNotif then M.setHitNotif(Value) end
        if LE and LE.setHitNotif then LE.setHitNotif(Value) end
        createNotification(Value and "Hit Notification ON" or "Hit Notification OFF")
        updateKeybindsList()
    end
})

CombatCol:AddSwitch({
    Name = "Hit Sound (히트 사운드)",
    Default = false,
    Callback = function(Value)
        local M = getgenv().MiscExtras
        if M and M.setHitSound then M.setHitSound(Value) end
        createNotification(Value and "Hit Sound ON" or "Hit Sound OFF")
        updateKeybindsList()
    end
})

CombatCol:AddDropdown({
    Name = "Hit Sound 종류",
    Options = {"Rust HS","Neverlose","sparkle","Minecraft Hit","Bonk","Osu","Among Us","Bruh","Vine","Gamesense"},
    Default = "Rust HS",
    Callback = function(Options)
        local M = getgenv().MiscExtras
        local v = type(Options) == "table" and Options[1] or Options
        if M and M.setHitSoundStyle then M.setHitSoundStyle(v) end
    end
})

-- Ragebot center HUD
local ragebotHudGui = nil
local ragebotHudTarget = nil
local ragebotHudAmmo = nil
local ragebotHudConn = nil

local function resolveTargetDisplayName(t)
    if not t then return nil end
    if typeof(t) == "Instance" then
        if t:IsA("Player") then
            return t.DisplayName ~= "" and t.DisplayName or t.Name
        end
        if t:IsA("Model") then
            local plr = Players:GetPlayerFromCharacter(t)
            if plr then
                return (plr.DisplayName and plr.DisplayName ~= "" and plr.DisplayName) or plr.Name
            end
            return t.Name
        end
        if t:IsA("BasePart") then
            local model = t:FindFirstAncestorOfClass("Model")
            if model then return resolveTargetDisplayName(model) end
        end
    end
    if type(t) == "string" and t ~= "" then return t end
    return nil
end

local function isLocalPlayerDead()
    local char = LocalPlayer.Character
    if not char then return true end
    local hum = char:FindFirstChildOfClass("Humanoid")
    if not hum then return true end
    if hum.Health <= 0 then return true end
    if hum:GetState() == Enum.HumanoidStateType.Dead then return true end
    return false
end

local function isHudVoidActive()
    -- only true during actual void-spam HIDE phase (not stuck position)
    local LE = getgenv().LunaraExtras
    local vs = LE and LE.config and LE.config.voidspam
    if vs and vs.enabled and tostring(vs.phase) == "hide" then
        return true
    end
    if getgenv().VOID_SPAM_HIDING == true then
        return true
    end
    if getgenv().RB4_VOID_PHASE == "hide" or getgenv().RB4_VOID_HIDING == true then
        return true
    end
    local R = getgenv().RageBot4
    if R and rawget(R, "VoidPhase") == "hide" then
        return true
    end
    return false
end

local function getHudRageTarget()
    local t = getgenv().RAGEBOT_ACTIVE_TARGET
    if not t then t = rb1CurrentTarget end
    if not t then t = rb1Target end
    if not t then
        local R = getgenv().RageBot4
        if R then
            t = rawget(R, "LockedChar") or rawget(R, "LastTarget") or rawget(R, "Target")
        end
    end
    if not t and OrbitBot then
        t = OrbitBot.CurrentTarget or OrbitBot.Target or OrbitBot.LastTarget
    end
    return t
end

local function isHudMovedToTarget(t)
    if not t then return false end
    -- actively TPing / desyncing toward target
    if rbEnabled and rb1Desync and rb1CurrentTarget then return true end
    if rb4Enabled then
        local R = getgenv().RageBot4
        if R and (rawget(R, "LockedChar") or rawget(R, "LastTarget")) then
            return true
        end
        return false
    end
    if OrbitCFG and OrbitCFG.Active and OrbitBot and (OrbitBot.CurrentTarget or OrbitBot.Target) then
        return true
    end
    if getgenv().RAGEBOT_ACTIVE_TARGET then return true end
    return false
end

-- void... / nickname... / nil
local function getRagebotHudStatusText()
    -- dead -> nil
    if isLocalPlayerDead() then
        return "nil"
    end
    if isHudVoidActive() then
        return "void..."
    end
    local t = getHudRageTarget()
    if isHudMovedToTarget(t) then
        local name = resolveTargetDisplayName(t)
        if name and name ~= "" then
            return name .. "..."
        end
        return "nil"
    end
    return "nil"
end

local function getLocalAmmoCount()
    local ammo = nil
    pcall(function()
        local fc = require(LocalPlayer.PlayerScripts.Controllers.FighterController)
        local lf = fc and fc.LocalFighter
        local item = lf and lf.EquippedItem
        if not item then return end
        if type(item.Get) == "function" then
            ammo = item:Get("Ammo") or item:Get("CurrentAmmo") or item:Get("MagazineAmmo")
        end
        if ammo == nil then
            local data = rawget(item, "Data") or rawget(item, "Info")
            if type(data) == "table" then
                ammo = data.Ammo or data.CurrentAmmo or data.MagazineAmmo
            end
        end
        if ammo == nil then
            ammo = rawget(item, "Ammo") or rawget(item, "CurrentAmmo")
        end
    end)
    if type(ammo) == "number" then
        return math.floor(ammo)
    end
    return nil
end

local function destroyRagebotHud()
    if ragebotHudConn then
        pcall(function() ragebotHudConn:Disconnect() end)
        ragebotHudConn = nil
    end
    if ragebotHudGui then
        pcall(function() ragebotHudGui:Destroy() end)
        ragebotHudGui = nil
        ragebotHudTarget = nil
        ragebotHudAmmo = nil
    end
end

local function ensureRagebotHud()
    if ragebotHudGui and ragebotHudGui.Parent then return end
    destroyRagebotHud()
    local pg = LocalPlayer:FindFirstChild("PlayerGui") or playerGui
    local gui = Instance.new("ScreenGui")
    gui.Name = "RagebotCenterHUD"
    gui.ResetOnSpawn = false
    gui.IgnoreGuiInset = true
    gui.DisplayOrder = 1000000
    gui.Parent = pg

    local targetLbl = Instance.new("TextLabel")
    targetLbl.Name = "TargetLine"
    targetLbl.AnchorPoint = Vector2.new(0.5, 0.5)
    targetLbl.Position = UDim2.new(0.5, 0, 0.5, -10)
    targetLbl.Size = UDim2.new(0, 600, 0, 22)
    targetLbl.BackgroundTransparency = 1
    targetLbl.TextColor3 = Color3.fromRGB(255, 255, 255)
    targetLbl.TextStrokeTransparency = 0.6
    targetLbl.TextStrokeColor3 = Color3.fromRGB(0, 0, 0)
    targetLbl.Font = Enum.Font.Gotham
    targetLbl.TextSize = 15
    targetLbl.Text = "ragebot : nil"
    targetLbl.TextXAlignment = Enum.TextXAlignment.Center
    targetLbl.Parent = gui

    local ammoLbl = Instance.new("TextLabel")
    ammoLbl.Name = "AmmoLine"
    ammoLbl.AnchorPoint = Vector2.new(0.5, 0.5)
    ammoLbl.Position = UDim2.new(0.5, 0, 0.5, 12)
    ammoLbl.Size = UDim2.new(0, 600, 0, 20)
    ammoLbl.BackgroundTransparency = 1
    ammoLbl.TextColor3 = Color3.fromRGB(255, 255, 255)
    ammoLbl.TextStrokeTransparency = 0.6
    ammoLbl.TextStrokeColor3 = Color3.fromRGB(0, 0, 0)
    ammoLbl.Font = Enum.Font.Gotham
    ammoLbl.TextSize = 14
    ammoLbl.Text = "ammo : -"
    ammoLbl.TextXAlignment = Enum.TextXAlignment.Center
    ammoLbl.Parent = gui

    ragebotHudGui = gui
    ragebotHudTarget = targetLbl
    ragebotHudAmmo = ammoLbl
end

local function setRagebotHudEnabled(on)
    RAGEBOT_UI_ENABLED = on and true or false
    if not RAGEBOT_UI_ENABLED then
        destroyRagebotHud()
        return
    end
    ensureRagebotHud()
    if ragebotHudConn then
        pcall(function() ragebotHudConn:Disconnect() end)
        ragebotHudConn = nil
    end
    ragebotHudConn = RunService.RenderStepped:Connect(function()
        if not RAGEBOT_UI_ENABLED then return end
        if not ragebotHudTarget or not ragebotHudTarget.Parent then
            ensureRagebotHud()
        end
        local status = "nil"
        pcall(function() status = getRagebotHudStatusText() end)
        if type(status) ~= "string" or status == "" then status = "nil" end
        if ragebotHudTarget then
            ragebotHudTarget.Text = "ragebot : " .. status
        end
        local ammo = getLocalAmmoCount()
        if ragebotHudAmmo then
            if ammo ~= nil then
                ragebotHudAmmo.Text = "ammo : " .. tostring(ammo)
            else
                ragebotHudAmmo.Text = "ammo : ..."
            end
        end
    end)
end

getgenv().setRagebotHudEnabled = setRagebotHudEnabled


RageCol = Library:CreateColumn("레이지봇")

RageCol:AddSwitch({
    Name = "ammo/target",
    Default = false,
    Callback = function(Value)
        if setRagebotHudEnabled then
            setRagebotHudEnabled(Value)
        else
            RAGEBOT_UI_ENABLED = Value and true or false
        end
        createNotification(Value and "ammo/target ON" or "ammo/target OFF")
        updateKeybindsList()
    end
})

RageCol:AddSwitch({
    Name = "Rage Bot 1 (레이지봇 1)",
    Default = false,
    Callback = function(Value)
        rbEnabled = Value
        if Value then
            if rb1DesyncEnabled == nil then rb1DesyncEnabled = true end
            startRageBot()
            createNotification("Rage Bot 1 ON")
        else
            rbEnabled = false
            pcall(stopRageBot)
            createNotification("Rage Bot 1 OFF")
        end
        updateKeybindsList()
    end
})

RageCol:AddSwitch({
    Name = "Hydron Ragebot (머리위 TP)",
    Default = false,
    Callback = function(Value)
        if Value then
            pcall(startHydronRagebot)
            createNotification("Hydron Ragebot ON")
        else
            pcall(stopHydronRagebot)
            createNotification("Hydron Ragebot OFF")
        end
        updateKeybindsList()
    end
})
RageCol:AddSwitch({
    Name = "Hydron Desync",
    Default = true,
    Callback = function(Value)
        if getgenv().HydronRage then
            getgenv().HydronRage.Desync = Value and true or false
        end
        createNotification(Value and "Hydron Desync ON" or "Hydron Desync OFF")
    end
})
RageCol:AddSlider({
    Name = "Hydron 높이 오프셋",
    Min = 0, Max = 10, Default = 2.5, Suffix = " studs",
    Callback = function(Value)
        if getgenv().HydronRage then
            getgenv().HydronRage.HeightOffset = tonumber(Value) or 2.5
        end
    end
})

RageCol:AddSwitch({
    Name = "RB1 Desync (레이지봇1 전용)",
    Default = false,
    Callback = function(Value)
        rb1DesyncEnabled = Value and true or false
        if not rb1DesyncEnabled then
            pcall(function() DesyncStop() end)
            pcall(function() if rb1StopDesync then rb1StopDesync() end end)
        end
        createNotification(rb1DesyncEnabled and "RB1 Desync ON" or "RB1 Desync OFF")
        updateKeybindsList()
    end
})

RageCol:AddSwitch({
    Name = "Void Spam (켠 레이지봇 전부)",
    Default = false,
    Callback = function(Value)
        local LE = getgenv().LunaraExtras
        if LE and LE.setVoidSpam then LE.setVoidSpam(Value) end
        createNotification(Value and "Void Spam ON (RB1/2/3/0)" or "Void Spam OFF")
        updateKeybindsList()
    end
})

RageCol:AddSwitch({
    Name = "Anti-Mine (지뢰 감지/회피)",
    Default = true,
    Callback = function(Value)
        ANTI_MINE_ENABLED = Value and true or false
        createNotification(ANTI_MINE_ENABLED and "Anti-Mine ON (16m)" or "Anti-Mine OFF")
        updateKeybindsList()
    end
})

RageCol:AddSwitch({
    Name = "Shield Check (보호막/면역 체크)",
    Default = true,
    Callback = function(Value)
        SHIELD_CHECK_ENABLED = Value and true or false
        createNotification(SHIELD_CHECK_ENABLED and "Shield Check ON" or "Shield Check OFF")
        updateKeybindsList()
    end
})

RageCol:AddSwitch({
    Name = "Auto Fire (자동 발사)",
    Default = true,
    Callback = function(Value)
        AUTO_FIRE_ENABLED = Value
        createNotification(Value and "Auto Fire ON" or "Auto Fire OFF")
        updateKeybindsList()
    end
})

RageCol:AddSwitch({
    Name = "무기 자동선택 (탄약0/시작시)",
    Default = false,
    Callback = function(Value)
        AUTO_WEAPON_SELECT_ENABLED = Value and true or false
        createNotification(AUTO_WEAPON_SELECT_ENABLED and "무기 자동선택 ON" or "무기 자동선택 OFF")
        updateKeybindsList()
        if AUTO_WEAPON_SELECT_ENABLED then
            pcall(function() if forceEquipPreferredWeapon then forceEquipPreferredWeapon(true) end end)
        end
    end
})
RageCol:AddSwitch({
    Name = "자동선택: Primary 사용",
    Default = true,
    Callback = function(Value)
        AUTO_WEAPON_USE_PRIMARY = Value and true or false
    end
})
RageCol:AddSwitch({
    Name = "자동선택: Secondary 사용",
    Default = true,
    Callback = function(Value)
        AUTO_WEAPON_USE_SECONDARY = Value and true or false
    end
})
RageCol:AddSwitch({
    Name = "자동선택: Melee 사용",
    Default = false,
    Callback = function(Value)
        AUTO_WEAPON_USE_MELEE = Value and true or false
    end
})


RageCol:AddDropdown({
    Name = "공격 모드 (Attack Mode)",
    Options = {"Gun (총/좌클릭)", "Melee (칼/우클릭)"},
    Default = "Gun (총/좌클릭)",
    Callback = function(Options)
        local v = type(Options) == "table" and Options[1] or Options
        if type(v) == "string" and v:find("Melee") then
            RAGE_ATTACK_MODE = "Melee"
        else
            RAGE_ATTACK_MODE = "Gun"
        end
        createNotification("Attack Mode: " .. tostring(RAGE_ATTACK_MODE))
        updateKeybindsList()
    end
})

RageCol:AddSwitch({
    Name = "마우스 자동발사 (커서 적)",
    Default = false,
    Callback = function(Value)
        if Value then
            startMouseAutoFire()
            createNotification("마우스 자동발사 ON")
        else
            stopMouseAutoFire()
            createNotification("마우스 자동발사 OFF")
        end
        updateKeybindsList()
    end
})

RageCol:AddSlider({
    Name = "마우스 자동발사 딜레이",
    Min = 8,
    Max = 50,
    Default = 15,
    Suffix = " x0.01s",
    Callback = function(Value)
        local d = (tonumber(Value) or 15) / 100
        if d < 0.08 then d = 0.08 end
        MOUSE_AUTO_FIRE_DELAY = d
    end
})

RageCol:AddSwitch({
    Name = "Rage Bot 4 (FOV)",
    Default = false,
    Callback = function(Value)
        local R = getgenv().RageBot4
        if Value then
            if R and R.setEnabled then R.setEnabled(true) else rb4Enabled = true end
            createNotification("Rage Bot 4 ON")
        else
            rb4Enabled = false
            if R and R.setEnabled then R.setEnabled(false) end
            pcall(function()
                if DesyncEngine and DesyncEngine.tag == "rb4" then DesyncStop() end
            end)
            createNotification("Rage Bot 4 OFF")
        end
        updateKeybindsList()
    end
})

RageCol:AddSwitch({
    Name = "RB4 Desync",
    Default = false,
    Callback = function(Value)
        local R = getgenv().RageBot4
        if R and R.setDesync then R.setDesync(Value) else rb4DesyncEnabled = Value end
        createNotification(Value and "RB4 Desync ON" or "RB4 Desync OFF")
        updateKeybindsList()
    end
})

RageCol:AddSwitch({
    Name = "RB4 Void Spam",
    Default = false,
    Callback = function(Value)
        local R = getgenv().RageBot4
        if R and R.setVoid then R.setVoid(Value) else rb4VoidEnabled = Value end
        createNotification(Value and "RB4 Void ON" or "RB4 Void OFF")
        updateKeybindsList()
    end
})

PlayerCol = Library:CreateColumn("플레이어탭")

PlayerCol:AddSlider({
    Name = "Walk Speed (걷기 속도)",
    Min = 1,
    Max = 200,
    Default = 16,
    Suffix = " Speed",
    Callback = function(Value)
        applyWalkSpeed(Value)
        startWalkSpeedLoop()
        forceWalkSpeed()
        createNotification("Walk Speed: " .. tostring(math.floor(WALK_SPEED)))
    end
})

PlayerCol:AddSwitch({
    Name = "Fly (비행)",
    Default = false,
    Callback = function(Value)
        flyEnabled = Value
        if flyEnabled then startFlying() else stopFlying() end
    end
})

PlayerCol:AddSlider({
    Name = "Fly 속도",
    Min = 10,
    Max = 300,
    Default = 50,
    Suffix = " Speed",
    Callback = function(Value) flySpeed = Value end
})

PlayerCol:AddSwitch({
    Name = "Noclip (벽 통과)",
    Default = false,
    Callback = function(Value)
        noclipEnabled = Value
        toggleNoclip(Value)
    end
})

PlayerCol:AddSwitch({
    Name = "Infinite Jump (무한 점프)",
    Default = false,
    Callback = function(Value) infJumpEnabled = Value end
})

PlayerCol:AddSwitch({
    Name = "Third Person (3인칭)",
    Default = false,
    Callback = function(Value)
        THIRD_PERSON_ENABLED = Value and true or false
        if THIRD_PERSON_ENABLED then
            pcall(enableThirdPerson)
        else
            pcall(disableThirdPerson)
        end
        updateKeybindsList()
    end
})
PlayerCol:AddSlider({
    Name = "Third Person Distance",
    Min = 5, Max = 30, Default = 12, Suffix = "st",
    Callback = function(Value)
        distance = math.clamp(tonumber(Value) or 12, 5, 30)
        if THIRD_PERSON_ENABLED then
            pcall(function()
                LocalPlayer.CameraMinZoomDistance = distance
                LocalPlayer.CameraMaxZoomDistance = distance + 8
            end)
        end
    end
})

PlayerCol:AddSwitch({
    Name = "Anti-Void (낙사 방지)",
    Default = false,
    Callback = function(Value)
        getgenv().InstanceSetUnderground(Value)
        createNotification(Value and "Anti-Void 활성화" or "Anti-Void 비활성화")
    end
})

PlayerCol:AddSwitch({
    Name = "Anti Flashbang (플래시 무효)",
    Default = true,
    Callback = function(Value)
        if Value then
            enableAntiFlashbang()
            createNotification("Anti Flashbang ON")
        else
            createNotification("Anti Flashbang OFF (재접속 시 원상복구)")
        end
    end
})

PlayerCol:AddSwitch({
    Name = "Slide Boost (슬라이드 부스트)",
    Default = false,
    Callback = function(Value)
        SLIDE_BOOST_ENABLED = Value and true or false
        if _G.Features and _G.Features.SlideBoost then
            _G.Features.SlideBoost.Enabled = SLIDE_BOOST_ENABLED
        end
        local M = getgenv().MiscExtras
        if M and M.setSlideBoost then
            M.setSlideBoost(SLIDE_BOOST_ENABLED)
        elseif M and M.setSlideBoostMult then
            if SLIDE_BOOST_ENABLED then
                M.setSlideBoostMult(tonumber(SLIDE_BOOST_MULT) or 1.5)
            else
                M.setSlideBoostMult(1)
            end
        end
        createNotification(SLIDE_BOOST_ENABLED and ("Slide Boost ON x" .. tostring(SLIDE_BOOST_MULT or 1.5)) or "Slide Boost OFF")
        updateKeybindsList()
    end
})

PlayerCol:AddSlider({
    Name = "Slide Boost (슬라이드 배율)",
    Min = 0,
    Max = 50,
    Default = 0,
    Suffix = " x0.1",
    Callback = function(Value)
        local mult = (tonumber(Value) or 0) / 10
        SLIDE_BOOST_MULT = mult
        SLIDE_BOOST_ENABLED = mult > 0.05
        if _G.Features and _G.Features.SlideBoost then
            _G.Features.SlideBoost.Speed = 50 * mult
        end
        local M = getgenv().MiscExtras
        if M and M.setSlideBoostMult then
            if SLIDE_BOOST_ENABLED then
                M.setSlideBoostMult(mult)
            else
                SLIDE_BOOST_MULT = mult
            end
        end
        createNotification("Slide 배율 x" .. tostring(mult) .. (SLIDE_BOOST_ENABLED and " (ON)" or " (OFF)"))
        updateKeybindsList()
    end
})

-- FOV tab removed

VisualCol = Library:CreateColumn("비주얼탭")

VisualCol:AddSwitch({
    Name = "ESP 3D (캐릭터 하이라이트)",
    Default = false,
    Callback = function(Value)
        ESP_3D = Value and true or false
        if ESP_3D then
            if not espConnection then startEsp() end
            createNotification("ESP 3D ON")
        else
            clearEsp3D()
            createNotification("ESP 3D OFF")
        end
        updateKeybindsList()
    end
})

VisualCol:AddSwitch({
    Name = "ESP (전체)",
    Default = false,
    Callback = function(Value)
        ESP_ENABLED = Value
        if Value then startEsp() else stopEsp() end
        createNotification(Value and "ESP ON" or "ESP OFF")
        updateKeybindsList()
    end
})
VisualCol:AddSwitch({
    Name = "ESP Box (박스)",
    Default = true,
    Callback = function(Value)
        ESP_BOX = Value
    end
})
VisualCol:AddSwitch({
    Name = "ESP Info (닉/체력/거리)",
    Default = true,
    Callback = function(Value)
        ESP_INFO = Value
    end
})
VisualCol:AddSwitch({
    Name = "ESP Weapon (무기)",
    Default = true,
    Callback = function(Value)
        ESP_WEAPON = Value
    end
})

VisualCol:AddSwitch({
    Name = "Tripmine ESP (트랩마인)",
    Default = false,
    Callback = function(Value)
        if getgenv().SetTripmineESP then
            getgenv().SetTripmineESP(Value)
        elseif getgenv().TripmineESP then
            getgenv().TripmineESP.Enabled = Value and true or false
        end
        createNotification(Value and "Tripmine ESP ON" or "Tripmine ESP OFF")
    end
})

VisualCol:AddSwitch({
    Name = "키바인드 표시 (HUD)",
    Default = true,
    Callback = function(Value)
        HUD_DISPLAY_ENABLED = Value
        updateKeybindsList()
    end
})

VisualCol:AddSwitch({
    Name = "Hit 표시 (Hit Marker)",
    Default = false,
    Callback = function(Value)
        HIT_INDICATOR_ENABLED = Value
        createNotification(Value and "Hit 표시 ON" or "Hit 표시 OFF")
    end
})

VisualCol:AddButton("Load Skin Changer", function()
    pcall(function()
        loadstring(game:HttpGet("https://raw.githubusercontent.com/mineminyee222/rivals-skin/refs/heads/main/%EB%9D%BC%EC%9D%B4%EB%B2%8C%20%EC%8A%A4%ED%82%A8%EC%B2%B4%EC%9D%B8%EC%A0%80", true))()
    end)
    createNotification("Skin Changer Executed")
end)

VisualCol:AddButton("Mesh Wrapping (메시 래핑)", function()
    meshWrappingActive = not meshWrappingActive

    if meshWrappingActive then
        local success = applyMeshWrapping()
        if success then
            createNotification("Mesh Wrapping Applied")
        else
            createNotification("ViewModels Not Found (Waiting...)")
        end

        if meshRenderConnection then meshRenderConnection:Disconnect() end
        meshRenderConnection = RunService.RenderStepped:Connect(function()
            if meshWrappingActive then
                applyMeshWrapping()
            end
        end)
    else
        if meshRenderConnection then
            meshRenderConnection:Disconnect()
            meshRenderConnection = nil
        end
        createNotification("Mesh Wrapping Disabled")
    end
end)

AnimMatchCol = Library:CreateColumn("애니 / 매치탭")
AnimMatchCol:AddSwitch({
    Name = "Emote Hop (이모트 합)",
    Default = false,
    Callback = function(Value)
        emoteHopEnabled = Value and true or false
        if emoteHopEnabled then
            local ok = play_emote(LocalPlayer.Character)
            createNotification(ok and "Emote Hop ON" or "Emote Hop ON (waiting character)")
        else
            stop_emote()
            createNotification("Emote Hop OFF")
        end
    end
})
AnimMatchCol:AddSlider({
    Name = "Emote Speed",
    Min = 1,
    Max = 40,
    Default = 40,
    Callback = function(Value)
        emoteSpeed = tonumber(Value) or 40
        ANIM_SPEED = emoteSpeed
        pcall(function()
            if emoteTrack and emoteTrack.IsPlaying then
                emoteTrack:AdjustSpeed(emoteSpeed)
            end
        end)
    end
})

AnimMatchCol:AddSwitch({
    Name = "Spinbot (스핀봇)",
    Default = false,
    Callback = function(Value)
        if setSpinbot then setSpinbot(Value) else isSpinning = Value end
        createNotification(Value and "Spinbot ON" or "Spinbot OFF")
        updateKeybindsList()
    end
})

AnimMatchCol:AddSlider({
    Name = "스핀봇 속도",
    Min = 5,
    Max = 100,
    Default = 20,
    Suffix = " Speed",
    Callback = function(Value) rotationSpeed = Value end
})

AnimMatchCol:AddSwitch({
    Name = "Auto Match",
    Default = false,
    Callback = function(Value)
        local M = getgenv().MiscExtras
        if M and M.setAutoQueue then
            M.setAutoQueue(Value)
        else
            AUTO_MATCH_ENABLED = Value
        end
        createNotification(Value and "Auto Match ON" or "Auto Match OFF")
        updateKeybindsList()
    end
})

AnimMatchCol:AddDropdown({
    Name = "Auto Match 모드",
    Options = {"1v1", "2v2", "3v3", "4v4", "5v5", "FFA"},
    Default = "1v1",
    Callback = function(Options)
        AUTO_MATCH_MODE = Options[1]
        local M = getgenv().MiscExtras
        if M and M.setQueueMode then M.setQueueMode(Options[1]) end
        createNotification("Auto Match 모드: " .. Options[1])
    end
})

AnimMatchCol:AddSwitch({
    Name = "Auto Match Ranked (랭크)",
    Default = false,
    Callback = function(Value)
        local M = getgenv().MiscExtras
        if M and M.setQueueRanked then M.setQueueRanked(Value) end
        createNotification(Value and "Ranked Queue ON" or "Ranked Queue OFF")
        updateKeybindsList()
    end
})

AnimMatchCol:AddSwitch({
    Name = "Auto Ban Ranked (무기 밴)",
    Default = false,
    Callback = function(Value)
        local M = getgenv().MiscExtras
        if M and M.setAutoBan then M.setAutoBan(Value) end
        createNotification(Value and "Auto Ban ON" or "Auto Ban OFF")
        updateKeybindsList()
    end
})

AnimMatchCol:AddDropdown({
    Name = "Ban Weapon 1",
    Options = {"Riot Shield","Katana","Assault Rifle","Sniper","Bow","Shotgun","RPG","Minigun","Revolver","Uzi","Knife","Fists","Scythe","Maul","Grenade","Flashbang","Medkit"},
    Default = "Riot Shield",
    Callback = function(Options)
        local M = getgenv().MiscExtras
        local v = type(Options) == "table" and Options[1] or Options
        if M and M.setBanWeapons then M.setBanWeapons(v, nil) end
    end
})

AnimMatchCol:AddDropdown({
    Name = "Ban Weapon 2",
    Options = {"Katana","Riot Shield","Assault Rifle","Sniper","Bow","Shotgun","RPG","Minigun","Revolver","Uzi","Knife","Fists","Scythe","Maul","Grenade","Flashbang","Medkit"},
    Default = "Katana",
    Callback = function(Options)
        local M = getgenv().MiscExtras
        local v = type(Options) == "table" and Options[1] or Options
        if M and M.setBanWeapons then M.setBanWeapons(nil, v) end
    end
})

EnvCol = Library:CreateColumn("환경탭")

EnvCol:AddSwitch({
    Name = "전체 쉐이더 (All Shaders)",
    Default = false,
    Callback = function(Value)
        envConfig.shaderEnabled = Value
        if Value then
            EnableModernShader()
        else
            DisableModernShader()
        end
        updateKeybindsList()
    end
})

EnvCol:AddSlider({
    Name = "Time of Day (시간)",
    Min = 0, Max = 24, Default = 12, Suffix = "h",
    Callback = function(Value)
        modernShaderHour = math.clamp(math.floor(tonumber(Value) or 12), 0, 24)
        if envConfig.shaderEnabled then
            Lighting.TimeOfDay = string.format("%02d:00:00", modernShaderHour % 24)
        end
    end
})

EnvCol:AddSwitch({
    Name = "커스텀 스카이박스 (Skybox)",
    Default = false,
    Callback = function(Value)
        envConfig.skyboxEnabled = Value
        toggleSkybox()
    end
})
EnvCol:AddDropdown({
    Name = "Sky Preset (스카이)",
    Options = {"Dark Sky","Vaporwave","Lake Sky","Black Mesa"},
    Default = "Dark Sky",
    Callback = function(v)
        envConfig.skyPreset = tostring(v or "Dark Sky")
        if envConfig.skyboxEnabled then
            applySkyPreset(envConfig.skyPreset)
        end
        createNotification("Sky: " .. envConfig.skyPreset)
    end
})


EnvCol:AddSwitch({
    Name = "Orbit Enable (오르빗)",
    Default = false,
    Callback = function(Value)
        OrbitCFG.Active = Value and true or false
        orbitLightEnabled = OrbitCFG.Active
        if Value then
            pcall(startOrbitLight)
            createNotification("Orbit ON")
        else
            pcall(stopOrbitLight)
            createNotification("Orbit OFF")
        end
        updateKeybindsList()
    end
})
EnvCol:AddSlider({
    Name = "Orbit Studs (거리)",
    Min = 10, Max = 10000, Default = 5003, Suffix = "st",
    Callback = function(Value)
        local v = math.clamp(tonumber(Value) or 5003, 10, 10000)
        OrbitCFG.Studs = v
        orbitLightRadius = v
    end
})
EnvCol:AddSlider({
    Name = "Orbit Speed (속도)",
    Min = 1, Max = 150, Default = 5, Suffix = "",
    Callback = function(Value)
        local v = math.clamp(tonumber(Value) or 5, 1, 150)
        OrbitCFG.Speed = v
        orbitLightSpeed = v
    end
})

ConfigCol = Library:CreateColumn("설정탭")

local function setUI(name, value)
    local fn = ConfigSystem and ConfigSystem.UIElements and ConfigSystem.UIElements[name]
    if type(fn) == "function" then
        pcall(fn, value)
        return true
    end
    return false
end

local function applyDeveloperVisualsPack()
    TRACER_ENABLED = true
    pcall(function()
        local R = getgenv().RageBot4
        if R and R.setTracer then R.setTracer(true) end
    end)
    if not setUI("Bullet Tracer (총알 궤적)", true) then
        TRACER_ENABLED = true
    end
    pcall(function()
        if getgenv().AntiKatana then getgenv().AntiKatana.Enabled = true end
        local LE = getgenv().LunaraExtras
        if LE and LE.setAntiKatana then LE.setAntiKatana(true) end
        local R = getgenv().RageBot4
        if R and R.setAntiKatana then R.setAntiKatana(true) end
    end)
    setUI("Anti Katana (안티 카타나)", true)
    ESP_ENABLED = true
    ESP_BOX = true
    ESP_INFO = true
    ESP_WEAPON = true
    ESP_3D = true
    setUI("ESP (전체)", true)
    setUI("ESP Box (박스)", true)
    setUI("ESP Info (닉/체력/거리)", true)
    setUI("ESP Weapon (무기)", true)
    setUI("ESP 3D (캐릭터 하이라이트)", true)
    pcall(startEsp)
    setUI("전체 쉐이더 (All Shaders)", true)
    envConfig.shaderEnabled = true
    modernShaderHour = 17
    pcall(EnableModernShader)
    pcall(function() Lighting.TimeOfDay = "17:00:00" end)
    local timeFn = ConfigSystem.UIElements["Time of Day (시간)"]
    if type(timeFn) == "function" then pcall(timeFn, 17) end
    updateKeybindsList()
end

ConfigCol:AddButton("개발자 에임 설정", function()
    setUI("Legit Aimbot (레짓 에임봇)", false)
    setUI("Aimbot (에임봇)", true)
    AIMBOT_SMOOTH = 75
    local spd = ConfigSystem.UIElements["Aimbot Speed (에임 속도)"]
    if type(spd) == "function" then pcall(spd, 75) end
    AIMBOT_KEY = Enum.UserInputType.MouseButton2
    aimbotKeyHeld = false
    if getgenv().updateAimbotKeyButton then getgenv().updateAimbotKeyButton() end
    applyDeveloperVisualsPack()
    createNotification("개발자 에임 설정 적용 (UI 스위치 포함)")
end)

ConfigCol:AddButton("개발자 레짓 설정", function()
    setUI("Aimbot (에임봇)", false)
    setUI("Legit Aimbot (레짓 에임봇)", true)
    LEGIT_AIMBOT_SMOOTH = 100
    local spd = ConfigSystem.UIElements["Legit 에임 속도"]
    if type(spd) == "function" then pcall(spd, 100) end
    AIMBOT_KEY = Enum.UserInputType.MouseButton2
    aimbotKeyHeld = false
    if getgenv().updateAimbotKeyButton then getgenv().updateAimbotKeyButton() end
    applyDeveloperVisualsPack()
    createNotification("개발자 레짓 설정 적용 (UI 스위치 포함)")
end)

ConfigCol:AddButton("개발자 레이지봇 설정", function()
    pcall(function()
        if getgenv().AntiKatana then getgenv().AntiKatana.Enabled = true end
        local LE = getgenv().LunaraExtras
        if LE and LE.setAntiKatana then LE.setAntiKatana(true) end
        local R = getgenv().RageBot4
        if R and R.setAntiKatana then R.setAntiKatana(true) end
    end)
    setUI("Anti Katana (안티 카타나)", true)
    TRACER_ENABLED = true
    pcall(function()
        local R = getgenv().RageBot4
        if R and R.setTracer then R.setTracer(true) end
    end)
    setUI("Bullet Track (총알 궤적)", true)
    setUI("Bullet Tracer (총알 궤적)", true)
    WEAPON_SPEED_ENABLED = true
    WEAPON_SPEED_BOOST = 100
    setUI("Weapon Attack Speed (공격속도)", true)
    local ws = ConfigSystem.UIElements["총기 연사속도 증가율 (%)"]
    if type(ws) == "function" then pcall(ws, 100) end
    local boostFn = ConfigSystem.UIElements["Attack Speed Boost (%)"]
    if type(boostFn) == "function" then pcall(boostFn, 100) end
    setUI("Automatic Weapon (단발→연사)", true)
    setUI("Weapon Attack Speed (공격속도)", true)
    AUTO_FIRE_ENABLED = true
    setUI("Auto Fire (자동 발사)", true)
    rb4Enabled = true
    rb4DesyncEnabled = false
    setUI("Rage Bot 4 (FOV)", true)
    setUI("RB4 Desync", false)
    pcall(function()
        local R = getgenv().RageBot4
        if R then
            if R.setEnabled then R.setEnabled(true) end
            if R.setDesync then R.setDesync(false) end
        end
    end)
    -- Orbit ON at max distance + max speed
    orbitLightRadius = 10000
    orbitLightSpeed = 150
    OrbitCFG.Studs = 10000
    OrbitCFG.Speed = 150
    OrbitCFG.Active = true
    orbitLightEnabled = true
    orbitDesyncEnabled = true
    setUI("Orbit Enable (오르빗)", true)
    pcall(function()
        local studFn = ConfigSystem.UIElements["Orbit Studs (거리)"]
        if type(studFn) == "function" then pcall(studFn, 10000) end
        local spdFn = ConfigSystem.UIElements["Orbit Speed (속도)"]
        if type(spdFn) == "function" then pcall(spdFn, 150) end
    end)
    pcall(startOrbitLight)
    HIT_SOUND_ENABLED = true
    HIT_SOUND_STYLE = "sparkle"
    pcall(function()
        local M = getgenv().MiscExtras
        if M then
            if M.setHitSound then M.setHitSound(true) end
            if M.setHitSoundStyle then M.setHitSoundStyle("sparkle") end
        end
    end)
    setUI("Hit Sound (히트 사운드)", true)
    ESP_ENABLED = true
    ESP_BOX = true
    ESP_INFO = true
    ESP_WEAPON = true
    ESP_3D = true
    setUI("ESP (전체)", true)
    setUI("ESP Box (박스)", true)
    setUI("ESP Info (닉/체력/거리)", true)
    setUI("ESP Weapon (무기)", true)
    setUI("ESP 3D (캐릭터 하이라이트)", true)
    pcall(function() if startEsp then startEsp() end end)
    pcall(function()
        if getgenv().TripmineESP then getgenv().TripmineESP.Enabled = true end
        setUI("Tripmine ESP (트랩마인)", true)
        setUI("Enable Tripmine ESP", true)
        setUI("지뢰 ESP", true)
    end)
    envConfig.shaderEnabled = true
    modernShaderHour = 17
    setUI("전체 쉐이더 (All Shaders)", true)
    pcall(EnableModernShader)
    pcall(function() Lighting.TimeOfDay = "17:00:00" end)
    local timeFn = ConfigSystem.UIElements["Time of Day (시간)"]
    if type(timeFn) == "function" then pcall(timeFn, 17) end
    rotationSpeed = 100
    if setSpinbot then setSpinbot(true) else isSpinning = true end
    setUI("Spinbot (스핀봇)", true)
    local ss = ConfigSystem.UIElements["스핀봇 속도"]
    if type(ss) == "function" then pcall(ss, 100) end
    ANTI_MINE_ENABLED = true
    setUI("Anti-Mine (지뢰 감지/회피)", true)
    SHIELD_CHECK_ENABLED = true
    setUI("Shield Check (보호막/면역 체크)", true)

    -- ammo/target HUD ON
    setUI("ammo/target", true)
    if setRagebotHudEnabled then
        pcall(setRagebotHudEnabled, true)
    else
        RAGEBOT_UI_ENABLED = true
    end

    updateKeybindsList()
    createNotification("개발자 레이지봇 설정 적용 완료")
end)

ConfigCol:AddButton("게임 재접속 (Rejoin)", function()
    createNotification("재접속 중...")
    pcall(function()
        local TeleportService = game:GetService("TeleportService")
        TeleportService:Teleport(game.PlaceId, LocalPlayer)
    end)
end)


end

pcall(buildHubUI)
function enableAntiFlashbang()
    pcall(function()
        local Flashed = require(LocalPlayer.PlayerScripts.Modules.ClientReplicatedClasses.ClientFighter.FighterInterface.Flashed)
        if Flashed and Flashed.Flash then
            Flashed.Flash = function() return end
        end
    end)
end
task.spawn(function()
    for _ = 1, 15 do
        enableAntiFlashbang()
        task.wait(1)
    end
end)
LocalPlayer.CharacterAdded:Connect(function()
    task.delay(1, enableAntiFlashbang)
end)
function clearEsp3D()
    for plr, h in pairs(espHighlights or {}) do
        pcall(function() if h then h:Destroy() end end)
        espHighlights[plr] = nil
    end
end

function updateEsp3D()
    if not ESP_3D then clearEsp3D() return end
    local seen = {}
    for _, player in ipairs(Players:GetPlayers()) do
        if player == LocalPlayer then continue end
        local char = player.Character
        local hum = char and char:FindFirstChildOfClass("Humanoid")
        if not char or not hum or hum.Health <= 0 then continue end
        local skip = false
        pcall(function()
            local a, b = LocalPlayer:GetAttribute("TeamID"), player:GetAttribute("TeamID")
            if a and b and a == b then skip = true end
        end)
        if skip then continue end
        seen[player] = true
        local hl = espHighlights[player]
        if not hl or not hl.Parent then
            pcall(function()
                if hl then hl:Destroy() end
                hl = Instance.new("Highlight")
                hl.Name = "ESP3D"
                hl.FillColor = Color3.fromRGB(255, 50, 50)
                hl.OutlineColor = Color3.fromRGB(255, 255, 255)
                hl.FillTransparency = 0.55
                hl.OutlineTransparency = 0
                hl.DepthMode = Enum.HighlightDepthMode.AlwaysOnTop
                hl.Adornee = char
                hl.Parent = char
                espHighlights[player] = hl
            end)
        else
            pcall(function() hl.Adornee = char; if hl.Parent ~= char then hl.Parent = char end end)
        end
    end
    for plr, h in pairs(espHighlights) do
        if not seen[plr] then pcall(function() if h then h:Destroy() end end); espHighlights[plr] = nil end
    end
end

function clearEspDrawings()
    for _, pack in pairs(espDrawings) do
        if type(pack) == "table" then
            for _, d in pairs(pack) do
                pcall(function()
                    if d and d.Remove then d:Remove() elseif d and d.Destroy then d:Destroy() end
                end)
            end
        end
    end
    espDrawings = {}
end

function getEnemyWeaponName(player)
    local weaponName = "None"
    pcall(function()
        local vmFolder = workspace:FindFirstChild("ViewModels")
        if not vmFolder then return end
        for _, viewmodel in pairs(vmFolder:GetChildren()) do
            local parts = string.split(viewmodel.Name, " - ")
            if #parts >= 3 then
                local playerName = parts[1]
                local gunName = parts[2]
                if playerName == player.Name then
                    weaponName = gunName
                    break
                end
            end
        end
    end)
    return weaponName
end

function makeText()
    local t = Drawing.new("Text")
    t.Size = 14
    t.Center = true
    t.Outline = true
    t.Color = Color3.fromRGB(255, 255, 255)
    t.Visible = false
    return t
end

function makeLine()
    local l = Drawing.new("Line")
    l.Thickness = 1
    l.Color = Color3.fromRGB(0, 255, 140)
    l.Visible = false
    return l
end

function ensureEspPack(player)
    if espDrawings[player] then return espDrawings[player] end
    local pack = {
        t = makeLine(), b = makeLine(), l = makeLine(), r = makeLine(),
        info = makeText(),
        weapon = makeText(),
    }
    espDrawings[player] = pack
    return pack
end

function worldToScreen(pos)
    local v, on = Camera:WorldToViewportPoint(pos)
    return Vector2.new(v.X, v.Y), on, v.Z
end

function updateEsp()
    if not ESP_ENABLED then
        clearEspDrawings()
        return
    end
    local myChar = LocalPlayer.Character
    local myRoot = myChar and myChar:FindFirstChild("HumanoidRootPart")
    local seen = {}

    for _, player in ipairs(Players:GetPlayers()) do
        if player == LocalPlayer then continue end
        local char = player.Character
        if not char then continue end
        local hum = char:FindFirstChildOfClass("Humanoid")
        local root = char:FindFirstChild("HumanoidRootPart")
        local head = char:FindFirstChild("Head")
        if not hum or not root or hum.Health <= 0 then continue end
        local skip = false
        pcall(function()
            local a, b = LocalPlayer:GetAttribute("TeamID"), player:GetAttribute("TeamID")
            if a and b and a == b then skip = true end
        end)
        if skip then continue end

        seen[player] = true
        local pack = ensureEspPack(player)

        local topPos = (head and head.Position or root.Position) + Vector3.new(0, 0.9, 0)
        local botPos = root.Position - Vector3.new(0, 2.5, 0)
        local top2d, on1, z1 = worldToScreen(topPos)
        local bot2d, on2, z2 = worldToScreen(botPos)
        if not on1 or not on2 or z1 < 0 then
            pack.t.Visible = false; pack.b.Visible = false; pack.l.Visible = false; pack.r.Visible = false
            pack.info.Visible = false; pack.weapon.Visible = false
            continue
        end

        local h = math.abs(top2d.Y - bot2d.Y)
        local w = h * 0.55
        local cx = (top2d.X + bot2d.X) / 2
        local topY, botY = top2d.Y, bot2d.Y
        local left, right = cx - w / 2, cx + w / 2

        if ESP_BOX then
            pack.t.From = Vector2.new(left, topY); pack.t.To = Vector2.new(right, topY); pack.t.Visible = true
            pack.b.From = Vector2.new(left, botY); pack.b.To = Vector2.new(right, botY); pack.b.Visible = true
            pack.l.From = Vector2.new(left, topY); pack.l.To = Vector2.new(left, botY); pack.l.Visible = true
            pack.r.From = Vector2.new(right, topY); pack.r.To = Vector2.new(right, botY); pack.r.Visible = true
        else
            pack.t.Visible = false; pack.b.Visible = false; pack.l.Visible = false; pack.r.Visible = false
        end

        local dist = myRoot and (myRoot.Position - root.Position).Magnitude or 0
        local hp = math.floor(hum.Health + 0.5)
        local maxhp = math.max(1, math.floor(hum.MaxHealth + 0.5))

        if ESP_INFO then
            pack.info.Text = string.format("%s | %d/%d HP | %dm", player.Name, hp, maxhp, math.floor(dist))
            pack.info.Position = Vector2.new(cx, topY - 16)
            pack.info.Color = Color3.fromRGB(255, 255, 255)
            pack.info.Visible = true
        else
            pack.info.Visible = false
        end

        if ESP_WEAPON then
            local wname = getEnemyWeaponName(player)
            pack.weapon.Text = "[" .. tostring(wname) .. "]"
            pack.weapon.Position = Vector2.new(cx, botY + 4)
            pack.weapon.Color = Color3.fromRGB(120, 200, 255)
            pack.weapon.Visible = true
        else
            pack.weapon.Visible = false
        end
    end

    for plr, pack in pairs(espDrawings) do
        if not seen[plr] then
            for _, d in pairs(pack) do
                pcall(function() if d.Remove then d:Remove() end end)
            end
            espDrawings[plr] = nil
        end
    end
end

function startEsp()
    if espConnection then espConnection:Disconnect() end
    espConnection = RunService.RenderStepped:Connect(function()
        pcall(updateEsp)
        pcall(updateEsp3D)
    end)
end

function stopEsp()
    ESP_ENABLED = false
    ESP_3D = false
    if espConnection then espConnection:Disconnect() espConnection = nil end
    clearEspDrawings()
    clearEsp3D()
end
ANIM_ENABLED = ANIM_ENABLED or false
ANIM_SPEED = ANIM_SPEED or 1

function playAnimById(id)
    id = tostring(id or ""):gsub("%D", "")
    if id == "" then id = "102820461604639" end
    ANIM_ID = id
    local char = LocalPlayer.Character
    if not char then return false end
    local hum = char:FindFirstChildOfClass("Humanoid")
    if not hum then return false end
    local animator = hum:FindFirstChildOfClass("Animator")
    if not animator then
        animator = Instance.new("Animator")
        animator.Parent = hum
    end
    pcall(function()
        if animTrack then
            animTrack:Stop(0)
            animTrack:Destroy()
            animTrack = nil
        end
        for _, t in ipairs(animator:GetPlayingAnimationTracks()) do
            if t.Priority == Enum.AnimationPriority.Action
                or t.Priority == Enum.AnimationPriority.Action2
                or t.Priority == Enum.AnimationPriority.Action3
                or t.Priority == Enum.AnimationPriority.Action4 then
            end
        end
    end)
    local anim = Instance.new("Animation")
    anim.AnimationId = "rbxassetid://" .. id
    pcall(function()
        game:GetService("ContentProvider"):PreloadAsync({anim})
    end)
    local ok, track = pcall(function()
        local t = animator:LoadAnimation(anim)
        t.Priority = Enum.AnimationPriority.Action4
        t.Looped = true
        t:Play(0.1, 1, math.clamp(tonumber(ANIM_SPEED) or 1, 0.1, 5))
        return t
    end)
    if ok and track then
        animTrack = track
        ANIM_ENABLED = true
        if animConnection then pcall(function() animConnection:Disconnect() end) end
        animConnection = RunService.Heartbeat:Connect(function()
            if not ANIM_ENABLED then return end
            if not animTrack then return end
            pcall(function()
                if not animTrack.IsPlaying then
                    animTrack:Play(0.1, 1, math.clamp(tonumber(ANIM_SPEED) or 1, 0.1, 5))
                end
            end)
        end)
        return true
    end
    return false
end

function stopAnimPlay()
    ANIM_ENABLED = false
    if animConnection then pcall(function() animConnection:Disconnect() end) animConnection = nil end
    pcall(function()
        if animTrack then animTrack:Stop(0.1) animTrack:Destroy() animTrack = nil end
    end)
end

LocalPlayer.CharacterAdded:Connect(function()
    task.delay(1, function()
        if ANIM_ID and ANIM_ID ~= "" then
            pcall(playAnimById, ANIM_ID)
        end
    end)
end)
function initMiscExtras()
    local weapons = {
        "Assault Rifle","Sniper","Bow","Burst Rifle","Crossbow","Gunblade","RPG","Shotgun",
        "Energy Rifle","Flamethrower","Grenade Launcher","Minigun","Paintball Gun","Distortion",
        "Permafrost","Handgun","Daggers","Flare Gun","Revolver","Shorty","Spray","Uzi",
        "Energy Pistols","Exogun","Slingshot","Warper","Fists","Battle Axe","Chainsaw","Katana",
        "Knife","Riot Shield","Scythe","Maul","Trowel","Grenade","Flashbang","Freeze Ray",
        "Jump Pad","Molotov","Satchel","Smoke Grenade","War Horn","Medkit","Substapce Tripmine",
        "Warpstone","Hook","Spear"
    }

    local banThread, queueThread = nil, nil
    local voteRemote = nil
    pcall(function()
        voteRemote = ReplicatedStorage:WaitForChild("Remotes", 5)
            :WaitForChild("Duels", 5):WaitForChild("Vote", 5)
    end)

    local function stopAutoBan()
        banThread = nil
    end
    local function startAutoBan()
        stopAutoBan()
        banThread = task.spawn(function()
            local i = 1
            local lastFire = 0
            while AUTO_BAN_ENABLED and banThread do
                if not voteRemote then
                    pcall(function()
                        voteRemote = ReplicatedStorage:FindFirstChild("Remotes")
                            and ReplicatedStorage.Remotes:FindFirstChild("Duels")
                            and ReplicatedStorage.Remotes.Duels:FindFirstChild("Vote")
                    end)
                end
                local list = {}
                if AUTO_BAN_W1 and AUTO_BAN_W1 ~= "" then table.insert(list, AUTO_BAN_W1) end
                if AUTO_BAN_W2 and AUTO_BAN_W2 ~= "" then table.insert(list, AUTO_BAN_W2) end
                local now = tick()
                if voteRemote and #list > 0 and (now - lastFire) >= 2.5 then
                    pcall(function() voteRemote:FireServer(list[i]) end)
                    i = i % #list + 1
                    lastFire = now
                end
                task.wait(0.5)
            end
        end)
    end

    local function stopAutoQueue()
        queueThread = nil
    end
    local function startAutoQueue()
        stopAutoQueue()
        queueThread = task.spawn(function()
            while AUTO_MATCH_ENABLED and queueThread do
                pcall(function()
                    local mm = ReplicatedStorage:FindFirstChild("Remotes")
                    mm = mm and mm:FindFirstChild("Matchmaking")
                    local jq = mm and mm:FindFirstChild("JoinQueue")
                    if not jq then return end
                    local mode = AUTO_MATCH_MODE or "1v1"
                    if AUTO_QUEUE_RANKED then
                        jq:InvokeServer(mode, true)
                    else
                        jq:InvokeServer(mode)
                    end
                end)
                task.wait(3)
            end
        end)
    end
    local hitGui = Instance.new("ScreenGui")
    hitGui.Name = "mineminyeeHitNotif"
    hitGui.ResetOnSpawn = false
    hitGui.DisplayOrder = 999998
    hitGui.Parent = playerGui
    local hitRoot = Instance.new("Frame")
    hitRoot.Size = UDim2.new(0, 320, 0, 280)
    hitRoot.Position = UDim2.new(0, 12, 0, 12)
    hitRoot.BackgroundTransparency = 1
    hitRoot.Parent = hitGui
    local hitLayout = Instance.new("UIListLayout")
    hitLayout.Padding = UDim.new(0, 4)
    hitLayout.Parent = hitRoot
    local hitEnabled = false
    local lastHp = {}

    local function pushHit(name, dmg, part)
        if not hitEnabled or dmg < 0.5 then return end
        local row = Instance.new("TextLabel")
        row.Size = UDim2.new(1, 0, 0, 22)
        row.BackgroundColor3 = Color3.fromRGB(20, 20, 28)
        row.BackgroundTransparency = 0.25
        row.BorderSizePixel = 0
        row.Text = string.format("hit %s for %d in the %s", name, math.floor(dmg + 0.5), part or "Body")
        row.TextColor3 = Color3.fromRGB(235, 235, 235)
        row.Font = Enum.Font.Code
        row.TextSize = 14
        row.TextXAlignment = Enum.TextXAlignment.Left
        row.Parent = hitRoot
        local c = Instance.new("UICorner")
        c.CornerRadius = UDim.new(0, 4)
        c.Parent = row
        task.delay(3, function()
            pcall(function() row:Destroy() end)
        end)
        local kids = hitRoot:GetChildren()
        local labels = {}
        for _, k in ipairs(kids) do
            if k:IsA("TextLabel") then table.insert(labels, k) end
        end
        while #labels > 8 do
            labels[1]:Destroy()
            table.remove(labels, 1)
        end
    end

    RunService.Heartbeat:Connect(function()
        if not hitEnabled then return end
        pcall(function()
            for _, plr in ipairs(Players:GetPlayers()) do
                if plr == LocalPlayer then continue end
                local hum = plr.Character and plr.Character:FindFirstChildOfClass("Humanoid")
                if not hum then continue end
                local prev = lastHp[plr]
                local cur = hum.Health
                if prev == nil then
                    lastHp[plr] = cur
                elseif cur < prev - 0.5 then
                    pushHit(plr.Name, prev - cur, "Body")
                    lastHp[plr] = cur
                    if HIT_SOUND_ENABLED then
                        pcall(function() getgenv().InstancePlayHitSound() end)
                    end
                elseif cur > prev then
                    lastHp[plr] = cur
                end
            end
        end)
    end)
    local soundFolder = "Hitsounds/sounds"
    local soundFiles = {
        ["Among Us"] = "amongus.mp3", ["Bonk"] = "bonk.mp3", ["Bruh"] = "bruh.mp3",
        ["Fart"] = "fart.mp3", ["Minecraft"] = "minecraft.mp3", ["Neverlose"] = "neverlose.mp3",
        ["Osu"] = "osu.mp3", ["Stars"] = "Stars.mp3", ["Rust HS"] = "rust hs.mp3", ["Vine"] = "vine.mp3",
    }
    local links = {
        ["amongus.mp3"] = "https://www.myinstants.com/media/sounds/roblox-death-sound_ytkBL7X.mp3",
        ["minecraft.mp3"] = "https://www.myinstants.com/media/sounds/steve-old-hurt-sound_XKZxUk4.mp3",
        ["bruh.mp3"] = "https://www.myinstants.com/media/sounds/discord-notification.mp3",
        ["fart.mp3"] = "https://www.myinstants.com/media/sounds/fart-moan3.mp3",
        ["neverlose.mp3"] = "https://www.myinstants.com/media/sounds/neverlose-s.mp3",
        ["rust hs.mp3"] = "https://www.myinstants.com/media/sounds/eaolwpzhgsba.mp3",
        ["osu.mp3"] = "https://www.myinstants.com/media/sounds/osu-hit-sound.mp3",
        ["Stars.mp3"] = "https://www.myinstants.com/media/sounds/starshitsound.mp3",
        ["bonk.mp3"] = "https://www.myinstants.com/media/sounds/bonk.mp3",
        ["vine.mp3"] = "https://www.myinstants.com/media/sounds/vine-boom.mp3",
    }
    task.spawn(function()
        pcall(function()
            if isfolder and makefolder and writefile and isfile then
                if not isfolder("Hitsounds") then makefolder("Hitsounds") end
                if not isfolder(soundFolder) then makefolder(soundFolder) end
                for fn, url in pairs(links) do
                    local fp = soundFolder .. "/" .. fn
                    if not isfile(fp) then
                        pcall(function() writefile(fp, game:HttpGet(url, true)) end)
                        task.wait(0.5)
                    end
                end
            end
        end)
    end)
task.defer(function()
    local function bindVM()
        pcall(function()
            local path = LocalPlayer.PlayerScripts.Modules.ClientReplicatedClasses.ClientFighter.ClientItem.ClientViewModel
            if not path then return end
            path.ChildAdded:Connect(function(child)
                if not HIT_SOUND_ENABLED then return end
                if not child:IsA("Sound") then return end
                if child.SoundId == "rbxassetid://16537449730" then return end
                pcall(function()
                    local map = {
                        ["Rust HS"] = "rbxassetid://4764109000",
                        ["Neverlose"] = "rbxassetid://97643101798871",
                        ["sparkle"] = "rbxassetid://110241936966089",
                        ["Minecraft Hit"] = "rbxassetid://8766809464",
                        ["Bonk"] = "rbxassetid://5766898159",
                        ["Osu"] = "rbxassetid://7149255551",
                        ["Among Us"] = "rbxassetid://5700183626",
                        ["Bruh"] = "rbxassetid://4578740568",
                        ["Vine"] = "rbxassetid://5332680810",
                        ["Gamesense"] = "rbxassetid://4817809188",
                    }
                    local id = map[HIT_SOUND_STYLE] or map["Rust HS"]
                    child.SoundId = id
                    child.PlaybackSpeed = tonumber(HIT_SOUND_PITCH) or 1
                    child.Volume = 0
                    local s = Instance.new("Sound")
                    s.SoundId = id
                    s.PlaybackSpeed = tonumber(HIT_SOUND_PITCH) or 1
                    s.Volume = tonumber(HIT_SOUND_VOLUME) or 0.5
                    s.Parent = game:GetService("SoundService")
                    s:Play()
                    game:GetService("Debris"):AddItem(s, 4)
                end)
            end)
        end)
    end
    for _ = 1, 15 do
        bindVM()
        task.wait(1)
    end
end)

getgenv().InstancePlayHitSound = function()
        if not HIT_SOUND_ENABLED then return end
        pcall(function()
            local soundAssets = {
                ["Rust HS"] = "rbxassetid://4764109000",
                ["Neverlose"] = "rbxassetid://97643101798871",
                ["sparkle"] = "rbxassetid://110241936966089",
                ["Minecraft Hit"] = "rbxassetid://8766809464",
                ["Bonk"] = "rbxassetid://5766898159",
                ["Osu"] = "rbxassetid://7149255551",
                ["Among Us"] = "rbxassetid://5700183626",
                ["Bruh"] = "rbxassetid://4578740568",
                ["Vine"] = "rbxassetid://5332680810",
                ["Gamesense"] = "rbxassetid://4817809188",
            }
            local id = soundAssets[HIT_SOUND_STYLE] or soundAssets["Rust HS"]
            local filename = soundFiles and soundFiles[HIT_SOUND_STYLE]
            if filename and isfile then
                local fullPath = soundFolder .. "/" .. filename
                if isfile(fullPath) then
                    local asset = (getsynasset and getsynasset(fullPath)) or (getcustomasset and getcustomasset(fullPath))
                    if asset then id = asset end
                end
            end
            local sound = Instance.new("Sound")
            sound.SoundId = id
            sound.Volume = HIT_SOUND_VOLUME or 0.5
            sound.PlaybackSpeed = HIT_SOUND_PITCH or 1
            sound.Parent = workspace
            sound:Play()
            task.delay(3, function() pcall(function() sound:Destroy() end) end)
        end)
    end
    local slideHooked = false
    local slideBaseSpeed = nil
    local function applySlideBoost()
        pcall(function()
            local mech = require(LocalPlayer.PlayerScripts.Controllers.MechanicsController)
            if not mech or not mech.Slide then return end
            if not slideHooked then
                local old = mech.Slide
                function mech:Slide(...)
                    local f = self.LocalFighter
                    if f then
                        pcall(function()
                            if slideBaseSpeed == nil then
                                slideBaseSpeed = f:Get("SlidingSpeedMax") or 3
                            end
                            local mult = tonumber(SLIDE_BOOST_MULT) or 1
                            if mult <= 1.01 then
                                f:Set("SlidingSpeedMax", slideBaseSpeed)
                            else
                                f:Set("SlidingSpeedMax", slideBaseSpeed * mult)
                            end
                        end)
                    end
                    return old(self, ...)
                end
                slideHooked = true
            end
            pcall(function()
                local fc = require(LocalPlayer.PlayerScripts.Controllers.FighterController)
                local f = fc and fc.LocalFighter
                if f then
                    if slideBaseSpeed == nil then
                        slideBaseSpeed = f:Get("SlidingSpeedMax") or 3
                    end
                    if not SLIDE_BOOST_ENABLED then
                        f:Set("SlidingSpeedMax", slideBaseSpeed)
                    else
                        local mult = tonumber(SLIDE_BOOST_MULT) or 1.5
                        if mult <= 1.01 then
                            f:Set("SlidingSpeedMax", slideBaseSpeed)
                        else
                            f:Set("SlidingSpeedMax", slideBaseSpeed * mult)
                        end
                    end
                end
            end)
        end)
    end
    task.spawn(function()
        for _ = 1, 25 do
            applySlideBoost()
            if slideHooked then break end
            task.wait(1)
        end
    end)
    AUTO_COLLECT_HEALTH = true
    AUTO_COLLECT_AMMO = true
    RunService.RenderStepped:Connect(function()
        pcall(function()
            local character = LocalPlayer.Character
            if not character then return end
            local hrp = character:FindFirstChild("HumanoidRootPart")
            if not hrp then return end
            local humanoid = character:FindFirstChildOfClass("Humanoid")
            local needsHealth = humanoid and humanoid.Health < humanoid.MaxHealth
            if not firetouchinterest then return end
            for _, obj in ipairs(workspace:GetChildren()) do
                if obj.Name == "_drop" and obj:IsA("BasePart") then
                    local want = false
                    if needsHealth and obj:FindFirstChild("Health") then
                        want = true
                    end
                    if obj:FindFirstChild("Ammo") then
                        want = true
                    end
                    if want then
                        pcall(function()
                            firetouchinterest(hrp, obj, 0)
                            firetouchinterest(hrp, obj, 1)
                        end)
                    end
                end
            end
        end)
    end)

    getgenv().MiscExtras = {
        weapons = weapons,
        setAutoBan = function(v)
            AUTO_BAN_ENABLED = v and true or false
            if AUTO_BAN_ENABLED then startAutoBan() else stopAutoBan() end
        end,
        setBanWeapons = function(w1, w2)
            if w1 then AUTO_BAN_W1 = w1 end
            if w2 then AUTO_BAN_W2 = w2 end
            if AUTO_BAN_ENABLED then startAutoBan() end
        end,
        setAutoQueue = function(v)
            AUTO_MATCH_ENABLED = v and true or false
            if AUTO_MATCH_ENABLED then startAutoQueue() else stopAutoQueue() end
        end,
        setQueueRanked = function(v)
            AUTO_QUEUE_RANKED = v and true or false
            if AUTO_MATCH_ENABLED then startAutoQueue() end
        end,
        setQueueMode = function(m)
            AUTO_MATCH_MODE = m or "1v1"
            if AUTO_MATCH_ENABLED then startAutoQueue() end
        end,
        setHitNotif = function(v) hitEnabled = v and true or false end,
        setHitSound = function(v) HIT_SOUND_ENABLED = v and true or false end,
        setHitSoundStyle = function(s) HIT_SOUND_STYLE = s or "Rust HS" end,
        setHitSoundVolume = function(v) HIT_SOUND_VOLUME = (tonumber(v) or 50) / 100 end,
        setHitSoundPitch = function(v) HIT_SOUND_PITCH = (tonumber(v) or 100) / 100 end,
        setSlideBoost = function(v)
            SLIDE_BOOST_ENABLED = v and true or false
            if SLIDE_BOOST_ENABLED then applySlideBoost() end
        end,
        setSlideBoostMult = function(v)
            SLIDE_BOOST_MULT = math.clamp(tonumber(v) or 1.5, 1, 5)
            SLIDE_BOOST_ENABLED = SLIDE_BOOST_MULT > 1.01
            applySlideBoost()
        end,
        allSounds = {"Among Us","Bonk","Bruh","Fart","Minecraft","Neverlose","Osu","Stars","Rust HS","Vine"},
    }
end
function initRageBot4()
    local CFG = {
        HitPart = "Head",
        FOV = math.huge,
        FireCooldown = 0,
        FOV = 400,
        VoidShoot = 1.0,
        VoidHide = 1.0,
    }
    local lastFire = 0
    local VFR_LIM, VFR_DEAD = 2147483646, 1147483646
    local vfrSnap = { cf = nil, lv = nil, av = nil }
    local rb4VisualCF = nil
    local Utility, EnumLibrary, localFighter

    pcall(function() Utility = require(ReplicatedStorage.Modules.Utility) end)
    pcall(function() EnumLibrary = require(ReplicatedStorage.Modules.EnumLibrary) end)
    task.spawn(function()
        for _ = 1, 20 do
            pcall(function()
                local fc = require(LocalPlayer.PlayerScripts.Controllers.FighterController)
                localFighter = fc and fc.LocalFighter
            end)
            if localFighter then break end
            task.wait(1)
        end
    end)
    local AntiKatana = { Enabled = true }
    local katanausers = {}
    task.spawn(function()
        local lp = LocalPlayer
        pcall(function() lp:WaitForChild("PlayerScripts", 30) end)
        local katana, attempts = nil, 0
        while attempts < 15 do
            pcall(function()
                local m = lp.PlayerScripts.Modules.Items:FindFirstChild("Katana", true)
                if m then katana = require(m) end
            end)
            if not katana then
                pcall(function()
                    for _, m in pairs(lp.PlayerScripts:GetDescendants()) do
                        if m.Name == "Katana" and m:IsA("ModuleScript") then
                            local ok, res = pcall(require, m)
                            if ok and type(res) == "table" then katana = res break end
                        end
                    end
                end)
            end
            if katana and type(katana) == "table" and katana.StartAiming then break end
            attempts = attempts + 1
            task.wait(1)
        end
        if katana and type(katana) == "table" and katana.StartAiming then
            local old = katana.StartAiming
            katana.StartAiming = function(self, force)
                local fighter = self.ClientFighter
                local player = fighter and fighter.Player
                if player then
                    katanausers[player] = true
                    local dur = (self.Info and self.Info.DeflectDuration) or 0.6
                    task.delay(dur, function() katanausers[player] = nil end)
                end
                return old(self, force)
            end
        end
    end)
    local function isDeflecting(player)
        return katanausers[player] == true
    end
    local function shouldSkipKatana(target)
        if typeof(target) == "Instance" then
            local plr = target:IsA("Player") and target or Players:GetPlayerFromCharacter(target)
            if not plr then return false end
            if isDeflecting(plr) then return true end
            local g = getgenv().ShouldIgnoreKatanaTarget
            if type(g) == "function" then
                local ok, r = pcall(g, plr)
                if ok and r then return true end
            end
            return false
        end
        return false
    end
    Players.PlayerRemoving:Connect(function(p) katanausers[p] = nil end)
    getgenv().AntiKatana = AntiKatana
    getgenv().IsKatanaDeflecting = isDeflecting
    getgenv().ShouldSkipKatanaTarget = shouldSkipKatana
    getgenv().InstanceIsKatanaDeflecting = function(plr)
        return isDeflecting(plr)
    end
    local soundAssets = {
        ["Rust HS"] = "rbxassetid://4764109000",
        ["Neverlose"] = "rbxassetid://97643101798871",
        ["sparkle"] = "rbxassetid://110241936966089",
        ["Minecraft Hit"] = "rbxassetid://8766809464",
        ["Bonk"] = "rbxassetid://5766898159",
        ["Osu"] = "rbxassetid://7149255551",
        ["Among Us"] = "rbxassetid://5700183626",
        ["Bruh"] = "rbxassetid://4578740568",
        ["Vine"] = "rbxassetid://5332680810",
        ["Gamesense"] = "rbxassetid://4817809188",
    }
    getgenv().InstancePlayHitSound = function()
        if not HIT_SOUND_ENABLED then return end
        pcall(function()
            local id = soundAssets[HIT_SOUND_STYLE] or soundAssets["Rust HS"]
            local snd = Instance.new("Sound")
            snd.SoundId = id
            snd.Volume = HIT_SOUND_VOLUME or 0.5
            snd.PlaybackSpeed = HIT_SOUND_PITCH or 1
            snd.Parent = workspace
            snd:Play()
            task.delay(4, function() pcall(function() snd:Destroy() end) end)
        end)
    end
    workspace.DescendantAdded:Connect(function(obj)
        if not HIT_SOUND_ENABLED and not (getgenv().MiscExtras) then return end
        if not obj:IsA("BillboardGui") then return end
        task.defer(function()
            if not obj.Parent then return end
            local lbl = obj:FindFirstChildWhichIsA("TextLabel", true)
            if lbl and tonumber(lbl.Text) then
                pcall(function() getgenv().InstancePlayHitSound() end)
            end
        end)
    end)
    local bulletTracers = {}
    local MAX_TRACERS = 40
    local tracerList = {}
    local MAX_TRACERS = 48
    local function makeTracer(fromPos, toPos)
        if not TRACER_ENABLED or not fromPos or not toPos then return end
        if typeof(fromPos) ~= "Vector3" or typeof(toPos) ~= "Vector3" then return end
        local dist = (toPos - fromPos).Magnitude
        if dist < 0.5 then return end

        while #tracerList >= MAX_TRACERS do
            local old = table.remove(tracerList, 1)
            if old then
                pcall(function()
                    if old.Beam then old.Beam:Destroy() end
                    if old.Near then old.Near:Destroy() end
                    if old.Far then old.Far:Destroy() end
                end)
            end
        end

        local near = Instance.new("Attachment")
        near.WorldPosition = fromPos
        near.Parent = workspace.Terrain
        local far = Instance.new("Attachment")
        far.WorldPosition = fromPos
        far.Parent = workspace.Terrain

        local beam = Instance.new("Beam")
        beam.Name = "BulletTrack"
        beam.Attachment0 = near
        beam.Attachment1 = far
        local col = TRACER_COLOR or Color3.fromRGB(120, 220, 255)
        beam.Color = ColorSequence.new(col)
        local w = tonumber(TRACER_WIDTH) or 0.08
        beam.Width0 = w
        beam.Width1 = w
        beam.FaceCamera = true
        local glow = math.clamp(tonumber(TRACER_GLOW) or 1, 1, 25)
        beam.LightEmission = 1
        beam.LightInfluence = 0
        beam.Brightness = 10000 ^ ((glow - 1) / 24)
        beam.Transparency = NumberSequence.new(0)
        beam.Parent = workspace.Terrain

        local entry = { Beam = beam, Near = near, Far = far }
        table.insert(tracerList, entry)

        local life = tonumber(TRACER_DURATION) or 0.45
        local t0 = tick()
        task.spawn(function()
            while beam.Parent and (tick() - t0) < life do
                local a = math.clamp((tick() - t0) / math.max(life * 0.15, 0.02), 0, 1)
                far.WorldPosition = fromPos:Lerp(toPos, a)
                local fade = math.clamp((tick() - t0) / life, 0, 1)
                beam.Transparency = NumberSequence.new(fade * 0.85)
                RunService.Heartbeat:Wait()
            end
            pcall(function()
                beam:Destroy()
                near:Destroy()
                far:Destroy()
            end)
            for i, e in ipairs(tracerList) do
                if e == entry then table.remove(tracerList, i) break end
            end
        end)
    end
    getgenv().DrawBulletTrack = makeTracer
    RunService.Heartbeat:Connect(function()
        local now = tick()
        for i = #bulletTracers, 1, -1 do
            local tr = bulletTracers[i]
            if not tr or (now - tr.t) > (tr.life or 0.5) then
                if tr then pcall(function() tr.beam:Destroy(); tr.a0:Destroy(); tr.a1:Destroy() end) end
                table.remove(bulletTracers, i)
            end
        end
    end)

    local function clearVoidSnap()
        vfrSnap.cf, vfrSnap.lv, vfrSnap.av = nil, nil, nil
    end
    local function rndSkip(mi, ma, dmi, dma)
        local val = math.random(mi, ma)
        while val >= dmi and val <= dma do val = math.random(mi, ma) end
        return val
    end
    local function snapVoid(hrp)
        if not hrp then return end
        if not vfrSnap.cf then
            local py = hrp.Position.Y
            if py < 3000 and py > -100 then
                vfrSnap.cf = hrp.CFrame
                vfrSnap.lv = hrp.AssemblyLinearVelocity
                vfrSnap.av = hrp.AssemblyAngularVelocity
            else
                return
            end
        end
        local originalCFrame = vfrSnap.cf
        local originalVelocity = vfrSnap.lv or hrp.AssemblyLinearVelocity
        local originalRotVelocity = vfrSnap.av or Vector3.zero
        local base = originalCFrame.Position
        local p = Vector3.new(
            base.X + (math.random() - 0.5) * 8,
            5500,
            base.Z + (math.random() - 0.5) * 8
        )
        hrp.CFrame = CFrame.new(p)
        pcall(function() RunService:UnbindFromRenderStep("RB4_VoidRestore") end)
        RunService:BindToRenderStep("RB4_VoidRestore", 101, function()
            if hrp and hrp.Parent and originalCFrame then
                hrp.CFrame = originalCFrame
                pcall(function()
                    hrp.AssemblyLinearVelocity = originalVelocity
                    hrp.AssemblyAngularVelocity = originalRotVelocity
                end)
            end
            pcall(function() RunService:UnbindFromRenderStep("RB4_VoidRestore") end)
        end)
    end

    local voidPhase, voidLast, voidDur = nil, 0, 0
    local function tickVoid4()
        -- 로비/사격장/시작 전: 보이드 TP 금지
        if (isInLobby and isInLobby())
            or (isLocalInShootingRange and isLocalInShootingRange())
            or (shouldBlockRageActions and shouldBlockRageActions()) then
            clearVoidSnap()
            voidPhase = nil
            getgenv().RB4_VOID_PHASE = nil
            getgenv().RB4_VOID_HIDING = false
            pcall(function() RunService:UnbindFromRenderStep("RB4_VoidRestore") end)
            return
        end
        if not rb4VoidEnabled then
            clearVoidSnap()
            voidPhase = nil
            getgenv().RB4_VOID_PHASE = nil
            getgenv().RB4_VOID_HIDING = false
            return
        end
        local hrp = LocalPlayer.Character and LocalPlayer.Character:FindFirstChild("HumanoidRootPart")
        local now = tick()
        if voidPhase == "shoot" then
            -- ensure out of void on shoot phase
            if hrp and vfrSnap.cf then
                pcall(function() hrp.CFrame = vfrSnap.cf end)
            end
            clearVoidSnap()
            getgenv().RB4_VOID_PHASE = "shoot"
            getgenv().RB4_VOID_HIDING = false
            if now - voidLast >= voidDur then
                voidPhase, voidLast, voidDur = "hide", now, CFG.VoidHide
                getgenv().RB4_VOID_PHASE = "hide"
                getgenv().RB4_VOID_HIDING = true
            end
        elseif voidPhase == "hide" then
            if hrp then snapVoid(hrp) end
            getgenv().RB4_VOID_PHASE = "hide"
            getgenv().RB4_VOID_HIDING = true
            if now - voidLast >= voidDur then
                voidPhase, voidLast, voidDur = "shoot", now, CFG.VoidShoot
                clearVoidSnap()
                getgenv().RB4_VOID_PHASE = "shoot"
                getgenv().RB4_VOID_HIDING = false
            end
        else
            voidPhase, voidLast, voidDur = "shoot", now, CFG.VoidShoot
            getgenv().RB4_VOID_PHASE = "shoot"
            getgenv().RB4_VOID_HIDING = false
        end
    end

    local function worldToScreen(worldPos)
        local v, on = Camera:WorldToViewportPoint(worldPos)
        if not on or v.Z <= 0 then return nil, false end
        return Vector2.new(v.X, v.Y), true
    end

    local function closestInFOV()
        local best, bestDist = nil, math.huge
        local myHRP = LocalPlayer.Character and LocalPlayer.Character:FindFirstChild("HumanoidRootPart")
        local myPos = myHRP and myHRP.Position or nil
        for _, plr in ipairs(Players:GetPlayers()) do
            if plr == LocalPlayer then continue end
            local enemy = true
            pcall(function()
                if type(isEnemy) == "function" then
                    enemy = isEnemy(plr)
                else
                    local a, b = LocalPlayer:GetAttribute("TeamID"), plr:GetAttribute("TeamID")
                    if a ~= nil and b ~= nil and a == b then enemy = false end
                end
            end)
            if not enemy then continue end
            if getgenv().IsTargetNearTripmine and getgenv().IsTargetNearTripmine(plr) then continue end
            if getgenv().IsTargetImmune and getgenv().IsTargetImmune(plr) then continue end
            if shouldSkipKatana(plr) then continue end
            local char = plr.Character
            if not char then continue end
            local hum = char:FindFirstChildOfClass("Humanoid")
            local hrp = char:FindFirstChild("HumanoidRootPart")
            if not hum or not hrp or hum.Health <= 0 then continue end
            local d = myPos and (hrp.Position - myPos).Magnitude or 0
            if d < bestDist then
                bestDist = d
                best = char
            end
        end
        return best
    end

    local function getRageFireInterval()
        -- 0s interval: fire every heartbeat (max rate)
        return 0
    end

    local function rageFire4(targetChar)
        if not rb4Enabled then return end
        if not AUTO_FIRE_ENABLED then return end
        if shouldBlockRageActions and shouldBlockRageActions() then return end
        if getgenv().IsTargetNearTripmine and getgenv().IsTargetNearTripmine(targetChar) then return end
        if getgenv().IsTargetImmune and getgenv().IsTargetImmune(targetChar) then return end
        if not targetChar or not targetChar.Parent then return end
        local hum = targetChar:FindFirstChildOfClass("Humanoid")
        if not hum or hum.Health <= 0 then return end
        local plr = Players:GetPlayerFromCharacter(targetChar)
        if not plr or plr == LocalPlayer then return end
        local okEnemy = true
        pcall(function()
            if type(isEnemy) == "function" then okEnemy = isEnemy(plr) end
        end)
        if not okEnemy then return end
        if shouldSkipKatana and shouldSkipKatana(plr) then return end
        if not Utility or not EnumLibrary then return end
        if not localFighter then
            pcall(function()
                local fc = require(LocalPlayer.PlayerScripts.Controllers.FighterController)
                localFighter = fc and fc.LocalFighter
            end)
        end
        local item = localFighter and localFighter.EquippedItem
        if not item then return end
        if rb4VoidEnabled and voidPhase == "hide" then return end

        local part = targetChar:FindFirstChild("HitboxHead")
            or targetChar:FindFirstChild("HitboxHeadSmall")
            or targetChar:FindFirstChild("Head")
        if not part or not part:IsA("BasePart") then return end
        local oid
        pcall(function() oid = item:Get("ObjectID") end)
        if not oid then return end

        local headPos = part.Position
        local shootPos = headPos + Vector3.new(0, 2.5, 0.5)
        local look = CFrame.lookAt(shootPos, headPos)
        local useItem = ReplicatedStorage.Remotes.Replication.Fighter.UseItem
        local ev = EnumLibrary:ToEnum("StartShooting")
        if not ev then return end
        local data = {
            [utf8.char(1)] = {
                [utf8.char(0)] = Utility:EncodeCFrame(look),
                [utf8.char(1)] = Utility:EncodeCFrame(look),
                [utf8.char(2)] = part,
                [utf8.char(3)] = Utility:EncodeCFrame(CFrame.new(0.43, 0.25, 0.42)),
            },
        }
        local headCF = part.CFrame
        local data2 = {
            [utf8.char(1)] = {
                [utf8.char(0)] = Utility:EncodeCFrame(look),
                [utf8.char(1)] = Utility:EncodeCFrame(headCF),
                [utf8.char(2)] = part,
                [utf8.char(3)] = Utility:EncodeCFrame(headCF:ToObjectSpace(CFrame.new(headPos))),
            },
        }
        for _ = 1, 64 do
            pcall(function() useItem:FireServer(oid, ev, data, nil) end)
            pcall(function() useItem:FireServer(oid, ev, data2, nil) end)
        end
        lastFire = tick()
    end

    pcall(function()
        RunService:UnbindFromRenderStep("Restore_RB4")
        RunService:BindToRenderStep("Restore_RB4", Enum.RenderPriority.Camera.Value - 1, function()
            if not rb4DesyncEnabled or not rb4Enabled or not rb4VisualCF then return end
            local hrp = LocalPlayer.Character and LocalPlayer.Character:FindFirstChild("HumanoidRootPart")
            local hum = LocalPlayer.Character and LocalPlayer.Character:FindFirstChildOfClass("Humanoid")
            if not hrp or not hum then return end
            hrp.CFrame = rb4VisualCF
            local md = hum.MoveDirection
            local spd = (WALK_SPEED and WALK_SPEED > 0) and WALK_SPEED or (hum.WalkSpeed or 16)
            local y = hrp.AssemblyLinearVelocity.Y
            if md.Magnitude > 0.05 then
                hrp.AssemblyLinearVelocity = Vector3.new(md.X * spd, y, md.Z * spd)
            else
                hrp.AssemblyLinearVelocity = Vector3.new(0, y, 0)
            end
        end)
    end)

    RunService.Heartbeat:Connect(function(dt)
        tickVoid4()
        if not rb4Enabled then
            rb4VisualCF = nil
            return
        end
        if shouldBlockRageActions and shouldBlockRageActions() then
            rb4VisualCF = nil
            return
        end
        -- stick until dead; if >6s still alive, switch to another enemy first
        local Rtab = getgenv().RageBot4
        local locked = Rtab and Rtab.LockedChar or nil
        local lockT = (Rtab and Rtab.LockStarted) or 0
        local now = tick()
        local target = nil
        if isRageLockedTargetValid(locked) then
            target = locked
            if typeof(locked) == "Instance" and locked:IsA("Player") then
                target = locked.Character
            end
            if lockT <= 0 then
                if Rtab then Rtab.LockStarted = now end
            elseif (now - lockT) >= (RAGE_LOCK_TIMEOUT or 6) then
                local stuckPlr = Players:GetPlayerFromCharacter(target) or (typeof(locked) == "Instance" and locked:IsA("Player") and locked)
                local alt = nil
                local bestD = math.huge
                local myHRP = LocalPlayer.Character and LocalPlayer.Character:FindFirstChild("HumanoidRootPart")
                local myPos = myHRP and myHRP.Position
                for _, plr in ipairs(Players:GetPlayers()) do
                    if plr == LocalPlayer or plr == stuckPlr then continue end
                    if not isRageLockedTargetValid(plr) then continue end
                    local hrp = plr.Character and plr.Character:FindFirstChild("HumanoidRootPart")
                    if not hrp then continue end
                    local d = myPos and (hrp.Position - myPos).Magnitude or 0
                    if d < bestD then bestD, alt = d, plr.Character end
                end
                if alt then
                    target = alt
                    if Rtab then
                        Rtab.LockedChar = alt
                        Rtab.LockStarted = now
                    end
                else
                    if Rtab then Rtab.LockStarted = now end
                end
            end
        else
            target = closestInFOV()
            if Rtab then
                Rtab.LockedChar = target
                Rtab.LockStarted = target and now or 0
            end
        end
        if not target then
            rb4VisualCF = nil
            if Rtab then Rtab.LockedChar = nil; Rtab.LastTarget = nil end
            if not rbEnabled then getgenv().RAGEBOT_ACTIVE_TARGET = nil end
            return
        end
        do
            local plr = Players:GetPlayerFromCharacter(target)
            getgenv().RAGEBOT_ACTIVE_TARGET = plr or target
            if Rtab then
                Rtab.LastTarget = plr or target
                Rtab.LockedChar = target
            end
        end
        local thrp = target:FindFirstChild("HumanoidRootPart")
        local thead = target:FindFirstChild("HitboxHead")
            or target:FindFirstChild("HitboxHeadSmall")
            or target:FindFirstChild("Head")
            or thrp
        local hrp = LocalPlayer.Character and LocalPlayer.Character:FindFirstChild("HumanoidRootPart")
        local hum = LocalPlayer.Character and LocalPlayer.Character:FindFirstChildOfClass("Humanoid")
        if thrp and hrp and hum and thead then
            local headPos = thead.Position
            local atk = headPos + Vector3.new(0, 2.5, 0.5)
            local destCF = CFrame.lookAt(atk, headPos)
            rb4VisualCF = hrp.CFrame
            local tPlayer = Players:GetPlayerFromCharacter(target)
            if rb4DesyncEnabled and tPlayer then
                if not DesyncEngine.active or DesyncEngine.currentTarget ~= tPlayer then
                    DesyncStart(tPlayer, "rb4")
                end
            else
                if DesyncEngine.tag == "rb4" then DesyncStop() end
            end
            pcall(function()
                hrp.CFrame = destCF
                hrp.AssemblyLinearVelocity = Vector3.zero
                hrp.AssemblyAngularVelocity = Vector3.zero
            end)
        end
        rageFire4(target)
    end)

    -- 추가 발사 (매 렌더 프레임 헤드 다발)
    RunService.RenderStepped:Connect(function()
        if not rb4Enabled then return end
        if AUTO_FIRE_ENABLED == false then return end
        if shouldBlockRageActions and shouldBlockRageActions() then return end
        local Rtab = getgenv().RageBot4
        local target = Rtab and Rtab.LockedChar
        if not target or not target.Parent then return end
        if rb4VoidEnabled and voidPhase == "hide" then return end
        rageFire4(target)
    end)

    getgenv().RageBot4 = {
        setEnabled = function(v)
            rb4Enabled = v and true or false
            if not rb4Enabled then
                rb4VisualCF = nil
                local R = getgenv().RageBot4
                if R then R.LockedChar = nil; R.LastTarget = nil end
                pcall(function()
                    if DesyncEngine and DesyncEngine.tag == "rb4" then DesyncStop() end
                end)
            end
        end,
        setDesync = function(v)
            rb4DesyncEnabled = v and true or false
            if not rb4DesyncEnabled then
                rb4VisualCF = nil
                pcall(function()
                    if DesyncEngine and DesyncEngine.tag == "rb4" then DesyncStop() end
                end)
            end
        end,
        setVoid = function(v)
            rb4VoidEnabled = v and true or false
            if not rb4VoidEnabled then
                clearVoidSnap()
                voidPhase = nil
            end
        end,
        setAntiKatana = function(v) AntiKatana.Enabled = v and true or false end,
        setTracer = function(v) TRACER_ENABLED = v and true or false end,
        CFG = CFG,
    }
end

function initLunaraExtras()
    local config = rawget(_G, "LunaraConfig") or {
        voidspam = {
            enabled = false,
            shoot_min = 0.5, shoot_max = 0.7,
            hide_min = 0.2, hide_max = 0.35,
            phase = nil, lastswitch = 0, currentduration = 0,
        },
        antikatana = true,
        levelSpoof = { enabled = false, value = 9999 },
        winStreakSpoof = { enabled = false, value = 9999 },
        hitNotif = { enabled = false },
    }
    _G.LunaraConfig = config

    local katanausers = {}
    local antikatana = false
    task.spawn(function()
        local lp = LocalPlayer
        if not lp:FindFirstChild("PlayerScripts") then
            pcall(function() lp.PlayerScriptsAdded:Wait() end)
        end
        local katana, attempts = nil, 0
        while attempts < 12 do
            pcall(function()
                local m = lp.PlayerScripts.Modules.Items:FindFirstChild("Katana", true)
                if m then katana = require(m) end
            end)
            if not katana then
                for _, m in pairs(lp.PlayerScripts:GetDescendants()) do
                    if m.Name == "Katana" and m:IsA("ModuleScript") then
                        local ok, res = pcall(require, m)
                        if ok then katana = res break end
                    end
                end
            end
            if katana and type(katana) == "table" and katana.StartAiming then break end
            attempts = attempts + 1
            task.wait(1)
        end
        if katana and type(katana) == "table" and katana.StartAiming then
            local old = katana.StartAiming
            katana.StartAiming = function(self, force)
                local fighter = self.ClientFighter
                local player = fighter and fighter.Player
                if player then
                    katanausers[player] = true
                    local dur = (self.Info and self.Info.DeflectDuration) or 0.6
                    task.delay(dur, function() katanausers[player] = nil end)
                end
                return old(self, force)
            end
        end
    end)

    local function isKatanaDeflecting(plr)
        if not plr then return false end
        if katanausers[plr] == true then return true end
        local char = plr.Character
        if not char then return false end
        local ok, def = pcall(function() return char:GetAttribute("Deflecting") or char:GetAttribute("IsDeflecting") end)
        if ok and def then return true end
        for _, c in ipairs(char:GetChildren()) do
            local n = string.lower(c.Name)
            if n:find("deflect") or n:find("katana") and c:IsA("Tool") then
            end
            if n:find("deflect") then return true end
        end
        return false
    end
    getgenv().InstanceIsKatanaDeflecting = isKatanaDeflecting
    local vfrSnap = { cf = nil, lv = nil, av = nil, active = false }

    local function randVs(a, b)
        a, b = tonumber(a) or 0.4, tonumber(b) or 0.6
        if a > b then a, b = b, a end
        return a + math.random() * (b - a)
    end

    local function clrVoidSnap()
        vfrSnap.cf, vfrSnap.lv, vfrSnap.av, vfrSnap.active = nil, nil, nil, false
    end

    local function voidHrp()
        local char = LocalPlayer.Character
        return char and char:FindFirstChild("HumanoidRootPart")
    end

    local function anyRagebotOn()
        return rbEnabled or rb2Enabled or rb3Enabled or rb4Enabled or rb0Enabled or DESYNC_ENABLED
            or (OrbitCFG and OrbitCFG.Active)
    end

    -- RB1-style void desync (main.lua reference): TP void then same-frame restore
    local function snapVoid(hrp)
        if not hrp or flyEnabled then return end
        local py = hrp.Position.Y
        -- seed safe CF only from non-void positions
        if not vfrSnap.cf then
            if py < 3000 and py > -100 then
                vfrSnap.cf = hrp.CFrame
                pcall(function()
                    vfrSnap.lv = hrp.AssemblyLinearVelocity
                    vfrSnap.av = hrp.AssemblyAngularVelocity
                end)
            else
                return
            end
        else
            -- keep SafeCF walking with player when visually restored
            local hum = LocalPlayer.Character and LocalPlayer.Character:FindFirstChildOfClass("Humanoid")
            if hum then
                local md = hum.MoveDirection
                if md and md.Magnitude > 0.05 then
                    local spd = (WALK_SPEED and WALK_SPEED > 0) and WALK_SPEED or (hum.WalkSpeed or 16)
                    vfrSnap.cf = vfrSnap.cf + md * spd * 0.016
                end
            end
        end
        vfrSnap.active = true

        local originalCFrame = vfrSnap.cf
        local originalVelocity, originalRotVelocity
        pcall(function()
            originalVelocity = hrp.AssemblyLinearVelocity
            originalRotVelocity = hrp.AssemblyAngularVelocity
        end)

        local base = originalCFrame.Position
        local voidPos = Vector3.new(
            base.X + (math.random() - 0.5) * 8,
            5500,
            base.Z + (math.random() - 0.5) * 8
        )
        -- network/server position = void
        hrp.CFrame = CFrame.new(voidPos)

        -- same-frame visual restore (RB1 desync style)
        pcall(function() RunService:UnbindFromRenderStep("VoidSpamRestore") end)
        RunService:BindToRenderStep("VoidSpamRestore", 101, function()
            if hrp and hrp.Parent and originalCFrame then
                hrp.CFrame = originalCFrame
                pcall(function()
                    if originalVelocity then hrp.AssemblyLinearVelocity = originalVelocity end
                    if originalRotVelocity then hrp.AssemblyAngularVelocity = originalRotVelocity end
                end)
                pcall(function()
                    local hum = LocalPlayer.Character and LocalPlayer.Character:FindFirstChildOfClass("Humanoid")
                    if hum and WALK_SPEED then hum.WalkSpeed = WALK_SPEED end
                end)
            end
            pcall(function() RunService:UnbindFromRenderStep("VoidSpamRestore") end)
        end)
    end


    local function tickVoidSpam()
        local vs = config.voidspam
        if (isInLobby and isInLobby())
            or (isLocalInShootingRange and isLocalInShootingRange())
            or (shouldBlockRageActions and shouldBlockRageActions()) then
            if vs then vs.phase = nil end
            getgenv().VOID_SPAM_HIDING = false
            pcall(function() if clrVoidSnap then clrVoidSnap() end end)
            return
        end
        if not vs or not vs.enabled or not anyRagebotOn() then
            if vfrSnap.active and vfrSnap.cf then
                local hrp = voidHrp()
                if hrp and voidDesyncOn() then
                    pcall(function() hrp.CFrame = vfrSnap.cf end)
                end
            end
            clrVoidSnap()
            if vs then vs.phase = nil end
            getgenv().VOID_SPAM_HIDING = false
            return
        end
        local hasEnemy = false
        pcall(function()
            for _, plr in ipairs(Players:GetPlayers()) do
                if plr ~= LocalPlayer and plr.Character then
                    local h = plr.Character:FindFirstChildOfClass("Humanoid")
                    if h and h.Health > 0 then
                        local a = LocalPlayer:GetAttribute("TeamID")
                        local b = plr:GetAttribute("TeamID")
                        if not (a and b and a == b) then
                            hasEnemy = true
                            break
                        end
                    end
                end
            end
        end)
        if not hasEnemy then
            local hrp = voidHrp()
            if hrp and vfrSnap.cf then
                pcall(function() hrp.CFrame = vfrSnap.cf end)
            end
            clrVoidSnap()
            getgenv().VOID_SPAM_HIDING = false
            if vs then vs.phase = "shoot" end
            return
        end
        local now = tick()
        if not vs.phase then
            vs.phase = "shoot"
            vs.lastswitch = now
            vs.currentduration = randVs(vs.shoot_min, vs.shoot_max)
        end
        local elapsed = now - (vs.lastswitch or 0)
        local hrp = voidHrp()

        if vs.phase == "shoot" then
            getgenv().VOID_SPAM_HIDING = false
            if hrp then
                -- refresh every frame so walkspeed / movement stays while void desync
                vfrSnap.cf = hrp.CFrame
                vfrSnap.lv = hrp.AssemblyLinearVelocity
                vfrSnap.av = hrp.AssemblyAngularVelocity
                pcall(function()
                    local hum = LocalPlayer.Character and LocalPlayer.Character:FindFirstChildOfClass("Humanoid")
                    if hum and WALK_SPEED then hum.WalkSpeed = WALK_SPEED end
                end)
            end
            vfrSnap.active = false
            if elapsed >= (vs.currentduration or 0.5) then
                vs.phase = "hide"
                vs.currentduration = randVs(vs.hide_min, vs.hide_max)
                vs.lastswitch = now
                getgenv().VOID_SPAM_HIDING = true
            end
        elseif vs.phase == "hide" then
            getgenv().VOID_SPAM_HIDING = true
            if hrp then
                snapVoid(hrp)
            end
            if elapsed >= (vs.currentduration or 0.3) then
                vs.phase = "shoot"
                vs.currentduration = randVs(vs.shoot_min, vs.shoot_max)
                vs.lastswitch = now
                if hrp and vfrSnap.cf then
                    pcall(function() hrp.CFrame = vfrSnap.cf end)
                end
                clrVoidSnap()
            end
        end
    end

    RunService.Heartbeat:Connect(function()
        pcall(tickVoidSpam)
    end)
    task.spawn(function()
        while true do
            pcall(function()
                local lp = LocalPlayer
                local lv = config.levelSpoof.value or 9999
                local wv = config.winStreakSpoof.value or 9999
                if config.levelSpoof.enabled then
                    lp:SetAttribute("Level", lv)
                    lp:SetAttribute("level", lv)
                    local ls = lp:FindFirstChild("leaderstats")
                    if ls then
                        for _, n in ipairs({"Level", "level", "Lvl"}) do
                            local v = ls:FindFirstChild(n)
                            if v and v:IsA("ValueBase") then v.Value = lv end
                        end
                    end
                end
                if config.winStreakSpoof.enabled then
                    lp:SetAttribute("WinStreak", wv)
                    lp:SetAttribute("Win Streak", wv)
                    lp:SetAttribute("Streak", wv)
                    local ls = lp:FindFirstChild("leaderstats")
                    if ls then
                        for _, n in ipairs({"Win Streak", "WinStreak", "Streak", "Winstreak"}) do
                            local v = ls:FindFirstChild(n)
                            if v and v:IsA("ValueBase") then v.Value = wv end
                        end
                    end
                    -- PlayerGui / 기타 표시 값
                    pcall(function()
                        for _, d in ipairs(lp:GetDescendants()) do
                            if d:IsA("ValueBase") then
                                local nm = string.lower(d.Name)
                                if nm:find("winstreak") or nm:find("win streak") or nm == "streak" then
                                    d.Value = wv
                                end
                            end
                        end
                    end)
                end
            end)
            task.wait(0.15)
        end
    end)
    local lastHp = {}
    RunService.Heartbeat:Connect(function()
        if not config.hitNotif.enabled then return end
        pcall(function()
            for _, plr in ipairs(Players:GetPlayers()) do
                if plr ~= LocalPlayer and plr.Character then
                    local hum = plr.Character:FindFirstChildOfClass("Humanoid")
                    if hum then
                        local prev = lastHp[plr] or hum.Health
                        local cur = hum.Health
                        if cur < prev - 0.5 then
                            local dmg = math.floor(prev - cur + 0.5)
                            print(string.format("[Hit] %s for %d", plr.Name, dmg))
                            local ok, label = pcall(function()
                                local t = Drawing.new("Text")
                                t.Text = string.format("hit %s for %d", plr.Name, dmg)
                                t.Size = 16
                                t.Center = true
                                t.Outline = true
                                t.Color = Color3.fromRGB(255, 80, 80)
                                t.Position = Vector2.new(Camera.ViewportSize.X/2, Camera.ViewportSize.Y * 0.35)
                                t.Visible = true
                                return t
                            end)
                            if ok and label then
                                task.delay(2, function()
                                    pcall(function() label:Remove() end)
                                end)
                            end
                        end
                        lastHp[plr] = cur
                    end
                end
            end
        end)
    end)
    getgenv().LunaraExtras = {
        config = config,
        setVoidSpam = function(v)
            config.voidspam.enabled = v and true or false
            if not v then
                config.voidspam.phase = nil
                clrVoidSnap()
            else
                config.voidspam.lastswitch = tick()
                config.voidspam.phase = "shoot"
                local a = config.voidspam.shoot_min or 1
                local b = config.voidspam.shoot_max or a
                config.voidspam.currentduration = a + math.random() * math.max(0, b - a)
            end
        end,
        setAntiKatana = function(v) config.antikatana = v and true or false end,
        setLevelSpoof = function(on, val)
            config.levelSpoof.enabled = on and true or false
            if val then config.levelSpoof.value = val end
        end,
        setWinStreakSpoof = function(on, val)
            config.winStreakSpoof.enabled = on and true or false
            if val then config.winStreakSpoof.value = val end
        end,
        setHitNotif = function(v) config.hitNotif.enabled = v and true or false end,
        setVoidTimes = function(shoot, hide)
            if shoot then
                shoot = math.clamp(tonumber(shoot) or 1, 0.1, 2)
                config.voidspam.shoot_min = shoot
                config.voidspam.shoot_max = shoot
            end
            if hide then
                hide = math.clamp(tonumber(hide) or 1, 0.1, 2)
                config.voidspam.hide_min = hide
                config.voidspam.hide_max = hide
            end
        end,
    }
end
task.defer(function()
    local BYPASS = {
        Slingshot = true, Bow = true, Exogun = true, Spray = true,
        Flamethrower = true, ["Grenade Launcher"] = true, RPG = true,
        Crossbow = true, Daggers = true,
    }
    local kusers = {}

    task.spawn(function()
        local attempts = 0
        while attempts < 20 do
            local katana
            pcall(function()
                local m = LocalPlayer.PlayerScripts.Modules.Items:FindFirstChild("Katana", true)
                if m then katana = require(m) end
            end)
            if not katana then
                pcall(function()
                    for _, m in pairs(LocalPlayer.PlayerScripts:GetDescendants()) do
                        if m.Name == "Katana" and m:IsA("ModuleScript") then
                            local ok, res = pcall(require, m)
                            if ok and type(res) == "table" and res.StartAiming then
                                katana = res
                                break
                            end
                        end
                    end
                end)
            end
            if katana and type(katana) == "table" and katana.StartAiming then
                local prev = katana.StartAiming
                katana.StartAiming = function(self, force)
                    local fighter = self.ClientFighter
                    local player = fighter and fighter.Player
                    if player then
                        kusers[player] = true
                        local dur = (self.Info and self.Info.DeflectDuration) or 0.6
                        task.delay(dur, function() kusers[player] = nil end)
                    end
                    return prev(self, force)
                end
                print("[mineminyee] Anti-Katana StartAiming hooked (Kicia)")
                break
            end
            attempts = attempts + 1
            task.wait(1)
        end
    end)

    getgenv().InstanceIsKatanaDeflecting = function(player)
        if not player then return false end
        local cfg = getgenv().LunaraExtras and getgenv().LunaraExtras.config
        if kusers[player] == true then return true end
        local char = player.Character
        if not char then return false end
        local ok, def = pcall(function()
            return char:GetAttribute("Deflecting") or char:GetAttribute("IsDeflecting")
        end)
        if ok and def then return true end
        for _, c in ipairs(char:GetChildren()) do
            if string.lower(c.Name):find("deflect") then return true end
        end
        return false
    end

    getgenv().AntiKatana = getgenv().AntiKatana or { Enabled = true }
    getgenv().IsItemKatanaDeflecting = isItemKatanaDeflecting

    getgenv().IsKatanaDeflectBypassWeapon = function(name)
        return BYPASS[name] == true
    end
end)
getgenv().ForceDisableFeature = function(name)
    name = tostring(name or ""):lower()
    if name == "silent" or name == "all" then
        SILENT_AIM_ENABLED = false
    end
    if name == "aimbot" or name == "all" then
        AIMBOT_ENABLED = false
        pcall(stopAimbot)
    end
    if name == "legit" or name == "aimbot" or name == "all" then
        LEGIT_AIMBOT_ENABLED = false
        pcall(stopLegitAimbot)
    end
    if name == "tp" or name == "third" or name == "all" then
        pcall(disableThirdPerson)
    end
    if name == "autoweapon" or name == "all" then
        AUTO_WEAPON_ENABLED = false
        WEAPON_SPEED_ENABLED = false
        pcall(refreshWeaponMods)
    end
    if name == "norecoil" or name == "all" then
        NO_RECOIL_ENABLED = false
        pcall(disableNoRecoil)
    end
    if name == "rb1" or name == "all" then
        rbEnabled = false
        pcall(stopRageBot)
    end
    if name == "rb2" or name == "all" then
        rb2Enabled = false
        pcall(stopRageBot2)
    end
    if name == "rb3" or name == "all" then
        rb3Enabled = false
        pcall(stopRageBot3)
    end
    if name == "rb4" or name == "all" then
        rb4Enabled = false
        pcall(function() if getgenv().RageBot4 then getgenv().RageBot4.setEnabled(false) end end)
    end
    if name == "void" or name == "all" then
        pcall(function()
            local LE = getgenv().LunaraExtras
            if LE and LE.setVoidSpam then LE.setVoidSpam(false) end
        end)
    end
    if name == "fly" or name == "all" then
        flyEnabled = false
    end
    if name == "desync" or name == "all" then
        rb1DesyncEnabled = false
        rb3DesyncEnabled = false
        rb4DesyncEnabled = false
        pcall(function() if DesyncStop then DesyncStop() end end)
        pcall(function() if rb1StopDesync then rb1StopDesync() end end)
    end
end
if not getgenv().IsTargetNearTripmine then
    getgenv().IsTargetNearTripmine = function() return false end
end
if not getgenv().IsTargetImmune then
    getgenv().IsTargetImmune = function() return false end
end
task.defer(function()
    local CS = game:GetService("CollectionService")
    local TAG = "SubspaceTripmine"
    local TRIPMINE_RANGE = 16
    local tracked = {}
    local ESP = {
        Enabled = false,
        MaxDistance = 300,
        TextSize = 14,
        Color = Color3.fromRGB(255, 50, 50),
    }

    local function createLabel()
        local ok, label = pcall(function()
            local t = Drawing.new("Text")
            t.Center = true
            t.Outline = true
            t.Font = 2
            t.Size = ESP.TextSize
            t.Color = ESP.Color
            t.Visible = false
            return t
        end)
        if ok then return label end
        return nil
    end

    local function destroyEntry(tm)
        local e = tracked[tm]
        if not e then return end
        if e.label then
            pcall(function() e.label.Visible = false end)
            pcall(function() e.label:Remove() end)
            e.label = nil
        end
        if e.destroyConn then pcall(function() e.destroyConn:Disconnect() end) e.destroyConn = nil end
        if e.ancestryConn then pcall(function() e.ancestryConn:Disconnect() end) e.ancestryConn = nil end
        tracked[tm] = nil
    end

    local function track(tm)
        if not tm or tracked[tm] then return end
        task.spawn(function()
            local hitbox = tm:FindFirstChild("Hitbox")
            if not hitbox then
                pcall(function() hitbox = tm:WaitForChild("Hitbox", 3) end)
            end
            if not hitbox or not hitbox:IsA("BasePart") or not tm.Parent then return end
            local entry = {
                hitbox = hitbox,
                label = createLabel(),
            }
            entry.destroyConn = hitbox.Destroying:Connect(function()
                destroyEntry(tm)
            end)
            pcall(function()
                tm.Destroying:Connect(function() destroyEntry(tm) end)
            end)
            pcall(function()
                entry.ancestryConn = tm.AncestryChanged:Connect(function(_, parent)
                    if not parent then destroyEntry(tm) end
                end)
            end)
            tracked[tm] = entry
        end)
    end

    pcall(function()
        for _, tm in ipairs(CS:GetTagged(TAG)) do track(tm) end
        CS:GetInstanceAddedSignal(TAG):Connect(track)
        CS:GetInstanceRemovedSignal(TAG):Connect(destroyEntry)
    end)

    local function nameLooksLikeMine(n)
        if type(n) ~= "string" then return false end
        return n == "Subspace Tripmine" or n == "SubspaceTripmine" or n:find("Tripmine") ~= nil
    end

    pcall(function()
        workspace.DescendantAdded:Connect(function(obj)
            if nameLooksLikeMine(obj.Name) and (obj:IsA("Model") or obj:IsA("BasePart")) then
                track(obj)
            end
        end)
    end)
    task.spawn(function()
        task.wait(1.5)
        pcall(function()
            for _, obj in ipairs(workspace:GetDescendants()) do
                if nameLooksLikeMine(obj.Name) and (obj:IsA("Model") or obj:IsA("BasePart")) then
                    track(obj)
                end
            end
        end)
    end)

    local function minePos(entry)
        local h = entry and entry.hitbox
        if h and h.Parent then return h.Position end
        return nil
    end
    local function posNearAnyMine(pos)
        if not pos then return false end
        local r2 = TRIPMINE_RANGE * TRIPMINE_RANGE
        for tm, entry in pairs(tracked) do
            if not tm or not tm.Parent then
                destroyEntry(tm)
            else
                local mp = minePos(entry)
                if mp then
                    local d = pos - mp
                    if d:Dot(d) <= r2 then
                        return true
                    end
                end
            end
        end
        return false
    end
    local function isTargetNearTripmine(target)
        if not ANTI_MINE_ENABLED then return false end
        if not target then return false end
        local char = target
        if typeof(target) == "Instance" and target:IsA("Player") then
            char = target.Character
        end
        if not char then return false end
        local hrp = char:FindFirstChild("HumanoidRootPart") or char:FindFirstChild("HitboxBody")
        if not hrp then return false end
        return posNearAnyMine(hrp.Position)
    end

    local function hideAllEsp()
        for tm, entry in pairs(tracked) do
            if entry.label then
                pcall(function() entry.label.Visible = false end)
            end
            if (not tm) or (not tm.Parent) or (not entry.hitbox) or (not entry.hitbox.Parent) then
                destroyEntry(tm)
            end
        end
    end

    local function updateEsp()
        if not ESP.Enabled then
            hideAllEsp()
            return
        end
        local char = LocalPlayer.Character
        local root = char and (char:FindFirstChild("HumanoidRootPart") or char:FindFirstChild("HitboxBody"))
        local cam = workspace.CurrentCamera
        if not root or not cam then
            hideAllEsp()
            return
        end
        local rootPos = root.Position
        local maxDistSq = ESP.MaxDistance * ESP.MaxDistance
        local dead = {}
        for tm, entry in pairs(tracked) do
            local hitbox = entry.hitbox
            if (not tm) or (not tm.Parent) or (not hitbox) or (not hitbox.Parent) then
                dead[#dead + 1] = tm
            end
        end
        for i = 1, #dead do destroyEntry(dead[i]) end
        for tm, entry in pairs(tracked) do
            local hitbox = entry.hitbox
            local label = entry.label
            if not hitbox or not hitbox.Parent or not tm.Parent then
                destroyEntry(tm)
            elseif label then
                local pos = hitbox.Position
                local offset = pos - rootPos
                local distSq = offset:Dot(offset)
                if distSq > maxDistSq then
                    label.Visible = false
                else
                    local screenPos, onScreen = cam:WorldToViewportPoint(pos)
                    if onScreen and screenPos.Z > 0 then
                        local meters = math.floor(math.sqrt(distSq) + 0.5)
                        label.Text = string.format("TRIPMINE | %dm", meters)
                        label.Size = ESP.TextSize
                        label.Color = ESP.Color
                        label.Position = Vector2.new(screenPos.X, screenPos.Y)
                        label.Visible = true
                    else
                        label.Visible = false
                    end
                end
            end
        end
    end

    local reconcileAcc = 0
    RunService.RenderStepped:Connect(function(dt)
        pcall(updateEsp)
        reconcileAcc = reconcileAcc + (dt or 0.016)
        if reconcileAcc > 0.5 then
            reconcileAcc = 0
            pcall(function()
                local alive = {}
                for _, tm in ipairs(CS:GetTagged(TAG)) do
                    alive[tm] = true
                    if not tracked[tm] then track(tm) end
                end
                for tm in pairs(tracked) do
                    if not alive[tm] or not tm.Parent then
                        destroyEntry(tm)
                    end
                end
            end)
        end
    end)

    getgenv().IsTargetNearTripmine = isTargetNearTripmine
    getgenv().IsNearEnemyTripmine = function()
        return false
    end
    getgenv().NEAR_ENEMY_TRIPMINE = false
    getgenv().TRIPMINE_RANGE = TRIPMINE_RANGE
    getgenv().TripmineESP = ESP
    getgenv().SetTripmineESP = function(v)
        ESP.Enabled = v and true or false
        if not ESP.Enabled then hideAllEsp() end
    end

    print("[mineminyee] Tripmine gate: skip rage/TP if TARGET within " .. TRIPMINE_RANGE .. "m of mine")
end)
task.defer(function()
    local hooked = false
    local function tryHook()
        if hooked then return end
        local ok, gun = pcall(function()
            return require(LocalPlayer.PlayerScripts.Modules.ItemTypes.Gun)
        end)
        if not ok or type(gun) ~= "table" then return end
        local oldLocal = rawget(gun, "_LocalTracers")
        if type(oldLocal) == "function" then
            gun._LocalTracers = function(self, data, ...)
                local r = oldLocal(self, data, ...)
                if TRACER_ENABLED and data then
                    pcall(function()
                        local rays = data.RaycastResults or data.raycastResults or {}
                        local muzzle = nil
                        pcall(function()
                            if self.ViewModel and self.ViewModel.GetMuzzlePosition then
                                muzzle = self.ViewModel:GetMuzzlePosition()
                            end
                        end)
                        if not muzzle then
                            muzzle = workspace.CurrentCamera and workspace.CurrentCamera.CFrame.Position
                        end
                        for _, ray in pairs(rays) do
                            local s = (type(ray) == "table" and (ray.StartPosition or ray.startPosition)) or muzzle
                            local e = (type(ray) == "table" and (ray.Position or ray.position or ray.EndPosition)) or nil
                            if s and e and getgenv().DrawBulletTrack then
                                getgenv().DrawBulletTrack(s, e)
                            end
                        end
                    end)
                end
                return r
            end
            hooked = true
            print("[mineminyee] Bullet Track hooked via _LocalTracers")
            return
        end
        if type(gun.StartShooting) == "function" and not gun.__bulletTrackWrapped then
            local prev = gun.StartShooting
            gun.StartShooting = function(self, ...)
                local results = { prev(self, ...) }
                if TRACER_ENABLED then
                    pcall(function()
                        local cam = workspace.CurrentCamera
                        local from = cam and cam.CFrame.Position
                        local look = cam and (cam.CFrame.Position + cam.CFrame.LookVector * 200)
                        if from and look and getgenv().DrawBulletTrack then
                        end
                    end)
                end
                return table.unpack(results)
            end
            gun.__bulletTrackWrapped = true
            hooked = true
            print("[mineminyee] Bullet Track StartShooting wrap (fallback)")
        end
    end
    for i = 1, 15 do
        tryHook()
        if hooked then break end
        task.wait(1)
    end
end)
pcall(function()
    initMiscExtras()
end)

-- HydronX Ragebot
local HydronRage = {
    Enabled = false,
    TeamCheck = true,
    Desync = true,
    HeightOffset = 2.5,
    Interval = 0,
    CurrentTarget = nil,
    LastFire = 0,
    SavedCF = nil,
    SavedVel = nil,
    SavedRotVel = nil,
}
getgenv().HydronRage = HydronRage

local function hydronStopRage()
    HydronRage.Enabled = false
    hydronRbEnabled = false
    HydronRage.CurrentTarget = nil
    HydronRage.SavedCF = nil
    HydronRage.SavedVel = nil
    HydronRage.SavedRotVel = nil
    pcall(function() RunService:UnbindFromRenderStep("HydronRagebotRestore") end)
end

local function hydronGetClosestTarget()
    local myRoot = LocalPlayer.Character and LocalPlayer.Character:FindFirstChild("HumanoidRootPart")
    if not myRoot then return nil end
    if shouldBlockRageActions and shouldBlockRageActions() then return nil end
    local closest, closestDist = nil, math.huge
    for _, plr in ipairs(Players:GetPlayers()) do
        if plr == LocalPlayer then continue end
        local okEnemy = true
        if HydronRage.TeamCheck then
            local a = LocalPlayer:GetAttribute("TeamID")
            local b = plr:GetAttribute("TeamID")
            if a ~= nil and b ~= nil and a == b then okEnemy = false end
            if LocalPlayer.Team and plr.Team and LocalPlayer.Team == plr.Team then okEnemy = false end
            local ch = plr.Character
            local ca = LocalPlayer.Character and LocalPlayer.Character:GetAttribute("TeamID")
            local cb = ch and ch:GetAttribute("TeamID")
            if ca ~= nil and cb ~= nil and ca == cb then okEnemy = false end
        end
        if not okEnemy then continue end
        if getgenv().IsTargetImmune and getgenv().IsTargetImmune(plr) then continue end
        if getgenv().IsTargetNearTripmine and getgenv().IsTargetNearTripmine(plr) then continue end
        local char = plr.Character
        if not char then continue end
        local hum = char:FindFirstChildOfClass("Humanoid")
        if not hum or hum.Health <= 0 then continue end
        local head = char:FindFirstChild("HitboxHead") or char:FindFirstChild("Head") or char:FindFirstChild("HitboxHeadSmall")
        local root = char:FindFirstChild("HumanoidRootPart")
        if not head or not root then continue end
        local d = (myRoot.Position - root.Position).Magnitude
        if d < closestDist then
            closestDist = d
            closest = plr
        end
    end
    return closest
end

local function hydronEncodeCF(cf)
    local ok, v = pcall(function()
        local U = require(ReplicatedStorage.Modules.Utility)
        return U:EncodeCFrame(cf)
    end)
    if ok and v ~= nil then return v end
    local rx, ry, rz = cf:ToOrientation()
    return {
        [utf8.char(0)] = cf.X,
        [utf8.char(1)] = cf.Y,
        [utf8.char(2)] = cf.Z,
        [utf8.char(3)] = rx,
        [utf8.char(4)] = ry,
        [utf8.char(5)] = rz,
    }
end

local function hydronFireAt(targetHead, shootPos)
    pcall(function()
        local enums = require(ReplicatedStorage.Modules.EnumLibrary)
        local fc = require(LocalPlayer.PlayerScripts.Controllers.FighterController)
        local lf = fc and fc.LocalFighter
        local item = lf and lf.EquippedItem
        if not item then return end
        local oid
        pcall(function() oid = item:Get("ObjectID") end)
        if not oid then return end
        local useItem = ReplicatedStorage.Remotes.Replication.Fighter.UseItem
        local look = CFrame.lookAt(shootPos, targetHead.Position)
        local data = {
            [utf8.char(1)] = {
                [utf8.char(0)] = hydronEncodeCF(look),
                [utf8.char(1)] = hydronEncodeCF(look),
                [utf8.char(2)] = targetHead,
                [utf8.char(3)] = hydronEncodeCF(CFrame.new(0.43, 0.25, 0.42)),
            },
        }
        local ev = enums:ToEnum("StartShooting")
        if ev then
            for _ = 1, 32 do
                useItem:FireServer(oid, ev, data, nil)
            end
        end
    end)
end

RunService.Heartbeat:Connect(function()
    if not HydronRage.Enabled then
        HydronRage.SavedCF = nil
        HydronRage.SavedVel = nil
        HydronRage.SavedRotVel = nil
        pcall(function() RunService:UnbindFromRenderStep("HydronRagebotRestore") end)
        return
    end

    if shouldBlockRageActions and shouldBlockRageActions() then return end

    local char = LocalPlayer.Character
    local root = char and char:FindFirstChild("HumanoidRootPart")
    local hum = char and char:FindFirstChildOfClass("Humanoid")
    if not root or not hum or hum.Health <= 0 then return end

    local target = hydronGetClosestTarget()
    if not target then
        HydronRage.CurrentTarget = nil
        HydronRage.SavedCF = nil
        return
    end

    HydronRage.CurrentTarget = target
    getgenv().RAGEBOT_ACTIVE_TARGET = target

    local targetChar = target.Character
    local targetHead = targetChar and (
        targetChar:FindFirstChild("HitboxHead")
        or targetChar:FindFirstChild("Head")
        or targetChar:FindFirstChild("HitboxHeadSmall")
    )
    local targetRoot = targetChar and targetChar:FindFirstChild("HumanoidRootPart")
    if not targetHead or not targetRoot then return end

    local destCF = CFrame.lookAt(
        targetHead.Position + Vector3.new(0, HydronRage.HeightOffset, 0),
        targetHead.Position
    )

    if HydronRage.Desync then
        HydronRage.SavedCF = root.CFrame
        HydronRage.SavedVel = root.AssemblyLinearVelocity
        HydronRage.SavedRotVel = root.AssemblyAngularVelocity
        pcall(function()
            root.CFrame = destCF
            root.AssemblyLinearVelocity = Vector3.zero
            root.AssemblyAngularVelocity = Vector3.zero
        end)
        pcall(function() RunService:UnbindFromRenderStep("HydronRagebotRestore") end)
        RunService:BindToRenderStep("HydronRagebotRestore", 101, function()
            local c = LocalPlayer.Character
            local r = c and c:FindFirstChild("HumanoidRootPart")
            if r and HydronRage.SavedCF then
                r.CFrame = HydronRage.SavedCF
                pcall(function()
                    r.AssemblyLinearVelocity = HydronRage.SavedVel or Vector3.zero
                    r.AssemblyAngularVelocity = HydronRage.SavedRotVel or Vector3.zero
                end)
            end
            pcall(function() RunService:UnbindFromRenderStep("HydronRagebotRestore") end)
        end)
    else
        pcall(function()
            root.CFrame = destCF
            root.AssemblyLinearVelocity = Vector3.zero
            root.AssemblyAngularVelocity = Vector3.zero
        end)
    end

    local now = tick()
    if now - HydronRage.LastFire < (HydronRage.Interval or 0) then return end
    HydronRage.LastFire = now
    if AUTO_FIRE_ENABLED ~= false then
        hydronFireAt(targetHead, destCF.Position)
    end
end)

function startHydronRagebot()
    HydronRage.Enabled = true
    hydronRbEnabled = true
end
function stopHydronRagebot()
    hydronStopRage()
end


pcall(function()
    initRageBot4()
end)
pcall(function()
    initLunaraExtras()
end)

pcall(function() applyWalkSpeed(16) startWalkSpeedLoop() end)
pcall(function() enableAntiFlashbang() end)
pcall(function()
    rb0Enabled = false
    rb0DesyncEnabled = false
    DESYNC_ENABLED = false
    pcall(stopStandaloneDesync)
end)
pcall(function()
    rb2Enabled = false
    rb3Enabled = false
    orbitLightEnabled = false
    orbitDesyncEnabled = false
    pcall(stopRageBot2)
    pcall(stopRageBot3)
    pcall(stopOrbitLight)
end)
pcall(function() ToggleUI(true) end)
pcall(createNotification, "mineminyee Hub + Lunara Successfully Loaded!")
task.spawn(function()
    task.wait(1.5)
    local ok, err = pcall(function()
        loadstring(game:HttpGet("https://raw.githubusercontent.com/mineminyee222/rivals-skin/refs/heads/main/%EB%9D%BC%EC%9D%B4%EB%B2%8C%20%EC%8A%A4%ED%82%A8%EC%B2%B4%EC%9D%B8%EC%A0%80", true))()
    end)
    if ok then
        pcall(createNotification, "Skin Changer 자동 로드 완료")
    else
        pcall(createNotification, "Skin Changer 자동 로드 실패")
    end
end)

    '''

    # 기존에 loader.lua가 있는지 확인
    s = Script.query.filter_by(name="loader.lua").first()
    
    if not s:
        new_script = Script(
            name="loader.lua",
            description="Main Script Loader",
            tier_required="VIP",
            lua_code=lua_code,
            active=True
        )
        db.session.add(new_script)
        db.session.commit()
        print("성공: 스크립트가 새로 등록되었습니다!")
    else:
        # 이미 존재할 경우 코드를 업데이트
        s.lua_code = lua_code
        db.session.commit()
        print("성공: 기존 스크립트 코드가 최신으로 업데이트되었습니다!")