# Ensure the script is running with administrative privileges
If (-NOT [System.Security.Principal.WindowsIdentity]::GetCurrent().Groups -contains [System.Security.Principal.WindowsBuiltinRole]::Administrator) {
    Write-Host "Please run this script as an Administrator."
    Exit
}

# Add the French Keyboard Layout
Write-Host "Adding French Keyboard Layout..."

# Add French language input method
$languageTag = "fr-FR"
$inputMethod = "040c:0000040c"

# Install the French keyboard layout
Set-WinUILanguageOverride -Language $languageTag
Set-WinUserLanguageList -LanguageList $languageTag -Force
Set-WinDefaultInputMethodOverride -InputMethodOverride $inputMethod

Write-Host "French Keyboard Layout added successfully."

# Optional: Confirm the addition of the keyboard layout
Write-Host "Displaying current input methods..."
Get-WinUserLanguageList

Write-Host "Script completed."
