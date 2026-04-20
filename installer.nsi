; ============================================================
;  Student Management System - NSIS Installer Script
;  Compile with: makensis installer.nsi
; ============================================================

!define APP_NAME        "Student Management System"
!define APP_VERSION     "1.0.0"
!define APP_PUBLISHER   "Your Name"
!define APP_EXE         "StudentManagementSystem.exe"
!define REG_KEY         "Software\Microsoft\Windows\CurrentVersion\Uninstall\StudentManagementSystem"

; SetCompressor MUST come before any data-generating instructions
SetCompressor /SOLID lzma

; ---------- MUI2 setup ----------
!include "MUI2.nsh"

!define MUI_ICON        "app\assets\icons\SMSIcon_sharp.ico"
!define MUI_UNICON      "app\assets\icons\SMSIcon_sharp.ico"
!define MUI_WELCOMEFINISHPAGE_BITMAP_NOSTRETCH
!define MUI_ABORTWARNING

; Installer pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!define MUI_FINISHPAGE_RUN          "$INSTDIR\${APP_EXE}"
!define MUI_FINISHPAGE_RUN_TEXT     "Launch ${APP_NAME}"
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"

; ---------- General settings ----------
Name                "${APP_NAME}"
OutFile             "StudentManagementSystem-Setup.exe"
InstallDir          "$LOCALAPPDATA\Programs\StudentManagementSystem"
InstallDirRegKey    HKCU "${REG_KEY}" "InstallLocation"
RequestExecutionLevel user
ShowInstDetails     show
ShowUnInstDetails   show

; ---------- Installer ----------
Section "MainSection" SEC01

    SetOutPath "$INSTDIR"
    File /r "dist\StudentManagementSystem\*"

    ; Pre-create the database folder so the app finds it writable
    CreateDirectory "$INSTDIR\database"

    WriteUninstaller "$INSTDIR\Uninstall.exe"

    ; Add/Remove Programs entry
    WriteRegStr   HKCU "${REG_KEY}" "DisplayName"      "${APP_NAME}"
    WriteRegStr   HKCU "${REG_KEY}" "DisplayVersion"   "${APP_VERSION}"
    WriteRegStr   HKCU "${REG_KEY}" "Publisher"        "${APP_PUBLISHER}"
    WriteRegStr   HKCU "${REG_KEY}" "InstallLocation"  "$INSTDIR"
    WriteRegStr   HKCU "${REG_KEY}" "DisplayIcon"      "$INSTDIR\${APP_EXE}"
    WriteRegStr   HKCU "${REG_KEY}" "UninstallString"  '"$INSTDIR\Uninstall.exe"'
    WriteRegDWORD HKCU "${REG_KEY}" "NoModify"         1
    WriteRegDWORD HKCU "${REG_KEY}" "NoRepair"         1

    ; Start Menu shortcut
    CreateDirectory "$SMPROGRAMS\${APP_NAME}"
    CreateShortcut  "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" \
                    "$INSTDIR\${APP_EXE}" "" "$INSTDIR\${APP_EXE}" 0
    CreateShortcut  "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk" \
                    "$INSTDIR\Uninstall.exe"

    ; Desktop shortcut
    CreateShortcut  "$DESKTOP\${APP_NAME}.lnk" \
                    "$INSTDIR\${APP_EXE}" "" "$INSTDIR\${APP_EXE}" 0

SectionEnd

; ---------- Uninstaller ----------
Section "Uninstall"

    ; Remove installed files (keeps user database)
    RMDir /r "$INSTDIR\_internal"
    Delete   "$INSTDIR\${APP_EXE}"
    Delete   "$INSTDIR\Uninstall.exe"
    ; Intentionally leave $INSTDIR\database\ so user data is preserved
    RMDir    "$INSTDIR"

    ; Remove shortcuts
    Delete   "$DESKTOP\${APP_NAME}.lnk"
    Delete   "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
    Delete   "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk"
    RMDir    "$SMPROGRAMS\${APP_NAME}"

    ; Remove registry entry
    DeleteRegKey HKCU "${REG_KEY}"

SectionEnd
