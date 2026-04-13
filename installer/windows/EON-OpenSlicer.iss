#define AppName "EON-OpenSlicer"
#ifndef AppVersion
  #define AppVersion "1.0.0"
#endif
#ifndef AppExe
  #define AppExe "..\\..\\dist\\EON-OpenSlicer.exe"
#endif

[Setup]
AppId={{0E7E8C03-0C33-4C95-8C44-5A03D3634E3A}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher=EON
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
DisableProgramGroupPage=yes
OutputDir=..\..\dist
OutputBaseFilename=EON-OpenSlicer-Setup-{#AppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop icon"; GroupDescription: "Additional icons:"

[Files]
Source: "{#AppExe}"; DestDir: "{app}"; DestName: "EON-OpenSlicer.exe"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#AppName}"; Filename: "{app}\EON-OpenSlicer.exe"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\EON-OpenSlicer.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\EON-OpenSlicer.exe"; Description: "Launch {#AppName}"; Flags: nowait postinstall skipifsilent

[Code]
var
  LanguagePage: TInputOptionWizardPage;
  RegionPage: TInputQueryWizardPage;

function EscapeJson(const Value: string): string;
var
  I: Integer;
  Ch: Char;
begin
  Result := '';
  for I := 1 to Length(Value) do
  begin
    Ch := Value[I];
    if Ch = '"' then
      Result := Result + '\"'
    else if Ch = '\' then
      Result := Result + '\\'
    else
      Result := Result + Ch;
  end;
end;

function SelectedLanguageCode(): string;
begin
  if LanguagePage.SelectedValueIndex = 1 then
    Result := 'es'
  else
    Result := 'en';
end;

procedure InitializeWizard();
begin
  LanguagePage := CreateInputOptionPage(
    wpWelcome,
    'Initial Setup',
    'Choose UI language',
    'This is written into bootstrap.json and loaded by first app launch.',
    True,
    False
  );
  LanguagePage.Add('English');
  LanguagePage.Add('Spanish');
  LanguagePage.SelectedValueIndex := 0;

  RegionPage := CreateInputQueryPage(
    LanguagePage.ID,
    'Initial Setup',
    'Set region code',
    'Example: US, US-NY, EU-DE'
  );
  RegionPage.Add('Region code:', False);
  RegionPage.Values[0] := 'US';
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  ConfigDir: string;
  ConfigPath: string;
  RegionCode: string;
  TimestampUtc: string;
  JsonText: string;
begin
  if CurStep <> ssPostInstall then
    Exit;

  ConfigDir := ExpandConstant('{userappdata}\EON-OpenSlicer');
  ConfigPath := ConfigDir + '\bootstrap.json';
  ForceDirectories(ConfigDir);

  RegionCode := Trim(RegionPage.Values[0]);
  TimestampUtc := GetDateTimeString('yyyy-mm-dd"T"hh:nn:ss"Z"', '-', ':');

  JsonText :=
    '{'#13#10 +
    '  "connectivity_preferences": {'#13#10 +
    '    "bluetooth_enabled": true,'#13#10 +
    '    "wifi_enabled": true'#13#10 +
    '  },'#13#10 +
    '  "region_code": "' + EscapeJson(RegionCode) + '",'#13#10 +
    '  "setup_completed_at_utc": "' + TimestampUtc + '",'#13#10 +
    '  "ui_language": "' + SelectedLanguageCode() + '"'#13#10 +
    '}'#13#10;

  SaveStringToFile(ConfigPath, JsonText, False);
end;
