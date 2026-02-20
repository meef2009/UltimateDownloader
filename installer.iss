#define MyAppName "UltimateDownloader"
#define MyAppVersion "1.0.8"
#define MyAppPublisher "MyCompany"
#define MyAppExeName "UltimateDownloader.exe"
#define MyUpdaterExe "UltimateDownloaderUpdater.exe"

[Setup]
AppId={{8F6A7E3D-3C11-4F9C-A111-2026V7APP}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}

; ✅ Per-user install (no admin, меньше Permission проблем)
DefaultDirName={localappdata}\{#MyAppName}
PrivilegesRequired=lowest

DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes

OutputDir=installer_output
OutputBaseFilename={#MyAppName}_Setup_{#MyAppVersion}

Compression=lzma2
SolidCompression=yes
WizardStyle=modern
SetupLogging=yes

UninstallDisplayIcon={app}\{#MyAppExeName}
SetupIconFile=assets\icon.ico

ArchitecturesInstallIn64BitMode=x64compatible
CloseApplications=yes
RestartApplications=no

; ✅ prevent multi-instance during install/update
AppMutex={#MyAppName}Mutex

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[Tasks]
Name: "desktopicon"; Description: "Create Desktop Icon"; GroupDescription: "Additional options:"; Flags: unchecked

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\{#MyUpdaterExe}"; DestDir: "{app}"; Flags: ignoreversion
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{userdesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Registry]
; ✅ store install path for app/updater
Root: HKCU; Subkey: "Software\{#MyAppPublisher}\{#MyAppName}"; ValueType: string; ValueName: "InstallPath"; ValueData: "{app}"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[Code]
function InitializeSetup(): Boolean;
var
  ResultCode: Integer;
begin
  // Если приложение запущено — попросим закрыть
  // /SILENT обновления тоже должны уметь закрывать приложение
  Exec('taskkill', '/F /IM "{#MyAppExeName}"', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  Exec('taskkill', '/F /IM "{#MyUpdaterExe}"', '', SW_HIDE, ewWaitUntilTerminated, ResultCode);
  Result := True;
end;